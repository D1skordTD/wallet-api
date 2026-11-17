import httpx
import pytest
import uuid
import asyncio
from main import app

@pytest.mark.asyncio
async def test_get_wallet_not_found():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/wallets/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
        assert response.json()== {"detail": "Wallet not found"}

@pytest.mark.asyncio
async def test_concurrent_withdrawals():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        wallet_id = str(uuid.uuid4())

        await client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={"operation_type": "DEPOSIT", "amount": 100},
        )

        responses = await asyncio.gather(*[
            client.post(
                f"/api/v1/wallets/{wallet_id}/operation",
                json={"operation_type": "WITHDRAW", "amount": 30},
            )
            for _ in range(5)
        ])

        statuses = [r.status_code for r in responses]
        assert statuses.count(200) == 3
        assert statuses.count(400) == 2

        final_response = await client.get(f"/api/v1/wallets/{wallet_id}")
        assert final_response.json()["balance"] == 10