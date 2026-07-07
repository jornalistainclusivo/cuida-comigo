import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import uuid
from app.models import CareGroupMember, UserRole, TaskStatus

async def create_test_user(client: AsyncClient, email: str, name: str) -> dict:
    """Registra e faz login de um usuário de teste para retornar o token e headers."""
    register_payload = {
        "email": email,
        "password": "SenhaSegura123!",
        "full_name": name,
    }
    await client.post("/api/v1/auth/register", json=register_payload)
    
    login_payload = {
        "username": email,
        "password": "SenhaSegura123!",
    }
    login_res = await client.post("/api/v1/auth/login", data=login_payload)
    token = login_res.json()["access_token"]
    
    return {
        "email": email,
        "full_name": name,
        "headers": {"Authorization": f"Bearer {token}"}
    }

@pytest.mark.asyncio
async def test_create_care_group(client: AsyncClient):
    user = await create_test_user(client, "test_api_cg@example.com", "Test Api CG")
    payload = {
        "name": "Grupo Silva",
        "recipient_name": "Maria Silva"
    }
    response = await client.post("/api/v1/care-groups", json=payload, headers=user["headers"])
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Grupo Silva"
    
@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    user = await create_test_user(client, "test_api_task@example.com", "Test Api Task")
    # 1. Create a care group
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Família O.", "recipient_name": "Sr. Oliveira"},
        headers=user["headers"]
    )
    group_id = group_res.json()["id"]
    
    # 2. Create task
    task_payload = {
        "title": "Medicação da Tarde",
        "description": "Dar o remédio de pressão",
        "due_date": "2026-05-10T15:00:00Z",
        "recurrence_rule": "FREQ=DAILY"
    }
    response = await client.post(
        f"/api/v1/care-groups/{group_id}/tasks",
        json=task_payload,
        headers=user["headers"]
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["status"] == "PENDING"
    assert data["due_date"] == "2026-05-10T15:00:00Z"
    
@pytest.mark.asyncio
async def test_claim_and_complete_task(client: AsyncClient, async_session: AsyncSession):
    user = await create_test_user(client, "test_api_claim@example.com", "Test Api Claim")
    # 1. Create a care group
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Família S.", "recipient_name": "João S."},
        headers=user["headers"]
    )
    group_id = group_res.json()["id"]
    
    # 2. Fetch the authenticated user's ID
    me_res = await client.get("/api/v1/auth/me", headers=user["headers"])
    user_id = uuid.UUID(me_res.json()["id"])
    
    # 3. Retrieve the automatically created CareGroupMember
    stmt = select(CareGroupMember).where(
        CareGroupMember.care_group_id == uuid.UUID(group_id),
        CareGroupMember.user_id == user_id
    )
    db_res = await async_session.execute(stmt)
    member = db_res.scalar_one()
    member_id = member.id
    
    # 4. Create task
    task_res = await client.post(
        f"/api/v1/care-groups/{group_id}/tasks",
        json={
            "title": "Fisioterapia",
            "due_date": "2026-05-10T15:00:00Z"
        },
        headers=user["headers"]
    )
    task_id = task_res.json()["id"]
    
    # 5. Claim Task
    claim_res = await client.patch(
        f"/api/v1/tasks/{task_id}/claim",
        json={"assignee_id": str(member_id)},
        headers=user["headers"]
    )
    assert claim_res.status_code == 200
    claim_data = claim_res.json()
    assert claim_data["status"] == "CLAIMED"
    assert claim_data["assignee_id"] == str(member_id)
    
    # 6. Complete Task
    complete_res = await client.patch(
        f"/api/v1/tasks/{task_id}/complete",
        headers=user["headers"]
    )
    assert complete_res.status_code == 200
    complete_data = complete_res.json()
    assert complete_data["status"] == "COMPLETED"
