from api.api_handler import ApiHandler

class ComethApiHandler(ApiHandler):
    def insertCometh(self, row, column, direction):
        self.addArgument('row', row)
        self.addArgument('column', column)
        self.addArgument('direction', direction)
        return self.generateRequest('POST', self.data)

    def deleteCometh(self, row, column):
        self.addArgument('row', row)
        self.addArgument('column', column)
        return self.generateRequest('DELETE', self.data)