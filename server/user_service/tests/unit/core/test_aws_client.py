import pytest
from app.core.aws_client import AWSClient

def test_get_client_singleton():
    client1 = AWSClient.get_client('dynamodb')
    client2 = AWSClient.get_client('dynamodb')
    assert client1 is client2  # 같은 인스턴스인지 확인

def test_get_client_different_services():
    dynamodb = AWSClient.get_client('dynamodb')
    cognito = AWSClient.get_client('cognito-idp')
    assert dynamodb is not cognito  # 다른 서비스는 다른 인스턴스