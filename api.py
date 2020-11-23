from flask import Flask, request, jsonify
from flask_cors import CORS
from ner import predict

app = Flask(__name__)
CORS(app)


@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'Health OK'

@app.route('/ner',methods=['GET', 'POST'])
def ner():
    text = request.json
    source_texts = text['sent']
    print(source_texts)
       # data = request.json["text"]
    result = predict(source_texts)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=True)