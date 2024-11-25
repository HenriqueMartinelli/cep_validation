from fastapi import HTTPException
from http import HTTPStatus
from schemas.validation_schema import ValidationRequest, ValidationResponse
from services.external_services import fetch_cnpj_data, fetch_cep_data

def get_value_by_possible_keys(data: dict, possible_keys: list) -> str:
    """
    Busca o valor no dicionário usando uma lista de chaves possíveis.
    """
    for key in possible_keys:
        if key in data:
            return data[key]
    return None

class ValidationService:
    async def validate(self, data: ValidationRequest) -> ValidationResponse:
        cnpj_data = await fetch_cnpj_data(data.cnpj)

        cep_data = await fetch_cep_data(data.cep)

        city_keys = ["city", "municipio", "localidade"]
        street_keys = ["street", "logradouro"]
        state_keys = ["uf", "state"]

        cnpj_city = get_value_by_possible_keys(cnpj_data, city_keys)
        cnpj_street = get_value_by_possible_keys(cnpj_data, street_keys)
        cnpj_state = get_value_by_possible_keys(cnpj_data, state_keys)

        cep_city = get_value_by_possible_keys(cep_data, city_keys)
        cep_street = get_value_by_possible_keys(cep_data, street_keys)
        cep_state = get_value_by_possible_keys(cep_data, state_keys)

        print(cep_city, cep_street, cep_state)
        print(cnpj_city,  cnpj_street, cnpj_state)
        if cnpj_state == cep_state and cnpj_city == cep_city and cnpj_street == cep_street:
            return ValidationResponse(
                status="valid",
                details="Addresses match"
            )

        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Address mismatch"
        )


def get_validation_service():
    return ValidationService()
