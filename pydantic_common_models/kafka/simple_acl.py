# Kafka Simple Authorizer data model
from enum import StrEnum
import re
from dataclasses import dataclass
from typing import Any, Dict

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler, BaseModel
from pydantic_core import CoreSchema, core_schema

re_principal = r"^User:(?P<user>\S+?)$"
re_principal_comp = re.compile(re_principal, re.IGNORECASE)


@dataclass
class SimplePrincipal(str):
    _username: str

    @property
    def user(self):
        return self._username

    def __init__(self, principal: str):
        self._username = self.validate_and_get_user(principal)

    def __repr__(self):
        return f'SimplePrincipal<User:{self._username}>'

    @classmethod
    def validate(cls, __input_value: str, _: core_schema.ValidationInfo):
        return cls(__input_value)

    @classmethod
    def validate_and_get_user(cls, __principal: str) -> str:
        match = re_principal_comp.fullmatch(__principal)
        if not match:
            raise ValueError('invalid principal name')

        return match.group("user")

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))


    @classmethod
    def __get_pydantic_json_schema__(
            cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(  # simplified regex here for brevity, see the wikipedia link above
            pattern=re_principal,
            # some example postcodes
            examples=['User:some_user_name'],
        )
        return json_schema


class _EnumCaseInsensitive:
    """_missing_ method override to make Enums CaseInsensitive"""
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value.lower() == value.lower():
                return member


class KafkaResourcePatternType(_EnumCaseInsensitive, StrEnum):
    """Kafka pattern type: literal or prefixed"""
    literal = 'LITERAL'
    prefixed = 'PREFIXED'


class KafkaTopicOperations(_EnumCaseInsensitive, StrEnum):
    all = 'All'
    alter = 'Alter'
    alter_configs = 'AlterConfigs'
    create = 'Create'
    delete = 'Delete'
    describe = 'Describe'
    describe_configs = 'DescribeConfigs'
    idempotent_write = 'IdempotentWrite'
    read = 'Read'
    write = 'Write'
    cluster_action = 'ClusterAction'

    @classmethod
    def get_all(cls):
        return list(filter(lambda cls: cls != 'All', cls))


class Resources(_EnumCaseInsensitive, StrEnum):
    cluster = 'Cluster'
    topic = 'Topic'
    group = 'Group'
    transactional_id = 'TransactionalId'
    delegation_token = 'DelegationToken'

    def validate_operation(self, operation: KafkaTopicOperations, allow_all=True):
        if allow_all and operation == KafkaTopicOperations.all:
            return

        match self:
            case Resources.cluster:
                if operation not in (
                        KafkaTopicOperations.alter,
                        KafkaTopicOperations.alter_configs,
                        KafkaTopicOperations.cluster_action,
                        KafkaTopicOperations.create,
                        KafkaTopicOperations.describe,
                        KafkaTopicOperations.describe_configs,
                        KafkaTopicOperations.idempotent_write
                ):
                    raise ValueError(f"Operation {operation} not allowed for resource {self}")
            case Resources.topic:
                if operation not in (
                        KafkaTopicOperations.alter,
                        KafkaTopicOperations.alter_configs,
                        KafkaTopicOperations.create,
                        KafkaTopicOperations.delete,
                        KafkaTopicOperations.describe,
                        KafkaTopicOperations.describe_configs,
                        KafkaTopicOperations.read,
                        KafkaTopicOperations.write
                ):
                    raise ValueError(f"Operation {operation} not allowed for resource {self}")
            case Resources.group:
                if operation not in (
                        KafkaTopicOperations.delete,
                        KafkaTopicOperations.describe,
                        KafkaTopicOperations.read
                ):
                    raise ValueError(f"Operation {operation} not allowed for resource {self}")
            case Resources.delegation_token:
                if operation not in (
                        KafkaTopicOperations.describe
                ):
                    raise ValueError(f"Operation {operation} not allowed for resource {self}")
            case Resources.transactional_id:
                if operation not in (
                        KafkaTopicOperations.describe,
                        KafkaTopicOperations.write
                ):
                    raise ValueError(f"Operation {operation} not allowed for resource {self}")
            case _:
                raise ValueError(f"Unexpected value: {self}")


class PermissionType(_EnumCaseInsensitive, StrEnum):
    allow = 'Allow'
    deny = 'Deny'
