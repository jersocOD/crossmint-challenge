from api.cometh_api import ComethApiHandler
from endpoint_secrets import kCrossmintAPIEndpoint

class Cometh:
    def __init__(self, row, column, direction, candidateId):
        self.row = row
        self.column = column
        self.direction = direction
        self.comethApiHandler = ComethApiHandler(kCrossmintAPIEndpoint + 'comeths', candidateId)

    def create(self):
        success = self.comethApiHandler.insertCometh(self.row, self.column, self.direction)
        if success:
            print('Cometh created at ({}, {}) facing {}'.format(self.row, self.column, self.direction))
        else:
            print('Failed to create Cometh at ({}, {})'.format(self.row, self.column))

    def remove(self):
        success = self.comethApiHandler.deleteCometh(self.row, self.column)
        if success:
            print('Cometh removed at ({}, {})'.format(self.row, self.column))
        else:
            print('Failed to remove Cometh at ({}, {})'.format(self.row, self.column))