'''
Created on May 19, 2017

@author: damjan
'''

import bottle
import zipfile
import os
import at.deep_align_thread
import Queue


@bottle.post('/compareAndAssess')
def compareAndAssess():
    """ Compare 1..* receptors to a target receptor
    
    POST Parameters:
    target_receptor -- one receptor to be compared with (usually would be a pdb but could be pdbqt file, and should work with zip too)
    receptors -- receptor(s) to compare (zip file)
    config -- DeepAlign config, it can be any of these options:
    
        -x range_1:             The residue range for the 1st input protein, (e.g., A:1-150) 
        -y range_2:             The residue range for the 2nd input protein, 
                                If not specified, all residues in the first chain will be used. See README for more details.
        
        -a alignment:           Specify an initial alignment in FASTA format from which to optimize it. 
        
        -o out_name:            Specify an output file name for the alignment. If not specified, 
                                the output file name is derived from the basenames of the two inputs. 
        
        -p out_option:         [0], do not output the alignment files, just screenout. (Set as default) 
                                1,  output alignment files for single solution. 
                                2,  output alignment files for multiple solutions.
        
        -u quality:             0,  fast, low quality. 
                               [1], slow, high quality. (Set as default) 
        
        -P screenout:           0,  simple screenout alignment scores. 
                               [1], detailed screenout alignment scores. (Set as default) 
        
        -n normalize_len:       Specify a normalization length for the calculation of TMscore,MAXSUB,GDT_TS/HA. In particular,
                               [0], the minimal length of the 1st and 2nd input protein. (Set as default)
                               -1,  the length of the first input protein. 
                               -2,  the length of the second input protein. 
        
        -s score_func:          1:distance-score, 2:vector-score, 4:evolution-score; Note that these scores could be combined,
                               [7], using all score combinations. (Set as default) 
        
        -C distance_cut:        Specify a distance cutoff to remove residue pairs whose distance exceeds the threshold. 
                                0,  keep all residue pairs. 
                               [-1],automatically assign a distance cutoff value according to d0 in TMscore. (Set as default) 
        
        -M multi_cut:           if multiple solution is specified, set a TMscore cutoff for minimal quality of the solution/ 
                                (default is 0.35)   
    
    threshold -- [optional] the value of a deepalign (DeepScore) threshold, above this are similar, below not (default: 500)
           
    Returns:
    JSON response of comparing all the receptors, including a flag: SIMILAR or NOT_SIMILAR     
    """
    # the json response
    to_return = {}
    to_return["data"] = {}
    # read the POST parameters. If any are missing return with a status 'fail' explaining the required parameter  
    target_receptor = bottle.request.files.get("target_receptor")
    if target_receptor is None:
        to_return["status"] = "fail"
        to_return["data"]["target_receptor"] = "Target receptor required as a POST parameter named 'target_receptor'!"
        return to_return
    
    receptors = bottle.request.files.get("receptors")
    if receptors is None:
        to_return["status"] = "fail"
        to_return["data"]["receptors"] = "Receptor(s) to compare required as a POST parameter named 'receptors'!"
        return to_return
    
    config = bottle.request.forms.get("config")
    if config is None:
        # config is optional
        config = ""
    
    threshold = bottle.request.forms.get("threshold")
    if threshold is None:
        # threshold is optional default value is 500
        threshold = 500.0
        print "DeepScore threshold value hasn't been specified - using the default: 500"
    else:
        threshold = float(threshold)    
    
    # this is needed to prevent comparing the target receptor to itself
    target_structure_id = bottle.request.forms.get("target_structure_id")
    
    # declare names of temporary directories where zip files will be unzipped
    temp_dir = "." + os.sep + "temp"
    target_temp_dir = temp_dir + os.sep + "target"
    receptors_temp_dir = temp_dir + os.sep + "receptors"
    # declare common file extensions
    zip_ext = ".zip"
    
    # delete temporary folders where zip files were extracted
    if os.path.exists(receptors_temp_dir):    
        for receptor_file in os.listdir(receptors_temp_dir):
            os.remove(receptors_temp_dir + os.sep + receptor_file)        
    if os.path.exists(target_temp_dir + os.sep + target_receptor.filename):     
        os.remove(target_temp_dir + os.sep + target_receptor.filename)        
    
    # make a temp directory first
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
        print temp_dir + " created \n"
    if not os.path.exists(target_temp_dir):
        os.mkdir(target_temp_dir)
        print target_temp_dir + " created \n"
    if not os.path.exists(receptors_temp_dir):
        os.mkdir(receptors_temp_dir)
        print receptors_temp_dir + " created \n"
    
    
    if target_receptor.filename.endswith(zip_ext):
        print target_receptor.filename + " is one file ending with " + zip_ext + " \n"
        with zipfile.ZipFile(target_receptor.file) as target_zip:
            target_zip.extractall(target_temp_dir)
            print target_receptor.filename + " extracted in " + target_temp_dir + " \n"
    else:
        print target_receptor.filename + " is one file not ending with " + zip_ext + " \n"
        target_receptor.save(target_temp_dir + os.sep + target_receptor.filename)        
        print target_receptor.filename + " saved as " + target_temp_dir + os.sep + target_receptor.filename + " \n"            
        
    if receptors.filename.endswith(zip_ext):
        print receptors.filename + " is one file ending with " + zip_ext + " \n"        
#         print zipfile.is_zipfile(receptors.file) check if zip this way ***
        with zipfile.ZipFile(receptors.file) as receptors_zip:
            receptors_zip.extractall(receptors_temp_dir)
            print receptors.filename + " extracted in " + receptors_temp_dir + " \n"
    else:
        print receptors.filename + " is one file not ending with " + zip_ext + " \n"
        receptors.save(receptors_temp_dir + os.sep + receptors.filename)
        print receptors.filename + " saved as " + receptors_temp_dir + os.sep + receptors.filename + " \n"
    
    # the similar receptor ids will be stored in this list.
    to_return["data"]["similar"] = []
    # the config and threshold will be returned in case they were not assigned or similar
    to_return["data"]["at_config"] = config
    to_return["data"]["threshold"] = threshold
    # this is a list of threads and a queue that will be passed to each thread
    threads = []
    queue = Queue.Queue()
    for receptor in os.listdir(receptors_temp_dir):
        # get the receptor id from the name of the file
        mdrr_structure_id = receptor.split("_")[0]
        # don't run DeepAlign if the same receptor as target_receptor exists in all_receptors.zip
        if not mdrr_structure_id == target_structure_id:
            # run the DeepAlign thread
            threadForDeepAlign = at.deep_align_thread.DeepAlign(
                queue, target_temp_dir + os.sep + target_receptor.filename, receptors_temp_dir + os.sep + receptor, mdrr_structure_id, config, threshold
                )
            threads.append(threadForDeepAlign)
            threadForDeepAlign.setDaemon(True)
            threadForDeepAlign.start()
        
    for thread in threads:
        thread.join()
    
    while queue.qsize():
        try:
            to_return["data"]["similar"].append(queue.get(0))             
        except Queue.Empty:
            pass   
    
    return to_return
    


bottle.run(host='localhost', port=8091, debug=True)
