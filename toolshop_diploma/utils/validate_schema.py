import json

import allure
from jsonschema import validate

from toolshop_diploma.utils.path import abs_path_from_project


def validate_response_to_json_schema(json_schema: str, response) -> None:
    schema_path = abs_path_from_project(
        f"toolshop_diploma/json_schemas/{json_schema}"
    )
    with open(schema_path, encoding="utf-8") as file:
        schema = json.loads(file.read())
    with allure.step(f"Validate JSON schema: {json_schema}"):
        validate(instance=response.json(), schema=schema)
