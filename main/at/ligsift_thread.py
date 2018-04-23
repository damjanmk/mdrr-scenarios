'''
Created on Nov 7, 2017

@author: damjan
'''

import threading
import subprocess
import at_assess.assess_ligsift

LIGSIFT_PATH = "/home/damjan/Documents/LigandSimilarity/LIGSIFT/LIGSIFT"

class Ligsift(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, queue, target_ligand, ligand, structure_id, ligand_name, config, output_file, threshold):
        '''
        Constructor
        '''
        self.queue = queue
        self.target_ligand = target_ligand
        self.ligand = ligand
        self.structure_id = structure_id
        self.ligand_name = ligand_name
        self.config = config
        self.threshold = threshold        
        self.output_file = output_file
        
        threading.Thread.__init__(self)
        
    def run(self):
        """ Starts the new thread that runs Ligsift        
        """
        try:            
            
#             print LIGSIFT_PATH, "-v", "-q", self.target_ligand, "-db", self.ligand, "-o", self.output_file, self.config
            
            LigsiftResult = subprocess.check_output([LIGSIFT_PATH, "-v", "-q", self.target_ligand, "-db", self.ligand, "-o", self.output_file, self.config], stderr=subprocess.STDOUT) 
            to_return = {}
            
            # add the MongoDB ligand _id and name...
            to_return["similar_ligand_structure_id"] = self.structure_id
            to_return["name"] = self.ligand_name
            # add the Ligsift result
            to_return["Ligsift_result"] = LigsiftResult
            
            # run the AT assess, if it has been deemed similar (True) then add this to the queue, otherwise don't             
            assessed = at_assess.assess_ligsift.Assess().ShapeSim(LigsiftResult, self.threshold)
            
            if (assessed):
                to_return["assessed_value"] = assessed
                self.queue.put( to_return )
                
        except subprocess.CalledProcessError as e:
            # if it is a non-zero result
            print("Ligsift stdout output on error:\n" + e.output)
            pass 
         
            