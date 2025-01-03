class AWSServiceException(Exception):
    # AWS 서비스 관련 기본 예외 클래스
    pass

class DynamoDBException(AWSServiceException):
    # DynamoDB 관련 예외
    pass

class S3Exception(AWSServiceException):
    # S3 관련 예외
    pass