import uuid
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict

from app.models import TaskStatus

class CareGroupCreate(BaseModel):
    name: str
    recipient_name: str

class CareGroupResponse(BaseModel):
    id: uuid.UUID
    name: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    recurrence_rule: Optional[str] = None

class TaskResponse(BaseModel):
    id: uuid.UUID
    status: TaskStatus
    due_date: datetime

class TaskClaimRequest(BaseModel):
    assignee_id: uuid.UUID

class TaskClaimResponse(BaseModel):
    id: uuid.UUID
    status: TaskStatus
    assignee_id: uuid.UUID

class ProtocolCreate(BaseModel):
    medication_name: str
    dosage: str
    frequency_interval_hours: int
    stock_count: int
    safety_threshold: int

class MedicationProtocolResponse(BaseModel):
    id: uuid.UUID
    care_recipient_id: uuid.UUID
    medication_name: str
    dosage: str
    frequency_interval_hours: int
    stock_count: int
    safety_threshold: int
    created_at: datetime
    updated_at: datetime

class MedicationLogCreate(BaseModel):
    administered_by: uuid.UUID
    administered_at: datetime
    notes: Optional[str] = None

class MedicationLogResponse(BaseModel):
    id: uuid.UUID
    protocol_id: uuid.UUID
    administered_by: uuid.UUID
    administered_at: datetime
    notes: Optional[str] = None
    stock_alert: bool = False
    remaining_balance: int
