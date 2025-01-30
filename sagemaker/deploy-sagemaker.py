from sagemaker.model import Model
import sagemaker

sagemaker_session = sagemaker.Session()
role = "arn:aws:iam::463470980614:role/service-role/AmazonSageMaker-ExecutionRole-20250121T102660"

model = Model(
    image_uri="463470980614.dkr.ecr.ap-northeast-2.amazonaws.com/gaenchwis/sagemaker:1.0.0",
    role=role,
    sagemaker_session=sagemaker_session
)

predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="gaenchwis-recommendation"
)

print("SageMaker 엔드포인트 배포 완료!")