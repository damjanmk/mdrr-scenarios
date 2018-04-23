'''
Created on Jun 7, 2017
'decider' usually used for a decisive sports match - but G. W. Bush has used it to mean 'decision maker' so it's legit ;)
@author: damjan
'''

import operator

class Decide():
    '''
    classdocs
    '''

    def __init__(self, assessed_results):
        '''
        Constructor
        assessed_results ={
            "data": {
                "good": 
                    [ 
                    {"result_id": xx, "ligand_id": xx, "receptor_structure_id": xx, "good_models": [ {"model_number": aa, "affinity": aaa}, ... ]}
                    , ... 
                    ]
                }
        }
        '''
        self.assessed_results = assessed_results
        
    def run(self):
        """ run the DM        
        """        
        to_return = {}
        to_return["best_suggestions"] = []
        
        docking_dict = self.assessed_results
        for result in docking_dict["data"]["good"]:
#             ligand_id = result["ligand"]            
            # get number of times this ligand has been suggested before
                            
            
            to_return["best_suggestions"].append( result )
                            
        return to_return

class SimpleDecide():
    '''
    classdocs
    '''

    def __init__(self, assessed_results, assessed_similar_receptors):
        '''
        Constructor
        '''
        self.assessed_results = assessed_results
        self.assessed_similar_receptors = assessed_similar_receptors
        
    def run(self):
        """ run the DM        
        """        
        to_return = []
        # join similar and good on receptor_structure_id
        
        for s in self.assessed_similar_receptors["data"]["similar"]:
            for g in self.assessed_results["data"]["good"]:
                if s["structure_id"] == g["receptor_structure_id"]:
                    g["DeepScore"] = s["DeepScore"]
                    to_return.append( g )
        
        # sort by similar.score
        # then sort by good.good_models.affinity
        to_return.sort(key=operator.itemgetter("good_models"))

        to_return.sort(key=operator.itemgetter('DeepScore'), reverse = True)
          
        return to_return


class SimilarReceptorsLigandsConfigs():
    def __init__(self, assessed_similar_receptors, similar_ligands, similar_configs):
        '''
        Constructor
        '''
        self.assessed_similar_receptors = assessed_similar_receptors
        self.similar_ligands = similar_ligands
        self.similar_configs = similar_configs
        
    def decide(self):
        """ run the DM
        """
        
        to_return = []
        
        # get threshold and at_config from  
        threshold_receptor = self.assessed_similar_receptors["data"]["threshold"]
        receptor_similarity_config = self.assessed_similar_receptors["data"]["at_config"]
        
        for similar_receptor in self.assessed_similar_receptors["data"]["similar"]:
            similar_receptor_id = similar_receptor["structure_id"]
            receptor_similarity_result = similar_receptor["DeepAlign_result"]
            receptor_similarity_value = similar_receptor["DeepScore"]
            if similar_receptor_id in self.similar_ligands:
                threshold_ligand = self.similar_ligands[similar_receptor_id]["data"]["threshold"]
                ligand_similarity_config = self.similar_ligands[similar_receptor_id]["data"]["at_config"]
                
                for similar_ligand_for_that_receptor in self.similar_ligands[similar_receptor_id]["data"]["similar"]:
                    similar_ligand_id = similar_ligand_for_that_receptor["similar_ligand_structure_id"]
                    ligand_similarity_result = similar_ligand_for_that_receptor["Ligsift_result"]
                    ligand_similarity_value = similar_ligand_for_that_receptor["assessed_value"]
                    ligand_name = similar_ligand_for_that_receptor["name"]
                    
                    
                    if similar_receptor_id in self.similar_configs:
                        if similar_ligand_id in self.similar_configs[similar_receptor_id]:
                            threshold_config = self.similar_configs[similar_receptor_id][similar_ligand_id]["data"]["threshold"]
                            for similar_config_for_that_receptor_ligand in self.similar_configs[similar_receptor_id][similar_ligand_id]["data"]["similar"]:
                                config_content = similar_config_for_that_receptor_ligand["similar_config_content"]
                                config_similarity_result = similar_config_for_that_receptor_ligand["CompareConfig_result"]
                                result_id_of_this_config = similar_config_for_that_receptor_ligand["result_id"]
                                # add the information regarding the receptor, ligand, and config to the to_return list
                                to_return.append({ 
                                                "similar_receptor_structure_id": similar_receptor_id,
                                                 "receptor_similarity_result": receptor_similarity_result,
                                                 "receptor_similarity_config": receptor_similarity_config,
                                                 "receptor_similarity_value": receptor_similarity_value,
                                                 "threshold_receptor": threshold_receptor,
                                                 "similar_ligand_structure_id": similar_ligand_id,
                                                 "ligand_name": ligand_name,
                                                 "ligand_similarity_result": ligand_similarity_result,
                                                 "ligand_similarity_config": ligand_similarity_config,
                                                 "threshold_ligand": threshold_ligand,
                                                 "ligand_similarity_value": ligand_similarity_value,
                                                 "config_content": config_content,
                                                 "config_similarity_result": config_similarity_result,
                                                 "threshold_config": threshold_config,
                                                 "result_id": result_id_of_this_config
                                                })
                                    
                                    
        # sort the list, first by receptor_similarity_value, then by ligand_similarity_value
        to_return.sort(key=operator.itemgetter("ligand_similarity_value"), reverse = True)
        to_return.sort(key=operator.itemgetter('receptor_similarity_value'), reverse = True)
        
        return to_return
        

#         
#         to_return = {}
#         to_return["suggestions"] = []
#         
#         docking_dict = json.loads(self.assessed_results)
#         for result in docking_dict["data"]["assessed"]:
#             for model in result["models"]:
#                 if model["assessed"] == "GOOD":
# #                     print "DM: this docking result is good"
#                     for receptor in self.assessed_similar_receptors["data"]["similar"]:
#                         # if receptor has been used for that result (if the receptor is present in this list it has been deemed similar)
#                         if receptor["structure_id"] == result["receptor"]:
# #                             print "DM: AND a similar receptor has been docked before"
#                             
#                             suggestion = {}
#                             suggestion["suggested_ligand_id"] = str(result["ligand"])
# #                             suggestion["rationale"] = "A similar receptor to the one you just used has been found in the repository. There is a record of a ligand that has been docked successfully to this receptor."
#                             suggestion["similar_receptor_structure_id"] = receptor["structure_id"]
#                             suggestion["result_id"] = str(result["_id"]) 
#                             to_return["suggestions"].append( suggestion )
#                             
#         return to_return