from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import uuid
from typing import List
from io import BytesIO

from app.database import get_session
from app.models import ClinicalDocument, CareGroupMember, User, CareRecipient
from app.schemas import DocumentResponse, PresignedUrlResponse
from app.auth.dependencies import get_current_user
from app.services.storage import upload_file, generate_presigned_url

router = APIRouter(prefix="/api/v1/care-groups", tags=["Clinical Documents"])

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_TYPES = ["application/pdf", "image/jpeg", "image/png"]

async def check_rbac(group_id: uuid.UUID, current_user: User, session: AsyncSession) -> CareGroupMember:
    member_stmt = select(CareGroupMember).where(
        CareGroupMember.care_group_id == group_id,
        CareGroupMember.user_id == current_user.id
    )
    member_result = await session.execute(member_stmt)
    member = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this care group")
    return member

async def get_recipient(group_id: uuid.UUID, session: AsyncSession) -> CareRecipient:
    recipient_stmt = select(CareRecipient).where(CareRecipient.care_group_id == group_id)
    recipient_result = await session.execute(recipient_stmt)
    recipient = recipient_result.scalars().first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado para o grupo especificado.")
    return recipient


@router.post("/{group_id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    group_id: uuid.UUID,
    title: str = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    member = await check_rbac(group_id, current_user, session)
    recipient = await get_recipient(group_id, session)

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported Media Type (Não é PDF, JPG ou PNG)")

    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Payload Too Large (acima de 10MB)")

    # Rewind for upload
    file_io = BytesIO(file_content)
    
    # Valida document_type
    if document_type not in ["RECEITA", "LAUDO", "EXAME", "OUTROS"]:
        raise HTTPException(status_code=422, detail="document_type inválido")

    s3_key = f"care_groups/{group_id}/documents/{uuid.uuid4()}_{file.filename}"
    success = upload_file(file_io, s3_key, file.content_type)
    if not success:
        raise HTTPException(status_code=500, detail="Erro no upload S3")

    document = ClinicalDocument(
        care_recipient_id=recipient.id,
        title=title,
        document_type=document_type,
        s3_key=s3_key,
        uploaded_by_id=member.id
    )
    session.add(document)
    await session.commit()
    await session.refresh(document)
    return document


@router.get("/{group_id}/documents", response_model=List[DocumentResponse])
async def list_documents(
    group_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    await check_rbac(group_id, current_user, session)
    recipient = await get_recipient(group_id, session)

    stmt = select(ClinicalDocument).where(
        ClinicalDocument.care_recipient_id == recipient.id
    ).order_by(ClinicalDocument.uploaded_at.desc())
    
    result = await session.execute(stmt)
    documents = result.scalars().all()
    return documents


@router.get("/{group_id}/documents/{doc_id}/download", response_model=PresignedUrlResponse)
async def download_document(
    group_id: uuid.UUID,
    doc_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    await check_rbac(group_id, current_user, session)

    stmt = select(ClinicalDocument).where(ClinicalDocument.id == doc_id)
    result = await session.execute(stmt)
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado no banco")

    # Verifica se pertence ao grupo através do recipient
    recipient = await get_recipient(group_id, session)
    if document.care_recipient_id != recipient.id:
        # Prevent accessing docs from other groups even if you know the UUID
        raise HTTPException(status_code=403, detail="Acesso Negado (Documento pertence a outro grupo)")

    presigned_url = generate_presigned_url(document.s3_key, expiration=300)
    if not presigned_url:
        raise HTTPException(status_code=500, detail="Erro ao gerar presigned url")
    
    return PresignedUrlResponse(url=presigned_url, expires_in=300)
