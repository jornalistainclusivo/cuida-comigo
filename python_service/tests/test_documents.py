import pytest
import pytest_asyncio
from httpx import AsyncClient
from datetime import datetime, timezone
import uuid
import io

from app.models import User, CareGroup, CareRecipient, CareGroupMember, UserRole, ClinicalDocument
from app.auth.security import hash_password

@pytest_asyncio.fixture(loop_scope="function")
async def setup_entities(async_session):
    # Criar user
    user = User(
        email=f"test_docs_{uuid.uuid4().hex}@example.com",
        hashed_password=hash_password("test"),
        full_name="Test User",
        is_active=True
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    
    # Criar group
    group = CareGroup(name="Grupo Teste Docs")
    async_session.add(group)
    await async_session.commit()
    await async_session.refresh(group)
    
    # Criar membro
    member = CareGroupMember(care_group_id=group.id, user_id=user.id, role=UserRole.ADMIN)
    async_session.add(member)
    
    # Criar recipient
    recipient = CareRecipient(care_group_id=group.id, name="Paciente Teste Docs")
    async_session.add(recipient)
    await async_session.commit()
    await async_session.refresh(recipient)
    
    return group, recipient, user, member

@pytest.mark.asyncio
async def test_upload_document_success(client: AsyncClient, setup_entities, mocker):
    group, recipient, user, member = setup_entities
    
    login_response = await client.post("/api/v1/auth/login", data={
        "username": user.email,
        "password": "test"
    })
    token = login_response.json()["access_token"]
    
    # Mock do S3
    mocker.patch("app.routers.documents.upload_file", return_value=True)

    file_content = b"PDF fake content"
    files = {
        "file": ("test.pdf", file_content, "application/pdf")
    }
    data = {
        "title": "Exame de Sangue",
        "document_type": "EXAME"
    }

    response = await client.post(
        f"/api/v1/care-groups/{group.id}/documents",
        data=data,
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    resp_data = response.json()
    assert resp_data["title"] == "Exame de Sangue"
    assert resp_data["document_type"] == "EXAME"
    assert resp_data["care_recipient_id"] == str(recipient.id)

@pytest.mark.asyncio
async def test_upload_document_invalid_type(client: AsyncClient, setup_entities):
    group, _, user, _ = setup_entities
    
    login_response = await client.post("/api/v1/auth/login", data={
        "username": user.email,
        "password": "test"
    })
    token = login_response.json()["access_token"]
    
    files = {
        "file": ("script.py", b"print('hello')", "text/x-python")
    }
    data = {
        "title": "Script",
        "document_type": "OUTROS"
    }

    response = await client.post(
        f"/api/v1/care-groups/{group.id}/documents",
        data=data,
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 415

@pytest.mark.asyncio
async def test_upload_document_too_large(client: AsyncClient, setup_entities):
    group, _, user, _ = setup_entities
    
    login_response = await client.post("/api/v1/auth/login", data={
        "username": user.email,
        "password": "test"
    })
    token = login_response.json()["access_token"]
    
    # Simula arquivo > 10MB
    large_content = b"0" * (10 * 1024 * 1024 + 1)
    
    files = {
        "file": ("large.jpg", large_content, "image/jpeg")
    }
    data = {
        "title": "Large Image",
        "document_type": "LAUDO"
    }

    response = await client.post(
        f"/api/v1/care-groups/{group.id}/documents",
        data=data,
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 413

@pytest.mark.asyncio
async def test_download_document_rbac_forbidden(
    client: AsyncClient, setup_entities, async_session, mocker
):
    group, recipient, user, member = setup_entities
    
    # Inserir documento direto no DB
    doc = ClinicalDocument(
        care_recipient_id=recipient.id,
        title="Receita Confidencial",
        document_type="RECEITA",
        s3_key="care_groups/doc1.pdf",
        uploaded_by_id=member.id
    )
    async_session.add(doc)
    await async_session.commit()
    await async_session.refresh(doc)
    
    # Criar usuário invasor
    other_user = User(
        email=f"hacker_{uuid.uuid4().hex}@example.com",
        hashed_password=hash_password("test"),
        full_name="Forasteiro",
        is_active=True
    )
    async_session.add(other_user)
    await async_session.commit()
    
    login_response = await client.post("/api/v1/auth/login", data={
        "username": other_user.email,
        "password": "test"
    })
    token = login_response.json()["access_token"]
    
    # Mock para provar que a rota intercepta ANTES de chegar no S3
    mock_s3 = mocker.patch("app.routers.documents.generate_presigned_url", return_value="http://fake-s3-url.com")
    
    response = await client.get(
        f"/api/v1/care-groups/{group.id}/documents/{doc.id}/download",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403
    mock_s3.assert_not_called()

@pytest.mark.asyncio
async def test_download_document_success(
    client: AsyncClient, setup_entities, async_session, mocker
):
    group, recipient, user, member = setup_entities
    
    doc = ClinicalDocument(
        care_recipient_id=recipient.id,
        title="Laudo Normal",
        document_type="LAUDO",
        s3_key="care_groups/doc2.pdf",
        uploaded_by_id=member.id
    )
    async_session.add(doc)
    await async_session.commit()
    await async_session.refresh(doc)
    
    login_response = await client.post("/api/v1/auth/login", data={
        "username": user.email,
        "password": "test"
    })
    token = login_response.json()["access_token"]
    
    mocker.patch("app.routers.documents.generate_presigned_url", return_value="http://s3.local/fake-presigned")
    
    response = await client.get(
        f"/api/v1/care-groups/{group.id}/documents/{doc.id}/download",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["url"] == "http://s3.local/fake-presigned"
    assert response.json()["expires_in"] == 300
