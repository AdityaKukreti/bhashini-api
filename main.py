from flask import Flask,request,jsonify
from BhashiniAPI import *

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
bhashiniApi = Bhashini()

@app.route('/')
def initialRoute():
    return "<p>call the <b>/config</b> route to get the service ids and model ids</p>"

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


   


if (__name__ == '__main__'):
    app.run(host = "0.0.0.0", port = 10000)

