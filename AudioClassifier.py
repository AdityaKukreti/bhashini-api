import requests

class AudioClassifier:
	
    def __init__(self) -> None:
        
        self.API_URL = "https://we5zf1eayf3g9pwi.us-east-1.aws.endpoints.huggingface.cloud"
        self.headers = {
            "Accept" : "application/json",
            "Authorization": "Bearer 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",
            "Content-Type": "audio/flac" 
        }

    def query(self,filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(self.API_URL, headers=self.headers, data=data)
        return response.json()

        
