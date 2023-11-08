from typing import Literal

from pydantic import AwareDatetime
from pydantic import BaseModel


class IddcPrincipalMetadata(BaseModel):
    entity: str
    domain: str


class IddcPrincipalPassword(BaseModel):
    kind: Literal["com.iddc.principal.password.v1"] = "com.iddc.principal.password.v1"
    dt: AwareDatetime
    upn: str
    password: str
