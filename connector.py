# connector.py

CONNECTOR_HASH = None  # placeholder estructural

class TapizConnector:
    def __init__(self):
        pass

    def build_payload(self, state):
        raise NotImplementedError

    def send(self, payload):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError
