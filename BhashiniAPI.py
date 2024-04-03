import os
import requests


class Bhashini:

    ulcaBaseURL = "https://meity-auth.ulcacontrib.org"
    modelPipelineEndpoint = "/ulca/apis/v0/model/getModelsPipeline"
    userId = os.getenv("ulcaUserID")
    apiKey = os.getenv("ulcaApiKey")


    def __init__(self):
        pass

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
    

    def speechToText(self,sourceLanguage,asrServiceId,payload,computeCallAuthKey,computeCallAuthValue,callbackUrl):
        header = {computeCallAuthKey:computeCallAuthValue}
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

        response = requests.post(callbackUrl,headers=header,json=body)
        return response.json()


    def textTranslation(self,callbackUrl,nmtServiceId,sourceLanguage,targetLanguage,text,computeCallAuthKey,computeCallAuthValue):
        header = {computeCallAuthKey:computeCallAuthValue}
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
        
        response = requests.post(callbackUrl,headers=header,json=body)
        return response.json()


    def textToSpeech(self,callbackUrl,ttsServiceId,text,targetLanguage,computeCallAuthKey,computeCallAuthValue):
        header = {computeCallAuthKey:computeCallAuthValue}
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

        response = requests.post(callbackUrl,headers=header,json=body)
        return response.json()
    
    def audioToAudioTranslation(self,sourceLanguage,targetLanguage,sourceAudio,targetAudio):
        print(f"Source Language: {sourceLanguage}")
        print(f"Target Language: {targetLanguage}")
        if (sourceAudio != ""):
            configData = self.sendHeaderWithConfig(sourceLanguage,targetLanguage)
            configs = {'asr':configData['pipelineResponseConfig'][0]['config'][0],'translation':configData['pipelineResponseConfig'][1]['config'][0],'tts':configData['pipelineResponseConfig'][2]['config'][0]}
            pipelineInferenceAPIEndPoint = configData['pipelineInferenceAPIEndPoint']
        
            callbackUrl = pipelineInferenceAPIEndPoint['callbackUrl']
            inferenceApiKey = pipelineInferenceAPIEndPoint['inferenceApiKey']
            speechToText = self.speechToText(sourceLanguage,configs["asr"]['serviceId'],sourceAudio,inferenceApiKey['name'],inferenceApiKey['value'],callbackUrl)
            textTranslation = self.textTranslation(callbackUrl,configs['translation']['serviceId'],sourceLanguage,targetLanguage,speechToText['pipelineResponse'][0]['output'][0]['source'],inferenceApiKey['name'],inferenceApiKey['value'])
            textToSpeech = self.textToSpeech(callbackUrl,configs['tts']['serviceId'],textTranslation['pipelineResponse'][0]['output'][0]['target'],targetLanguage,inferenceApiKey['name'],inferenceApiKey['value'])
            # response = {'sourceLanguage':sourceLanguage,'targetLanguage':targetLanguage, 'sourceAudio':sourceAudio,'targetAudio':textToSpeech['pipelineResponse'][0]['audio'][0]['audioContent'],'sourceText':speechToText['pipelineResponse'][0]['output'][0]['source'],'targetText':textTranslation['pipelineResponse'][0]['output'][0]['target']}
            response = {'P1':{'text':speechToText['pipelineResponse'][0]['output'][0]['source'],'audio':sourceAudio,'emotion':'','intent':''},'P2':{'text':textTranslation['pipelineResponse'][0]['output'][0]['target'],'audio':textToSpeech['pipelineResponse'][0]['audio'][0]['audioContent'],'emotion':'','intent':''},'LM':0}
            print(f"Source Text: {response['P1']['text']}")
            print(f"Target Text: {response['P2']['text']}")
            return response
        
        configData = self.sendHeaderWithConfig(sourceLanguage,targetLanguage)
        configs = {'asr':configData['pipelineResponseConfig'][0]['config'][0],'translation':configData['pipelineResponseConfig'][1]['config'][0],'tts':configData['pipelineResponseConfig'][2]['config'][0]}
        pipelineInferenceAPIEndPoint = configData['pipelineInferenceAPIEndPoint']
        callbackUrl = pipelineInferenceAPIEndPoint['callbackUrl']
        inferenceApiKey = pipelineInferenceAPIEndPoint['inferenceApiKey']

        speechToText = self.speechToText(sourceLanguage,configs["asr"]['serviceId'],targetAudio,inferenceApiKey['name'],inferenceApiKey['value'],callbackUrl)
        textTranslation = self.textTranslation(callbackUrl,configs['translation']['serviceId'],sourceLanguage,targetLanguage,speechToText['pipelineResponse'][0]['output'][0]['source'],inferenceApiKey['name'],inferenceApiKey['value'])
        textToSpeech = self.textToSpeech(callbackUrl,configs['tts']['serviceId'],textTranslation['pipelineResponse'][0]['output'][0]['target'],targetLanguage,inferenceApiKey['name'],inferenceApiKey['value'])
        # response = {'sourceLanguage':sourceLanguage,'targetLanguage':targetLanguage, 'sourceAudio':sourceAudio,'targetAudio':textToSpeech['pipelineResponse'][0]['audio'][0]['audioContent'],'sourceText':speechToText['pipelineResponse'][0]['output'][0]['source'],'targetText':textTranslation['pipelineResponse'][0]['output'][0]['target']}
        # response = {'P1':{'text':speechToText['pipelineResponse'][0]['output'][0]['source'],'audio':sourceAudio,'emotion':'','intent':''},'P2':{'text':textTranslation['pipelineResponse'][0]['output'][0]['target'],'audio':textToSpeech['pipelineResponse'][0]['audio'][0]['audioContent'],'emotion':'','intent':''},'LM':0}
        response = {'P1':{'text':textTranslation['pipelineResponse'][0]['output'][0]['target'],'audio':textToSpeech['pipelineResponse'][0]['audio'][0]['audioContent'],'emotion':'','intent':''},'P2':{'text':speechToText['pipelineResponse'][0]['output'][0]['source'],'audio':targetAudio,'emotion':'','intent':''},'LM':0}
        return response

