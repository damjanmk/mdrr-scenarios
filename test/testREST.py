import requests

""" 
Arguments:
target_config -- the zip file of target_config
configs -- zip file of configs     

Returns:
The response of the server after adding the resutls to the MongoDB

This method uses the requests module to send a HTTP request to the MDRR at url
    
Raises requests.exceptions.RequestException (prints the error code and error message on terminal beforehand)     
"""
try:
    target_config = "./conf.txt"
    configs = "./config.zip"
    
    post_values = [('threshold', 9.99)]
            
    post_files = [('target_config', open(target_config, 'rb')),
                  ('configs', open(configs, 'rb'))]
    
    r = requests.post("http://localhost:8094/compareConfigs", files=post_files, data=post_values, verify=False)            
    # get the HTTP response code, e.g. 200.
    response_code = r.status_code 
    
    if response_code != 200:
        print('Response Code: %d' % response_code)
    print r.text

except requests.exceptions.RequestException, e:
    # print the error code and message and raise the error again
    print e
    raise e