from api.soloons_api import SoloonsApiHandler
from endpoint_secrets import kCrossmintAPIEndpoint

class Soloon:
    def __init__(self, row, column, color, candidateId):
        self.row = row
        self.column = column
        self.color = color
        self.soloonApiHandler = SoloonsApiHandler(kCrossmintAPIEndpoint + 'soloons', candidateId)

    def create(self):
        success = self.soloonApiHandler.insertSoloon(self.row, self.column, self.color)
        if success:
            print('Soloon created at ({}, {}) with color {}'.format(self.row, self.column, self.color))
        else:
            print('Failed to create Soloon at ({}, {})'.format(self.row, self.column))

    def remove(self):
        success = self.soloonApiHandler.deleteSoloon(self.row, self.column)
        if success == 200:
            print('Soloon removed at ({}, {})'.format(self.row, self.column))
        else:
            print('Failed to remove Soloon at ({}, {})'.format(self.row, self.column))
