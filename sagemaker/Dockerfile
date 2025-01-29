FROM 763104351884.dkr.ecr.ap-northeast-2.amazonaws.com/pytorch-inference:2.0.1-cpu-py310

WORKDIR /opt/ml/model

RUN pip install --no-cache-dir boto3 numpy flask gunicorn torch torchvision

COPY . /opt/ml/model/code

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "code.inference:app"]
