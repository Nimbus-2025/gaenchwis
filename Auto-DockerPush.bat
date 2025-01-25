aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 463470980614.dkr.ecr.ap-northeast-2.amazonaws.com

docker push piwhyjey/job_posting:1
docker push piwhyjey/user_service:1
docker push piwhyjey/essay_service:2
docker push piwhyjey/scheduling_service:1
docker push piwhyjey/gaenchwis-frontend:1