from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.database import get_session
from app.models import MedicationProtocol, MedicationLog, CareRecipient
from app.schemas import ProtocolCreate, MedicationLogCreate

router = APIRouter(tags=["Protocols"])

@router.post("/api/v1/care-recipients/{recipient_id}/protocols")
async def create_protocol(recipient_id: uuid.UUID, payload: ProtocolCreate, session: AsyncSession = Depends(get_session)):
    recipient = await session.get(CareRecipient, recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Care recipient not found")
        
    protocol = MedicationProtocol(
        care_recipient_id=recipient_id,
        **payload.model_dump()
    )
    session.add(protocol)
    await session.commit()
    await session.refresh(protocol)
    return protocol

@router.post("/api/v1/protocols/{protocol_id}/logs")
async def log_medication(protocol_id: uuid.UUID, payload: MedicationLogCreate, session: AsyncSession = Depends(get_session)):
    protocol = await session.get(MedicationProtocol, protocol_id)
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
        
    log = MedicationLog(
        protocol_id=protocol_id,
        **payload.model_dump()
    )
    # Deduct stock
    if protocol.stock_count > 0:
        protocol.stock_count -= 1
        
    session.add(log)
    session.add(protocol)
    await session.commit()
    await session.refresh(log)
    return log
