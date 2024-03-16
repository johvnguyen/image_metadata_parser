class HuffmanTable:
    def __init__(self):
        self.root = []
        self.elements = []
        
        self.count = 0
        
    def DecodeHuffmanBits(self,  lengths, elements):
        '''
        DecodeHuffmanBits - This function builds the nested list data structure which maps Huffman encodings to the corresponding element by list index. Effectively, makes self.root become a Huffman tree.
            lengths:    lengths of the bitstrings of te corresponding elements
            elements:   values which the bitstrings map to (are actually delta encoding values)
        '''
        # It doesn't seem like self.elements is referenced anywhere else... this variable seems unecessary
        self.elements = elements
        elem_iter = 0
        
        # iterate over each length value, equivalently, iterates over each element value as these lists should be the same length
        # IDEA: Add an assert statement to verify this is true
        for i in range(len(lengths)):
            # Iterate over each element of this specific length value
            for j in range(lengths[i]):
                # Put this element into the huffman tree
                self.BitsFromLengths(self.root, elements[elem_iter], i)
                # Iterate the element in the array
                elem_iter += 1
                
        return
    
    def BitsFromLengths(self, root, element, pos):
        # Consider the inputs as:
        # root: The current sub-list we are traversing. The index to get to this sub-list is the prefix for the bitstring encoding we are considering
        # element: The value we are trying to place in our Huffman Tree
        # pos: The length of the remaining suffix of the encoded value (that we are trying to determine)
        # if root input is not a list (i.e. a list value) then return False
        if isinstance(root,list):
            # if pos == 0, then we are trying to place the element in this list
            if pos==0:
                # if there is room, append the element to the list
                if len(root)<2:
                    root.append(element)
                    return True
                # If there is no room in (i.e. all encodings at this length with this prefix has been assigned), then return False
                return False
            # this for-loop executes as the recursive step
            for i in [0,1]:
                # if the root is empty or already has 1 element (and we are still trying to place another element), add a new list to represent considering a new bit
                # NOTE: If there is no room in any previous sublist and all lengths available in self.root has already been assigned, this case will always make room for a new element by creating a new sub-list
                if len(root) == i:
                    root.append([])
                # Recursive call to try to place an element in this new sublist. If this fails, return False
                if self.BitsFromLengths(root[i], element, pos-1) == True:
                    return True
        return False
    


    def Find(self,st):
        r = self.root
        while isinstance(r, list):
            #print(self.count)
            #self.count += 1
            #print(type(r))
            #print(len(r))
            r=r[st.GetBit()]
        return  r 

    def GetCode(self, st):
        while(True):
            res = self.Find(st)
            if res == 0:
                return 0
            elif ( res != -1):
                return res
