from typing import Callable, Type, TypeVar

from django.db import transaction
from django.db.models import Model, Q
from onec_client import OneCODataClient

client = OneCODataClient()
ModelSubclass = TypeVar("ModelSubclass", bound=Model)


class ODataToDjangoDataSyncer:
    def __init__(
        self,
        model: Type[ModelSubclass],
        objects_odata: list[dict],
        fields_mapping: dict[str, str],
        primary_key_name: str | None = None,
        nested_key: str | None = None,
        update: bool = True,
        preproc_function: Callable[[dict], dict] | None = None,
    ) -> None:
        """
        :param objects_odata: Данные по объектам от 1c.
        :param fields_mapping: Отображение названий полей в БД Джанго на названия полей
        в БД 1C.

        :param primary_key_name: Название первичного ключа от 1с.
        :param nested_key: Если данные по объекту нужно получать по вложенному ключу при
        переборе массива, то нужно передать в параметре этот ключ.
        :param update: Нужно ли обновлять данные по существующим объектам?
        :preproc_function: Функция, которую нужно применить для предобработки
        данных от 1с
        """
        self.model = model
        self.objects_odata = objects_odata
        self.fields_mapping = fields_mapping
        self.primary_key_name = primary_key_name
        self.nested_key = nested_key
        self.update = update
        self.preproc_function = preproc_function

        self.natural_keys_mapping = None

        self.created_objects = []
        self.updated_objects = []
        self.seen_ids = set()

        if not self.primary_key_name:
            # Если не передали первичный ключ, получаем поля для естественного ключа
            self.set_natural_keys_mapping()

    def set_natural_keys_mapping(self) -> None:
        natural_keys_mapping = self.fields_mapping.copy()
        for key in self.model.NOT_NATURAL_KEYS:
            natural_keys_mapping.pop(key)
        self.natural_keys_mapping = natural_keys_mapping

    def get_natural_keys_query(self, object_odata: dict) -> Q:
        """
        Получает запрос Джанго ORM для получения объекта из БД по значению
        его естественных ключей.
        """
        query = Q()
        for django_field_name in self.natural_keys_mapping:
            odata_field_value = object_odata[
                self.natural_keys_mapping[django_field_name]
            ]
            query &= Q(**{django_field_name: odata_field_value})
        return query

    def sync_one_object(
        self,
        object_odata: dict,
    ) -> None:
        if self.preproc_function:
            object_odata = self.preproc_function(object_odata)

        # Проверяем, какую операцию нужно выполнить: создание или обновление
        if self.primary_key_name:
            # При получении объекта из БД Джанго по первичному ключу, нам достаточно
            # знать, существует ли такой объект
            object_pk = object_odata.get(self.primary_key_name)
            django_object = self.model.objects.filter(pk=object_pk).exists()
        else:
            # При получении объекта из БД Джанго по естественным ключам,
            # нужно узнать ещё ID объекта в БД Джанго.
            query = self.get_natural_keys_query(object_odata)
            django_object = self.model.objects.filter(query).values("id")

        django_object_data = {}
        for django_field_name, onec_field_name in self.fields_mapping.items():
            django_object_data[django_field_name] = object_odata.get(onec_field_name)

        object_instance = self.model(**django_object_data)

        if django_object:
            if not self.primary_key_name:
                object_pk = django_object[0]["id"]
                object_instance.pk = object_pk

            self.updated_objects.append(object_instance)
            self.seen_ids.add(object_pk)
        else:
            self.created_objects.append(object_instance)

    def sync_objects(self) -> str:
        """
        Синхронизирует данные в БД Джанго и от API 1C.
        """

        for object_odata in self.objects_odata:
            if self.nested_key:
                nested_objects_odata = object_odata[self.nested_key]
                for nested_object_odata in nested_objects_odata:
                    self.sync_one_object(nested_object_odata)
            else:
                self.sync_one_object(object_odata)

        updated_count = 0
        with transaction.atomic():

            if self.update:
                update_fields = list(self.fields_mapping.keys())

                # через .bulk_update() нельзя обновлять PK
                if self.primary_key_name:
                    update_fields.remove(self.model._meta.pk.name)
                else:
                    # Нет смысла обновлять значения полей, которые мы использовали
                    # для получения по естественному ключу
                    update_fields = [
                        field
                        for field in update_fields
                        if field not in self.natural_keys_mapping.keys()
                    ]

                updated_count = self.model.objects.bulk_update(
                    self.updated_objects, update_fields, batch_size=1000
                )

            deleted_count = self.model.objects.filter(
                ~Q(pk__in=self.seen_ids)
            ).delete()[0]
            created_count = len(
                self.model.objects.bulk_create(
                    self.created_objects, ignore_conflicts=True
                )
            )
        return (
            f"{created_count} created, {updated_count} updated, {deleted_count} deleted"
        )
