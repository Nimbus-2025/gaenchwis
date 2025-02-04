aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 463470980614.dkr.ecr.ap-northeast-2.amazonaws.com
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.ap-northeast-2.amazonaws.com

docker build --platform linux/amd64 --provenance=false --output oci-mediatypes=false,type=image,push=true -t 463470980614.dkr.ecr.ap-northeast-2.amazonaws.com/gaenchwis/sagemaker:1.0.0 .