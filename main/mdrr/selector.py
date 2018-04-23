import pprint
import receptor_parser
import config_parser
import bson

'''
Created on Feb 16, 2017

@author: damjan
'''

class Selector():
    ''' Interface to show / view the data in the MDRR
    '''

    def __init__(self, db):
        '''
        Constructor
        Parameters: db - the MongoDB database to connect to
        '''
        self.db = db
    
    def select_ligand_confs_where_result_has_receptor(self, structure_id):
        '''
        Build a dictionary from the results collection. It contains ligands and configs of all results
        that contain the receptor with structure_id 'structure_id'. For each ligand structure_id, the 
        dictionary stores the 'structure' and an array of all the configs.
        
        {
            "123_ligand_structure_id_123": {
                                            "structure": "lorem ipsum, text explaining the structure",
                                            "configs": [
                                                        "lorem ipsum dolor, text explaining config1",
                                                        "lorem ipsum dolor, text explaining config2",
                                                        "lorem ipsum dolor, text explaining config3"
                                                        ]
                                            }
        }
        {
            "123_ligand_structure_id_123": {
                                            "structure": "lorem ipsum, text explaining the structure",
                                            "result_id_configs": {
                                                        "result_id1": "lorem ipsum dolor, text explaining config1",
                                                        "result_id2": "lorem ipsum dolor, text explaining config2",
                                                        "result_id3": "lorem ipsum dolor, text explaining config3"
                                                        }
                                            }
        }
        
        '''
#         ligand_confs = {}
#         results = self.select_results_where_receptor_structure_id( structure_id )
#         ConfigParser = config_parser.Vina()
#         for result in results:
#             ligand_structure_id = result["ligand"]
#             if not ligand_structure_id in ligand_confs:
#                 ligand_structure_name = self.select_ligand_structure_name( ligand_structure_id )
#                 ligand_confs[ ligand_structure_id ] = {}
#                 ligand_confs[ ligand_structure_id ]["name"] = ligand_structure_name["name"]
#                 ligand_confs[ ligand_structure_id ]["structure"] = ligand_structure_name["structure"]
#                 ligand_confs[ ligand_structure_id ]["configs"] = set()
#             config_string = ConfigParser.dictionary2string( result["config"] )
#             if config_string:
#                 ligand_confs[ ligand_structure_id ]["configs"].add( config_string )
#                  
#         return ligand_confs
        ligand_confs = {}
        results = self.select_results_where_receptor_structure_id( structure_id )
        ConfigParser = config_parser.Vina()
        for result in results:
            ligand_structure_id = result["ligand"]
            if not ligand_structure_id in ligand_confs:
                ligand_structure_name = self.select_ligand_structure_name( ligand_structure_id )
                ligand_confs[ ligand_structure_id ] = {}
                ligand_confs[ ligand_structure_id ]["name"] = ligand_structure_name["name"]
                ligand_confs[ ligand_structure_id ]["structure"] = ligand_structure_name["structure"]
                ligand_confs[ ligand_structure_id ]["result_id_configs"] = {}
            config_string = ConfigParser.dictionary2string( result["config"] )
            if config_string:
                ligand_confs[ ligand_structure_id ]["result_id_configs"][result["_id"]] = config_string
                  
        return ligand_confs
    
    def select_ligands_where_result_has_receptor(self, structure_id):
        ''' return ligand structures that have been docked with a receptor described by 'structure_id'
        '''
        ligands = []
        results = self.select_results_where_receptor_structure_id(structure_id)
        for result in results:
            ligands.append( self.select_ligand_structure(result["ligand"]) )
        return ligands
    
    def select_ligand_structure_name(self, structure_id):
        ''' return the structure and name of the ligand with that structure_id
        '''
        return self.db.ligands.find_one({"structure_id": structure_id}, {"structure": True, "name": True})
    
    def select_ligand_structure(self, structure_id):
        ''' return the structure of the ligand with that structure_id
        '''
        return self.db.ligands.find_one({"structure_id": structure_id}, {"structure": True})
    
    def select_ligand(self, structure_id):
        ''' return the ligand with that structure_id
        '''
        return self.db.ligands.find_one({"structure_id": structure_id})
    
    def select_ligand_by_id(self, ligand_id):
        ''' return a ligand with that _id 
        '''
        print ligand_id
        return self.db.ligands.find_one({"_id": bson.ObjectId( ligand_id )})
    
    def select_ligands_canonical_SMILES(self, structure_ids):
        ''' Return canonical_SMILES of ligands '''
        return self.db.ligands.find({"structure_id": {"$in": structure_ids}}, {"canonical_SMILES": True})
