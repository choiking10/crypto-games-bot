
class CryptoException(BaseException):

    def __init__(self, s):
        self.message = s
