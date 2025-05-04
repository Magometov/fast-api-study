from fastapi import status
from httpx import AsyncClient

ENDPOINT = "auth/ton/"

async def test_ton_proof_payload_generation(api_client: AsyncClient) -> None:
    response = await api_client.get(ENDPOINT)
    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_data.get("payload") is not None
