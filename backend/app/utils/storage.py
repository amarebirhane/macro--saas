import os
import uuid
import boto3
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from PIL import Image
from app.core.config import settings
from app.core.logging_config import logger

UPLOAD_DIR = Path("uploads")
AVATAR_DIR = UPLOAD_DIR / "avatars"

class StorageProvider(ABC):
    @abstractmethod
    async def save_file(self, file_content, filename: str, folder: str) -> str:
        pass

    @abstractmethod
    def delete_file(self, filename: str, folder: str):
        pass

class LocalStorageProvider(StorageProvider):
    def __init__(self):
        AVATAR_DIR.mkdir(parents=True, exist_ok=True)

    async def save_file(self, image: Image.Image, filename: str, folder: str) -> str:
        filepath = UPLOAD_DIR / folder / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Save based on extension
        extension = filename.split(".")[-1].lower()
        if extension in ["jpg", "jpeg"]:
            image.save(filepath, "JPEG", quality=85)
        else:
            image.save(filepath, "PNG")
        
        return filename

    def delete_file(self, filename: str, folder: str):
        filepath = UPLOAD_DIR / folder / filename
        if filepath.exists():
            os.remove(filepath)

class S3StorageProvider(StorageProvider):
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
            endpoint_url=settings.S3_ENDPOINT_URL,
        )
        self.bucket = settings.S3_BUCKET

    async def save_file(self, image: Image.Image, filename: str, folder: str) -> str:
        import io
        buffer = io.BytesIO()
        extension = filename.split(".")[-1].lower()
        format_type = "JPEG" if extension in ["jpg", "jpeg"] else "PNG"
        
        image.save(buffer, format=format_type)
        buffer.seek(0)
        
        key = f"{folder}/{filename}"
        self.s3.upload_fileobj(
            buffer, 
            self.bucket, 
            key, 
            ExtraArgs={"ContentType": f"image/{extension}"}
        )
        return key

    def delete_file(self, filename: str, folder: str):
        key = f"{folder}/{filename}"
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=key)
        except Exception as e:
            logger.error(f"Failed to delete S3 object {key}: {e}")

class StorageService:
    def __init__(self):
        if settings.USE_S3:
            self.provider = S3StorageProvider()
        else:
            self.provider = LocalStorageProvider()

    async def save_avatar(self, file: UploadFile) -> str:
        """
        Saves a user avatar, resizes it to a square, and returns the identifier.
        """
        extension = file.filename.split(".")[-1].lower()
        if extension not in ["jpg", "jpeg", "png"]:
            raise ValueError("Only JPG and PNG files are allowed.")

        filename = f"{uuid.uuid4()}.{extension}"
        
        try:
            # Open image with Pillow
            image = Image.open(file.file)

            # Auto-crop to square
            width, height = image.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2

            image = image.crop((left, top, right, bottom))
            image = image.resize((400, 400), Image.LANCZOS)

            return await self.provider.save_file(image, filename, "avatars")
        except Exception as e:
            logger.error(f"Failed to save avatar: {e}")
            raise

    def delete_old_avatar(self, identifier: Optional[str]):
        """Deletes an old avatar identifier (filename or S3 key)."""
        if not identifier:
            return
        # If identifier contains folder, split it
        if "/" in identifier:
            folder, filename = identifier.split("/", 1)
        else:
            folder, filename = "avatars", identifier
            
        self.provider.delete_file(filename, folder)

storage_service = StorageService()
