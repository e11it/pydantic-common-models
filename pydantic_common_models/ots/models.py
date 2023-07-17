from pydantic import BaseModel


class OtsSecretResponse(BaseModel):
    custid: str
    metadata_key: str
    secret_key: str
    ttl: int
    metadata_ttl: int
    secret_ttl: int
    state: str
    updated: int
    created: int
    recipient: list[str]
    passphrase_required: bool