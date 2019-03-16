class ProxyModel(object):
    def __init__(self,data):
        self.ip = data['ip']
        self.port = data['port']
        self.proxy = 'https://{}:{}'.format(self.ip,self.port)

