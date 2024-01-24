from JPGParser.SegmentParser.SegmentParser import SegmentParser
import struct
import logging

class StartOfFrameSegmentParser(SegmentParser):
    def __init__(self, sig, length):
        assert(sig == 0xffc0)
        
        self.seg_name = 'Start of rame'
        self.sig = sig
        self.len = length
        
        self.precision = None
        self.img_height = None
        self.img_width = None
        self.n_components = None
        self.components = {}
        
    def parse(self, image_fp):
        self.parse_precision(image_fp)
        self.parse_img_dim(image_fp)
        self.parse_n_components(image_fp)
        
        self.parse_components(image_fp)
        
        return
    
    def parse_precision(self, image_fp):
        precision_fmt_str = '>B'
        precision_size = struct.calcsize(precision_fmt_str)
        precision_bytes = image_fp.read(precision_size)
        precision = struct.unpack(precision_fmt_str, precision_bytes)[0]
        
        self.precision = precision
        
        return
    
    def parse_img_dim(self, image_fp):
        dim_fmt_str = '>HH'
        dim_size = struct.calcsize(dim_fmt_str)
        dim_bytes = image_fp.read(dim_size)
        
        (height, width) = struct.unpack(dim_fmt_str, dim_bytes)
        
        self.img_height = height
        self.img_width = width

        return
    
    def parse_n_components(self, image_fp):
        # Parsing the number of components
        noc_fmt_str = '>B'
        noc_size = struct.calcsize(noc_fmt_str)
        noc_bytes = image_fp.read(noc_size)
        number_of_components = struct.unpack(noc_fmt_str, noc_bytes)[0]
        
        self.n_components = number_of_components

        return
    
    def parse_components(self, image_fp):
        for i in range(self.n_components):
            self.parse_component(image_fp)
            
        return
    
    def parse_component(self, image_fp):
        component_fmt_str = '>BBB'
        component_size = struct.calcsize(component_fmt_str)
        component_bytes = image_fp.read(component_size)
        component_data = struct.unpack(component_fmt_str, component_bytes)
        
        self.extract_component(component_data)
        
        return
        
    def extract_component(self, component_data):
        component_id = component_data[0]
        component_sampling_factors = component_data[1]
        component_qtn = component_data[2]
        
        assert(component_id not in self.components.keys())
        
        component_map = {}
        component_map['Sampling Factors'] = component_sampling_factors
        component_map['QT Mapping'] = component_qtn

        self.components[component_id] = component_map
        
        return

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Segment Name: {self.seg_name}')
        print(f'Segment Signature: {self.sig}')
        print(f'Precision: {self.precision}')
        print(f'Image Height: {self.img_height}')
        print(f'Image Width: {self.img_width}')
        print(f'Number of components: {self.n_components}')
        
        self.print_components()
        
        print(f'----------------------------------------\n\n')
        return
        
    def print_components(self):
        print(f'Component Data: ')
        for component_id in self.components.keys():
            print(f'\tComponent Id: {component_id}')\
            
            self.print_sampling_factors(self.components[component_id]['Sampling Factors'])
            
            print(f'\tQuantization Table Mapping: {self.components[component_id]["QT Mapping"]}')
            
        return
    
    def print_sampling_factors(self, sampling_factor):
        [v_sampling_factor, h_sampling_factor] = self.decode_sampling_factor(sampling_factor)
        
        print(f'\tSampling Factor - Vertical: {v_sampling_factor}')
        print(f'\tSampling Factor - Horizontal: {h_sampling_factor}')
        
        return
    
    def decode_sampling_factor(self, sampling_factor):
       v_sampling_factor = sampling_factor & 0b11110000
       h_sampling_factor = sampling_factor & 0b00001111
       
       return [v_sampling_factor, h_sampling_factor]