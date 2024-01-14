class SegmentParserFactory():
    def __init__(self):
        # TODO
        return
    
    def generate(self, signature, length = None):
        if signature == 0xffd8:
            # TODO
        elif signature == 0xffd9:
            # TODO
        elif signature == 0xffe0:
            # TODO
        elif signature == 0xffdb:
            # TODO
        elif signature == 0xffc0:
            # TODO
        elif signature == 0xffc4:
            # TODO
        elif signature == 0xffda:
            # TODO
        else:
            raise ValueError(f'Found section signature {signature} which is not supported.')
        
        return
    
