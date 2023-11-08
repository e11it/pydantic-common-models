from typing import Literal, Optional, List, Dict, Any

from pydantic import BaseModel, ConfigDict


class JWTRole(BaseModel):
    model_config = ConfigDict(extra='forbid')

    token_policies: List[str]
    role_type: Literal['jwt'] = "jwt"
    token_explicit_max_ttl: Optional[int] = None
    user_claim: str
    bound_claims: Optional[Dict[str, Any]]
    allowed_redirect_uris: List[str] = []
    # bound_audiences = None,
    # clock_skew_leeway = None,
    # expiration_leeway = None,
    # not_before_leeway = None,
    # bound_subject = None,
    # bound_claims = None,
    # groups_claim = None,
    # claim_mappings = None,
    # oidc_scopes = None,
    # bound_claims_type = "string",
    # verbose_oidc_logging = False,
    # token_ttl = None,
    # token_max_ttl = None,
    # token_policies = None,
    # token_bound_cidrs = None,
    # token_explicit_max_ttl = None,
    # token_no_default_policy = None,
    # token_num_uses = None,
    # token_period = None,
    # token_type = None,
    # path = None,
    # user_claim_json_pointer = None