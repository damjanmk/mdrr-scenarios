'''
Created on Nov 9, 2017

@author: damjan
'''
import threading
from math import sqrt
import os

class Assess(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, queue, target_config, config, threshold):
        '''
        Constructor
        '''
        self.queue = queue
        self.target_config = target_config
        self.config = config
        self.threshold = threshold
        threading.Thread.__init__(self)
        
    def run(self):
        """ Starts the new thread that runs CompareConfig
        
        
        center_x = 0.0
        center_y = 0.0
        center_z = 0.0
        size_x = 36.6112111111
        size_y = 32.5278777778
        size_z = 34.3195444444
        exhaustiveness = 8        
        """
        try:
            
            similar_config = ""
            # open config
            with open(self.config, "r") as vina_config:
                for line in vina_config.readlines():
                    similar_config += line
                    split_line = line.split("=")
                    # get centre point
                    if split_line[0].startswith("center_x"):
                        center_x = float( split_line[1].strip() )
                        continue
                    elif split_line[0].startswith("center_y"):
                        center_y = float( split_line[1].strip() )
                        continue
                    elif split_line[0].startswith("center_z"):
                        center_z = float( split_line[1].strip() )
                        continue
                    # get size point
                    elif split_line[0].startswith("size_x"):
                        size_x = float( split_line[1].strip() )
                        continue
                    elif split_line[0].startswith("size_y"):
                        size_y = float( split_line[1].strip() )
                        continue
                    elif split_line[0].startswith("size_z"):
                        size_z = float( split_line[1].strip() )
                        continue
                    

            
            # open target_config
            with open(self.target_config, "r") as vina_config2:
                for line in vina_config2.readlines():
                    split_line = line.split("=")
                    # get centre point
                    if split_line[0].startswith("center_x"):
                        target_center_x = float( split_line[1].strip() )
                        continue
                    elif split_line[0].startswith("center_y"):
                        target_center_y = float( split_line[1].strip() )
                        continue
                    elif split_line[0].startswith("center_z"):
                        target_center_z = float( split_line[1].strip() )
                        continue
                    # get size point
                    elif split_line[0].startswith("size_x"):
                        target_size_x = float( split_line[1].strip() )
                        continue
                    elif split_line[0].startswith("size_y"):
                        target_size_y = float( split_line[1].strip() )
                        continue
                    elif split_line[0].startswith("size_z"):
                        target_size_z = float( split_line[1].strip() )
                        continue

            # distance between two centres
            center_distance = sqrt( (center_x - target_center_x)**2 + (center_y - target_center_y)**2 + (center_z - target_center_z)**2 )
            
            # distance between two size points
            size_distance = sqrt( (size_x - target_size_x)**2 + (size_y - target_size_y)**2 + (size_z - target_size_z)**2 )

            # average of distances
            comparison_value = (center_distance + size_distance) / 2
            print str(comparison_value) + "___" + str(self.threshold)
            if comparison_value < self.threshold:
                to_return = {}
                # add the CompareConfig result
                to_return["similar_config_content"] = similar_config
                to_return["result_id"] = os.path.basename( self.config ).split("_")[0]
                to_return["CompareConfig_result"] = comparison_value
                self.queue.put( to_return )
        
        except Exception, e:
            print e