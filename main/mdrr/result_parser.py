'''
Created on Feb 15, 2017

@author: damjan
'''
# from datetime import datetime
# # to get file name from path
# import ntpath                                                                 
# import collections   

class Plain():
    '''
    The simplest parser, it:
    * opens the log file, named <path>_log.txt and from there it obtains: 
        ** number of cpus 'cpus' 
        ** the random seed 'random_seed' used
    * opens <path> and from there it obtains all models in the result. Each model JSON object contains:
        ** model number (e.g. 1, 2, ...)
        ** affinity (the vina result value)
        ** rmsd from best model lower bound and upper bount (stored as a list 'rmsd_from_best=["0.0", "0.0"]'
        ** model - a copy of the entire PDBQT model description stored in a list
    '''


    def __init__(self):
        '''
        Constructor - a parser for AutoDock Vina results
        '''
    def parse(self, path):
        path_to_log = path + "_log.txt"
        # open file and parse it line by line
        with open(path_to_log) as f:                                            
            # the number of CPUS is shown in a line e.g. "Detected 1 CPU"
            for line in f:                                                      
                if line.startswith("Detected"):                                 
                    # convert to int
                    cpus = int(line.split()[1])                                      
                # the random seed number is shown in a line e.g. "Using random seed: -892596696"
                elif line.startswith("Using random seed:"):                       
                    random_seed = line.split()[3]                               
                    # no need to finish reading the file
                    break                                                       
                
        struct = []                                                             
        with open(path) as f:                                                   
            # declare the list for 2 values: "rmsd from best l.b. and u.b." - floats
            rmsd_from_best = [0.0, 0.0]                                     
            # declare the list to store the entire PDBQT models
            model = []                                                                  
            for line in f:                                                      
                # append each line to the list "model" containing pdbqt models
                model.append(line)                                              
                # the model number is shown in a line e.g. "MODEL 1"
                if line.startswith("MODEL"):
                    # convert to int                                    
                    model_number = int(line.split()[1])                              
                # the affinity (vina result value) and rmsd from best are shown in a line e.g.
                # "REMARK VINA RESULT:      -5.5      2.597      4.189"                        
                elif line.startswith("REMARK VINA RESULT"):                     
                    split_line = line.split()
                    # convert to float                                       
                    affinity = float(split_line[3])
                    # put lower bound (l.b.) in rmsd_from_best[0] upper bound (u.b.) in rmsd_from_best[1]
                    # convert to float  
                    rmsd_from_best[0] = float(split_line[4])                           
                    rmsd_from_best[1] = float(split_line[5])                           
                if line.startswith("ENDMDL"):
                    # when you reach "ENDMDL" append everything to the list "struct". 
                    # This includes the model number, affinity, rmsd from best, and the entire PDBQT model
                    struct.append({"model_number": model_number, "affinity": affinity, "rmsd_from_best": rmsd_from_best, "model": model})
                    # reset the rmsd_from_best and model lists - start filling a new model in the next iteration
                    rmsd_from_best = ["0.0", "0.0"]                             
                    model = []
        
        result_dict = {}
        result_dict["CPUs"] = cpus                                              
        result_dict["random_seed"] = random_seed                                
        result_dict["models"] = struct                                              
        
        return result_dict
    