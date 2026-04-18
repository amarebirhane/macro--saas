import os
import uuid
from typing import Optional
from pathlib import Path
from fastapi import UploadFile
from PIL import Image

UPLOAD_DIR = Path("uploads")
AVATAR_DIR = UPLOAD_DIR / "avatars"

# Ensure directories exist
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

class StorageService:
    @staticmethod
    async def save_avatar(file: UploadFile) -> str:
        """
        Saves a user avatar, resizes it to a square, and returns the filename.
        """
        # Validate extension
        extension = file.filename.split(".")[-1].lower()
        if extension not in ["jpg", "jpeg", "png"]:
            raise ValueError("Only JPG and PNG files are allowed.")
        
        # Generate unique filename
        filename = f"{uuid.uuid4()}.{extension}"
        filepath = AVATAR_DIR / filename
        
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
        
        # Resize to standard size (e.g., 400x400)
        image = image.resize((400, 400), Image.LANCZOS)
        
        # Save
        if extension in ["jpg", "jpeg"]:
            image.save(filepath, "JPEG", quality=85)
        else:
            image.save(filepath, "PNG")
            
        return filename

    @staticmethod
    def delete_old_avatar(filename: Optional[str]):
        """Deletes an old avatar file if it exists."""
        if not filename:
            return
        filepath = AVATAR_DIR / filename
        if filepath.exists():
            os.remove(filepath)

storage_service = StorageService()
