from abc import ABC, abstractmethod

class ImageParser(ABC):
    def __init__(self):
        self.image_fp = None

    @abstractmethod
    def parse(self, filename):
        pass

    @abstractmethod
    def print_metadata(self):
        pass


