from flask import Flask,request,jsonify
from BhashiniAPI import *

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
bhashiniApi = Bhashini()

@app.route('/')
def initialRoute():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>API Endpoints</title>
<style>
body {
    font-family: Arial, sans-serif;
    margin: 20px;
    color: #333;
    background-color: #f7f7f7;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 5px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.endpoint {
    margin-bottom: 40px;
    padding: 20px;
    border-radius: 5px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.endpoint h2 {
    color: #007bff;
    margin-top: 0;
}

.endpoint p {
    margin-bottom: 10px;
}

.endpoint pre {
    background-color: #f4f4f4;
    padding: 10px;
    border-radius: 5px;
    overflow-x: auto;
}

</style>
</head>
<body>

<div class="container">
    <div class="endpoint">
        <h2>/</h2>
        <p><strong>Description:</strong> Home Route</p>
        <p>Returns a brief description of all available routes.</p>
    </div>

    <div class="endpoint">
        <h2>/config</h2>
        <p><strong>Method:</strong> POST</p>
        <p><strong>Description:</strong> Get the service IDs and model IDs.</p>
        <p><strong>JSON Data:</strong></p>
        <pre>
{
  "sourceLanguage": "string",
  "targetLanguage": "string"
}
        </pre>
        <p><strong>Returns:</strong></p>
        <pre>
{
  "response": {
    "data": "string"
  }
}
        </pre>
    </div>

    <div class="endpoint">
        <h2>/speechTranslation</h2>
        <p><strong>Method:</strong> POST</p>
        <p><strong>Description:</strong> Get speech translation from source to target language.</p>
        <p><strong>JSON Data:</strong></p>
        <pre>
{
  "sourceLanguage": "string",
  "targetLanguage": "string",
  "asrServiceId": "string",
  "nmtServiceId": "string",
  "ttsServiceId": "string",
  "payload": "string",
  "computeCallAuthName": "string",
  "computeCallAuthValue": "string",
  "callbackURL": "string"
}
        </pre>
        <p><strong>Returns:</strong></p>
        <pre>
{
  "translatedAudio": "string"
}
        </pre>
    </div>

    <div class="endpoint">
        <h2>/speechToText</h2>
        <p><strong>Method:</strong> POST</p>
        <p><strong>Description:</strong> Get audio transcription.</p>
        <p><strong>JSON Data:</strong></p>
        <pre>
{
  "sourceLanguage": "string",
  "asrServiceId": "string",
  "payload": "string",
  "computeCallAuthName": "string",
  "computeCallAuthValue": "string",
  "callbackURL": "string"
}
        </pre>
        <p><strong>Returns:</strong></p>
        <pre>
{
  "response": {
    "data": "string"
  }
}
        </pre>
    </div>

    <div class="endpoint">
        <h2>/textTranslation</h2>
        <p><strong>Method:</strong> POST</p>
        <p><strong>Description:</strong> Get translation of text from source to target language.</p>
        <p><strong>JSON Data:</strong></p>
        <pre>
{
  "sourceLanguage": "string",
  "targetLanguage": "string",
  "nmtServiceId": "string",
  "text": "string",
  "computeCallAuthName": "string",
  "computeCallAuthValue": "string",
  "callbackURL": "string"
}
        </pre>
        <p><strong>Returns:</strong></p>
        <pre>
{
  "response": {
    "data": "string"
  }
}
        </pre>
    </div>

    <div class="endpoint">
        <h2>/textToSpeech</h2>
        <p><strong>Method:</strong> POST</p>
        <p><strong>Description:</strong> Get audio of the text.</p>
        <p><strong>JSON Data:</strong></p>
        <pre>
{
  "targetLanguage": "string",
  "ttsServiceId": "string",
  "text": "string",
  "computeCallAuthName": "string",
  "computeCallAuthValue": "string",
  "callbackURL": "string"
}
        </pre>
        <p><strong>Returns:</strong></p>
        <pre>
{
  "response": {
    "data": "string"
  }
}
        </pre>
    </div>

    <div class="endpoint">
        <h2>/getTranslations</h2>
        <p><strong>Method:</strong> POST</p>
        <p><strong>Description:</strong> Get translation of audio from source to target language.</p>
        <p><strong>JSON Data:</strong></p>
        <pre>
{
  "sourceLanguage": "string",
  "targetLanguage": "string",
  "sourceAudio": "string",
  "targetAudio": "string"
}
        </pre>
        <p><strong>Returns:</strong></p>
        <pre>
{
  "response": {
    "data": "string"
  }
}
        </pre>
    </div>
</div>

</body>
</html>
"""

@app.route('/config', methods = ['POST'])
def getConfig():
    data = request.get_json()
    sourceLanguage = data['sourceLanguage']
    targetLanguage = data['targetLanguage']
    return jsonify({'response':bhashiniApi.sendHeaderWithConfig(sourceLanguage,targetLanguage)})

@app.route('/speechTranslation',methods = ['POST'])
def speechTranslation():
    data = request.get_json()
    sourceLanguage = data['sourceLanguage']
    targetLanguage = data['targetLanguage']
    asrServiceId = data['asrServiceId']
    nmtServiceId = data['nmtServiceId']
    ttsServiceId = data['ttsServiceId']
    payload = data['payload']
    computeCallAuthName = data['computeCallAuthName']
    computeCallAuthValue = data['computeCallAuthValue']
    callbackURL = data['callbackURL']

    audioText = bhashiniApi.speechToText(sourceLanguage,asrServiceId,payload,computeCallAuthName,computeCallAuthValue,callbackURL)['pipelineResponse'][0]['output'][0]['source']
    translatedText = bhashiniApi.textTranslation(callbackURL,nmtServiceId,sourceLanguage,targetLanguage,audioText,computeCallAuthName,computeCallAuthValue)['pipelineResponse'][0]['output'][0]['target']
    textAudio = bhashiniApi.textToSpeech(callbackURL,ttsServiceId,translatedText,targetLanguage,computeCallAuthName,computeCallAuthValue)['pipelineResponse'][0]['audio'][0]['audioContent']
    return jsonify({"translatedAudio":textAudio})


@app.route('/speechToText', methods = ['POST'])
def speechRecognition():
    data = request.get_json()
    sourceLanguage = data['sourceLanguage']
    asrServiceId = data['asrServiceId']
    payload = data['payload']
    computeCallAuthName = data['computeCallAuthName']
    computeCallAuthValue = data['computeCallAuthValue']
    callbackURL = data['callbackURL']
    return jsonify({'response':bhashiniApi.speechToText(sourceLanguage,asrServiceId,payload,computeCallAuthName,computeCallAuthValue,callbackURL)})

@app.route('/textTranslation',methods = ['POST'])
def textTranslation():
    data = request.get_json()
    sourceLanguage = data['sourceLanguage']
    targetLanguage = data['targetLanguage']
    nmtServiceId = data['nmtServiceId']
    text = data['text']
    computeCallAuthName = data['computeCallAuthName']
    computeCallAuthValue = data['computeCallAuthValue']
    callbackURL = data['callbackURL']

    return jsonify({'response':bhashiniApi.textTranslation(callbackURL,nmtServiceId,sourceLanguage,targetLanguage,text,computeCallAuthName,computeCallAuthValue)})


@app.route('/textToSpeech',methods = ['POST'])
def textToSpeech():
    data = request.get_json()
    targetLanguage = data['targetLanguage']
    ttsServiceId = data['ttsServiceId']
    text = data['text']
    computeCallAuthName = data['computeCallAuthName']
    computeCallAuthValue = data['computeCallAuthValue']
    callbackURL = data['callbackURL']

    return jsonify({'respnse':bhashiniApi.textToSpeech(callbackURL,ttsServiceId,text,targetLanguage,computeCallAuthName,computeCallAuthValue)})


@app.route('/getTranslations', methods = ['POST'])
def getTranslation():
    data = request.get_json()
    sourceLanguage = data['sourceLanguage']
    targetLanguage = data['targetLanguage']
    sourceAudio= data['sourceAudio']
    targetAudio = data['sourceAudio']
    return jsonify({'response':bhashiniApi.audioToAudioTranslation(sourceLanguage,targetLanguage,sourceAudio,targetAudio)})
    
   


if (__name__ == '__main__'):
    app.run(host = "0.0.0.0", port = 10000)
