aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 463470980614.dkr.ecr.ap-northeast-2.amazonaws.com

docker push 463470980614.dkr.ecr.ap-northeast-2.amazonaws.com/pyj/test_repo/job_posting:1
docker push 463470980614.dkr.ecr.ap-northeast-2.amazonaws.com/pyj/test_repo/user_service:1
docker push 463470980614.dkr.ecr.ap-northeast-2.amazonaws.com/pyj/test_repo/essay_service:1
docker push 463470980614.dkr.ecr.ap-northeast-2.amazonaws.com/pyj/test_repo/scheduling_service:1
docker push 463470980614.dkr.ecr.ap-northeast-2.amazonaws.com/pyj/test_repo/gaenchwis-frontend:1