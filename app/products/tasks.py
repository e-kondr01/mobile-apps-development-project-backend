"""
Таски Celery для актуализиации данных в БД по данным от API 1C.
"""

from onec_client import OneCODataClient
from products.models import Product

from app.celery import app

client = OneCODataClient()


def sync_objects(
    objects_odata: list[dict],
    fields_mapping: dict[str, str],
    product_primary_key: str,
    create_objects: bool = False,
) -> str:
    """
    Синхронизирует данные в БД Джанго и от API 1C.

    :param objects_odata: Данные по объектам от 1c.
    :param fields_mapping: Отображение названий полей в БД джанго на названия полей в
    БД 1C.
    :param product_primary_key: Название поля PK товара.
    :param create_objects: Нужно ли создавать товар, если товара с таким PK нет
    в БД Джанго?
    """
    created_objects = []
    updated_objects = []
    for object_odata in objects_odata:
        product_pk = object_odata.get(product_primary_key)
        django_object_data = {}
        for django_field_name, onec_field_name in fields_mapping.items():
            django_object_data[django_field_name] = object_odata.get(onec_field_name)

        product_instance = Product(**django_object_data)
        product_exists = Product.objects.filter(ref_key=product_pk).exists()
        if product_exists:
            updated_objects.append(product_instance)
        elif create_objects:
            created_objects.append(product_instance)

    if create_objects:
        created_count = len(Product.objects.bulk_create(created_objects))

    update_fields = list(django_object_data.keys())
    # через .bulk_update() нельзя обновлять PK
    if "ref_key" in update_fields:
        update_fields.remove("ref_key")

    updated_count = Product.objects.bulk_update(updated_objects, update_fields)

    res = ""
    if create_objects:
        res += f"{created_count} created, "
    res += f"{updated_count} updated"
    return res


@app.task()
def sync_products() -> str:
    """
    Синхронизация данных по товарам.
    """
    objects_odata: list[dict] = client.get(
        "Catalog_Номенклатура", odata_filter="IsFolder eq false"
    )["value"]
    return sync_objects(
        objects_odata,
        {"ref_key": "Ref_Key", "description": "Description"},
        "Ref_Key",
        create_objects=True,
    )


@app.task()
def sync_sizes() -> str:
    """
    Синхронизация данных по размерам.
    """
    objects_odata: list[dict] = client.get("Catalog_ХарактеристикиНоменклатуры")[
        "value"
    ]
    return sync_objects(objects_odata, {"size": "Description"}, "Owner")
