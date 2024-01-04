from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class tIMEChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(data_len == 7)
        assert(chunk_type == 'tIME')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        

        self.parse_time(image_fp)

        return

    def parse_time(self, image_fp):
        time_format_string = '>HBBBBB'
        time_size = struct.calcsize(time_format_string)
        time_bytes = image_fp.read(time_size)
        time_data = struct.Struct(time_format_string).unpack_from(time_bytes)

        self.validate_time_data(time_data)

        self.data['Year'] = time_data[0]
        self.data['Month'] = time_data[1]
        self.data['Day'] = time_data[2]
        self.data['Hour'] = time_data[3]
        self.data['Minute'] = time_data[4]
        self.data['Second'] = time_data[5]

        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)[0]

        return

    def validate_time_data(self, time_data):
        year = time_data[0]
        month = time_data[1]
        day = time_data[2]
        hour = time_data[3]
        minute = time_data[4]
        second = time_data[5]

        self.validate_month(month)
        self.validate(day)
        self.validate_hour(hour)
        self.validate_minute(minute)
        self.validate_second(second)

        return

    def validate_month(self, month):
        assert(1 <= month)
        assert(month <= 12)

        return

    def validate_day(self, day):
        assert(1 <= day)
        assert(day <= 31)

        return

    def validate_hour(self, hour):
        assert(0 <= hour)
        assert(hour <= 23)

        return

    def validate_minute(self, minute):
        assert(0 <= minute)
        assert(minute <= 59)

        return

    def validate_second(self, second):
        assert(0 <= second)
        assert(second <= 60)

        return


    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        for key in self.data.keys():
            print(f'{key} = {self.data[key]}')

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return
