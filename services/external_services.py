import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

# URLs das APIs
CNPJ_API_URL = "https://brasilapi.com.br/api/cnpj/v1"
CEP_PROVIDER_PRIMARY = "https://brasilapi.com.br/api/cep/v2"
CEP_PROVIDER_SECONDARY = "https://viacep.com.br/ws"

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
async def fetch_cnpj_data(cnpj: str) -> dict:
    """
    Busca os dados de uma empresa usando o CNPJ.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CNPJ_API_URL}/{cnpj}")
        response.raise_for_status()
        return response.json()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
async def fetch_cep_data(cep: str) -> dict:
    """
    Busca os dados de endereço usando o CEP.
    Primeiro tenta o provedor primário e, em caso de erro, o secundário.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CEP_PROVIDER_PRIMARY}/{cep}")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError:
            response = await client.get(f"{CEP_PROVIDER_SECONDARY}/{cep}/json/")
            response.raise_for_status()
            return response.json()
