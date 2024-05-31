import requests

kCandidateId = '57c56985-13a3-43df-bdfc-a7489c3e99bc'
kCrossmintAPIEndpoint = 'https://challenge.crossmint.io/api/'
kPolyanetsUrl = kCrossmintAPIEndpoint + 'polyanets'
kMaxRetries = 20
class ApiHandler:
    def __init__(self, url, candidateId):
        self.url = url
        self.data = {'candidateId': candidateId}

    def generate_request(self, method, data):
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
        success = self.polyanetApiHandler.insert_polyanet(self.row, self.column)
        if success:
            print('Polyanet created at row: ' + str(self.row) + ' and column: ' + str(self.column))
        else:
            print('Failed to create Polyanet at row: ' + str(self.row) + ' and column: ' + str(self.column))
    def remove(self):
        success = self.polyanetApiHandler.delete_polyanet(self.row, self.column)
        if success:
            print('Polyanet removed at row: ' + str(self.row) + ' and column: ' + str(self.column))
        else:
            print('Failed to remove Polyanet at row: ' + str(self.row) + ' and column: ' + str(self.column))
    
class SoloonsApiHandler(ApiHandler):
    def insert_soloon(self, row, column, color):
        self.add_argument('row', row)
        self.add_argument('column', column)
        self.add_argument('color', color)
        return self.generate_request('POST', self.data)

    def delete_soloon(self, row, column):
        self.add_argument('row', row)
        self.add_argument('column', column)
        return self.generate_request('DELETE', self.data)

class ComethApiHandler(ApiHandler):
    def insert_cometh(self, row, column, direction):
        self.add_argument('row', row)
        self.add_argument('column', column)
        self.add_argument('direction', direction)
        return self.generate_request('POST', self.data)

    def delete_cometh(self, row, column):
        self.add_argument('row', row)
        self.add_argument('column', column)
        return self.generate_request('DELETE', self.data)

class Soloon:
    def __init__(self, row, column, color, candidateId):
        self.row = row
        self.column = column
        self.color = color
        self.soloonApiHandler = SoloonsApiHandler(kCrossmintAPIEndpoint + 'soloons', candidateId)

    def create(self):
        success = self.soloonApiHandler.insert_soloon(self.row, self.column, self.color)
        if success:
            print('Soloon created at ({}, {}) with color {}'.format(self.row, self.column, self.color))
        else:
            print('Failed to create Soloon at ({}, {})'.format(self.row, self.column))

    def remove(self):
        success = self.soloonApiHandler.delete_soloon(self.row, self.column)
        if success == 200:
            print('Soloon removed at ({}, {})'.format(self.row, self.column))
        else:
            print('Failed to remove Soloon at ({}, {})'.format(self.row, self.column))

class Cometh:
    def __init__(self, row, column, direction, candidateId):
        self.row = row
        self.column = column
        self.direction = direction
        self.comethApiHandler = ComethApiHandler(kCrossmintAPIEndpoint + 'comeths', candidateId)

    def create(self):
        success = self.comethApiHandler.insert_cometh(self.row, self.column, self.direction)
        if success:
            print('Cometh created at ({}, {}) facing {}'.format(self.row, self.column, self.direction))
        else:
            print('Failed to create Cometh at ({}, {})'.format(self.row, self.column))

    def remove(self):
        success = self.comethApiHandler.delete_cometh(self.row, self.column)
        if success:
            print('Cometh removed at ({}, {})'.format(self.row, self.column))
        else:
            print('Failed to remove Cometh at ({}, {})'.format(self.row, self.column))


class Space:
    SPACE = 0
    POLYANET = 1

import requests

class Map:
    def __init__(self, candidateId):
        self.candidateId = candidateId
        self.map = [[None for _ in range(30)] for _ in range(30)]  # Adjusted for a 30x30 grid based on your data
        self.entities = []

    def getGoalMap(self):
        url = kCrossmintAPIEndpoint + 'map/' + self.candidateId + '/goal'
        response = requests.get(url)
        data = response.json()
        goal = data['goal']

        # Parse the goal map and instantiate objects
        for i, row in enumerate(goal):
            for j, cell in enumerate(row):
                if cell == "POLYANET":
                    self.entities.append(Polyanet(i, j, self.candidateId))
                elif "SOLOON" in cell:
                    color = cell.split('_')[0]
                    self.entities.append(Soloon(i, j, color.lower(), self.candidateId))
                elif "COMETH" in cell:
                    direction = cell.split('_')[0]
                    self.entities.append(Cometh(i, j, direction.lower(), self.candidateId))

    def generateGoalMap(self):
        # Create all entities on the map
        for entity in self.entities:
            entity.create()

    def deleteAllEntities(self):
        # Delete all entities from the map in reverse to handle dependencies
        for entity in reversed(self.entities):
            entity.remove()

    def generateXMap(self):
        # Generate a map with X leaving two elements of padding on the sides
        for i in range(2, 9):
            Polyanet(i, i, kCandidateId).create()
            Polyanet(i, 10 - i, kCandidateId).create()
                
def main():
    map = Map(kCandidateId)
    map.getGoalMap()
    # map.deleteAllEntities()
    map.generateGoalMap()
    # map.generateXMap()
    # map.deleteAllPolyanets(kCandidateId)

main()