# aws_service/exceptions.py
class AWSServiceException(Exception):
    """AWS 서비스 관련 기본 예외 클래스"""
    pass

class StorageException(AWSServiceException):
    """스토리지 서비스 관련 예외"""
    pass