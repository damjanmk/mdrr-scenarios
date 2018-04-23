import requests
""" Call MDRR-RestApi insertMany

Arguments:
ligands -- the zip file of ligands
receptors -- zip file of receptors
configs -- zip file of conf.txt file (1-to-1 mapping with receptors, one conf for each receptor)  
results -- zip file with results (recName_ligName_out.pdbqt and recName_ligName_out.pdbqt_log.txt)
url -- the url of the MDRR server

Returns:
The response of the server after adding the resutls to the MongoDB

This method uses the requests module to send a HTTP request to the MDRR at url
    
Raises requests.exceptions.RequestException (prints the error code and error message on terminal beforehand)     
"""
try:
    target_receptor = "./rec.pdbqt"
    receptors = "./receptors.zip"
    
    post_files = [('target_receptor', open(target_receptor, 'rb')),
                  ('receptors', open(receptors, 'rb'))]

    r = requests.post("http://localhost:8091/compareAndAssess", files=post_files, verify=False)            
    # get the HTTP response code, e.g. 200.
    response_code = r.status_code 
    
    if response_code != 200:
        print('Response Code: %d' % response_code)
    print r.text
    
except requests.exceptions.RequestException, e:
    # print the error code and message and raise the error again
    print e
    raise e
        
