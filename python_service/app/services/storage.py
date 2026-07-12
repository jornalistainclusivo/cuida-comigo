import os
import boto3
from botocore.exceptions import ClientError
from typing import Optional

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=os.getenv('S3_ENDPOINT_URL'),
        aws_access_key_id=os.getenv('S3_ACCESS_KEY', 'minioadmin'),
        aws_secret_access_key=os.getenv('S3_SECRET_KEY', 'minioadmin'),
        region_name=os.getenv('S3_REGION', 'us-east-1')
    )

def get_bucket_name() -> str:
    return os.getenv('S3_BUCKET_NAME', 'cuidacomigo-docs')

def upload_file(file_obj, object_name: str, content_type: str = None) -> bool:
    """
    Faz upload de um objeto file-like para o S3.
    """
    s3_client = get_s3_client()
    bucket = get_bucket_name()
    ExtraArgs = {}
    if content_type:
        ExtraArgs['ContentType'] = content_type

    try:
        s3_client.upload_fileobj(file_obj, bucket, object_name, ExtraArgs=ExtraArgs)
        return True
    except ClientError as e:
        print(f"Erro no upload pro S3: {e}")
        return False

def generate_presigned_url(object_name: str, expiration: int = 300) -> Optional[str]:
    """
    Gera um presigned URL para download do objeto, válido por `expiration` segundos.
    """
    s3_client = get_s3_client()
    bucket = get_bucket_name()
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': object_name},
            ExpiresIn=expiration
        )
        return response
    except ClientError as e:
        print(f"Erro ao gerar presigned url: {e}")
        return None
