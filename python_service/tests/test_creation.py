"""
TDD — Backend Creation Engines (Fase 4) Tests

Cenários de teste para as rotas:
  - POST /api/v1/care-groups/{group_id}/tasks
  - POST /api/v1/care-recipients/{recipient_id}/protocols

Garante que as rotas exijam token JWT de membro do grupo (BR-TSK-01 e BR-PRT-01).
"""

import pytest
import uuid
from httpx import AsyncClient
from datetime import datetime, timezone

# Helper do test_onboarding.py adaptado
async def create_test_user(client: AsyncClient, email: str, name: str) -> dict:
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
        "headers": {"Authorization": f"Bearer {token}"}
    }


# ---------------------------------------------------------------------------
# 1. POST /api/v1/care-groups/{group_id}/tasks
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_task_unauthorized(client: AsyncClient):
    """POST /api/v1/care-groups/{group_id}/tasks sem token retorna 401."""
    group_id = str(uuid.uuid4())
    payload = {
        "title": "Dar remédio",
        "due_date": datetime.now(timezone.utc).isoformat()
    }
    res = await client.post(f"/api/v1/care-groups/{group_id}/tasks", json=payload)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_create_task_success(client: AsyncClient):
    """POST /api/v1/care-groups/{group_id}/tasks por membro do grupo retorna 201."""
    user = await create_test_user(client, "member_tasks@example.com", "Membro Silva")
    
    # Criar grupo
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Família Silva"},
        headers=user["headers"]
    )
    group_id = group_res.json()["id"]
    
    payload = {
        "title": "Medir Pressão",
        "description": "Usar aparelho digital",
        "due_date": datetime.now(timezone.utc).isoformat()
    }
    
    # Act
    res = await client.post(
        f"/api/v1/care-groups/{group_id}/tasks",
        json=payload,
        headers=user["headers"]
    )
    
    # Assert
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Medir Pressão"
    assert data["care_group_id"] == group_id


@pytest.mark.asyncio
async def test_create_task_forbidden_non_member(client: AsyncClient):
    """POST /api/v1/care-groups/{group_id}/tasks por não membro retorna 403."""
    user_owner = await create_test_user(client, "owner_tasks@example.com", "Dono Silva")
    user_intruder = await create_test_user(client, "intruder_tasks@example.com", "Intruso Silva")
    
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Família Silva"},
        headers=user_owner["headers"]
    )
    group_id = group_res.json()["id"]
    
    payload = {
        "title": "Tarefa Invasora",
        "due_date": datetime.now(timezone.utc).isoformat()
    }
    
    # Act
    res = await client.post(
        f"/api/v1/care-groups/{group_id}/tasks",
        json=payload,
        headers=user_intruder["headers"]
    )
    
    # Assert
    assert res.status_code == 403
    assert res.json()["detail"] == "User is not a member of this CareGroup"


# ---------------------------------------------------------------------------
# 2. POST /api/v1/care-recipients/{recipient_id}/protocols
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_protocol_unauthorized(client: AsyncClient):
    """POST /api/v1/care-recipients/{recipient_id}/protocols sem token retorna 401."""
    recipient_id = str(uuid.uuid4())
    payload = {
        "medication_name": "Paracetamol",
        "dosage": "500mg",
        "frequency_interval_hours": 8,
        "stock_count": 20,
        "safety_threshold": 5
    }
    res = await client.post(f"/api/v1/care-recipients/{recipient_id}/protocols", json=payload)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_create_protocol_success(client: AsyncClient):
    """POST /api/v1/care-recipients/{recipient_id}/protocols por membro do grupo retorna 201."""
    user = await create_test_user(client, "member_protocols@example.com", "Membro Protocolos")
    
    # Criar grupo
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Família Silva"},
        headers=user["headers"]
    )
    group_id = group_res.json()["id"]
    
    # Criar receptor de cuidados
    recipient_res = await client.post(
        "/api/v1/care-recipients",
        json={"care_group_id": group_id, "name": "Maria Silva"},
        headers=user["headers"]
    )
    recipient_id = recipient_res.json()["id"]
    
    payload = {
        "medication_name": "Dipirona",
        "dosage": "1g",
        "frequency_interval_hours": 6,
        "stock_count": 30,
        "safety_threshold": 6
    }
    
    # Act
    res = await client.post(
        f"/api/v1/care-recipients/{recipient_id}/protocols",
        json=payload,
        headers=user["headers"]
    )
    
    # Assert
    assert res.status_code == 201
    data = res.json()
    assert data["medication_name"] == "Dipirona"
    assert data["care_recipient_id"] == recipient_id


@pytest.mark.asyncio
async def test_create_protocol_forbidden_non_member(client: AsyncClient):
    """POST /api/v1/care-recipients/{recipient_id}/protocols por não membro retorna 403."""
    user_owner = await create_test_user(client, "owner_protocols@example.com", "Dono Silva")
    user_intruder = await create_test_user(client, "intruder_protocols@example.com", "Intruso Silva")
    
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Família Silva"},
        headers=user_owner["headers"]
    )
    group_id = group_res.json()["id"]
    
    recipient_res = await client.post(
        "/api/v1/care-recipients",
        json={"care_group_id": group_id, "name": "Maria Silva"},
        headers=user_owner["headers"]
    )
    recipient_id = recipient_res.json()["id"]
    
    payload = {
        "medication_name": "Rivotril",
        "dosage": "2mg",
        "frequency_interval_hours": 24,
        "stock_count": 10,
        "safety_threshold": 2
    }
    
    # Act
    res = await client.post(
        f"/api/v1/care-recipients/{recipient_id}/protocols",
        json=payload,
        headers=user_intruder["headers"]
    )
    
    # Assert
    assert res.status_code == 403
    assert res.json()["detail"] == "User is not a member of the CareGroup managing this recipient"
