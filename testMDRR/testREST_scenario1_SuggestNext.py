import requests
from datetime import datetime
import random
 

def insertMany():    
    try:
        ligands = "./ligands.zip"
        receptors = "./receptors.zip"
        configs = "./configs.zip"
        results = "./results.zip"
        
        post_values = [('group_id', datetime.now().strftime("%Y%m%d-%H%M%S%Z-") + str(random.random()))]
        post_files = [('ligands', open(ligands, 'rb')),
                      ('receptors', open(receptors, 'rb')),
                      ('configs', open(configs, 'rb')),
                      ('results', open(results, 'rb'))]
        
        r = requests.post("http://localhost:8090/insertMany", files=post_files, data=post_values, verify=False)            
        # get the HTTP response code, e.g. 200.
        response_code = r.status_code 
        
        if response_code != 200:
            print('Response Code: %d' % response_code)
        print r.text
    except requests.exceptions.RequestException, e:
        # print the error code and message and raise the error again
        print e
        raise e 
 
def suggestNext():
    try:
        receptors = "./receptors.zip"
        
        post_values = [('thresholdDeepAlign', "777"),
                       ('thresholdVinaDocking', "-7.0"),
                       ('group_id', datetime.now().strftime("%Y%m%d-%H%M%S%Z-") + str(random.random()))]
        post_files = [('receptors', open(receptors, 'rb'))]
        
        r = requests.post("http://localhost:8090/suggestNext", files=post_files, data=post_values, verify=False)            
        # get the HTTP response code, e.g. 200.
        response_code = r.status_code 
        
        if response_code != 200:
            print('Response Code: %d' % response_code)
        print r.text
    except requests.exceptions.RequestException, e:
        # print the error code and message and raise the error again
        print e
        raise e
    
    
# insertMany()
suggestNext()


