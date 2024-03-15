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