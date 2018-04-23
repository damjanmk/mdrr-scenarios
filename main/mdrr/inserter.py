'''
Created on Feb 11, 2017

@author: damjan
'''
# to communicate with MongoDB
import pymongo                                                                
from datetime import datetime                                                 
import json                                                                   
# to do md5 hashing of receptor structure
import hashlib                                                                
# to get file name from path
import ntpath                                                                 
import os

import receptor_parser
import ligand_parser
import result_parser
import config_parser
# openbabel API to calculate molecule properties
import pybel                                                                  

class Inserter():
    '''
    classdocs
    '''
    def __init__(self, database):
        '''
        Constructor 
        Parameters: 
        database - the MongoDB database (it may, but doesn't have to have collections called: 'results', 'receptors', 'ligands'; if it doesn't they will be created)
        '''
        self.db = database

    # insert into analysis type = inserting_results, inserted_results    
    def insert_analysis_inserting(self, group_id="", inserted_results = []):
        analysis_dict = {}
        analysis_dict["group_id"] = group_id
        analysis_dict["type"] = "Inserting Results"
        analysis_dict["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S%Z")
        analysis_dict["inserted_results"] = inserted_results
        return self.db.analysis.insert_one(analysis_dict).inserted_id
    
    
    def insert_analysis_at(self, group_id="", at_type="Ligand Similarity (Structural Alignment)", tool="Ligsift", config="", target="", results_list=[]):
        inserted_id_list = []
        for result in results_list:
            analysis_dict = {}
            analysis_dict["group_id"] = group_id
            analysis_dict["type"] = at_type
            analysis_dict["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S%Z")
            analysis_dict["tool"] = tool
            analysis_dict["config"] = config
            analysis_dict["target"] = target
            analysis_dict["similar"] = result
            inserted_id_list.append( self.db.analysis.insert_one(analysis_dict).inserted_id )
        return inserted_id_list
    
    def insert_analysis_at_assessment(self, group_id="", at_type="Receptor Structural Alignment Assessment", assessment_type="User Input Threshold", threshold="", assessed=[]):
        analysis_dict = {}
        analysis_dict["group_id"] = group_id
        analysis_dict["type"] = at_type
        analysis_dict["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S%Z")
        analysis_dict["assessment_type"] = assessment_type
        analysis_dict["assessed"] = assessed
        return self.db.analysis.insert_one(analysis_dict).inserted_id
       
