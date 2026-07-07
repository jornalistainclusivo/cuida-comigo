"""
TDD — Backend CRUD (Fase 5) Tests

Cenários de teste para as rotas PATCH e DELETE das 4 entidades:
  - CareGroups (PATCH/DELETE /api/v1/care-groups/{id})
  - CareRecipients (PATCH/DELETE /api/v1/care-recipients/{id})
  - Tasks (PATCH/DELETE /api/v1/tasks/{id})
  - MedicationProtocols (PATCH/DELETE /api/v1/protocols/{id})

Garante segurança de acesso (403 Forbidden para não membros) e integridade dos dados.
"""

import pytest
import uuid
from httpx import AsyncClient
from datetime import datetime, timezone

# Helper para criação de usuários e login
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
# 1. CareGroups CRUD
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_care_group_crud_unauthorized(client: AsyncClient):
    group_id = str(uuid.uuid4())
    # PATCH sem token
    res = await client.patch(f"/api/v1/care-groups/{group_id}", json={"name": "Novo Nome"})
    assert res.status_code == 401

    # DELETE sem token
    res = await client.delete(f"/api/v1/care-groups/{group_id}")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_care_group_crud_forbidden(client: AsyncClient):
    owner = await create_test_user(client, "owner_cg_crud@example.com", "Dono Grupo")
    intruder = await create_test_user(client, "intruder_cg_crud@example.com", "Intruso Grupo")

    # Criar grupo pelo Dono
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Grupo Original"},
        headers=owner["headers"]
    )
    group_id = group_res.json()["id"]

    # PATCH pelo Intruso
    res = await client.patch(
        f"/api/v1/care-groups/{group_id}",
        json={"name": "Nome Alterado"},
        headers=intruder["headers"]
    )
    assert res.status_code == 403

    # DELETE pelo Intruso
    res = await client.delete(f"/api/v1/care-groups/{group_id}", headers=intruder["headers"])
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_care_group_crud_success(client: AsyncClient):
    owner = await create_test_user(client, "owner_cg_success@example.com", "Dono Grupo")

    # Criar grupo
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Grupo Antigo"},
        headers=owner["headers"]
    )
    group_id = group_res.json()["id"]

    # PATCH
    res = await client.patch(
        f"/api/v1/care-groups/{group_id}",
        json={"name": "Grupo Atualizado"},
        headers=owner["headers"]
    )
    assert res.status_code == 200
    assert res.json()["name"] == "Grupo Atualizado"

    # DELETE
    del_res = await client.delete(f"/api/v1/care-groups/{group_id}", headers=owner["headers"])
    assert del_res.status_code == 204


# ---------------------------------------------------------------------------
# 2. CareRecipients CRUD
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_care_recipient_crud_unauthorized(client: AsyncClient):
    recipient_id = str(uuid.uuid4())
    res = await client.patch(f"/api/v1/care-recipients/{recipient_id}", json={"name": "Novo Nome"})
    assert res.status_code == 401

    res = await client.delete(f"/api/v1/care-recipients/{recipient_id}")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_care_recipient_crud_forbidden(client: AsyncClient):
    owner = await create_test_user(client, "owner_cr_crud@example.com", "Dono Grupo")
    intruder = await create_test_user(client, "intruder_cr_crud@example.com", "Intruso Grupo")

    # Criar grupo
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Grupo Silva"},
        headers=owner["headers"]
    )
    group_id = group_res.json()["id"]

    # Criar receptor de cuidados
    recipient_res = await client.post(
        "/api/v1/care-recipients",
        json={"care_group_id": group_id, "name": "Vovó Maria"},
        headers=owner["headers"]
    )
    recipient_id = recipient_res.json()["id"]

    # PATCH pelo Intruso
    res = await client.patch(
        f"/api/v1/care-recipients/{recipient_id}",
        json={"name": "Vovó Maria Alterada"},
        headers=intruder["headers"]
    )
    assert res.status_code == 403

    # DELETE pelo Intruso
    res = await client.delete(f"/api/v1/care-recipients/{recipient_id}", headers=intruder["headers"])
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_care_recipient_crud_success(client: AsyncClient):
    owner = await create_test_user(client, "owner_cr_success@example.com", "Dono Grupo")

    # Criar grupo
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Grupo Silva"},
        headers=owner["headers"]
    )
    group_id = group_res.json()["id"]

    # Criar receptor de cuidados
    recipient_res = await client.post(
        "/api/v1/care-recipients",
        json={"care_group_id": group_id, "name": "Vovó Maria"},
        headers=owner["headers"]
    )
    recipient_id = recipient_res.json()["id"]

    # PATCH
    res = await client.patch(
        f"/api/v1/care-recipients/{recipient_id}",
        json={"name": "Vovó Maria Silva", "blood_type": "O+"},
        headers=owner["headers"]
    )
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Vovó Maria Silva"
    assert data["blood_type"] == "O+"

    # DELETE
    del_res = await client.delete(f"/api/v1/care-recipients/{recipient_id}", headers=owner["headers"])
    assert del_res.status_code == 204


