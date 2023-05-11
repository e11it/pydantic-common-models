# Kafka Simple Authorizer data model
from enum import StrEnum
import re

re_principal = r"^User:(?P<user>\S+?)$"
re_principal_comp = re.compile(re_principal, re.IGNORECASE)


class SimplePrincipal(str):
    """
    Kafka Simple Acl principal name
    """

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            # simplified regex here for brevity, see the wikipedia link above
            pattern=re_principal,
            # some example postcodes
            examples=['User:some_user_name'],
        )

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        return cls(v)

    def __init__(self, principal):
        match = re_principal_comp.fullmatch(principal)
        if not match:
            raise ValueError('invalid principal name')

        self._user = match.group("user")

    @property
    def user(self):
        return self._user

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
