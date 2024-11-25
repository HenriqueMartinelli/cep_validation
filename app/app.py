from http import HTTPStatus
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from services.validation_service import ValidationService, get_validation_service
from schemas.validation_schema import ValidationRequest, ValidationResponse, ErrorMessage

app = FastAPI()

router = APIRouter(prefix='/validate', tags=['validation'])

def get_validation_controller(
    validation_service: ValidationService = Depends(get_validation_service),
):
    return validation_service

@router.post(
    '/compare',
    responses={
        HTTPStatus.OK: {
            "description": "Addresses match",
            "model": ValidationResponse,
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Address mismatch",
            "model": ErrorMessage,
        },
    },
)
async def validate_address(
    data: ValidationRequest,
    validation_service: ValidationService = Depends(get_validation_controller),
):
    """
    Valida os endereços consultados via CNPJ e CEP e retorna se coincidem.
    """
    try:
        return await validation_service.validate(data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

app.include_router(router)