# ---------------------------------------------------------------------------
# 3. Tasks CRUD
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_task_crud_unauthorized(client: AsyncClient):
    task_id = str(uuid.uuid4())
    res = await client.patch(f"/api/v1/tasks/{task_id}", json={"title": "Novo Nome"})
    assert res.status_code == 401

    res = await client.delete(f"/api/v1/tasks/{task_id}")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_task_crud_forbidden(client: AsyncClient):
    owner = await create_test_user(client, "owner_task_crud@example.com", "Dono Grupo")
    intruder = await create_test_user(client, "intruder_task_crud@example.com", "Intruso Grupo")

    # Criar grupo
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Grupo Silva"},
        headers=owner["headers"]
    )
    group_id = group_res.json()["id"]

    # Criar tarefa
    task_res = await client.post(
        f"/api/v1/care-groups/{group_id}/tasks",
        json={"title": "Medir Saturação", "due_date": datetime.now(timezone.utc).isoformat()},
        headers=owner["headers"]
    )
    task_id = task_res.json()["id"]

    # PATCH pelo Intruso
    res = await client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Medir Saturação Alterada"},
        headers=intruder["headers"]
    )
    assert res.status_code == 403

    # DELETE pelo Intruso
    res = await client.delete(f"/api/v1/tasks/{task_id}", headers=intruder["headers"])
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_task_crud_success(client: AsyncClient):
    owner = await create_test_user(client, "owner_task_success@example.com", "Dono Grupo")

    # Criar grupo
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Grupo Silva"},
        headers=owner["headers"]
    )
    group_id = group_res.json()["id"]

    # Criar tarefa
    task_res = await client.post(
        f"/api/v1/care-groups/{group_id}/tasks",
        json={"title": "Medir Saturação", "due_date": datetime.now(timezone.utc).isoformat()},
        headers=owner["headers"]
    )
    task_id = task_res.json()["id"]

    # PATCH
    res = await client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Medir Saturação com Oxímetro", "description": "Lavar as mãos antes"},
        headers=owner["headers"]
    )
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Medir Saturação com Oxímetro"
    assert data["description"] == "Lavar as mãos antes"

    # DELETE
    del_res = await client.delete(f"/api/v1/tasks/{task_id}", headers=owner["headers"])
    assert del_res.status_code == 204


# ---------------------------------------------------------------------------
# 4. Protocols CRUD
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_protocol_crud_unauthorized(client: AsyncClient):
    protocol_id = str(uuid.uuid4())
    res = await client.patch(f"/api/v1/protocols/{protocol_id}", json={"medication_name": "Novo Nome"})
    assert res.status_code == 401

    res = await client.delete(f"/api/v1/protocols/{protocol_id}")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_protocol_crud_forbidden(client: AsyncClient):
    owner = await create_test_user(client, "owner_p_crud@example.com", "Dono Grupo")
    intruder = await create_test_user(client, "intruder_p_crud@example.com", "Intruso Grupo")

    # Criar grupo
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Grupo Silva"},
        headers=owner["headers"]
    )
    group_id = group_res.json()["id"]

    # Criar receptor de cuidados
    recipient_res = await client.post(
        "/api/v1/care-recipients",
        json={"care_group_id": group_id, "name": "Vovó Maria"},
        headers=owner["headers"]
    )
    recipient_id = recipient_res.json()["id"]

    # Criar medicamento
    med_res = await client.post(
        f"/api/v1/care-recipients/{recipient_id}/protocols",
        json={
            "medication_name": "Ibuprofeno",
            "dosage": "400mg",
            "frequency_interval_hours": 8,
            "stock_count": 20,
            "safety_threshold": 4
        },
        headers=owner["headers"]
    )
    protocol_id = med_res.json()["id"]

    # PATCH pelo Intruso
    res = await client.patch(
        f"/api/v1/protocols/{protocol_id}",
        json={"medication_name": "Ibuprofeno Suspensão"},
        headers=intruder["headers"]
    )
    assert res.status_code == 403

    # DELETE pelo Intruso
    res = await client.delete(f"/api/v1/protocols/{protocol_id}", headers=intruder["headers"])
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_protocol_crud_success(client: AsyncClient):
    owner = await create_test_user(client, "owner_p_success@example.com", "Dono Grupo")

    # Criar grupo
    group_res = await client.post(
        "/api/v1/care-groups",
        json={"name": "Grupo Silva"},
        headers=owner["headers"]
    )
    group_id = group_res.json()["id"]

    # Criar receptor de cuidados
    recipient_res = await client.post(
        "/api/v1/care-recipients",
        json={"care_group_id": group_id, "name": "Vovó Maria"},
        headers=owner["headers"]
    )
    recipient_id = recipient_res.json()["id"]

    # Criar medicamento
    med_res = await client.post(
        f"/api/v1/care-recipients/{recipient_id}/protocols",
        json={
            "medication_name": "Ibuprofeno",
            "dosage": "400mg",
            "frequency_interval_hours": 8,
            "stock_count": 20,
            "safety_threshold": 4
        },
        headers=owner["headers"]
    )
    protocol_id = med_res.json()["id"]

    # PATCH
    res = await client.patch(
        f"/api/v1/protocols/{protocol_id}",
        json={"medication_name": "Ibuprofeno Gotas", "dosage": "20 gotas"},
        headers=owner["headers"]
    )
    assert res.status_code == 200
    data = res.json()
    assert data["medication_name"] == "Ibuprofeno Gotas"
    assert data["dosage"] == "20 gotas"

    # DELETE
    del_res = await client.delete(f"/api/v1/protocols/{protocol_id}", headers=owner["headers"])
    assert del_res.status_code == 204
