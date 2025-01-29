aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 463470980614.dkr.ecr.ap-northeast-2.amazonaws.com

docker push 463470980614.dkr.ecr.ap-northeast-2.amazonaws.com/gaenchwis/sagemaker:1.0.0