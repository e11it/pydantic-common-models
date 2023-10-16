import pytest
import csv
from csv import DictReader
from io import StringIO

from pydantic_common_models.ksm.csv_acl import KafkaACLCSV

MOCK_DATA = '''
KafkaPrincipal,ResourceType,PatternType,ResourceName,Operation,PermissionType,Host
User:dsfsdfgsdfgsdfg,Topic,LITERAL,sdfgsdfgsdfgsdfg,Read,Allow,*
User:sdfgsdfgdfsgsf,Topic,LITERAL,sdfgsdfgsdfgsdfgsdfg,Read,Allow,*
User:hjghdfghdfhfgh,Group,PREFIXED,dfghdfghdfghdfghdfh,All,Allow,*
User:dfghdfghdfghdfgh,Topic,PREFIXED,dfghdfghdfgh,All,Allow,*
User:asdfasdfasdf,Cluster,LITERAL,kafka-cluster,DESCRIBE,Allow,*
User:fgdhfgbdgfhfh,Cluster,LITERAL,kafka-cluster,IdempotentWrite,Allow,*
User:dfgnbcvb45tdfgdf@app-nl-st-ibakfk,TRANSACTIONALID,PREFIXED,dfghdfghdfghdfghd,All,Allow,*
User:dgfh4hdfgfgh,Group,PREFIXED,dfghfghdfghdfghdfh,All,Allow,*
User:dgndgh4g,Topic,PREFIXED,0dfghdfghd.,Read,Allow,*
'''.strip()

def test_mock_acl():
    fd = StringIO(MOCK_DATA)
    result = list()
    mock_data_csv_reader = DictReader(fd)
    mock_data_csv_reader.fieldnames
    for line in mock_data_csv_reader:
        acl = KafkaACLCSV(**line)
        acl.resource_type.validate_operation(acl.operation)
        result.append(acl)

    assert len(result) == 9
