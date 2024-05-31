from entities.cometh import Cometh
from entities.polyanet import Polyanet
from entities.soloon import Soloon
import requests
from endpoint_secrets import kCrossmintAPIEndpoint

class Map:
    def __init__(self, candidateId):
        self.candidateId = candidateId
        self.map = [[None for _ in range(30)] for _ in range(30)]
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
        if not self.entities:
            print('No entities to create. Please call getGoalMap first to load entities.')
        for entity in self.entities:
            entity.create()

    def deleteAllEntities(self):
        # Delete all entities from the map in reverse to handle dependencies
        for entity in reversed(self.entities):
            entity.remove()

    def generateXMap(self):
        # Generate a map with X leaving two elements of padding on the sides for Phase 1
        for i in range(2, 9):
            Polyanet(i, i, self.candidateId).create()
            Polyanet(i, 10 - i, self.candidateId).create()