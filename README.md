
NER TF 2.0 inference(single sentence)for CoNLL-2003 NER dataset. 

(Inference for single sentence)

A detailed blog for training the model in TF 2.0 is available at

https://medium.com/analytics-vidhya/ner-tensorflow-2-2-0-9f10dcf5a0a. 

## Folder structure

- Download and store glove.6B.100d.txt from [here](http://nlp.stanford.edu/data/glove.6B.zip)
- data folder has the dataset. 
- model output files after training will be written to the model_outout directory.

```
├── data
│   ├── train.txt
│   ├── valid.txt
│   ├── test.txt
│
├── embeddings
│   ├── glove.6B.100d.txt
│   
├── model_output
│   ├── checkpoint
│   ├── embedding.pkl
│   ├── idx2Label.pkl
│   ├── model_weights.data-00000-of-00001
│   ├── model_weights.index
│   ├── word2Idx.pkl
│   
```
## Setup 
```bash
python3 -m venv venv1
source venv1/bin/activate
pip install -r requirements.txt
```
## Model training 
``` bash
python3 train.py --data data --output  model_output --overwrite True 
```

## API
```bash 
python3 api.py
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


Predict on test Dataset
```bash
python3 predict.py --data data --model_dir models_output
```
Predict a single sentence - Assign the sentence to test_sentence variable. 

```bash
python3 predict.py --data data --model_dir models_output --predsingle True
```

Visualisations 
```bash
tensorboard --logdir=model_output/logs/train --port=6006 --bind_all
tensorboard --logdir=model_output/logs/valid --port=6006 --bind_all
```

