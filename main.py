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
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            font-size: 28px;
            color: #333;
            margin-bottom: 20px;
        }
        h2 {
            font-size: 24px;
            color: #555;
            margin-top: 30px;
            margin-bottom: 10px;
        }
        p, ul {
            font-size: 16px;
            color: #666;
        }
        ul {
            margin-left: 20px;
            list-style-type: disc;
        }
        li {
            margin-bottom: 5px;
        }
        b {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>API Endpoints</h1>
        <p>Below are the available endpoints:</p>
        
        <h2>/config</h2>
        <p><b>Method:</b> POST</p>
        <p><b>Arguments:</b></p>
        <ul>
            <li>sourceLanguage (string)</li>
            <li>targetLanguage (string)</li>
        </ul>

        <h2>/speechTranslation</h2>
        <p><b>Method:</b> POST</p>
        <p><b>Arguments:</b></p>
        <ul>
            <li>sourceLanguage (string)</li>
            <li>targetLanguage (string)</li>
            <li>asrServiceId (string)</li>
            <li>nmtServiceId (string)</li>
            <li>ttsServiceId (string)</li>
            <li>payload (string)</li>
            <li>computeCallAuthName (string)</li>
            <li>computeCallAuthValue (string)</li>
            <li>callbackURL (string)</li>
        </ul>

        <h2>/speechToText</h2>
        <p><b>Method:</b> POST</p>
        <p><b>Arguments:</b></p>
        <ul>
            <li>sourceLanguage (string)</li>
            <li>asrServiceId (string)</li>
            <li>payload (string)</li>
            <li>computeCallAuthName (string)</li>
            <li>computeCallAuthValue (string)</li>
            <li>callbackURL (string)</li>
        </ul>

        <h2>/textTranslation</h2>
        <p><b>Method:</b> POST</p>
        <p><b>Arguments:</b></p>
        <ul>
            <li>sourceLanguage (string)</li>
            <li>targetLanguage (string)</li>
            <li>nmtServiceId (string)</li>
            <li>text (string)</li>
            <li>computeCallAuthName (string)</li>
            <li>computeCallAuthValue (string)</li>
            <li>callbackURL (string)</li>
        </ul>

        <h2>/textToSpeech</h2>
        <p><b>Method:</b> POST</p>
        <p><b>Arguments:</b></p>
        <ul>
            <li>targetLanguage (string)</li>
            <li>ttsServiceId (string)</li>
            <li>text (string)</li>
            <li>computeCallAuthName (string)</li>
            <li>computeCallAuthValue (string)</li>
            <li>callbackURL (string)</li>
        </ul>

        <h2>/getTranslations</h2>
        <p><b>Method:</b> POST</p>
        <p><b>Arguments:</b></p>
        <ul>
            <li>sourceLanguage (string)</li>
            <li>targetLanguage (string)</li>
            <li>sourceAudio (string)</li>
            <li>targetAudio (string)</li>
        </ul>
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
