import logging
from urllib.parse import quote, urlencode

import environ
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

env = environ.Env()


class OneCODataClient:
    """
    Клиент для взаимодействия с 1c по API.
    """

    def __init__(self, url="", username="", password=""):
        self.odata_url = url or env.str("ONEC_ODATA_URL")

        self.odata_username = username or env.str("ONEC_ODATA_LOGIN")
        self.odata_password = password or env.str("ONEC_ODATA_PASSWORD")

        params_set = any(
            bool(x) for x in [self.odata_url, self.odata_username, self.odata_password]
        )
        if not params_set:
            raise ValueError(
                "Connection params not set! Be sure ONEC_ODATA_URL, ONEC_ODATA_LOGIN "
                "and ONEC_ODATA_PASSWORD variables are set "
                "or pass them to client class!"
            )

        self.odata_url = self.odata_url.rstrip("/")

        self.session = requests.Session()
        self.session.auth = (self.odata_username.encode(), self.odata_password.encode())

    def get(
        self,
        odata_entity: str = "",
        odata_filter: str | None = None,
        odata_select: str | None = None,
        odata_expand: str | None = None,
        odata_count: int = 0,
        odata_format: str = "json",
    ) -> dict:
        url = f"{self.odata_url}/{odata_entity}"
        params = {"$format": odata_format}
        if odata_filter is not None:
            params["$filter"] = odata_filter
        if odata_select is not None:
            params["$select"] = odata_select
        if odata_count > 0:
            params["$top"] = odata_count
        if odata_expand is not None:
            params["$expand"] = odata_expand

        params_encoded = urlencode(params, quote_via=quote)

        response = self.session.get(
            f"{url}?{params_encoded}", timeout=settings.ONEC_REQUESTS_TIMEOUT
        )
        logger.info("Got response from OneC API")
        response.encoding = "utf-8-sig"

        if response.status_code == 401:
            raise PermissionError(
                "Wrong username or password for OData client provided"
            )

        return response.json()

    def post(
        self, odata_entity: str, create_data: dict, odata_format: str = "json"
    ) -> dict:
        url = f"{self.odata_url}/{odata_entity}"
        params = {"$format": odata_format}

        params_encoded = urlencode(params, quote_via=quote)

        response = self.session.post(
            f"{url}?{params_encoded}",
            json=create_data,
            timeout=settings.ONEC_REQUESTS_TIMEOUT,
        )
        response.encoding = "utf-8-sig"

        if response.status_code == 401:
            raise PermissionError(
                "Wrong username or password for OData client provided"
            )

        return response.json()

    def patch(
        self, odata_entity: str, update_data: dict, odata_format: str = "json"
    ) -> dict:
        url = f"{self.odata_url}/{odata_entity}"
        params = {"$format": odata_format}

        params_encoded = urlencode(params, quote_via=quote)

        response = self.session.patch(
            f"{url}?{params_encoded}",
            json=update_data,
            timeout=settings.ONEC_REQUESTS_TIMEOUT,
        )
        response.encoding = "utf-8-sig"

        if response.status_code == 401:
            raise PermissionError(
                "Wrong username or password for OData client provided"
            )

        return response.json()

    def put(
        self, odata_entity: str, update_data: dict, odata_format: str = "json"
    ) -> dict:
        url = f"{self.odata_url}/{odata_entity}"
        params = {"$format": odata_format}

        params_encoded = urlencode(params, quote_via=quote)

        response = self.session.put(
            f"{url}?{params_encoded}",
            json=update_data,
            timeout=settings.ONEC_REQUESTS_TIMEOUT,
        )
        response.encoding = "utf-8-sig"

        if response.status_code == 401:
            raise PermissionError(
                "Wrong username or password for OData client provided"
            )

        return response.json()

    def delete(self, odata_entity: str, odata_format: str = "json") -> dict | str:
        url = f"{self.odata_url}/{odata_entity}"
        params = {"$format": odata_format}

        params_encoded = urlencode(params, quote_via=quote)

        response = self.session.delete(
            f"{url}?{params_encoded}", timeout=settings.ONEC_REQUESTS_TIMEOUT
        )
        response.encoding = "utf-8-sig"

        if response.status_code == 401:
            raise PermissionError(
                "Wrong username or password for OData client provided"
            )
        if response.status_code == 204:
            return ""

        return response.json()
