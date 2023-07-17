from pydantic import model_validator, ConfigDict, BaseModel, Field
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
    kafka_principal: SimplePrincipal = Field(..., alias="KafkaPrincipal")
    resource_type: Resources = Field(..., alias="ResourceType")
    pattern_type: KafkaResourcePatternType = Field(..., alias="PatternType")
    resource_name: str = Field(..., alias="ResourceName", pattern=r'^(\*|[a-zA-Z0-9._-]+)$')
    operation: KafkaTopicOperations = Field(..., alias="Operation")
    permission_type: PermissionType = Field(..., alias="PermissionType")
    host: str = Field(..., alias="Host", pattern=r'^(\*|\S+)$')

    @model_validator(skip_on_failure=True)
    @classmethod
    def validate_structure(cls, values):
        operation, resource_type = values.get('operation'), values.get('resource_type')
        pattern_type, resource_name = values.get('pattern_type'), values.get('resource_name')
        # validate and raise error
        resource_type.validate_operation(operation)
        # https://docs.confluent.io/platform/current/kafka/authorization.html#prefixed-acls
        if pattern_type == KafkaResourcePatternType.prefixed and resource_name == '*':
            raise ValueError("PREFIXED pattern cant be used with resource: '*'")
        return values


class KafkaACLCSV(KafkaACL):
    # TODO[pydantic]: The following keys were removed: `getter_dict`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(from_attributes=True, getter_dict=KafkaAclCSVGetter)
