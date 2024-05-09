from flask import Flask,request,jsonify
from BhashiniAPI import *
from AudioClassifier import AudioClassifier
from voiceToText import VoiceToText
from likenessAndIntent import LikenessAndIntent
import base64



# os.mkdir('uploads')
UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bhashiniApi = Bhashini()
audioClassifier = AudioClassifier()
voiceToText = VoiceToText()
likenessAndIntent = LikenessAndIntent()

@app.route('/')
def initialRoute():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bhashini API Endpoints</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 1000px;
            padding: 20px;
        }
        .card {
            background-color: #fff;
            border-radius: 10px;
            margin-bottom: 20px;
            padding: 20px;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2);
        }
        .card h2 {
            margin-top: 0;
            color: #007bff;
        }
        .card p {
            color: #666;
            margin-bottom: 5px;
        }
        .method {
            background-color: #007bff;
            color: #fff;
            padding: 3px 8px;
            border-radius: 3px;
            margin-right: 5px;
        }
        .description {
            margin-bottom: 10px;
        }
        .argument-container,
        .response-container {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
            background-color: #f9f9f9;
        }
        .argument-container h3,
        .response-container h3 {
            margin-top: 0;
            color: #007bff;
        }
        .argument-list,
        .response-list {
            list-style: none;
            padding: 0;
        }
        .argument-item,
        .response-item {
            margin-bottom: 5px;
        }
        .argument-item span.data-type,
        .response-item span.data-type {
            color: #28a745;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h2>/textTranslation</h2>
            <div class="description">
                <p><b>Description:</b> Translate text from one language to another.</p>
                <p><b>Method:</b> <span class="method">POST</span></p>
            </div>
            <div class="argument-container">
                <h3>Arguments:</h3>
                <ul class="argument-list">
                    <li class="argument-item"><b>sourceLanguage:</b> <span class="data-type">string</span></li>
                    <li class="argument-item"><b>targetLanguage:</b> <span class="data-type">string</span></li>
                    <li class="argument-item"><b>nmtServiceId:</b> <span class="data-type">string</span></li>
                    <li class="argument-item"><b>text:</b> <span class="data-type">string</span></li>
                </ul>
            </div>
            <div class="response-container">
                <h3>Response:</h3>
                <ul class="response-list">
                    <li class="response-item"><b>TranslatedText:</b> <span class="data-type">string</span></li>
                </ul>
            </div>
        </div>

        <div class="card">
            <h2>/textToSpeech</h2>
            <div class="description">
                <p><b>Description:</b> Convert text to speech in the specified language.</p>
                <p><b>Method:</b> <span class="method">POST</span></p>
            </div>
            <div class="argument-container">
                <h3>Arguments:</h3>
                <ul class="argument-list">
                    <li class="argument-item"><b>targetLanguage:</b> <span class="data-type">string</span></li>
                    <li class="argument-item"><b>ttsServiceId:</b> <span class="data-type">string</span></li>
                    <li class="argument-item"><b>text:</b> <span class="data-type">string</span></li>
                </ul>
            </div>
            <div class="response-container">
                <h3>Response:</h3>
                <ul class="response-list">
                    <li class="response-item"><b>Audio:</b> <span class="data-type">audio</span></li>
                </ul>
            </div>
        </div>

        <div class="card">
            <h2>/getTranslations</h2>
            <div class="description">
                <p><b>Description:</b> Translate audio from one language to another.</p>
                <p><b>Method:</b> <span class="method">POST</span></p>
            </div>
            <div class="argument-container">
                <h3>Arguments:</h3>
                <ul class="argument-list">
                    <li class="argument-item"><b>sourceLanguage:</b> <span class="data-type">string</span></li>
                    <li class="argument-item"><b>targetLanguage:</b> <span class="data-type">string</span></li>
                    <li class="argument-item"><b>sourceAudio:</b> <span class="data-type">audio</span></li>
                    <li class="argument-item"><b>targetAudio:</b> <span class="data-type">audio</span></li>
                </ul>
            </div>
            <div class="response-container">
                <h3>Response:</h3>
                <ul class="response-list">
                    <li class="response-item"><b>TranslatedAudio:</b> <span class="data-type">audio</span></li>
                </ul>
            </div>
        </div>

        <div class="card">
            <h2>/audioSentiment</h2>
            <div class="description">
                <p><b>Description:</b> Analyze sentiment of the provided audio file.</p>
                <p><b>Method:</b> <span class="method">POST</span></p>
            </div>
            <div class="argument-container">
                <h3>Arguments:</h3>
                <ul class="argument-list">
                    <li class="argument-item"><b>file:</b> <span class="data-type">audio</span></li>
                </ul>
            </div>
            <div class="response-container">
                <h3>Response:
                <ul class="response-list">
                    <li class="response-item"><b>Sentiment:</b> <span class="data-type">string</span></li>
                </ul>
            </div>
        </div>

        <div class="card">
            <h2>/getAllTextTranslations</h2>
            <div class="description">
                <p><b>Description:</b> Get translations of the provided text in multiple languages.</p>
                <p><b>Method:</b> <span class="method">POST</span></p>
            </div>
            <div class="argument-container">
                <h3>Arguments:</h3>
                <ul class="argument-list">
                    <li class="argument-item"><b>text:</b> <span class="data-type">string</span></li>
                    <li class="argument-item"><b>sourceLanguage:</b> <span class="data-type">string</span></li>
                </ul>
            </div>
            <div class="response-container">
                <h3>Response:</h3>
                <ul class="response-list">
                    <li class="response-item"><b>Translations:</b> <span class="data-type">map[string]string</span></li>
                </ul>
            </div>
        </div>

        <div class="card">
            <h2>/getAllVoiceTranslations</h2>
            <div class="description">
                <p><b>Description:</b> Get translations of the provided audio file in multiple languages.</p>
                <p><b>Method:</b> <span class="method">POST</span></p>
            </div>
            <div class="argument-container">
                <h3>Arguments:</h3>
                <ul class="argument-list">
                    <li class="argument-item"><b>audio_file:</b> <span class="data-type">audio</span></li>
                    <li class="argument-item"><b>sourceLanguage:</b> <span class="data-type">string</span></li>
                </ul>
            </div>
            <div class="response-container">
                <h3>Response:</h3>
                <ul class="response-list">
                    <li class="response-item"><b>Audios:</b> <span class="data-type">map[string]string</span></li>
                    <li class="response-item"><b>Transcriptions:</b> <span class="data-type">map[string]string</span></li>
                    <li class="response-item"><b>Sentiment:</b> <span class="data-type">string</span></li>
                </ul>
            </div>
        </div>

        <div class="card">
            <h2>/getLikenessAndIntent</h2>
            <div class="description">
                <p><b>Description:</b> Analyze likeness and intent of the provided conversation.</p>
                <p><b>Method:</b> <span class="method">POST</span></p>
            </div>
            <div class="argument-container">
                <h3>Arguments:</h3>
                <ul class="argument-list">
                    <li class="argument-item"><b>conversation:</b> <span class="data-type">string</span></li>
                </ul>
            </div>
            <div class="response-container">
                <h3>Response:</h3>
                <ul class="response-list">
                    <li class="response-item"><b>Response:</b> <span class="data-type">string</span></li>
                </ul>
            </div>
        </div>
    </div>
    </div>
</body>
</html>


    """


    

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



@app.route('/getAllVoiceTranslations', methods=['POST'])
def getAllVoiceTranslations():

    data = request.get_json()
    audio = base64.b64decode(data['base64'])
    sourceLanguage = data['sourceLanguage']
    with open("audioFile.mp3","wb") as f:
        f.write(audio)
    

    text = voiceToText.getTranscription("audioFile.mp3",sourceLanguage)
    response = bhashiniApi.getAllVoiceTranslations(text, sourceLanguage)


    return jsonify({'response': response,'sentiment':audioClassifier.query("audioFile.mp3")})


@app.route('/getLikenessAndIntent', methods = ['POST'])
def getLikenessAndIntent():
    
    data = request.get_json()
    conversation = data['conversation']

    return jsonify({"response":likenessAndIntent.analyze_conversation(conversation)})



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
