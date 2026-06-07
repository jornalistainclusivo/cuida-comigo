import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.models import CareGroupMember, UserRole, TaskStatus

@pytest.mark.asyncio
async def test_create_care_group(client: AsyncClient):
    payload = {
        "name": "Grupo Silva",
        "recipient_name": "Maria Silva"
    }
    response = await client.post("/api/v1/care-groups", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Grupo Silva"
    
@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    # 1. Create a care group
    group_res = await client.post("/api/v1/care-groups", json={"name": "Família O.", "recipient_name": "Sr. Oliveira"})
    group_id = group_res.json()["id"]
    
    # 2. Create task
    task_payload = {
        "title": "Medicação da Tarde",
        "description": "Dar o remédio de pressão",
        "due_date": "2024-05-10T15:00:00Z",
        "recurrence_rule": "FREQ=DAILY"
    }
    response = await client.post(f"/api/v1/care-groups/{group_id}/tasks", json=task_payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == "PENDING"
    assert data["due_date"] == "2024-05-10T15:00:00Z"
    
@pytest.mark.asyncio
async def test_claim_and_complete_task(client: AsyncClient, async_session: AsyncSession):
    # 1. Create a care group
    group_res = await client.post("/api/v1/care-groups", json={"name": "Família S.", "recipient_name": "João S."})
    group_id = group_res.json()["id"]
    
    # 2. Add a member directly via DB for testing
    member_id = uuid.uuid4()
    member = CareGroupMember(id=member_id, care_group_id=uuid.UUID(group_id), user_id=uuid.uuid4(), role=UserRole.SUPPORT)
    async_session.add(member)
    await async_session.commit()
    
    # 3. Create task
    task_res = await client.post(f"/api/v1/care-groups/{group_id}/tasks", json={
        "title": "Fisioterapia",
        "due_date": "2024-05-10T15:00:00Z"
    })
    task_id = task_res.json()["id"]
    
    # 4. Claim Task
    claim_res = await client.patch(f"/api/v1/tasks/{task_id}/claim", json={"assignee_member_id": str(member_id)})
    assert claim_res.status_code == 200
    claim_data = claim_res.json()
    assert claim_data["status"] == "CLAIMED"
    assert claim_data["assignee_id"] == str(member_id)
    
    # 5. Complete Task
    complete_res = await client.patch(f"/api/v1/tasks/{task_id}/complete")
    assert complete_res.status_code == 200
    complete_data = complete_res.json()
    assert complete_data["status"] == "COMPLETED"
