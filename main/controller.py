'''
Created on May 19, 2017

@author: damjan
'''

import bottle
import zipfile
import os
import at_assess.compare_config
import Queue


@bottle.post('/compareConfigs')
def compare():
    """ Compare config files
    Parameters:
    target_config -- one config file
    configs -- a set of config files
    threshold -- a threshold signifying the minimum distance betweeen the cubes (average of (distance between centre, distance between size)
    Returns:
    JSON response of comparing all the configs, including a flag: SIMILAR or NOT_SIMILAR     
    """
    # the json response
    to_return = {}
    to_return["data"] = {}
    # read the POST parameters. If any are missing return with a status 'fail' explaining the required parameter  
    target_config = bottle.request.files.get("target_config")
    if target_config is None:
        to_return["status"] = "fail"
        to_return["data"]["target_config"] = "Target config required as a POST parameter named 'target_config'!"
        return to_return
    
    configs = bottle.request.files.get("configs")
    if configs is None:
        to_return["status"] = "fail"
        to_return["data"]["configs"] = "config(s) to compare required as a POST parameter named 'configs'!"
        return to_return
        
    threshold = bottle.request.forms.get("threshold")
    if threshold is None:
        # threshold is optional default value is 21.0
        threshold = 21.0
        print "Average config distance threshold value hasn't been specified - using the default: 21.0"
    else:
        threshold = float(threshold)    
    
    # declare names of temporary directories where zip files will be unzipped
    temp_dir = "." + os.sep + "temp"
    target_temp_dir = temp_dir + os.sep + "target"
    configs_temp_dir = temp_dir + os.sep + "configs"
    # declare common file extensions
    zip_ext = ".zip"
    
    # delete temporary folders where zip files were extracted
    if os.path.exists(configs_temp_dir):    
        for config_file in os.listdir(configs_temp_dir):
            os.remove(configs_temp_dir + os.sep + config_file)        
    if os.path.exists(target_temp_dir + os.sep + target_config.filename):     
        os.remove(target_temp_dir + os.sep + target_config.filename)        
    
    # make a temp directory first
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
        print temp_dir + " created \n"
    if not os.path.exists(target_temp_dir):
        os.mkdir(target_temp_dir)
        print target_temp_dir + " created \n"
    if not os.path.exists(configs_temp_dir):
        os.mkdir(configs_temp_dir)
        print configs_temp_dir + " created \n"
    
    
    if target_config.filename.endswith(zip_ext):
        print target_config.filename + " is one file ending with " + zip_ext + " \n"
        with zipfile.ZipFile(target_config.file) as target_zip:
            target_zip.extractall(target_temp_dir)
            print target_config.filename + " extracted in " + target_temp_dir + " \n"
    else:
        print target_config.filename + " is one file not ending with " + zip_ext + " \n"
        target_config.save(target_temp_dir + os.sep + target_config.filename)        
        print target_config.filename + " saved as " + target_temp_dir + os.sep + target_config.filename + " \n"            
        
    if configs.filename.endswith(zip_ext):
        print configs.filename + " is one file ending with " + zip_ext + " \n"        
#         print zipfile.is_zipfile(configs.file) check if zip this way ***
        with zipfile.ZipFile(configs.file) as configs_zip:
            configs_zip.extractall(configs_temp_dir)
            print configs.filename + " extracted in " + configs_temp_dir + " \n"
    else:
        print configs.filename + " is one file not ending with " + zip_ext + " \n"
        configs.save(configs_temp_dir + os.sep + configs.filename)
        print configs.filename + " saved as " + configs_temp_dir + os.sep + configs.filename + " \n"
    
    # the similar config ids will be stored in this list.
    to_return["data"]["similar"] = []
    # the  threshold will be returned in case it were not assigned or similar
    to_return["data"]["threshold"] = threshold
    # this is a list of threads and a queue that will be passed to each thread
    threads = []
    queue = Queue.Queue()
    for config in os.listdir(configs_temp_dir):

        # run the CompareConfig thread
        threadForCompareConfig = at_assess.compare_config.Assess(
            queue, target_temp_dir + os.sep + target_config.filename, configs_temp_dir + os.sep + config, threshold
            )
        threads.append(threadForCompareConfig)
        threadForCompareConfig.setDaemon(True)
        threadForCompareConfig.start()
        
    for thread in threads:
        thread.join()
    
    while queue.qsize():
        try:
            to_return["data"]["similar"].append(queue.get(0))             
        except Queue.Empty:
            pass   
    
    return to_return
    


bottle.run(host='localhost', port=8094, debug=True)