#         return self.db.ligands.find({"structure_id": {"$in": structure_ids}}, {"canonical_SMILES": True, "_id": False})
    
    def select_all_results(self):
        ''' return everything in the results collection 
        '''
        return self.db.results.find()        
    
    def select_result_by_id(self, result_id):
        ''' return a result with that _id 
        '''
        return self.db.results.find_one({"_id": bson.ObjectId( result_id )})
        
    def select_all_results_receptors_ligands(self):
        ''' Return a list of objects that contain all information about a receptor-ligand-result
        '''
        # get all the results
        cursor = self.db.results.find()
        rec_lig_res_list = []
        
        for document in cursor:
            # get the receptor
            receptor = self.db.receptors.find_one({"_id": document["receptor"]})
            # get the ligand
            ligand = self.db.ligands.find_one({"_id": document["ligand"]})
            # put a new receptor-ligand-result object in the list to be returned
            rec_lig_res_list.append(Rec_Lig_Res(receptor, ligand, document))
            
        return rec_lig_res_list[0]
        
    def select_results_where_receptor_file(self, path):
        ''' return results where the 'receptor' is the same as the one described in 'path'
        '''
        # this is relative to the location of either selector or receptor_parser, so the path can remain the same
        parser = receptor_parser.Plain()
        structure_id = parser.path_to_structure_id(path)
        
        # get all results that have that structure_id as receptor
        return self.select_results_where_receptor_structure_id(structure_id)    
        
    def select_results_where_receptor_structure_id(self, structure_id):
        ''' Return results that have the receptor with 'structure_id' as a receptor
        '''
        return self.db.results.find({"receptor": structure_id})
    
    def select_results_where_receptor_structure_ids(self, structure_ids):
        ''' Return results that have the receptor with receptor_structure_id as a receptor
        Parameters:
        structure_ids - an array! of with many structure_id elements, e.g. [12321312123,343534534534,12312323454]
        
        db.getCollection('results').aggregate(
        [
            {"$match": {"receptor": {$in: ["1f64a6e0a4f0a8588f40ad3dab7eafde", "d47bcfc8f7c1b91e4f6d451cc11dce07"]} } },
            {"$group": 
                {"_id": { "random_seed": "$random_seed", "ligand": "$ligand", "receptor": "$receptor", "config": "$config"}, "models": {"$first": "$models"}}
            }
        ]
        )
        
        '''
        return self.db.results.aggregate([
            {"$match": {"receptor": {"$in": structure_ids} } },
            {"$group": 
                {"_id": { 
                    "random_seed": "$random_seed", 
                    "ligand": "$ligand", 
                    "receptor": "$receptor", 
                    "config": "$config"
                        }, 
                 "result_id": {"$first": "$_id" }, 
                 "models": {"$first": "$models"}}
            }
        ], allowDiskUse=True)
    
    def select_results_grouped_format(self, result_ids):
        ''' 
        Selects results in 'grouped' format, the same format used by 'select_results_where_receptor_structure_ids'.
        This 'grouped' format selects results, grouping them by 'random_seed', 'ligand', 'receoptor', 'config'. Because of the randomness of 'random_seed'
        this is practically going to be one result per group. 
        Before the grouping it filters (matches) only results that are in the list of result_ids. In effect there will always be only one result per one result_id 
        This format can be directly used by AssessDockingResults, therefore it is a better way to select results by _id if you're using AssessDockingResults.
        
        Parameters:
        result_ids - an array of ObjectId, the _id of the results
        
        db.getCollection('results').aggregate(
        [
            {"$match": {"_id": {$in: [ObjectId("599adbadc831de424ee97830"), ObjectId("599adbadc831de424ee9782d")]} } },
            {"$group": 
                {"_id": { "random_seed": "$random_seed", "ligand": "$ligand", "receptor": "$receptor", "config": "$config"}, 
                "models": {"$first": "$models"},
                "result_id": {"$first": "$_id"}}
            }
        ]
        )
        '''
        result_object_ids = [bson.ObjectId(res_id) for res_id in result_ids]
        return self.db.results.aggregate([
            {"$match": {"_id": {"$in": result_object_ids} } },
            {"$group": 
                {"_id": { 
                    "random_seed": "$random_seed", 
                    "ligand": "$ligand", 
                    "receptor": "$receptor", 
                    "config": "$config"
                        }, 
                 "result_id": {"$first": "$_id" }, 
                 "models": {"$first": "$models"}}
            }
        ], allowDiskUse=True)
        
    def select_all_receptors(self):
        ''' return everything in the receptors collection
        '''
        return self.db.receptors.find()

    def select_receptor(self, structure_id):
        ''' return a receptor with that structure_id
        '''
        return self.db.receptors.find_one({"structure_id": structure_id})
    
    def select_receptor_by_id(self, receptor_id):
        ''' return a receptor with that _id
        '''
        return self.db.receptors.find_one({"_id": bson.ObjectId( receptor_id )})
            
    def print_all_results(self):
        ''' print everything in the results collection to terminal
        '''
        cursor = self.db.results.find()        
        for document in cursor:
            print(document)    
    
    def print_all_results_with_receptors_ligands(self):
        ''' print every receptor-ligand-result pair on terminal
        '''
        cursor = self.db.results.find()        
        rec_lig_res_list = []
        for document in cursor:
            receptor = self.db.receptors.find_one({"_id": document["receptor"]})
            ligand = self.db.ligands.find_one({"_id": document["ligand"]})
            rec_lig_res_list.append(Rec_Lig_Res(receptor, ligand, document))
        rec_lig_res_list[0].print_all()
        
    def print_all_receptors(self):
        ''' print everything in the receptors collection on terminal
        '''
        cursor = self.db.receptors.find()
        for document in cursor:
            print(document)
            
            
class Rec_Lig_Res():
    ''' The class of a receptor-ligand-result object.
    '''
    
    def __init__(self, receptor="", ligand="", result=""):
        self.receptor = receptor
        self.ligand = ligand
        self.result = result
    
    # getters and setters     
    def get_receptor(self):
        return self.receptor    
    def get_ligand(self):
        return self.ligand
    def get_result(self):
        return self.result
    def set_receptor(self, receptor):
        self.receptor = receptor                
    def set_ligand(self, ligand):
        self.ligand = ligand    
    def set_result(self, result):
        self.result = result     
    
    def print_all(self):
        ''' prints the receptor-ligand-result  object using the pprint module
        '''
        
        print "receptor: "
        pprint.pprint(self.receptor)
        print "ligand: "
        pprint.pprint(self.ligand)
        print "result: "
        pprint.pprint(self.result)


