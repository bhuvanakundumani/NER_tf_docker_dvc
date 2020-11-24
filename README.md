
NER TF 2.0 inference(single sentence)for CoNLL-2003 NER dataset. 

A detailed blog for training the model in TF 2.0 is available at

https://medium.com/analytics-vidhya/ner-tensorflow-2-2-0-9f10dcf5a0a. 

## S3 credentials
Create a file .env with secrets
``` bash
AWS_ACCESS_KEY_ID=aws_access_key_id
AWS_SECRET_ACCESS_KEY=aws_secret_access_key
```
## Docker instructions
- To build and start the container

```bash
docker-compose up
```

- To stop the container

```bash
docker-compose down
```

## cURL 
- test 

```bash 
curl -i -H "Content-Type: application/json" \
-X POST http://0.0.0.0:8088/test
```
- single sentence 

```bash 
curl -i -H "Content-Type: application/json" \
-X POST http://0.0.0.0:8088/ner -d '{"sent":"Steve went to Paris"}'
```

## Setup without docker 
- Please refer the code [Here](https://github.com/bhuvanakundumani/NER_tf_dvc_s3)

