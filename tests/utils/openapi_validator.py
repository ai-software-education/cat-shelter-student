import yaml
import json
import allure
from openapi_core import Spec, validate_response
from openapi_core.contrib.requests import (
    RequestsOpenAPIRequest,
    RequestsOpenAPIResponse,
)
from openapi_core.validation.response.exceptions import ResponseValidationError
from openapi_core.templating.responses.exceptions import ResponseNotFound


class OpenAPIValidator:
    def __init__(self, spec_path: str):
        with open(spec_path, "r", encoding="utf-8") as f:
            spec_dict = yaml.safe_load(f)

        self.spec = Spec.from_dict(spec_dict)

    def validate_response(self, response):
        openapi_request = RequestsOpenAPIRequest(response.request)
        openapi_response = RequestsOpenAPIResponse(response)

        try:
            validate_response(
                spec=self.spec,
                request=openapi_request,
                response=openapi_response,
            )
        except (ResponseValidationError, ResponseNotFound) as e:
            msg = f"Контракт нарушен: {e}"

        else:
            return  # контракт валиден

        #  Allure 
        allure.attach( f"{response.request.method} {response.request.url}",
            name="Запрос", attachment_type=allure.attachment_type.TEXT)

        allure.attach(str(response.status_code), name="Статус-код",
            attachment_type=allure.attachment_type.TEXT)

        try:
            body = json.dumps(response.json(), indent=2, ensure_ascii=False)
            attachment_type = allure.attachment_type.JSON
        except Exception:
            body = response.text
            attachment_type = allure.attachment_type.TEXT
        allure.attach(body, name="Тело ответа",
            attachment_type=attachment_type)
            
        allure.attach(msg, name="Ошибка контракта",
            attachment_type=allure.attachment_type.TEXT)

        raise AssertionError(msg)
