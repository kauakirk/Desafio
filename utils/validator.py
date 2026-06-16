from jsonschema import validate, ValidationError
from utils.schemas import (
    cart_create_schema,
    login_response_schema,
    product_create_schema,
    product_response_schema,
    user_create_schema,
    user_login_schema,
    user_response_schema,
    cart_response_schema,
)


def validate_payload(payload, schema):
    try:
        validate(instance=payload, schema=schema)
    except ValidationError as exc:
        raise AssertionError(f"Payload não passa no schema: {exc.message}")


def validate_user_create(payload):
    validate_payload(payload, user_create_schema)


def validate_user_login(payload):
    validate_payload(payload, user_login_schema)


def validate_product_create(payload):
    validate_payload(payload, product_create_schema)


def validate_cart_create(payload):
    validate_payload(payload, cart_create_schema)


def validate_user_response(payload):
    validate_payload(payload, user_response_schema)


def validate_login_response(payload):
    validate_payload(payload, login_response_schema)


def validate_product_response(payload):
    validate_payload(payload, product_response_schema)


def validate_cart_response(payload):
    validate_payload(payload, cart_response_schema)
