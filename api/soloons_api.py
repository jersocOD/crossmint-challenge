from api.api_handler import ApiHandler

class SoloonsApiHandler(ApiHandler):
    def insertSoloon(self, row, column, color):
        self.addArgument('row', row)
        self.addArgument('column', column)
        self.addArgument('color', color)
        return self.generateRequest('POST', self.data)

    def deleteSoloon(self, row, column):
        self.addArgument('row', row)
        self.addArgument('column', column)
        return self.generateRequest('DELETE', self.data)