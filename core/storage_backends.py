import mimetypes
import uuid
from io import BytesIO
from pathlib import PurePosixPath

import cloudinary
import cloudinary.uploader
import cloudinary.utils
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from PIL import Image, ImageOps, UnidentifiedImageError


@deconstructible
class CloudinaryMediaStorage(Storage):
    """
    Store user uploaded media in Cloudinary.

    Images are normalized with Pillow before upload so Vercel does not need to
    persist or serve local media files.
    """

    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )

        self.folder = getattr(settings, "CLOUDINARY_FOLDER", "").strip("/")
        self.max_width = getattr(settings, "CLOUDINARY_IMAGE_MAX_WIDTH", 1600)
        self.max_height = getattr(settings, "CLOUDINARY_IMAGE_MAX_HEIGHT", 1600)
        self.quality = getattr(settings, "CLOUDINARY_IMAGE_QUALITY", 85)
        self.image_format = getattr(settings, "CLOUDINARY_IMAGE_FORMAT", "WEBP").upper()

    def _save(self, name, content):
        clean_name = self._clean_name(name)
        public_id = self._build_public_id(clean_name)

        processed_file = self._process_image(content)
        if processed_file is not None:
            upload_result = cloudinary.uploader.upload(
                processed_file,
                public_id=public_id,
                resource_type="image",
                overwrite=False,
                unique_filename=False,
            )
            return upload_result["public_id"]

        if hasattr(content, "seek"):
            content.seek(0)

        raw_public_id = self._build_public_id(clean_name, keep_suffix=True)
        upload_result = cloudinary.uploader.upload(
            content,
            public_id=raw_public_id,
            resource_type="auto",
            overwrite=False,
            unique_filename=False,
        )
        return upload_result["public_id"]

    def url(self, name):
        if not name:
            return ""

        if str(name).startswith(("http://", "https://")):
            return name

        resource_type = self._resource_type_for_name(name)
        options = {
            "secure": True,
            "resource_type": resource_type,
        }
        if resource_type == "image":
            options.update({"quality": "auto", "fetch_format": "auto"})

        url, _options = cloudinary.utils.cloudinary_url(name, **options)
        return url

    def exists(self, name):
        return False

    def delete(self, name):
        if not name:
            return

        cloudinary.uploader.destroy(
            name,
            resource_type=self._resource_type_for_name(name),
            invalidate=True,
        )

    def _process_image(self, content):
        if hasattr(content, "seek"):
            content.seek(0)

        try:
            image = Image.open(content)
            image.verify()
        except (UnidentifiedImageError, OSError):
            return None

        if hasattr(content, "seek"):
            content.seek(0)

        image = Image.open(content)
        image = ImageOps.exif_transpose(image)
        image.thumbnail((self.max_width, self.max_height), Image.Resampling.LANCZOS)

        save_options = {"optimize": True}
        if self.image_format in {"JPEG", "WEBP"}:
            save_options["quality"] = self.quality

        if self.image_format == "JPEG" and image.mode in {"RGBA", "P"}:
            image = image.convert("RGB")
        elif self.image_format == "WEBP" and image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGB")

        output = BytesIO()
        image.save(output, format=self.image_format, **save_options)
        output.seek(0)
        output.name = f"upload.{self.image_format.lower()}"
        return output

    def _build_public_id(self, name, keep_suffix=False):
        path = PurePosixPath(name)
        stem = path.stem
        stem = stem or "upload"
        parent = str(path.parent).strip(".")
        suffix = path.suffix if keep_suffix else ""
        unique_name = f"{stem}-{uuid.uuid4().hex[:12]}{suffix}"
        public_path = str(PurePosixPath(parent) / unique_name) if parent else unique_name
        return str(PurePosixPath(self.folder) / public_path) if self.folder else public_path

    def _clean_name(self, name):
        path = str(name).replace("\\", "/").strip("/")
        guessed_type, _encoding = mimetypes.guess_type(path)
        if guessed_type and guessed_type.startswith("image/"):
            return path
        return path

    def _resource_type_for_name(self, name):
        guessed_type, _encoding = mimetypes.guess_type(str(name))
        if guessed_type and not guessed_type.startswith("image/"):
            return "raw"
        return "image"
