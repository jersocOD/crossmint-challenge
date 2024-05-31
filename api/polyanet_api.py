from api.api_handler import ApiHandler

class PolyanetApiHandler(ApiHandler):

    def __init__(self, url, candidateId):
        super().__init__(url, candidateId)

    def insertPolyanet(self, row, column):
        self.addArgument('row', row)
        self.addArgument('column', column)
        return self.generateRequest('POST', self.data)


    def deletePolyanet(self, row, column):
        self.addArgument('row', row)
        self.addArgument('column', column)
        return self.generateRequest('DELETE', self.data)
