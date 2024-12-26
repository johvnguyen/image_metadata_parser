from abc import ABC, abstractmethod

class SegmentParser(ABC):
    @abstractmethod
    def parse(self, image_fp):
        pass
    
    @abstractmethod
    def print_metadata(self):
        pass


