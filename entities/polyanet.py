from endpoint_secrets import kCrossmintAPIEndpoint
from api.polyanet_api import PolyanetApiHandler

class Polyanet:
    def __init__(self, row, column, candidateId):
        self.row = row
        self.column = column
        self.candidateId = candidateId
        # Initialize the polyanet API handler and adds the polyanet to the map
        self.polyanetApiHandler = PolyanetApiHandler(kCrossmintAPIEndpoint + 'polyanets', candidateId)
    def create(self): 
        success = self.polyanetApiHandler.insertPolyanet(self.row, self.column)
        if success:
            print('Polyanet created at row: ' + str(self.row) + ' and column: ' + str(self.column))
        else:
            print('Failed to create Polyanet at row: ' + str(self.row) + ' and column: ' + str(self.column))
    def remove(self):
        success = self.polyanetApiHandler.deletePolyanet(self.row, self.column)
        if success:
            print('Polyanet removed at row: ' + str(self.row) + ' and column: ' + str(self.column))
        else:
            print('Failed to remove Polyanet at row: ' + str(self.row) + ' and column: ' + str(self.column))
    
