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
 
def consult():
    try:
        results = ["5a5cc8e8c831de11a5d80a79", "5a5d0855c831de11a5d82759", "5a5d0856c831de11a5d82810", "5a5d0859c831de11a5d82a1a", "5a5d085dc831de11a5d82c8a"]
        
        post_values = [('query', "Complexity < 270"),
                       ('results', str(results)),
                       ('thresholdVinaDocking', "-5.6"),
                       ('inserted', "True")]
        
        r = requests.post("http://localhost:8090/consult", data=post_values, verify=False)            
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
consult()