#     def insert_analysis_structural_alignment(self, group_id="", tool="DeepAlign", config="", target_receptor="", similar_list=[]):
#         inserted_id_list = []
#         for similar in similar_list:
#             analysis_dict = {}
#             analysis_dict["group_id"] = group_id
#             analysis_dict["type"] = "Structural Alignment"
#             analysis_dict["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S%Z")
#             analysis_dict["tool"] = tool
#             analysis_dict["config"] = config
#             analysis_dict["target_receptor"] = target_receptor
#             analysis_dict["similar"] = similar
#             inserted_id_list.append( self.db.analysis.insert_one(analysis_dict).inserted_id )
#         return inserted_id_list
#     
#     def insert_analysis_structural_alignment_assessment(self, group_id="", assessment_type="User Input Threshold", threshold="", assessed_as_similar=[]):
#         analysis_dict = {}
#         analysis_dict["group_id"] = group_id
#         analysis_dict["type"] = "Structural Alignment Assessment"
#         analysis_dict["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S%Z")
#         analysis_dict["assessment_type"] = assessment_type
#         analysis_dict["assessed_as_similar"] = assessed_as_similar
#         return self.db.analysis.insert_one(analysis_dict).inserted_id
        
    def insert_analysis_docking_assessment(self, group_id="", assessment_type="User Input Threshold", threshold="", good_dockings=[]):
        analysis_dict = {}
        analysis_dict["group_id"] = group_id
        analysis_dict["type"] = "Docking Assessment"
        analysis_dict["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S%Z")
        analysis_dict["assessment_type"] = assessment_type
        analysis_dict["assessed_as_good"] = good_dockings
        return self.db.analysis.insert_one(analysis_dict).inserted_id    
        
    def insert_analysis_decision(self, group_id="", decision_type="Sorted by DeepScore then by Vina Affinity", decision=[]):
        analysis_dict = {}
        analysis_dict["group_id"] = group_id
        analysis_dict["type"] = "Decision"
        analysis_dict["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S%Z")
        analysis_dict["decision_type"] = decision_type
        analysis_dict["decision"] = decision
        return self.db.analysis.insert_one(analysis_dict).inserted_id
        
    def insert_result(self, 
                      receptor="unknown", receptor_path_or_content="path", receptor_name="unknown", receptor_species="unknown", 
                      ligand="unknown", ligand_path_or_content="path", 
                      result_path="unknown", 
                      config="unknown", config_path_or_content="path"):
        '''
        Inserts a result into the collection 'results'.
        Parameters:
        receptor - the path to the receptor or the content of the file describing the receptor structure 
        receptor_path_or_content - 'path' if the receptor's path is given in 'receptor', and 'content' if it's the content of the structure
        receptor_name - the human readable name of the receptor
        receptor_species - the species of this receptor (if known)
        ligand - the path to the ligand or the content of the file describing the ligand structure
        ligand_path_or_content - 'path' if the ligand's path is given in 'ligand', and 'content' if it's the content of the structure
        result_path - the path the the result file (.pdbqt for vina, assuming that there is a .pdbqt_log.txt file in the same directory)
        config - the path to the config or the content of the file describing the config
        config_path_or_content - 'path' if the config's path is given in 'config', and 'content' if it's the content of the config
        *** make a function that will analyse a string and decide if it is a path to file or not ***
        '''
        # make an instance of a result_parser, e.g. Plain, JsonStructure, ...
        parser = result_parser.Plain()
        # the parsed values of the resulting models are stored in the dict 'result_dict'
        result_dict = parser.parse(result_path)                                                         

        # get the name of the file only
        filename = ntpath.basename(result_path)
        # add today's date, the name of the docking tool, hard-coded, version of tool will be needed ***
        result_dict["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S%Z")                                       
        result_dict["docking_tool"] = "AutoDock Vina"                                                    
        # get the receptor ObjectId from 'insert_receptor' and 'insert_ligand'
        result_dict["receptor"] = self.insert_receptor(receptor, receptor_path_or_content, receptor_name, receptor_species)  
        result_dict["ligand"] = self.insert_ligand(ligand, ligand_path_or_content)
        result_dict["filename"] = filename
        
        #run 'insert_config' and store the resulting dictionary
        result_dict["config"] = self.insert_config(config, config_path_or_content)

        # insert 'result_dict' in MongoDB using the PyMongo 'insert_one' method
        result = self.db.results.insert_one(result_dict).inserted_id                                
        return result
    
    def fake_insert_results_grouped_format(self, list_of_path_to_results, list_of_path_to_ligands):
        '''
        Return a list of results in the 'grouped' format, as they would be returned by selector.select_results_grouped_format()
        This method is in the Inserter because it uses the result_parser, as it receives the path to results. The content of files
        at this path firstly need to be parsed to the format used by the database (converted to a python dictionary). Then, this 
        needs to be formatted in the 'grouped' format, ready for AssessDockingResults
        '''
        
        list_of_result_dicts = []
        parser = result_parser.Plain()
        for result_path in list_of_path_to_results:
            result_filename = ntpath.basename(result_path)
            ligand_of_result = result_filename.split("_")[1]
            ligand_path = [lig_path for lig_path in list_of_path_to_ligands if ligand_of_result in ntpath.basename(lig_path)] [0]
            
            result_dict = parser.parse( result_path )
            result_grouped_format = {}
            result_grouped_format["_id"] = {}
            result_grouped_format["_id"]["ligand"] = ligand_path            
            result_grouped_format["_id"]["receptor"] = "<receptor>"
            result_grouped_format["_id"]["config"] = "<config>"
            result_grouped_format["_id"]["receptor"] = result_dict["random_seed"]
            result_grouped_format["models"] = result_dict["models"]
            result_grouped_format["result_id"] = "<result_id>"
            list_of_result_dicts.append( result_grouped_format )
        
        return list_of_result_dicts
    
    
    def insert_config(self, config, config_path_or_content):
        '''
        Read the config file line by line, or read it straight as a content string. 
        This will work at least for AutoDock VIna where the config file is a text file with properties specified in each new line.
        '''
        ConfigParser = config_parser.Vina()
        config_dict = {}
        if config_path_or_content == "path":
            # open the file and parse it line by line
            with open(config) as config_file:
                config_dict = ConfigParser.lines2dictionary(config_file)
                    
        elif config_path_or_content == "content":
            # parse the content line by line
            config_dict = ConfigParser.lines2dictionary(config.getvalue().split(os.linesep))                    
        
        return config_dict
    
      
    
    def insert_receptor(self, receptor, receptor_path_or_content, receptor_name, receptor_species):
        '''
        Inserts into the collection 'receptors'. 
        '''
        # the dictionary which will be inserted into MongoDB
        receptor_dict = {}                                                                          
        # make an instance of a receptor_parser, e.g. Plain, JsonStructure, ...
        parser = receptor_parser.Plain()                                                            
        # parser = receptor_parser.JsonStructure()
        if receptor_path_or_content == "path":
            # the parsed structure is stored in the dict 'struct'
            struct = parser.parse(receptor)                                                        
            # get the name of the file only
            filename = ntpath.basename(receptor)                                                   
            receptor_dict["filename"] = filename                                                        
        elif receptor_path_or_content == "content":
            struct = parser.parse_content(receptor)
        
        # MongoDB has an 'index key limit' of 1024B, so the entire structure of a receptor
        # cannot be a unique index - I use another unique value - an md5 hash of the entire structure.
        # hash the structure with md5. Before that, use json.dumps() to convert from dict to json
        hashed_structure = hashlib.md5(json.dumps(struct))                                          

        receptor_dict["name"] = receptor_name                                                       
        receptor_dict["species"] = receptor_species                                                 
        # receptor structure, this is the entire 'struct' Python dictionary
        receptor_dict["structure"] = struct                                                         
        # receptor structure_id, this is the md5 hashed value of the 'struct' dictionary
        structure_id = hashed_structure.hexdigest()
        receptor_dict["structure_id"] = structure_id                     

        try:
            # insert 'receptor_dict' in MongoDB using the PyMongo 'insert_one' method
            self.db.receptors.insert_one(receptor_dict)
            # return the  'structure_id' not the _id
            result = structure_id
        except pymongo.errors.DuplicateKeyError, e:
            # the error message is located in a field called 'errmsg' inside the dict 'details'
            errmsg = e.details["errmsg"]                                                            
            print "A receptor with that structure already exists in the database."
            print "Error message: " + errmsg                                                        
            result = structure_id
            
            
