class DynamoDBException(Exception):
    """DynamoDB 관련 기본 예외 클래스"""
    pass

class TableNotFoundException(DynamoDBException):
    """테이블을 찾을 수 없을 때 발생하는 예외"""
    pass

class ConditionCheckFailedException(DynamoDBException):
    """조건부 작업 실패시 발생하는 예외"""
    pass

class ValidationException(DynamoDBException):
    """데이터 유효성 검증 실패시 발생하는 예외"""
    pass

class OperationException(DynamoDBException):
    """DynamoDB 작업 수행 중 발생하는 예외"""
    pass