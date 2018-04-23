import requests

""" 
Arguments:
target_ligand -- the zip file of target_ligand
ligands -- zip file of ligands
Returns:
The response of the server after adding the resutls to the MongoDB

This method uses the requests module to send a HTTP request to the MDRR at url
    
Raises requests.exceptions.RequestException (prints the error code and error message on terminal beforehand)     
"""
try:
    target_ligand = "./ZINC00000036.pdbqt"
    ligands = "./ligands.zip"
    
    post_files = [('target_ligand', open(target_ligand, 'rb')),
                  ('ligands', open(ligands, 'rb'))]
    
    r = requests.post("http://localhost:8093/compareAndAssessLigands", files=post_files, verify=False)            
    # get the HTTP response code, e.g. 200.
    response_code = r.status_code 
    
    if response_code != 200:
        print('Response Code: %d' % response_code)
    print r.text
    
except requests.exceptions.RequestException, e:
    # print the error code and message and raise the error again
    print e
    raise e