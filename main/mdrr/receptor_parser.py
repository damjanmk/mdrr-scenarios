'''
Created on Feb 15, 2017

@author: damjan
'''

# to use OrderedDict, a dict with keys with order of inserting
import collections  
# to do md5 hashing of receptor structure
import hashlib 
import json                                             


class Plain():
    '''
    The simplest parser, it just copies the value of the PDBQT structure as a list
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def parse(self, path):
        '''
        Parse file at 'path' into a list
        '''
        #i'll store the structure of the receptor in a list
        struct = []                                      
        # open the file and parse it line by line
        with open(path) as f:                                                   
            for line in f:                                                      
                struct.append(line)                                             

        return struct    
    
    def parse_content(self, content):
        '''
        Parse the content string of a receptor into a list
        '''
        struct = []
        for line in content:
            struct.append(line)            
        return struct
    
    def dict_to_string(self, struct):
        ''' Parse a dictionary into a string representation of the receptor
        '''
        pdb_struct = ""        
        for line in struct:
            pdb_struct = pdb_struct + line
        return pdb_struct
    
    def path_to_structure_id(self,path):
        
        # get the structure of the receptor at 'path'                                        
        struct = self.parse(path)
        
        # MongoDB has an 'index key limit' of 1024B, so the entire structure of a receptor
        # cannot be a unique index - I use another unique value - an md5 hash of the entire structure.
        # hash the structure with md5. Before that, use json.dumps() to convert from dict to json
        hashed_structure = hashlib.md5(json.dumps(struct))  
        # receptor structure_id, this is the md5 hashed value of the 'struct' dictionary
        return hashed_structure.hexdigest()
    
        
class JsonStructure():
    '''
    A more complex parser, parsing the content of the PDBQT structure as a JSON object
    '''
    def __init__(self):
        '''
        Constructor. ***Needs testing and more work***
        '''
    
    def parse(self, path):          
        # i'll store the structure of the receptor in an ordered dictionary
        # (OrderedDict) which remembers the order in which keys have been added.
        # this will result in a dictionary containing
        # "REMARK" : ["...", "..."]
        # "ATOM" : ["...", "..."] ...
        struct = collections.OrderedDict()                                      
        # open the file and parse it line by line
        with open(path) as f:                                                   
            for line in f:                                                      
                # split the line into ["first-word", "rest-of-pdb-line"]
                record_type_rest = line.split(' ', 1)                           
                # get the first word which is the 'record name', e.g. ATOM
                record_name = record_type_rest[0]                               
                # get the rest of the line which is e.g. "2532  OXT LEU A 288      -6.440  22.798  -7.914  1.00  0.00    -0.646 OA"
                rest = record_type_rest[1].rstrip('\n').lstrip()                
                 
                # filling in the 'struct' dictionary
                # if the 'record_name' (e.g. ATOM) is already a key in 'struct'
                if record_name in struct:                                       
                    # get the value for that key into the variable 'records_list' the value will be a list - append the 'rest' of the new line to this list
                    records_list = struct[record_name]
                    records_list.append(rest)                                    
                # if the 'record_name' (e.g. ATOM) is not a key in 'struct'
                else:                                                               
                    # store the 'rest' of the new line as a list in the variable 'records_list'
                    records_list = [rest]                                           
                # update the dictionary to include the new line, 'record_name': 'records_list'
                struct.update({record_name: records_list})                      
         
        return struct