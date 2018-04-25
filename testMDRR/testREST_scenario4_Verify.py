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

def verify():
    try:
        ligand = "./ligand590.pdbqt"
        receptor = "./1rka_new.pdbqt"
        config = "./conf.txt"
        
        post_values = [('thresholdDeepAlign', "777"),
                       ('thresholdLigsift', "0.6"),
                       ('thresholdConfig', "9.99")]
        post_files = [('ligand', open(ligand, 'rb')),
                      ('receptor', open(receptor, 'rb')),
                      ('config', open(config, 'rb'))]
        
        r = requests.post("http://localhost:8090/verify", files=post_files, data=post_values, verify=False)            
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
verify()
