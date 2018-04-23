'''
Created on Jun 7, 2017

@author: damjan
'''

import threading
import subprocess
import at_assess.assess_deep_align

DEEPALIGN_PATH = "/home/damjan/Documents/StructAlign/DeepAlign/DeepAlign"

class DeepAlign(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, queue, target_receptor, receptor, structure_id, config, threshold):
        '''
        Constructor
        '''
        self.queue = queue
        self.target_receptor = target_receptor
        self.receptor = receptor
        self.structure_id = structure_id
        self.config = config
        self.threshold = threshold
        threading.Thread.__init__(self)
        
    def run(self):
        """ Starts the new thread that runs DeepAlign        
        """
        try:
            DeepAlignResult = subprocess.check_output([DEEPALIGN_PATH, self.target_receptor, self.receptor, self.config], stderr=subprocess.STDOUT) #, stdout=redirect_to_file)
            to_return = {}
            # add the target receptor and the potential similar receptor - *** not needed
#             to_return["target_receptor"] = self.target_receptor
#             to_return["receptor"] = self.receptor

            # add the MongoDB receptor _id ...
            to_return["structure_id"] = self.structure_id
            # add the DeepAlign result
            to_return["DeepAlign_result"] = DeepAlignResult
            
            # run the AT assess, if it has been deemed similar (True) then add this to the queue, otherwise don't             
            assessed = at_assess.assess_deep_align.Assess().run(DeepAlignResult, self.threshold)
            
            if (assessed):
                to_return["DeepScore"] = assessed
                self.queue.put( to_return )
                
        except subprocess.CalledProcessError as e:
            # if it is a non-zero result
            print("DeepAlign stdout output on error:\n" + e.output)
            pass 
         
            