#         # even if there is a duplicate receptor, this method needs to return the id of the existing document
#         except pymongo.errors.DuplicateKeyError, e:
#             # the error message is located in a field called 'errmsg' inside the dict 'details'
#             errmsg = e.details["errmsg"]                                                            
#             print "A receptor with that structure already exists in the database."
#             print "Error message: " + errmsg                                                        
#             # obtain the the 'structure_id', contained in the error message
#             existing_structure_id = errmsg[errmsg.index("{ : \"") + 5 : len(errmsg) - 3]            
#             # run a query to find the receptor with that structure_id
#             existing_receptor = self.db.receptors.find_one({"structure_id": existing_structure_id}) 
#             result = existing_receptor["_id"]
                                                                  
        return result                                                                               

    def insert_ligand(self, ligand, ligand_path_or_content):
        '''
        Inserts into the collection 'ligands'. 
        '''
        # the dictionary which will be inserted into MongoDB
        ligand_dict = {}                                                                            
        # make an instance of a receptor_parser, e.g. Plain, JsonStructure, ...
        parser = ligand_parser.Plain()                                                              
        if ligand_path_or_content == "path":            
            # get the name of the file only
            filename = ntpath.basename(ligand)                                                     
            ligand_dict["filename"] = filename                                                     
            # the parsed structure is stored in the dict 'struct'
            struct = parser.parse(ligand)       
        elif ligand_path_or_content == "content":
            struct = parser.parse_content(ligand)                                                  
        
        # MongoDB has an 'index key limit' of 1024B, so the entire structure of a ligand
        # cannot be a unique index - I use another unique value - an md5 hash of the entire structure.
        # hash the structure with md5. Before that, use json.dumps() to convert from dict to json
        hashed_structure = hashlib.md5(json.dumps(struct))                                          
                                                          
        print "in insert_ligand, ligand: " + ligand
        # read the file in PyBel, this returns a parsed object 'mol'
        mol = pybel.readfile("pdbqt", ligand).next()               
        # process this mol object with the self.obprop() method to read particular properties of the ligand
        obprop_properties = self.obprop(mol)
        # store the properties in ligand_dict and include the fingerprint of the ligand calculated with self.ob2fps()
        for mol_property in obprop_properties.keys():
            ligand_dict[mol_property] = obprop_properties[mol_property] 
        ligand_dict["fingerprint_fps"] = self.ob2fps(mol)
        # ligand structure, this is the entire 'struct' Python dictionary
        ligand_dict["structure"] = struct                                                           
        # ligand structure_id, this is the md5 hashed value of the 'struct' dictionary
        structure_id = hashed_structure.hexdigest()
        # return the  'structure_id' not the _id
        ligand_dict["structure_id"] = structure_id                                  

        try:
            # insert 'ligand_dict' in MongoDB using the PyMongo 'insert_one' method
            self.db.ligands.insert_one(ligand_dict).inserted_id
            result = structure_id                            
        except pymongo.errors.DuplicateKeyError, e:
            # the error message is located in a field called 'errmsg' inside the dict 'details'
            errmsg = e.details["errmsg"]                                                            
            print "A ligand with that structure already exists in the database."
            print "Error message: " + errmsg                                                        
            result = structure_id
        
