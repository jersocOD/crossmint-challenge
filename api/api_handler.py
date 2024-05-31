import requests

kMaxRetries = 20
class ApiHandler:
    def __init__(self, url, candidateId):
        self.url = url
        self.data = {'candidateId': candidateId}

    def generateRequest(self, method, data):
        count = 0
        while count < kMaxRetries:
            if method == 'POST':
                response = requests.post(self.url, data=data)
            elif method == 'DELETE':
                response = requests.delete(self.url, data=data)
            if response.status_code == 200:
                return True
            else:
                print('Failed to make request to ' + self.url)
                print(response.status_code, response.text)
                count += 1
        return False
    def addArgument(self, key, value):
        self.data[key] = value
