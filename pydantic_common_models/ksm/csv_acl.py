from pydantic import BaseModel, Field, root_validator
from pydantic.utils import GetterDict
from typing import Any

from pydantic_common_models.kafka.simple_acl import \
    PermissionType, \
    KafkaTopicOperations, \
    KafkaResourcePatternType, \
    Resources, SimplePrincipal

#
KSM_CSV_HEADERS = ["KafkaPrincipal",
                   "ResourceType",
                   "PatternType",
                   "ResourceName",
                   "Operation",
                   "PermissionType",
                   "Host"
                   ]


class KafkaAclCSVGetter(GetterDict):
    def get(self, key: str, default: Any) -> Any:
        try:
            return self._obj[key]
        except (AttributeError, KeyError):
            return default


class KafkaACL(BaseModel):
    kafka_principal: SimplePrincipal = Field(..., alias="KafkaPrincipal",  regex=r'^User:[a-zA-Z0-9_@\.-]+$')
    resource_type: Resources = Field(..., alias="ResourceType")
    pattern_type: KafkaResourcePatternType = Field(..., alias="PatternType")
    resource_name: str = Field(..., alias="ResourceName", regex=r'^(\*|[a-zA-Z0-9._-]+)$')
    operation: KafkaTopicOperations = Field(..., alias="Operation")
    permission_type: PermissionType = Field(..., alias="PermissionType")
    host: str = Field(..., alias="Host", regex=r'^(\*|\S+)$')

    @root_validator(skip_on_failure=True)
    def validate_structure(cls, values):
        operation, resource_type = values.get('operation'), values.get('resource_type')
        # validate and raise error
        resource_type.validate_operation(operation)
        return values


class KafkaACLCSV(KafkaACL):
    class Config:
        orm_mode = True
        getter_dict = KafkaAclCSVGetter
