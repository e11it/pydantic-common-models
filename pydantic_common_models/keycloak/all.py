from typing import Optional, Any
from pydantic import BaseModel


class CredentialData(BaseModel):
    hashIterations: int
    algorithm: str


class SecretData(BaseModel):
    salt: str
    value: str


class CredentialRepresentation(BaseModel):
    createdDate: Optional[int] = None
    credentialData: Optional[str] = None
    id: Optional[str] = None
    priority: Optional[int] = None
    secretData: Optional[str] = None
    temporary: Optional[bool] = None
    type: Optional[str] = None
    userLabel: Optional[str] = None
    value: Optional[str] = None


class UserRepresentation(BaseModel):
    username: Optional[str] = None
    enabled: Optional[bool] = None
    credentials: Optional[list[CredentialRepresentation]] = None
    groups: Optional[Any] = None
    email: Optional[str] = None
    emailVerified: Optional[str] = None
    attributes: Optional[Any] = None
