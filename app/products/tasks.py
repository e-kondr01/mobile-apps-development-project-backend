"""
Таски Celery для актуализиации данных в БД по данным от API 1C.
"""


from dateutil import parser
from django.utils import timezone
from onec_client import OneCODataClient
from products.models import (
    Barcode,
    Characteristic,
    PriceChange,
    PriceType,
    Product,
    ProductMovement,
)
from products.syncer import ODataToDjangoDataSyncer

from app.celery import app

client = OneCODataClient()


def preproc_period(object_odata: dict) -> dict:
    """
    Переводит время и дату из строки в ``datetime.datetime``
    """
    object_odata["Period"] = parser.parse(object_odata["Period"]).astimezone(
        timezone.get_current_timezone()
    )
    return object_odata


def preproc_product_movement(object_odata: dict) -> dict:
    object_odata = preproc_period(object_odata)
    if object_odata["RecordType"] == "Expense":
        object_odata["Количество"] *= -1
    return object_odata


@app.task()
def sync_products() -> str:
    """
    Синхронизация данных по товарам.
    """
    objects_odata: list[dict] = client.get(
        "Catalog_Номенклатура", odata_filter="IsFolder eq false"
    )["value"]
    return ODataToDjangoDataSyncer(
        model=Product,
        objects_odata=objects_odata,
        fields_mapping={"ref_key": "Ref_Key", "name": "Description", "sku": "Артикул"},
        primary_key_name="Ref_Key",
    ).sync_objects()


@app.task()
def sync_price_types() -> str:
    """
    Синхронизация данных по типам цен.
    """

    objects_odata: list[dict] = client.get("Catalog_ВидыЦен")["value"]
    return ODataToDjangoDataSyncer(
        model=PriceType,
        objects_odata=objects_odata,
        fields_mapping={"ref_key": "Ref_Key", "name": "Description"},
        primary_key_name="Ref_Key",
    ).sync_objects()


@app.task()
def sync_characteristics() -> str:
    """
    Синхронизация данных по характеристикам товаров.
    """

    objects_odata: list[dict] = client.get("Catalog_ХарактеристикиНоменклатуры")[
        "value"
    ]
    return ODataToDjangoDataSyncer(
        model=Characteristic,
        objects_odata=objects_odata,
        fields_mapping={"ref_key": "Ref_Key", "name": "Description"},
        primary_key_name="Ref_Key",
    ).sync_objects()


@app.task()
def sync_barcodes() -> str:
    """
    Синхронизация данных по штрихкодам.
    """

    objects_odata: list[dict] = client.get("InformationRegister_Штрихкоды")["value"]
    fields_mapping = {
        "barcode": "Штрихкод",
        "product_id": "Владелец",
        "characteristic_id": "Характеристика_Key",
    }
    return ODataToDjangoDataSyncer(
        model=Barcode,
        objects_odata=objects_odata,
        fields_mapping=fields_mapping,
        update=False,
    ).sync_objects()


@app.task()
def sync_product_movements() -> str:
    """
    Синхронизация данных по движениям товаров.
    """

    objects_odata: list[dict] = client.get(
        "AccumulationRegister_ТоварыНаСкладах",
        odata_filter=(
            "Recorder_Type eq 'StandardODATA.Document_ВозвратТоваровОтПокупателя'"
        ),
    )["value"]

    return ODataToDjangoDataSyncer(
        model=ProductMovement,
        objects_odata=objects_odata,
        fields_mapping={
            "product_id": "Номенклатура_Key",
            "characteristic_id": "Характеристика_Key",
            "amount": "Количество",
            "period": "Period",
        },
        preproc_function=preproc_product_movement,
        nested_key="RecordSet",
        update=False,
    ).sync_objects()


@app.task()
def sync_price_changes() -> str:
    """
    Синхронизация данных по изменениям цен товаров.
    """

    objects_odata: list[dict] = client.get(
        "InformationRegister_ЦеныНоменклатуры",
    )["value"]

    return ODataToDjangoDataSyncer(
        model=PriceChange,
        objects_odata=objects_odata,
        fields_mapping={
            "product_id": "Номенклатура_Key",
            "characteristic_id": "Характеристика_Key",
            "price": "Цена",
            "period": "Period",
            "price_type_id": "ВидЦены_Key",
        },
        preproc_function=preproc_period,
        nested_key="RecordSet",
        update=False,
    ).sync_objects()
