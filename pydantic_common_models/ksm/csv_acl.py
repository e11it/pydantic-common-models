from pydantic import model_validator, ConfigDict, BaseModel, Field

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


class KafkaACL(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    kafka_principal: SimplePrincipal = Field(..., alias="KafkaPrincipal")
    resource_type: Resources = Field(..., alias="ResourceType")
    pattern_type: KafkaResourcePatternType = Field(..., alias="PatternType")
    resource_name: str = Field(..., alias="ResourceName", pattern=r'^(\*|[a-zA-Z0-9._-]+)$')
    operation: KafkaTopicOperations = Field(..., alias="Operation")
    permission_type: PermissionType = Field(..., alias="PermissionType")
    host: str = Field(..., alias="Host", pattern=r'^(\*|\S+)$')

    @model_validator(mode='after')
    def root_validator(self) -> 'KafkaACL':
        self.resource_type.validate_operation(self.operation)
        # https://docs.confluent.io/platform/current/kafka/authorization.html#prefixed-acls
        if self.pattern_type == KafkaResourcePatternType.prefixed and self.resource_name == '*':
            raise ValueError("PREFIXED pattern cant be used with resource: '*'")
        return self


class KafkaACLCSV(KafkaACL):
    pass
    # TODO[pydantic]: The following keys were removed: `getter_dict`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    #model_config = ConfigDict(from_attributes=True, getter_dict=KafkaAclCSVGetter)
