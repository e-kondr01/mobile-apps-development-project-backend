"""
Таски Celery для актуализиации данных в БД по данным от API 1C.
"""

from typing import Type, TypeVar

from dateutil import parser
from django.db import transaction
from django.db.models import Model, Q
from onec_client import OneCODataClient
from products.models import Barcode, Characteristic, PriceType, Product

from app.celery import app

client = OneCODataClient()
ModelSubclass = TypeVar("ModelSubclass", bound=Model)


def preproc_period(object_odata: dict) -> dict:
    """
    Переводит время и дату из строки в ``datetime.datetime``
    """
    object_odata["period"] = parser.parse(object_odata["period"])


def get_natural_keys_query(
    natural_keys_mapping: dict[str, str], object_odata: dict
) -> Q:
    query = Q()
    for django_field_name in natural_keys_mapping:
        odata_field_value = object_odata[natural_keys_mapping[django_field_name]]
        query &= Q(**{django_field_name: odata_field_value})
    return query


def sync_objects(
    model: Type[ModelSubclass],
    objects_odata: list[dict],
    fields_mapping: dict[str, str],
    primary_key_name: str | None = None,
    nested_key: str | None = None,
    natural_keys_mapping: dict[str, str] | None = None,
    preproc_function=None,
) -> str:
    """
    Синхронизирует данные в БД Джанго и от API 1C.

    :param objects_odata: Данные по объектам от 1c.
    :param fields_mapping: Отображение названий полей в БД Джанго на названия полей в
    БД 1C.

    :param primary_key_name: Название первичного ключа от 1с.
    :param nested_key: Если данные по объекту нужно получать по вложенному ключу при
    переборе массива, то нужно передать в параметре этот ключ.
    :param natural_keys: Если у объекта от 1с нет уникального первичного ключа,
    то нужно передать отображение полей, по которым можно однозначно определить
    этот объект в БД Джанго.
    """
    created_objects = []
    updated_objects = []
    for object_odata in objects_odata:
        if nested_key:
            object_odata = object_odata[nested_key]

        if primary_key_name:
            object_pk = object_odata.get(primary_key_name)
            query = Q(pk=object_pk)
            django_object = model.objects.filter(query).exists()
        else:
            query = get_natural_keys_query(natural_keys_mapping, object_odata)
            django_object = model.objects.filter(query).values("id")

        django_object_data = {}
        for django_field_name, onec_field_name in fields_mapping.items():
            django_object_data[django_field_name] = object_odata.get(onec_field_name)

        object_instance = model(**django_object_data)
        if django_object:
            if not primary_key_name:
                object_instance.pk = django_object[0]["id"]
            updated_objects.append(object_instance)
        else:
            created_objects.append(object_instance)

    with transaction.atomic():
        created_count = len(model.objects.bulk_create(created_objects))

        update_fields = list(django_object_data.keys())
        # через .bulk_update() нельзя обновлять PK
        try:
            update_fields.remove(model._meta.pk.name)
        except ValueError:
            pass

        print("reached bulk update")
        print(len(updated_objects))
        updated_count = model.objects.bulk_update(
            updated_objects, update_fields, batch_size=1000
        )
        # FIXME:
    #         django.db.utils.IntegrityError: duplicate key value violates unique constraint "unique_barcode"
    # DETAIL:  Key (product_id, characteristic_id, barcode)=(e0559cf8-82c0-11e9-80db-50e5492f9e3a, f38ce1a7-bf62-11e5-adcb-50e5492f9e3a, 2200000059178) already exists.
    return f"{created_count} created, {updated_count} updated"


@app.task()
def sync_products() -> str:
    """
    Синхронизация данных по товарам.
    """
    objects_odata: list[dict] = client.get(
        "Catalog_Номенклатура", odata_filter="IsFolder eq false"
    )["value"]
    return sync_objects(
        model=Product,
        objects_odata=objects_odata,
        fields_mapping={"ref_key": "Ref_Key", "name": "Description", "sku": "Артикул"},
        primary_key_name="Ref_Key",
    )


@app.task()
def sync_price_types() -> str:
    """
    Синхронизация данных по типам цен.
    """

    objects_odata: list[dict] = client.get("Catalog_ВидыЦен")["value"]
    return sync_objects(
        model=PriceType,
        objects_odata=objects_odata,
        fields_mapping={"ref_key": "Ref_Key", "name": "Description"},
        primary_key_name="Ref_Key",
    )


@app.task()
def sync_characteristics() -> str:
    """
    Синхронизация данных по характеристикам товаров.
    """

    objects_odata: list[dict] = client.get("Catalog_ХарактеристикиНоменклатуры")[
        "value"
    ]
    return sync_objects(
        model=Characteristic,
        objects_odata=objects_odata,
        fields_mapping={"ref_key": "Ref_Key", "name": "Description"},
        primary_key_name="Ref_Key",
    )


@app.task()
def sync_barcodes() -> str:
    """
    Синхронизация данных по штрихкодам.
    """

    objects_odata: list[dict] = client.get("InformationRegister_Штрихкоды")["value"]
    return sync_objects(
        model=Barcode,
        objects_odata=objects_odata,
        fields_mapping={
            "barcode": "Штрихкод",
            "product_id": "Владелец",
            "characteristic_id": "Характеристика_Key",
        },
        natural_keys_mapping={
            "product_id": "Владелец",
            "characteristic_id": "Характеристика_Key",
        },
    )
