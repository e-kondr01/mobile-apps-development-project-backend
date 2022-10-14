from onec_client import OneCODataClient
from products.models import Product

from app.celery import app


@app.task()
def sync_products() -> str:
    """
    Актуализирует данные в БД с данными от API 1C.
    """
    client = OneCODataClient()
    objects_odata: list[dict] = client.get(
        "Catalog_Номенклатура", odata_filter="IsFolder eq false", odata_count=1
    )["value"]
    created_objects = []
    updated_objects = []
    for object_odata in objects_odata:
        ref_key = object_odata.get("Ref_Key")
        django_object_data = {
            "ref_key": ref_key,
            "description": object_odata.get("Description"),
        }
        product_instance = Product(**django_object_data)
        product_exists = Product.objects.filter(ref_key=ref_key).exists()
        if product_exists:
            updated_objects.append(product_instance)
        else:
            created_objects.append(product_instance)

    created_count = len(Product.objects.bulk_create(created_objects))
    update_fields = list(django_object_data.keys())
    update_fields.remove("ref_key")
    updated_count = Product.objects.bulk_update(updated_objects, update_fields)

    return f"{created_count} created, {updated_count} updated"
