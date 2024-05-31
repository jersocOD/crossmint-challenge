import requests
import json
import time

kCandidateId = '57c56985-13a3-43df-bdfc-a7489c3e99bc'
kCrossmintAPIEndpoint = 'https://challenge.crossmint.io/api/'
kPolyanetsUrl = kCrossmintAPIEndpoint + 'polyanets'
kMaxRetries = 20
class ApiHandler:
    def __init__(self, url, candidateId):
        self.url = url
        self.data = {'candidateId': candidateId}

    def generate_request(self, method, data):
        if method == 'POST':
            response = requests.post(self.url, data=data)
        elif method == 'DELETE':
            response = requests.delete(self.url, data=data)
        return response
    
    def add_argument(self, key, value):
        self.data[key] = value

class PolyanetApiHandler(ApiHandler):

    def __init__(self, url, candidateId):
        super().__init__(url, candidateId)

    def insert_polyanet(self, row, column):
        self.add_argument('row', row)
        self.add_argument('column', column)
        return self.generate_request('POST', self.data)

    def delete_polyanet(self, row, column):
        self.add_argument('row', row)
        self.add_argument('column', column)
        return self.generate_request('DELETE', self.data)

class Polyanet:
    def __init__(self, row, column, candidateId):
        self.row = row
        self.column = column
        self.candidateId = candidateId
        # Initialize the polyanet API handler and adds the polyanet to the map
        self.polyanetApiHandler = PolyanetApiHandler(kPolyanetsUrl, candidateId)
    def create(self):
        count = 0
        while count < kMaxRetries:
            response = self.polyanetApiHandler.insert_polyanet(self.row, self.column)
            if response.status_code == 200:
                print('Polyanet created at row: ' + str(self.row) + ' and column: ' + str(self.column))
                return True
            else:
                print('Failed to create Polyanet at row: ' + str(self.row) + ' and column: ' + str(self.column))
                print(response.status_code, response.text)
                count += 1
        return False
    def remove(self):
        # retry the request until it fails 20 times
        count = 0
        while count < kMaxRetries:
            response = self.polyanetApiHandler.delete_polyanet(self.row, self.column)
            if response.status_code == 200:
                print('Polyanet removed at row: ' + str(self.row) + ' and column: ' + str(self.column))
                return True
            else:
                print('Failed to remove Polyanet at row: ' + str(self.row) + ' and column: ' + str(self.column))
                print(response.status_code, response.text)
                count += 1
        return False
class Space:
    SPACE = 0
    POLYANET = 1

class Map:
    def __init__(self, candidateId):
        self.candidateId = candidateId
        self.map = [[0 for i in range(11)] for j in range(11)]
        self.goalMap = [[0 for i in range(11)] for j in range(11)]

    def getGoalMap(self):
        # call https://challenge.crossmint.io/api/map/57c56985-13a3-43df-bdfc-a7489c3e99bc/goal to get a json with the map 
        # and the goal
        url = kCrossmintAPIEndpoint + 'map/' + self.candidateId + '/goal'
        print(url)
        response = requests.get(url)
        data = response.json()
        print(data)
        self.goal = data['goal']
        
        for i in range(len(self.goal)):
            for j in range(len(self.goal[i])):
                if self.goal[i][j] == "SPACE":
                    self.goalMap[i][j] = Space.SPACE
                elif self.goal[i][j] == "POLYANET":
                    self.goalMap[i][j] = Space.POLYANET
    def deleteAllPolyanets(self, candidateId):
        for i in range(11):
            for j in range(11):
                Polyanet(i, j, candidateId).remove()
    def generateGoalMap(self):
        # generate a map with the goal
        for i in range(11):
            for j in range(11):
                if self.goalMap[i][j] == Space.POLYANET:
                    Polyanet(i, j, self.candidateId).create()
    def generateXMap(self):
        # generate a map with X leaving two elements of padding on the sides
        for i in range(2, 9):
            Polyanet(i, i, kCandidateId).create()
            Polyanet(i, 10 - i, kCandidateId).create()
                
def main():
    map = Map(kCandidateId)
    map.getGoalMap()
    map.generateGoalMap()
    # map.generateXMap()
    # map.deleteAllPolyanets(kCandidateId)

main()