from flask import Flask,request,jsonify
from BhashiniAPI import *
from AudioClassifier import AudioClassifier
import json
import base64



# os.mkdir('uploads')
UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bhashiniApi = Bhashini()
audioClassifier = AudioClassifier()

@app.route('/')
def initialRoute():
    return """<p>call the <b>/config</b> route to get the service ids and model ids</p>
    <p>call the <b>/speechTranslation</b> route to get the speech translation from source to target language</p>
    <p>call the <b>/speechToText</b> route to get the audio transcription</p>
    <p>call the <b>/textTranslation</b> route to get the translation of text from source to target language</p>
    <p>call the <b>/textToSpeech</b> route to get the audio of the text</p>
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
    

    audioText = bhashiniApi.speechToText(sourceLanguage,asrServiceId,payload)['pipelineResponse'][0]['output'][0]['source']
    translatedText = bhashiniApi.textTranslation(nmtServiceId,sourceLanguage,targetLanguage,audioText)['pipelineResponse'][0]['output'][0]['target']
    textAudio = bhashiniApi.textToSpeech(ttsServiceId,translatedText,targetLanguage)['pipelineResponse'][0]['audio'][0]['audioContent']
    return jsonify({"translatedAudio":textAudio})


@app.route('/speechToText', methods = ['POST'])
def speechRecognition():
    data = request.get_json()
    sourceLanguage = data['sourceLanguage']
    asrServiceId = data['asrServiceId']
    payload = data['payload']
 
    return jsonify({'response':bhashiniApi.speechToText(sourceLanguage,asrServiceId,payload)})

@app.route('/textTranslation',methods = ['POST'])
def textTranslation():
    data = request.get_json()
    sourceLanguage = data['sourceLanguage']
    targetLanguage = data['targetLanguage']
    nmtServiceId = data['nmtServiceId']
    text = data['text']

    return jsonify({'response':bhashiniApi.textTranslation(nmtServiceId,sourceLanguage,targetLanguage,text)})


@app.route('/textToSpeech',methods = ['POST'])
def textToSpeech():
    data = request.get_json()
    targetLanguage = data['targetLanguage']
    ttsServiceId = data['ttsServiceId']
    text = data['text']
   

    return jsonify({'respnse':bhashiniApi.textToSpeech(ttsServiceId,text,targetLanguage)})


@app.route('/getTranslations', methods = ['POST'])
def getTranslation():
    data = request.get_json()
    sourceLanguage = data['sourceLanguage']
    targetLanguage = data['targetLanguage']
    sourceAudio= data['sourceAudio']
    targetAudio = data['sourceAudio']
    return jsonify({'response':bhashiniApi.audioToAudioTranslation(sourceLanguage,targetLanguage,sourceAudio,targetAudio)})

@app.route('/audioSentiment', methods = ['POST'])
def getSentiment():
    if 'file' in request.files:
        # File is uploaded
        file = request.files['file']

        if file.filename != '':
            # If a file is provided, save it
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

        return jsonify(audioClassifier.query(file_path))
    
   
@app.route('/getAllTextTranslations', methods = ['POST'])
def getAllTextTranslations():
    data = request.get_json()
    text = data['text']
    sourceLanguage = data['sourceLanguage']

    response = bhashiniApi.getAllTranslations(text,sourceLanguage)
    response[sourceLanguage] = text

    return jsonify({'response':response})

# @app.route('/getAllVoiceTranslations', methods = ['POST'])
# def getAllVoiceTranslations():
#     data = request.get_json()
#     sourceLanguage = data['sourceLanguage']
#     payload = data['payload']

#     payload = base64.b64encode(payload).decode('utf-8')

#     response = bhashiniApi.getAllVoiceTranslations(bhashiniApi.speechToText(sourceLanguage,payload),sourceLanguage)
    
#     with open(response,'r') as file:
#         return {"response":json.load(file)}

@app.route('/getAllVoiceTranslations', methods=['POST'])
def getAllVoiceTranslations():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and file.filename.lower().endswith('.mp3'):
        # Read the MP3 file and convert its data to base64
        file_data = file.read()
        payload = base64.b64encode(file_data).decode('utf-8')

        # Get the source language from the form data
        sourceLanguage = request.form.get('sourceLanguage')
        if sourceLanguage is None:
            return jsonify({"error": "Source language not provided"}), 400

        # Call the speechToText function with the payload and source language
        response = bhashiniApi.getAllVoiceTranslations(bhashiniApi.speechToText(sourceLanguage, payload), sourceLanguage)

        with open(response, 'r') as file:
            return jsonify({"response": json.load(file)})
    else:
        return jsonify({"error": "Invalid file format. Only MP3 files are allowed."}), 400

if (__name__ == '__main__'):
    app.run(host = "0.0.0.0", port = 10000)
