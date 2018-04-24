'''
Created on Jun 7, 2017

@author: damjan
'''
import json

class AssessDockingWithThreshold():
    '''
    classdocs
    '''


    def __init__(self, docking_results, threshold):
        '''
        Constructor
        '''
        self.docking_results = docking_results
        self.threshold = threshold
        
    def run(self):
        """ Assesses the docking results, in the current version it just compares it with the threshold.
          
        """        
        to_return = []
        
        with open(self.docking_results) as results_json:
            docking_dict = json.load(results_json)
        
        if not docking_dict == None:     
            for result in docking_dict:
                # for each result create an empty dictionary with values for the ones that have at least one 'good' model
                assessed = {}
                # a flag that is False at start and becomes True when the first 'good' model is found
                at_least_one_good_model = False
                for model in result["models"]:
                    if model["affinity"] < self.threshold:
                        # if this is the first 'good' model, set the values for result_id, ligand, and create the 'good_models' list
                        if not at_least_one_good_model:                        
                            assessed["result_id"] = result["_id"]
                            assessed["ligand_structure_id"] = result["ligand"]
                            assessed["receptor_structure_id"] = result["receptor"]
                            assessed["good_models"] = []
                            # set this flag to True
                            at_least_one_good_model = True
                        
                        # append the model_number and affinity information to the 'good_models' list     
                        assessed["good_models"].append( {"model_number": model["model_number"], "affinity": model["affinity"]} ) 
                
                # check if the assessed dictionary is empty. Empty dictionary in python evaluates to False, non-empty to True
                if assessed:
                    to_return.append( assessed )  
                    
        return to_return
    
    
    def runFile(self):
        """ Assesses the docking results, in the current version it just compares it with the threshold.
          
        """        
        to_return = []
        
        docking_dict = json.load(self.docking_results)
            
        for result in docking_dict:
            # for each result create an empty dictionary with values for the ones that have at least one 'good' model
            assessed = {}
            # a flag that is False at start and becomes True when the first 'good' model is found
            at_least_one_good_model = False
            for model in result["models"]:
                if float(model["affinity"]) < self.threshold:
                    # if this is the first 'good' model, set the values for result_id, ligand, and create the 'good_models' list
                    if not at_least_one_good_model:                        
                        assessed["result_id"] = str(result["_id"])
                        assessed["ligand_structure_id"] = result["ligand"]
                        assessed["receptor_structure_id"] = result["receptor"]
                        assessed["good_models"] = []
                        # set this flag to True
                        at_least_one_good_model = True
                    
                    # append the model_number and affinity information to the 'good_models' list     
                    assessed["good_models"].append( {"model_number": model["model_number"], "affinity": model["affinity"]} ) 
            
            # check if the assessed dictionary is empty. Empty dictionary in python evaluates to False, non-empty to True
            if assessed:
                to_return.append( assessed )  
                    
        return to_return
    