#         # even if there is a duplicate receptor, this method needs to return the id of the existing documents
#         except pymongo.errors.DuplicateKeyError, e:
#             # the error message is located in a field called 'errmsg' inside the dict 'details'
#             errmsg = e.details["errmsg"]                                                            
#             print "A ligand with that structure already exists in the database."
#             print "Error message: " + errmsg                                                        
#             # obtain the the 'structure_id', contained in the error message
#             existing_structure_id = errmsg[errmsg.index("{ : \"") + 5 : len(errmsg) - 3]            
#             # run a query to find the receptor with that structure_id
#             existing_ligand = self.db.ligands.find_one({"structure_id": existing_structure_id})     
#             result = existing_ligand["_id"]
                                                           
        return result                                                                               

    def canonical_SMILES_from_pdbqt(self, path_to_ligand):
        # read the file in PyBel, this returns a parsed object 'mol'
        mol = pybel.readfile("pdbqt", path_to_ligand).next()
        return mol.write("can").split()[0]

    def obprop(self, mol):
        '''
        Call the various PyBel and OpenBabel (the python module) functions to get the additional molecular properties.
        Parameters:
        mol - the obprop read molecule (e.g. first read from a file) 
        This is an example of what the openbabel command obprop returns:
        name             ZINC00000725
        formula          C9H11NO3
        mol_weight       181.189
        exact_mass       181.074
        canonical_SMILES O[C@@H](c1ccccc1)COC(=O)N    ZINC00000725
        
        InChI            InChI=1S/C9H11NO3/c10-9(12)13-6-8(11)7-4-2-1-3-5-7/h1-5,8,11H,6H2,(H2,10,12)/t8-/m1/s1
        
        num_atoms        24
        num_bonds        24
        num_residues     1
        num_rotors       4
        sequence         LIG
        num_rings        1
        logP             1.5156
        PSA              72.55
        MR               46.5652
        '''        
        obprop_dict = {}        
        # this is needed: add hydrogens to fill out implicit valence spots
        mol.OBMol.AddHydrogens()                                                                    
           
        # calculate descriptiors (the molecular additional properties)
        descvalues = mol.calcdesc()                                                                 
        # combine this dict descvalues with the existing mol.data
        mol.data.update(descvalues)   
        title = mol.title
        # this is to avoid path as a title which is then used in scenario4. If there's a need for '/' in the name, this should be changed
        if "/" in title:
            title_elements = title.split("/")
            title = title_elements[ len(title_elements) - 1 ]                           
        obprop_dict["name"] = title
        obprop_dict["formula"] = mol.formula
        obprop_dict["mol_weight"] = str(mol.molwt)
        obprop_dict["exact_mass"] = str(mol.exactmass)
        obprop_dict["canonical_SMILES"] = mol.write("can").split()[0].strip() # needed to get only the can_smiles, not the name of the molecule that follows
        obprop_dict["InChI"] = mol.write("inchi")
        obprop_dict["num_atoms"] = str(len(mol.atoms))
        obprop_dict["num_bonds"] = str(mol.OBMol.NumBonds())
        num_residues = mol.OBMol.NumResidues()
        obprop_dict["num_residues"] = str(num_residues)
        obprop_dict["num_rotors"] = str(mol.OBMol.NumRotors())
        # the sequence is stored as an array, convert it into ABC-DEF-GHI (for a ligand it would be just LIG)
        seq = ""
        for i in range(num_residues):
            seq += mol.OBMol.GetResidue(i).GetName() + '-'
        seq = seq.strip('-')    
        obprop_dict["sequence"] = seq
        obprop_dict["num_rings"] = str(len(mol.sssr))
        obprop_dict["logP"] = str(mol.data['logP'])
        obprop_dict["PSA"] = str(mol.data['TPSA'])
        obprop_dict["MR"] = str(mol.data['MR'])
        
        return obprop_dict

    def ob2fps(self, mol):
        '''
        Call the PyBel function to get the fingerprints
        Parameters:
        mol - the obprop read molecule (e.g. first read from a file) 
        This is an example of what the openbabel command obprop returns:
        
        FPS1
        num_bits=1021
        type=OpenBabel-FP2/1
        software=OpenBabel/2.3.2
        source=cp_prep_zinc_25763228.pdbqt
        date=2017-03-17T23:58:35
        801606c000f0040402004e0010804000808005400020601c80050192082000011001610040c91063008b804c011510410100a0000400000c00010822000404244c00080046200020a00201800488048208b800600c0630084a0958004049000002940018e1208080000004008001000000060100003b00000080000806c24000    cp_prep_zinc_25763228.pdbqt
        '''
        return str(mol.calcfp())