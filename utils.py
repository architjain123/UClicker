
class KeyManager:

    key_manager = ''

    def __init__(self):
        self.KEY = ''
        self.SECRETKEY = ''
        self.load_secret_keys()

    @staticmethod
    def getInstance():
        if KeyManager.key_manager == '':
            KeyManager.key_manager = KeyManager()
        return KeyManager.key_manager

    def load_secret_keys(self):
        with open("rootkey.csv", "r") as f:
            for line in f:
                key, value = line.split('=')
                if key.strip() == 'AWSAccessKeyId':
                    self.KEY = value.strip()
                if key.strip() == 'AWSSecretKey':
                    self.SECRETKEY = value.strip()