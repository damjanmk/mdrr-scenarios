'''
Created on Feb 15, 2017

@author: damjan
'''
import os                  

class Vina():
    '''
    The simplest parser, it just copies the value of the PDBQT structure as a list
    '''
    def __init__(self):
        '''
        Constructor
        '''
    
    def lines2dictionary(self, config_lines):
        '''
        Parse an iterable into a dictionary, splitting each item and storing item[0] as key, and item[2] as value
        Parameters:
        config_lines - the iterable to be converted into a dictionary
        '''
        config_dict = {}
        for line in config_lines:            
            # split each line
            split_line = line.split()
            # if it is not an empty line, process it, otherwise ignore
            if len(split_line) > 0:
                # e.g. center_x = 30.0 => [0]: "center_x, [1]: "=", [2]: "30.0"
                key = split_line[0]
                value = split_line[2]
                # update the dictionary with values [0] and [2]
                config_dict.update({key: value})
        return config_dict  
    
    def dictionary2string(self, config_dictionary):
        '''
        Parse a dictionary into a string, separating key and value with " = " and key-value pairs with "\n"
        Parameters:
        config_dictionary - the dictionary to be converted into a string
        '''
        string_to_return = ""
        for (key, value) in config_dictionary.iteritems():            
            string_to_return += key + " = " + value + os.linesep
            
        return string_to_return.strip()