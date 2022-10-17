"""
Таски Celery для актуализиации данных в БД по данным от API 1C.
"""

from typing import Type, TypeVar

from django.db.models import Model
from onec_client import OneCODataClient
from products.models import Characteristic, PriceType, Product

from app.celery import app

client = OneCODataClient()
ModelSubclass = TypeVar("ModelSubclass", bound=Model)


def sync_objects(
    model: Type[ModelSubclass],
    objects_odata: list[dict],
    fields_mapping: dict[str, str],
    primary_key_name: str,
) -> str:
    """
    Синхронизирует данные в БД Джанго и от API 1C.

    :param objects_odata: Данные по объектам от 1c.
    :param fields_mapping: Отображение названий полей в БД Джанго на названия полей в
    БД 1C.
    :param primary_key_name: Название первичного ключа от 1с.
    """
    created_objects = []
    updated_objects = []
    for object_odata in objects_odata:
        object_pk = object_odata.get(primary_key_name)
        django_object_data = {}
        for django_field_name, onec_field_name in fields_mapping.items():
            django_object_data[django_field_name] = object_odata.get(onec_field_name)

        object_instance = model(**django_object_data)
        object_exists = model.objects.filter(pk=object_pk).exists()
        if object_exists:
            updated_objects.append(object_instance)
        else:
            created_objects.append(object_instance)

    created_count = len(model.objects.bulk_create(created_objects))

    update_fields = list(django_object_data.keys())
    # через .bulk_update() нельзя обновлять PK
    update_fields.remove(model._meta.pk.name)

    updated_count = model.objects.bulk_update(updated_objects, update_fields)
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
    Синхронизация данных характеристикам товаров.
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
