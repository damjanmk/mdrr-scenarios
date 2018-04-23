'''
Created on May 19, 2017

@author: damjan
'''

import bottle
import zipfile
import os
import at.ligsift_thread
import Queue


@bottle.post('/compareAndAssessLigands')
def compareAndAssess():
    """ Compare 1..* ligands to a target ligand
    
    POST Parameters:
    target_ligand -- ligand to be compared with (a .mol2 file, can be .pdbqt)
    ligands -- ligand(s) to compare (a .mol2 'database' file, can be .zip of .pdbqt files)
    threshold -- [optional] the value of a LIGSIFT (ShapeSim) threshold, above this are similar, below not (default: 0.5)
    config -- Ligsift config, it can be any of these options (mainly the -opt):
    
        Usage:
        LIGSIFT -q    <query molecules, MOL2>
                -db   <database molecules,MOL2>
                -o    <Output score file>
        Additional options:
                -s    <Superposed database molecules on query,MOL2>
                -v    For verbose output
                -opt  0(Overlap optimized based on Shape similarity)
                      1(Overlap optimized based on Shape + Chemical similarity)
                      2(Overlap optimized based on Chemical similarity:Default method)
        For example:
        
        ./LIGSIFT -q ZINCXXX.mol2   -db DB.mol2   -o alignment_scores.txt   -s superposed.mol2
       
    Returns:
    JSON response of comparing all the ligands, including a flag: SIMILAR or NOT_SIMILAR     
    """
    # the json response
    to_return = {}
    to_return["data"] = {}
    # read the POST parameters. If any are missing return with a status 'fail' explaining the required parameter  
    target_ligand = bottle.request.files.get("target_ligand")
    if target_ligand is None:
        to_return["status"] = "fail"
        to_return["data"]["target_ligand"] = "Target ligand required as a POST parameter named 'target_ligand'!"
        return to_return
    
    ligands = bottle.request.files.get("ligands")
    if ligands is None:
        to_return["status"] = "fail"
        to_return["data"]["ligands"] = "ligand(s) to compare required as a POST parameter named 'ligands'!"
        return to_return
    
    config = bottle.request.forms.get("config")
    if config is None:
        # config is optional
        config = ""
    
    threshold = bottle.request.forms.get("threshold")
    if threshold is None:
        # threshold is optional default value is 0.6
        threshold = 0.6
        print "LIGSIFT (ShapeSim) threshold value hasn't been specified - using the default: 0.6"
    else:
        threshold = float(threshold)    
    
    # this is needed to prevent comparing the target ligand to itself
    target_structure_id = bottle.request.forms.get("target_structure_id")
    
    # declare names of temporary directories where zip files will be unzipped
    temp_dir = "." + os.sep + "temp"
    target_temp_dir = temp_dir + os.sep + "target"
    ligands_temp_dir = temp_dir + os.sep + "ligands"
    # declare common file extensions
    zip_ext = ".zip"
    
    # delete temporary folders where zip files were extracted
    if os.path.exists(ligands_temp_dir):    
        for ligand_file in os.listdir(ligands_temp_dir):
            os.remove(ligands_temp_dir + os.sep + ligand_file)        
    if os.path.exists(target_temp_dir + os.sep + target_ligand.filename):     
        os.remove(target_temp_dir + os.sep + target_ligand.filename)        
    
    # make a temp directory first
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
        print temp_dir + " created \n"
    if not os.path.exists(target_temp_dir):
        os.mkdir(target_temp_dir)
        print target_temp_dir + " created \n"
    if not os.path.exists(ligands_temp_dir):
        os.mkdir(ligands_temp_dir)
        print ligands_temp_dir + " created \n"
    
    
    if target_ligand.filename.endswith(zip_ext):
        print target_ligand.filename + " is one file ending with " + zip_ext + " \n"
        with zipfile.ZipFile(target_ligand.file) as target_zip:
            target_zip.extractall(target_temp_dir)
            print target_ligand.filename + " extracted in " + target_temp_dir + " \n"
    else:
        print target_ligand.filename + " is one file not ending with " + zip_ext + " \n"
        target_ligand.save(target_temp_dir + os.sep + target_ligand.filename)        
        print target_ligand.filename + " saved as " + target_temp_dir + os.sep + target_ligand.filename + " \n"            
        
    if ligands.filename.endswith(zip_ext):
        print ligands.filename + " is one file ending with " + zip_ext + " \n"        
#         print zipfile.is_zipfile(ligands.file) check if zip this way ***
        with zipfile.ZipFile(ligands.file) as ligands_zip:
            ligands_zip.extractall(ligands_temp_dir)
            print ligands.filename + " extracted in " + ligands_temp_dir + " \n"
    else:
        print ligands.filename + " is one file not ending with " + zip_ext + " \n"
        ligands.save(ligands_temp_dir + os.sep + ligands.filename)
        print ligands.filename + " saved as " + ligands_temp_dir + os.sep + ligands.filename + " \n"
    
    # the similar ligand ids will be stored in this list.
    to_return["data"]["similar"] = []
    # the config and threshold will be returned in case they were not assigned or similar
    to_return["data"]["at_config"] = config
    to_return["data"]["threshold"] = threshold
    # this is a list of threads and a queue that will be passed to each thread
    threads = []
    queue = Queue.Queue()
    for ligand in os.listdir(ligands_temp_dir):
        # get the ligand id from the name of the file
        mdrr_ligand_structure_id = ligand.split("_")[0]
        ligand_name = ligand.split("_")[1]
        # don't run Ligsift if the same ligand as target_ligand exists in all_ligands.zip
        if not mdrr_ligand_structure_id == target_structure_id:
            output_file = temp_dir + os.sep + "dummy_output.out"
            # create an empty file
            open(output_file, "w").close()
                
            # run the Ligsift thread
            threadForLigsift = at.ligsift_thread.Ligsift(
                queue, target_temp_dir + os.sep + target_ligand.filename, ligands_temp_dir + os.sep + ligand, mdrr_ligand_structure_id, ligand_name, config, output_file, threshold
                )
            threads.append(threadForLigsift)
            threadForLigsift.setDaemon(True)
            threadForLigsift.start()
        
    for thread in threads:
        thread.join()
    
    while queue.qsize():
        try:
            to_return["data"]["similar"].append(queue.get(0))             
        except Queue.Empty:
            pass   
    
    return to_return
    


bottle.run(host='localhost', port=8093, debug=True)
