import os
import requests
import json


class Bhashini:

    ulcaBaseURL = "https://meity-auth.ulcacontrib.org"
    modelPipelineEndpoint = "/ulca/apis/v0/model/getModelsPipeline"
    userId = os.getenv("ulcaUserID")
    apiKey = os.getenv("ulcaApiKey")


    def __init__(self):
        body = {
            "pipelineTasks" : [
                {
                    "taskType" : "asr"
                },
                {
                    "taskType": "translation"
                },
                {  
                    "taskType": "tts"
                }
            ],
            "pipelineRequestConfig" : {
                "pipelineId": "64392f96daac500b55c543cd"
            }
        }
        
        self.response = requests.post(url=self.ulcaBaseURL + self.modelPipelineEndpoint,json=body, headers={"userID": self.userId, "ulcaApiKey": self.apiKey}).json()
        self.asrData = self.response['pipelineResponseConfig'][0]['config']
        self.nmtData = self.response['pipelineResponseConfig'][1]['config']
        self.ttsData = self.response['pipelineResponseConfig'][2]['config']
        availableLang = ['bn', 'en', 'gu', 'hi', 'kn', 'ml', 'mr', 'or', 'pa','ta','te']
        self.asrConfigs = {}
        self.nmtConfigs = {}
        self.ttsConfigs = {}

        for i in availableLang:
            self.nmtConfigs[i] = []

        for i in self.asrData:
            if (i['language']['sourceLanguage'] in availableLang):
                self.asrConfigs[i['language']['sourceLanguage']] = i['serviceId']
          

        for i in availableLang:
            data = []
            for j in self.nmtData:
                if (j['language']['sourceLanguage'] == i):
                    data.append({'targetLanguage':j['language']['targetLanguage'],'serviceId': j['serviceId']})
            self.nmtConfigs[i] = data

        for i in self.ttsData:
            if (i['language']['sourceLanguage'] in availableLang):
                self.ttsConfigs[i['language']['sourceLanguage']] = i['serviceId']
          
      

        self.inferenceApiKey = {
            "Authorization":
            "hXd6A71xfDHygwnSEXUjFsmd64Vi8vpmhV4geokrx37JZQYXLf0QKsEaABvz4GRX"
        }

        self.callbackUrl = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

        # print(self.response['pipelineResponseConfig'])

    def sendHeaderWithConfig(self, sourceLanguage, targetLanguage):
        header = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": {
                            "sourceLanguage": sourceLanguage
                        }
                    }
                },
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": sourceLanguage,
                            "targetLanguage": targetLanguage
                        }
                    }
                },
                {
                    "taskType": "tts",
                    "config": {
                        "language": {
                            "sourceLanguage": targetLanguage
                        }
                    }
                }
            ],
            "pipelineRequestConfig": {
                "pipelineId": "64392f96daac500b55c543cd"
            }
        }
        try:
            response = requests.post(url=self.ulcaBaseURL + self.modelPipelineEndpoint, json=header, headers={"userID": self.userId, "ulcaApiKey": self.apiKey})
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return None
    

    def speechToText(self,sourceLanguage,asrServiceId,payload):
        body = {
                "pipelineTasks": [
                    {
                        "taskType": "asr",
                        "config": {
                            "language": {
                                "sourceLanguage": sourceLanguage
                            },
                            "serviceId": asrServiceId,
                            "audioFormat": "flac",
                            "samplingRate": 16000
                        }
                    }
                ],
                "inputData": {
                    "audio": [
                        {
                            "audioContent": payload
                        }
                    ]
                }
            }

        response = requests.post(self.callbackUrl,headers=self.inferenceApiKey,json=body).json()['pipelineResponse'][0]['output'][0]['source']
        return response


    def textTranslation(self,nmtServiceId,sourceLanguage,targetLanguage,text):
        body = {
                "pipelineTasks": [
                    {
                        "taskType": "translation",
                        "config": {
                            "language": {
                                "sourceLanguage": sourceLanguage,
                                "targetLanguage": targetLanguage
                            },
                            "serviceId": nmtServiceId
                        }
                    }
                ],
                "inputData": {
                    "input": [
                        {
                            "source": text
                        }
                    ]
                }
            }
        
        response = requests.post(self.callbackUrl,headers=self.inferenceApiKey,json=body)
        return response.json()


    def textToSpeech(self,ttsServiceId,text,targetLanguage):
        body = {
                "pipelineTasks": [       
                {
                    "taskType": "tts",
                    "config": {
                        "language": {
                            "sourceLanguage": targetLanguage
                        },
                        "serviceId": ttsServiceId,
                        "gender": "female",
                        "samplingRate": 8000
                    }
                }
            ],
            "inputData": {
                "input": [
                    {
                        "source": text
                    }
                ]
            }
        }

        response = requests.post(self.callbackUrl,headers=self.inferenceApiKey,json=body)
        return response.json()
    
    def audioToAudioTranslation(self,sourceLanguage,targetLanguage,sourceAudio,targetAudio):
        configs = {}
        
        ASRData = Bhashini().response['pipelineResponseConfig'][0]['config']
        for i in ASRData:
            if (i['language']['sourceLanguage'] == sourceLanguage):
                configs['asr'] = i['serviceId']

        NMTData = Bhashini().response['pipelineResponseConfig'][1]['config']
        for i in NMTData:
            if (i['language']['sourceLanguage'] == sourceLanguage and i['language']['targetLanguage'] == targetLanguage):
                configs['translation'] = i['serviceId']

        TTSData = Bhashini().response['pipelineResponseConfig'][2]['config']
        for i in TTSData:
            if (i['language']['sourceLanguage'] == targetLanguage):
                configs['tts'] = i['serviceId']

        if (sourceAudio != ""):
            
            speechToText = self.speechToText(sourceLanguage,configs["asr"],sourceAudio)
            textTranslation = self.textTranslation(configs['translation'],sourceLanguage,targetLanguage,speechToText['pipelineResponse'][0]['output'][0]['source'])
            textToSpeech = self.textToSpeech(configs['tts'],textTranslation['pipelineResponse'][0]['output'][0]['target'],targetLanguage)
            
            response = {'P1':{'text':speechToText['pipelineResponse'][0]['output'][0]['source'],'audio':sourceAudio,'emotion':'','intent':''},'P2':{'text':textTranslation['pipelineResponse'][0]['output'][0]['target'],'audio':textToSpeech['pipelineResponse'][0]['audio'][0]['audioContent'],'emotion':'','intent':''},'LM':0}
          
            return response
        
        
        speechToText = self.speechToText(sourceLanguage,configs["asr"],targetAudio)
        textTranslation = self.textTranslation(configs['translation'],sourceLanguage,targetLanguage,speechToText['pipelineResponse'][0]['output'][0]['source'])
        textToSpeech = self.textToSpeech(configs['tts'],textTranslation['pipelineResponse'][0]['output'][0]['target'],targetLanguage)
       
        response = {'P1':{'text':textTranslation['pipelineResponse'][0]['output'][0]['target'],'audio':textToSpeech['pipelineResponse'][0]['audio'][0]['audioContent'],'emotion':'','intent':''},'P2':{'text':speechToText['pipelineResponse'][0]['output'][0]['source'],'audio':targetAudio,'emotion':'','intent':''},'LM':0}
        
        return response
    
    def getAllTranslations(self,text,sourceLanguage):
        response = {}
        languageConfigs = self.nmtConfigs[sourceLanguage]

        for i in languageConfigs:
            response[i['targetLanguage']] = self.textTranslation(i['serviceId'],sourceLanguage,i['targetLanguage'],text)['pipelineResponse'][0]['output'][0]['target']

        return response

    def voiceTranslations(self,textTranslation):
        response = {}

        for i in self.ttsConfigs:
            # response[i] = self.(i,self.ttsConfigs[i],textTranslspeechToTextation)
            response[i] = self.textToSpeech(self.ttsConfigs[i],textTranslation[i],i)['pipelineResponse'][0]['audio'][0]['audioContent']

        return response

    def getAllVoiceTranslations(self,base64,sourceLanguage):
        
        voiceToText = self.speechToText(sourceLanguage,self.asrConfigs[sourceLanguage],base64)
        textTranslation = self.getAllTranslations(voiceToText,sourceLanguage)
        textTranslation[sourceLanguage] = voiceToText
        textToSpeech = self.voiceTranslations(textTranslation)
        
        return textToSpeech

        


# Bhashini().getAllVoiceTranslations(open('sourceAudio.txt').read(),'en')

# print(Bhashini().getAllTranslations('hi','en'))

# Bhashini().getAllVoiceTranslations()