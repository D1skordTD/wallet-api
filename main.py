from pydantic import BaseModel
from decimal import Decimal
from typing import Literal
from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import Wallet

app = FastAPI()


class OperationRequest(BaseModel):
    operation_type: Literal["DEPOSIT", "WITHDRAW"]
    amount: Decimal


@app.get("/api/v1/wallets/{wallet_id}")
async def get_wallet(wallet_id: UUID, db: AsyncSession = Depends(get_db)):
    wallet = await db.get(Wallet, wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"wallet_id": wallet_id, "balance": wallet.balance}


@app.post("/api/v1/wallets/{wallet_id}/operation")
async def do_operation(
    wallet_id: UUID,
    operation: OperationRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Wallet).where(Wallet.id == wallet_id).with_for_update())
    wallet = result.scalar_one_or_none()

    if wallet is None:
        wallet = Wallet(id=wallet_id, balance=Decimal("0"))
        db.add(wallet)

    if operation.operation_type == "DEPOSIT":
        wallet.balance += operation.amount
    else:
        if wallet.balance < operation.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        wallet.balance -= operation.amount

    await db.commit()

    return {"wallet_id": wallet_id, "balance": wallet.balance}
