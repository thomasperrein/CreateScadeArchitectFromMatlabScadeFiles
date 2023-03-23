""" Using error gestion for the archi code library """

class SanityCheckError(Exception):
    """ Sanity Check class """
    def __init__(self, message="Sanity checks of file don't pass"):
        self.message = message
        super().__init__(self.message)

class PortError(Exception):
    """ Port error class """
    def __init__(self, message="The object inside Block is not a common port"):
        self.message = message
        super().__init__(self.message)