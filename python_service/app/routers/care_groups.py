from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.database import get_session
from app.models import CareGroup, CareRecipient, Task
from app.schemas import CareGroupCreate, CareGroupResponse, TaskCreate, TaskResponse

router = APIRouter(prefix="/api/v1/care-groups", tags=["Care Groups"])

@router.post("", response_model=CareGroupResponse)
async def create_care_group(payload: CareGroupCreate, session: AsyncSession = Depends(get_session)):
    group = CareGroup(name=payload.name)
    session.add(group)
    await session.commit()
    await session.refresh(group)
    
    recipient = CareRecipient(care_group_id=group.id, name=payload.recipient_name)
    session.add(recipient)
    await session.commit()
    
    return group

@router.post("/{group_id}/tasks", response_model=TaskResponse)
async def create_task(group_id: uuid.UUID, payload: TaskCreate, session: AsyncSession = Depends(get_session)):
    group = await session.get(CareGroup, group_id)
    if not group:
         raise HTTPException(status_code=404, detail="Care group not found")
         
    task = Task(
        care_group_id=group_id,
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        recurrence_rule=payload.recurrence_rule
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    
    return task
