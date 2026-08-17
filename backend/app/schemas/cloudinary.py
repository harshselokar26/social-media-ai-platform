from pydantic import BaseModel


class CloudinaryUploadResponse(BaseModel):
    public_id: str | None = None
    secure_url: str
    format: str | None = None
    width: int | None = None
    height: int | None = None
    resource_type: str | None = None