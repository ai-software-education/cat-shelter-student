import yaml
from openapi_core import Spec, validate_response
from openapi_core.contrib.requests import (
    RequestsOpenAPIRequest,
    RequestsOpenAPIResponse,
)

class OpenAPIValidator:
    def __init__(self, spec_path: str):
        with open(spec_path, "r", encoding="utf-8") as f:
            spec_dict = yaml.safe_load(f)

        self.spec = Spec.from_dict(spec_dict)

    def validate_response(self, response):
        openapi_request = RequestsOpenAPIRequest(response.request)
        openapi_response = RequestsOpenAPIResponse(response)

        validate_response(
            spec=self.spec,
            request=openapi_request,
            response=openapi_response,
        )
