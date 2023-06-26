from typing import Literal

from pydantic import BaseModel, Field,  AnyHttpUrl


class VaultTokenAuth(BaseModel):
    auth_type: Literal['token']
    token: str


class VaultK8SAuth(BaseModel):
    auth_type: Literal['k8s']
    mount_point: str
    role: str
    jwt_path: str = '/var/run/secrets/kubernetes.io/serviceaccount/token'


class VaultClient(BaseModel):
    url: AnyHttpUrl
    auth: VaultTokenAuth | VaultK8SAuth = Field(..., discriminator='auth_type')