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
    
def verify():
    try:
        ligand = "./ZINC00000384.pdbqt"
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
   
def consult():
    try:
        results = ["59522cc4c831de0e7c524636", "59522cc4c831de0e7c524639", "5952217cc831de0e7c52461a", "59998c29c831de10b17eed58", "592f2cfac831de25fe46f1d7"]
        
        post_values = [('query', "Complexity < 220"),
                       ('results', str(results)),
                       ('thresholdVinaDocking', "-7.0"),
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
    
def consult2():
    try:
        results = "./results.zip"
        ligands = "./ligands.zip"
        
        post_values = [('query', "Complexity < 220"),
                       ('thresholdVinaDocking', "-5.6"),
                       ('inserted', "False")]
        post_files = [('ligands', open(ligands, 'rb')),
                      ('results', open(results, 'rb'))]
        
        r = requests.post("http://localhost:8090/consult", files=post_files, data=post_values, verify=False)            
        # get the HTTP response code, e.g. 200.
        response_code = r.status_code 
        
        if response_code != 200:
            print('Response Code: %d' % response_code)
        print r.text
    except requests.exceptions.RequestException, e:
        # print the error code and message and raise the error again
        print e
        raise e
    
    
# consult()
# consult2()
verify()
# insertMany()
# suggestNext()










# import pycurl
# from StringIO import StringIO
# from datetime import datetime
# import random
#  
# """ Call MDRR-RestApi insertMany
#  
# Arguments:
# ligands -- the zip file of ligands
# receptors -- zip file of receptors
# configs -- zip file of conf.txt file (1-to-1 mapping with receptors, one conf for each receptor)  
# results -- zip file with results (recName_ligName_out.pdbqt and recName_ligName_out.pdbqt_log.txt)
# url -- the url of the MDRR server
#  
# Returns:
# The response of the server after adding the resutls to the MongoDB
#  
# This method uses pycurl to send a HTTP request to the MDRR at url
#      
# Raises pycurl.error (prints the error code and error message on terminal beforehand)     
# """
# def insertMany():
#     try:
#         ligands = "./ligands.zip"
#         receptors = "./receptors.zip"
#         configs = "./configs.zip"
#         results = "./results.zip"
#         # the post parameters: ligands='ligands' (file), receptors='...'(file), configs='...' (file), results='...'(file)
#         pf = [('ligands', (pycurl.FORM_FILE, ligands)),
#               ('receptors', (pycurl.FORM_FILE, receptors)),
#               ('configs', (pycurl.FORM_FILE, configs)),
#               ('results', (pycurl.FORM_FILE, results)),
#               ('group_id', datetime.now().strftime("%Y%m%d-%H%M%S%Z-") + str(random.random()))
#              ]
#         # create new pycurl object
#         c = pycurl.Curl()
#         # set the parameters: URL, HTTPPOST parameters
#         c.setopt(c.URL, "http://localhost:8090/insertMany")
#         c.setopt(c.HTTPPOST, pf)
#         # ignore SSL error (equivalent to curl --insecure or curl -k)
#     #     c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#     #            # uncomment the next line for verbose (curl -v)  
#     #             c.setopt(c.VERBOSE, False)
#         #this StringIO is needed to store the response in
#         response_buffer = StringIO()
#         # set the option to write the response into the response_buffer
#         c.setopt(c.WRITEDATA, response_buffer)
#         # send the request
#         c.perform()            
#         # get the HTTP response code, e.g. 200.
#         response_code = c.getinfo(c.RESPONSE_CODE) 
#         if response_code != 200:
#             print('Response Code: %d' % response_code)
#         c.close()
#         print response_buffer.getvalue()
#     except pycurl.error, e:
#         # print the error code and message and raise the error again
#         print "Error code: ", e[0]
#         print "Error message: ", e[1]  
#         raise e
#  
#  
# def suggestNext():
#     try:
#         receptors = "./receptors.zip"
#         # the post parameters: ligands='ligands' (file), receptors='...'(file), configs='...' (file), results='...'(file)
#         pf = [('receptors', (pycurl.FORM_FILE, receptors)),
#               ('thresholdDeepAlign', "777"),
#               ('thresholdVinaDocking', "-7.0"),
#               ('group_id', datetime.now().strftime("%Y%m%d-%H%M%S%Z-") + str(random.random()))
#              ]
#         # create new pycurl object
#         c = pycurl.Curl()
#         # set the parameters: URL, HTTPPOST parameters
#         c.setopt(c.URL, "http://localhost:8090/suggestNext")
#         c.setopt(c.HTTPPOST, pf)
#         # ignore SSL error (equivalent to curl --insecure or curl -k)
#     #     c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#     #            # uncomment the next line for verbose (curl -v)  
#     #             c.setopt(c.VERBOSE, False)
#         #this StringIO is needed to store the response in
#         response_buffer = StringIO()
#         # set the option to write the response into the response_buffer
#         c.setopt(c.WRITEDATA, response_buffer)
#         # send the request
#         c.perform()            
#         # get the HTTP response code, e.g. 200.
#         response_code = c.getinfo(c.RESPONSE_CODE) 
#         if response_code != 200:
#             print('Response Code: %d' % response_code)
#         c.close()
#         print response_buffer.getvalue()
#     except pycurl.error, e:
#         # print the error code and message and raise the error again
#         print "Error code: ", e[0]
#         print "Error message: ", e[1]  
#         raise e  
#  
#  
# def insertFindSimilarAssess():
#     try:
#         ligands = "./ligands.zip"
#         receptors = "./receptors.zip"
# #         configs = "./configs.zip"
#         configs = "./conf.txt"
#         results = "./results.zip"
#         # the post parameters: ligands='ligands' (file), receptors='...'(file), configs='...' (file), results='...'(file)
#         pf = [('ligands', (pycurl.FORM_FILE, ligands)),
#               ('receptors', (pycurl.FORM_FILE, receptors)),
#               ('configs', (pycurl.FORM_FILE, configs)),
#               ('results', (pycurl.FORM_FILE, results)),
#               ('thresholdDeepAlign', "777"),
#               ('thresholdVinaDocking', "-7.0"),
#              ]
#         # create new pycurl object
#         c = pycurl.Curl()
#         # set the parameters: URL, HTTPPOST parameters
#         c.setopt(c.URL, "http://localhost:8090/insertFindSimilarAssess")
#         c.setopt(c.HTTPPOST, pf)
#         # ignore SSL error (equivalent to curl --insecure or curl -k)
#     #     c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#     #            # uncomment the next line for verbose (curl -v)  
#     #             c.setopt(c.VERBOSE, False)
#         #this StringIO is needed to store the response in
#         response_buffer = StringIO()
#         # set the option to write the response into the response_buffer
#         c.setopt(c.WRITEDATA, response_buffer)
#         # send the request
#         c.perform()            
#         # get the HTTP response code, e.g. 200.
#         response_code = c.getinfo(c.RESPONSE_CODE) 
#         if response_code != 200:
#             print('Response Code: %d' % response_code)
#         c.close()
#         print response_buffer.getvalue()
#     except pycurl.error, e:
#         # print the error code and message and raise the error again
#         print "Error code: ", e[0]
#         print "Error message: ", e[1]  
#         raise e        
#  
#  
# def verify():
#     try:
#         ligand = "./ZINC00000384.pdbqt"
#         receptor = "./1rka_new.pdbqt"
#         config = "./conf.txt"
#         # the post parameters: ligands='ligands' (file), receptors='...'(file), configs='...' (file), results='...'(file)
#         pf = [('ligand', (pycurl.FORM_FILE, ligand)),
#               ('receptor', (pycurl.FORM_FILE, receptor)),
#               ('config', (pycurl.FORM_FILE, config)),
#               ('thresholdDeepAlign', "777"),
#               ('thresholdLigsift', "0.6"),
#               ('thresholdConfig', "9.99")
#              ]
#         # create new pycurl object
#         c = pycurl.Curl()
#         # set the parameters: URL, HTTPPOST parameters
#         c.setopt(c.URL, "http://localhost:8090/verify")
#         c.setopt(c.HTTPPOST, pf)
#         # ignore SSL error (equivalent to curl --insecure or curl -k)
#     #     c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#     #            # uncomment the next line for verbose (curl -v)  
#     #             c.setopt(c.VERBOSE, False)
#         #this StringIO is needed to store the response in
#         response_buffer = StringIO()
#         # set the option to write the response into the response_buffer
#         c.setopt(c.WRITEDATA, response_buffer)
#         # send the request
#         c.perform()            
#         # get the HTTP response code, e.g. 200.
#         response_code = c.getinfo(c.RESPONSE_CODE) 
#         if response_code != 200:
#             print('Response Code: %d' % response_code)
#         c.close()
#         print response_buffer.getvalue()
#     except pycurl.error, e:
#         # print the error code and message and raise the error again
#         print "Error code: ", e[0]
#         print "Error message: ", e[1]  
#         raise e        
#  
#  
# def consult():
#     try:
#         results = ["59522cc4c831de0e7c524636", "59522cc4c831de0e7c524639", "5952217cc831de0e7c52461a", "59998c29c831de10b17eed58", "592f2cfac831de25fe46f1d7"]
#         # the post parameters: ligands='ligands' (file), receptors='...'(file), configs='...' (file), results='...'(file)
# #         ('ligands', (pycurl.FORM_FILE, ligand)),
#         pf = [
#               ('query', "Complexity < 220"),
#               ('results', str(results)),
#               ('thresholdVinaDocking', "-7.0"),
#               ('inserted', "True")
#              ]
#         # create new pycurl object
#         c = pycurl.Curl()
#         # set the parameters: URL, HTTPPOST parameters
#         c.setopt(c.URL, "http://localhost:8090/consult")
#         c.setopt(c.HTTPPOST, pf)
#         # ignore SSL error (equivalent to curl --insecure or curl -k)
#     #     c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#     #            # uncomment the next line for verbose (curl -v)  
#     #             c.setopt(c.VERBOSE, False)
#         #this StringIO is needed to store the response in
#         response_buffer = StringIO()
#         # set the option to write the response into the response_buffer
#         c.setopt(c.WRITEDATA, response_buffer)
#         # send the request
#         c.perform()            
#         # get the HTTP response code, e.g. 200.
#         response_code = c.getinfo(c.RESPONSE_CODE)
#          
#         print('Response Code: %d' % response_code)
#          
#         c.close()
#         print response_buffer.getvalue()
#     except pycurl.error, e:
#         # print the error code and message and raise the error again
#         print "Error code: ", e[0]
#         print "Error message: ", e[1]  
#         raise e  
#  
# def consult2():
#     try:
#         results = "./results.zip"
#         ligands = "./ligands.zip"
#         # the post parameters: ligands='ligands' (file), receptors='...'(file), configs='...' (file), results='...'(file)
# #         ('ligands', (pycurl.FORM_FILE, ligand)),
#         pf = [
#               ('query', "Complexity < 220"),
#               ('results', (pycurl.FORM_FILE, results)),
#               ('ligands', (pycurl.FORM_FILE, ligands)),
#               ('thresholdVinaDocking', "-5.6"),
#               ('inserted', "False")
#              ]
#         # create new pycurl object
#         c = pycurl.Curl()
#         # set the parameters: URL, HTTPPOST parameters
#         c.setopt(c.URL, "http://localhost:8090/consult")
#         c.setopt(c.HTTPPOST, pf)
#         # ignore SSL error (equivalent to curl --insecure or curl -k)
#     #     c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#     #            # uncomment the next line for verbose (curl -v)  
#     #             c.setopt(c.VERBOSE, False)
#         #this StringIO is needed to store the response in
#         response_buffer = StringIO()
#         # set the option to write the response into the response_buffer
#         c.setopt(c.WRITEDATA, response_buffer)
#         # send the request
#         c.perform()            
#         # get the HTTP response code, e.g. 200.
#         response_code = c.getinfo(c.RESPONSE_CODE)
#          
#         print('Response Code: %d' % response_code)
#          
#         c.close()
#         print response_buffer.getvalue()
#     except pycurl.error, e:
#         # print the error code and message and raise the error again
#         print "Error code: ", e[0]
#         print "Error message: ", e[1]  
#         raise e
#      
# # consult()
# # consult2()
# verify()
# # insertMany()
# # suggestNext()


# '''
# Created on May 19, 2017
# 
# @author: damjan
# '''
# 
# import bottle
# import zipfile
# import os
# import pymongo    
# import json
# import pycurl
# import requests
# from StringIO import StringIO
# import bson.json_util
# import time
# import ast
# import mdrr.inserter
# import mdrr.selector
# import mdrr.receptor_parser
# import dm.decider
# 
# @bottle.post('/insertMany')
# def insertMany():
#     """ Insert 1..* results made up of 1..* ligands, 1..* receptors and 1..* config files
#     
#     POST Parameters:
#     ligands -- ligand(s) (.zip for > 1 ligand, .pdqbt for 1 ligand)
#     receptors -- receptor(s) (.zip for > 1 ligand, .pdqbt for 1 ligand)
#     configs -- config file(s) (1-to-1 mapping with receptors, one conf for each receptor, .zip for > 1 ligand, other for 1 ligand)  
#     results -- results zip file (one or more sets of: recName_ligName_out.pdbqt and recName_ligName_out.pdbqt_log.txt)
#         
#     Returns:
#     JSON response of adding the results to the MongoDB repository     
#     """
#     print "Welcome to 'insertMany'"
#     to_return = {}
#     to_return["data"] = {}
#     # read the POST parameters. If any are missing return with a status 'fail' explaining the required parameter  
#     ligands = bottle.request.files.get("ligands")
#     if not ligands:
#         to_return["status"] = "fail"
#         to_return["data"]["ligands"] = "Ligands required as a POST parameter named 'ligands'!"
#         return to_return
#     
#     receptors = bottle.request.files.get("receptors")
#     if not receptors:
#         to_return["status"] = "fail"
#         to_return["data"]["receptors"] = "Receptors required as a POST parameter named 'receptors'!"
#         return to_return
#     
#     configs = bottle.request.files.get("configs")
#     if not configs:
#         to_return["status"] = "fail"
#         to_return["data"]["configs"] = "Configs required as a POST parameter named 'configs'!"
#         return to_return
#     
#     results = bottle.request.files.get("results")
#     if not results:
#         to_return["status"] = "fail"
#         to_return["data"]["results"] = "Results required as a POST parameter named 'results'!"
#         return to_return
#     
#     group_id = bottle.request.params.get("group_id")
#     
#     # declare names of temporary directories where zip files will be unzipped
#     temp_dir = "." + os.sep + "temp"
#     
#     #make a temp directory
#     if not os.path.exists(temp_dir):
#         os.mkdir(temp_dir)
#         print temp_dir + " created \n"
#     
#     results_temp_dir = temp_dir + os.sep + "results"
#     configs_temp_dir = temp_dir + os.sep + "configs"
#     ligands_temp_dir = temp_dir + os.sep + "ligands"
#     receptors_temp_dir = temp_dir + os.sep + "receptors"
#     
#     # connect to the MongoDB - this could go in another method
#     client = pymongo.MongoClient()      
#     db = client.mdrr_1
#     
#     # call the method to insert the data in MongoDB
#     to_return = insert(db, ligands, ligands_temp_dir, receptors, receptors_temp_dir, configs, configs_temp_dir, results, results_temp_dir, group_id)
#         
#     # delete temporary folders where zip files were extracted
#     if os.path.exists(configs_temp_dir):
#         for config_file in os.listdir(configs_temp_dir):
#             os.remove(configs_temp_dir + os.sep + config_file)
#         os.removedirs(configs_temp_dir)
#     
#     if os.path.exists(receptors_temp_dir): 
#         for receptor_file in os.listdir(receptors_temp_dir):
#             os.remove(receptors_temp_dir + os.sep + receptor_file)
#         os.removedirs(receptors_temp_dir)
#     
#     if os.path.exists(ligands_temp_dir): 
#         for ligand_file in os.listdir(ligands_temp_dir):
#             os.remove(ligands_temp_dir + os.sep + ligand_file)
#         os.removedirs(ligands_temp_dir)
#     
#     if os.path.exists(results_temp_dir): 
#         for result_file in os.listdir(results_temp_dir):
#             os.remove(results_temp_dir + os.sep + result_file)
#         os.removedirs(results_temp_dir)
#     
#     #return the json with data about all the steps and the final decision
#     print "Goodbye from 'insertMany'"
#     return to_return #this one asks bottle to call json.dumps() 
#     
# 
# def insert(db, ligands, ligands_temp_dir, receptors, receptors_temp_dir, configs, configs_temp_dir, results, results_temp_dir, group_id):
#     """ Insert 1..* results made up of 1..* ligands, 1..* receptors and 1..* config files
#     
#     Parameters:
#     ligands -- ligand(s) (.zip for > 1 ligand, .pdqbt for 1 ligand)
#     receptors -- receptor(s) (.zip for > 1 ligand, .pdqbt for 1 ligand)
#     configs -- config file(s) (1-to-1 mapping with receptors, one conf for each receptor, .zip for > 1 ligand, other for 1 ligand)  
#     results -- results zip file (one or more sets of: recName_ligName_out.pdbqt and recName_ligName_out.pdbqt_log.txt)
#     group_id --    
#     Returns:
#     dict response of adding the results to the MongoDB repository     
#     """
#     print "Welcome to 'insert'"
#     # the dict response
#     to_return = {}
#     to_return["data"] = {}
#     
#     # instantiate an inserter
#     mdrr_inserter = mdrr.inserter.Inserter(db)
#     
#     # declare common file extensions
#     vina_input_ext = ".pdbqt"
#     zip_ext = ".zip"
#     
#     # unzip the results zip file     
#     with zipfile.ZipFile(results.file) as results_zip:
#         results_zip.extractall(results_temp_dir)
#         print results.filename + " extracted in " + results_temp_dir + " \n"
#     
#     to_return["data"]["inserted_results"] = []
#     
#     # look at all combinations of one or more receptors, ligands, configs (this is all for AutoDock Vina)
#     # if 1 receptor has been sent
#     if receptors.filename.endswith(vina_input_ext):
#         print receptors.filename + " is one file ending with " + vina_input_ext + " \n"
#         # if 1 ligand has been sent
#         if ligands.filename.endswith(vina_input_ext):
#             # this  means there is 1 receptor, 1 ligand, 1 config and 1 result
#             print ligands.filename + " is one file ending with " + vina_input_ext + " \n"            
#             result_file = ""
#             for unzipped_result in os.listdir(results_temp_dir):
#                 if unzipped_result.endswith("_out.pdbqt"): # could be replaced with 'vina_input_ext'
#                     result_file = results_temp_dir + os.sep + unzipped_result
#             print "There is one result file: " + result_file + " \n"
#             # if a zip with a config file has been sent, unzip it (if the zip contains more than 1 config the first will be taken)
#             if configs.filename.endswith(zip_ext):
#                 print configs.filename + " is a zip file ending with " + zip_ext + " \n"                
#                 with zipfile.ZipFile(configs.file) as configs_zip:
#                     configs_zip.extractall(configs_temp_dir)
#                 print "inserting into mdrr... \n"
#                 to_return["data"]["inserted_results"].append(
#                                             {"result_id": str(
#                                             mdrr_inserter.insert_result(receptor=receptors.file, receptor_path_or_content="content", 
#                                                 ligand=ligands.file, ligand_path_or_content="content",
#                                                 result_path=result_file, 
#                                                 config = os.listdir(configs_temp_dir)[0], config_path_or_content="path")
#                                             ), 
#                                              "receptor": receptors.filename})
#             # if 1 config file is sent [i.e. configs.filename.endswith(".txt") or ".conf" or "cnf"]
#             else:
#                 print configs.filename + " is one file ending with something else (e.g. .txt) \n"                
#                 print "inserting into mdrr... \n"
#                 to_return["data"]["inserted_results"].append(
#                                             {"result_id": str(
#                                             mdrr_inserter.insert_result(receptor=receptors.file, receptor_path_or_content="content", 
#                                                 ligand=ligands.file, ligand_path_or_content="content",
#                                                 result_path=result_file, 
#                                                 config = configs.file, config_path_or_content="content")
#                                             ), 
#                                              "receptor": receptors.filename})
#                 
#         # if a zip with ligands has been sent, unzip it
#         elif ligands.filename.endswith(zip_ext):
#             # there are 1 receptor, many ligands, 1 config, and many results
#             print ligands.filename + " is a zip file ending with " + zip_ext + " \n"            
#             with zipfile.ZipFile(ligands.file) as ligands_zip:
#                     ligands_zip.extractall(ligands_temp_dir)
#             # if a zip with a config file has been sent, unzip it (if the zip contains more than 1 config the first will be taken)        
#             if configs.filename.endswith(zip_ext):
#                 with zipfile.ZipFile(configs.file) as configs_zip:
#                     configs_zip.extractall(configs_temp_dir)
#                 print configs.filename + " is a zip file ending with " + zip_ext + " \n" 
#                    
#                 # for each ligand in the zip file, insert one item in the mdrr with the first config file inside the zip
#                 for one_ligand in os.listdir(ligands_temp_dir):
#                     print "inserting into mdrr... \n"
#                     to_return["data"]["inserted_results"].append(
#                                             {"result_id": str(
#                                             mdrr_inserter.insert_result(receptor=receptors.file, receptor_path_or_content="content", 
#                                                 ligand=ligands_temp_dir + os.sep + one_ligand, ligand_path_or_content="path",
#                                                 result_path=result_file, 
#                                                 config = os.listdir(configs_temp_dir)[0], config_path_or_content="path")
#                                             ), 
#                                              "receptor": receptors.filename})
#             # if 1 config file is sent [i.e. configs.filename.endswith(".txt") or ".conf" or "cnf"]
#             else:
#                 print configs.filename + " is one file ending with something else (e.g. .txt) \n"
#                 # for each ligand in the zip file, insert one item in the mdrr with the file sent as config 
#                 for one_ligand in os.listdir(ligands_temp_dir):
#                     print "inserting into mdrr... \n"
#                     to_return["data"]["inserted_results"].append(
#                                             {"result_id": str(
#                                             mdrr_inserter.insert_result(receptor=receptors.file, receptor_path_or_content="content", 
#                                                 ligand=ligands_temp_dir + os.sep + one_ligand, ligand_path_or_content="path",
#                                                 result_path=result_file, 
#                                                 config = configs.file, config_path_or_content="content")
#                                             ), 
#                                              "receptor": receptors.filename})
#     # if a zip with receptors has been sent, unzip it
#     elif receptors.filename.endswith(zip_ext):
#         print receptors.filename + " is a zip file ending with " + zip_ext + " \n"
#         with zipfile.ZipFile(receptors.file) as receptors_zip:
#             receptors_zip.extractall(receptors_temp_dir)
#         
#         # if 1 ligand has been sent
#         if ligands.filename.endswith(vina_input_ext):
#             # now there are many receptor, 1 ligand, many configs and many results
#             print ligands.filename + " is one file ending with " + vina_input_ext + " \n"
#             # if a zip with a config file has been sent, unzip it (it should be 1-to-1 mapping with receptors)
#             if configs.filename.endswith(zip_ext):
#                 print configs.filename + " is a zip file ending with " + zip_ext + " \n"
#                 with zipfile.ZipFile(configs.file) as configs_zip:
#                     configs_zip.extractall(configs_temp_dir)
#                 # a list of all the config files
#                 all_configs = os.listdir(configs_temp_dir)
#                 mapped_config = 0
#                 # for each receptor, insert a tuple into the mdrr with the correct config
#                 for one_receptor in os.listdir(receptors_temp_dir):
#                     print "inserting into mdrr... \n"
#                     to_return["data"]["inserted_results"].append(
#                                             {"result_id": str(
#                                             mdrr_inserter.insert_result(receptor=one_receptor, receptor_path_or_content="path", 
#                                                 ligand=ligands.file, ligand_path_or_content="content",
#                                                 result_path=results_temp_dir + os.path.splitext(one_receptor)[0] + "_" + os.path.splitext(ligands.filename)[0] + "_out.pdbqt", 
#                                                 config = configs_temp_dir + os.sep + all_configs[mapped_config], config_path_or_content="path")
#                                             ), 
#                                              "receptor": one_receptor})
#                     
#                     mapped_config = mapped_config + 1
#             # if 1 config file is sent [i.e. configs.filename.endswith(".txt") or ".conf" or "cnf"]
#             else: 
#                 # this may be true if there is one same config used for all receptors
#                 print configs.filename + " is one file ending with something else (e.g. .txt) \n"
#                 # for each receptor insert a tuple into the mdrr with that config file 
#                 for one_receptor in os.listdir(receptors_temp_dir):
#                     print "inserting into mdrr... \n"
#                     to_return["data"]["inserted_results"].append(
#                                             {"result_id": str(
#                                             mdrr_inserter.insert_result(receptor=one_receptor, receptor_path_or_content="path", 
#                                                 ligand=ligands.file, ligand_path_or_content="content",
#                                                 result_path=results_temp_dir + os.path.splitext(one_receptor)[0] + "_" + os.path.splitext(ligands.filename)[0] + "_out.pdbqt",
#                                                 config = configs.file, config_path_or_content="content")
#                                             ), 
#                                              "receptor": one_receptor})
#         # if a zip with ligands has been sent, unzip it        
#         elif ligands.filename.endswith(zip_ext):
#             # there are many receptor, many ligands, many config, and many results
#             print ligands.filename + " is a zip file ending with " + zip_ext + " \n"
#             # unzip the ligands
#             with zipfile.ZipFile(ligands.file) as ligands_zip:
#                     ligands_zip.extractall(ligands_temp_dir)
#             # if a zip with a config file has been sent, unzip it (it should be 1-to-1 mapping with receptors)        
#             if configs.filename.endswith(zip_ext):
#                 print configs.filename + " is a zip file ending with " + zip_ext + " \n" 
#                 with zipfile.ZipFile(configs.file) as configs_zip:
#                     configs_zip.extractall(configs_temp_dir)
#                     
#                 # probably there will be a different number of ligands and different number of receptors
#                 # so, a tuple needs to be inserted for each ligand-receptor pair, but there is one config for each receptor
#                 # that is why in the following code the index of the list of configs moves each time a new receptor is processed
#                 # mapped_config is the config index. old_receptor is there to help find out when a new  receptor appears
#                 mapped_config = 0
#                 
#                 
#                 all_configs = os.listdir(configs_temp_dir)
#                 print "This is what I get for the folder: "
#                 print configs_temp_dir
#                 print ">>>"
#                 print all_configs
#                 print "<<<"
#                 # get only the vina result file not the vina log file
#                 all_results = os.listdir(results_temp_dir)
#                 no_logs_results = [ fname for fname in all_results if fname.endswith('_out.pdbqt')]
#                 split_first_result = no_logs_results[0].split("_")
#                 old_receptor = split_first_result[0] + vina_input_ext
#                 
#                 for one_result in no_logs_results:
#                     # split the name of the result file into ligand name and receptor name
#                     split_result = one_result.split("_")              
#                     one_receptor = split_result[0] + vina_input_ext
#                     one_ligand = split_result[1] + vina_input_ext
#                     
#                     print "inserting into mdrr... \n"
#                     to_return["data"]["inserted_results"].append(
#                                             {"result_id": str(
#                                             mdrr_inserter.insert_result(receptor=receptors_temp_dir + os.sep + one_receptor, receptor_path_or_content="path", 
#                                                 ligand=ligands_temp_dir + os.sep + one_ligand, ligand_path_or_content="path",
#                                                 result_path=results_temp_dir + os.sep + one_result, 
#                                                 config = configs_temp_dir + os.sep + all_configs[mapped_config], config_path_or_content="path")
#                                             ), 
#                                              "receptor": one_receptor})
#                     
#                     if one_receptor != old_receptor:
#                         old_receptor = one_receptor
#                         mapped_config = mapped_config + 1
#             # if 1 config file is sent [i.e. configs.filename.endswith(".txt") or ".conf" or "cnf"]
#             else: 
#                 # this may happen if there is one same config used for all receptors
#                 print configs.filename + " is one file ending with something else (e.g. .txt) \n"
#                 
#                 # get only the vina result file not the vina log file
#                 all_results = os.listdir(results_temp_dir)
#                 no_logs_results = [ fname for fname in all_results if fname.endswith('_out.pdbqt')]
#                 
#                 # for each result, insert the correct tuple by processing the name of the result file
#                 for one_result in no_logs_results:
#                     # split the name of the result file into ligand name and receptor name
#                     split_result = one_result.split("_")                    
#                     one_receptor = split_result[0] + vina_input_ext
#                     one_ligand = split_result[1] + vina_input_ext
#                     print "inserting into mdrr... \n"
#                     to_return["data"]["inserted_results"].append(
#                                             {"result_id": str(
#                                             mdrr_inserter.insert_result(receptor=receptors_temp_dir + os.sep + one_receptor, receptor_path_or_content="path", 
#                                                 ligand=ligands_temp_dir + os.sep + one_ligand, ligand_path_or_content="path",
#                                                 result_path=results_temp_dir + os.sep + one_result,
#                                                 config = configs.file, config_path_or_content="content")
#                                             ), 
#                                              "receptor": one_receptor})
#     
#     # insert into analysis type = inserting_results, inserted_results    
#     mdrr_inserter.insert_analysis_inserting(group_id=group_id,
#                                             inserted_results = to_return["data"]["inserted_results"])
#     
#     # return json with status:success
#     to_return["status"] = "success"
#     to_return["group_id"] = group_id
#     print "Goodbye from 'insert'"
#     return to_return
# 
# @bottle.post('/suggestNext')
# def suggestNext():
#     """ 
#     1) Find similar receptors in the MDRR
#     2) Assess docking results of docking runs in the MDRR that have used these receptors
#     3) The results of 1) and 2) are analysed by the DM
#     4) Insert into analysis and call the DM
#     
#     POST Parameters:
#     receptors -- receptor(s) (.zip for > 1 ligand, .pdqbt for 1 ligand)
#     thresholdDeepAlign -- user input threshold, value of DeepScore e.g. 750.0
#     thresholdVinaDocking -- user input threshold, value of Vina affinity e.g. -6.0
#         
#     Returns:
#     JSON response containing a recommended protein-ligand pair to dock next      
#     """
#     print "Welcome to 'suggestNext'"
#     # the results from the assessment of the docking results will be stored here
#     assessed_results = None
#     # the results from the assessment of the AT deepalign will be stored here 
#     assessed_similar_receptors = None
# 
#     to_return = {}
#     to_return["data"] = {}
#     # read the POST parameters. If any are missing return with a status 'fail' explaining the required parameter  
#     receptors = bottle.request.files.get("receptors")
#     if not receptors:
#         to_return["status"] = "fail"
#         to_return["data"]["receptors"] = "Receptors required as a POST parameter named 'receptors'!"
#         return to_return
#     
#     thresholdDeepAlign = bottle.request.params.get("thresholdDeepAlign")
#     thresholdVinaDocking = bottle.request.params.get("thresholdVinaDocking")
#     group_id = bottle.request.params.get("group_id")
#     
#     # declare names of temporary directories where zip files will be unzipped
#     temp_dir = "." + os.sep + "temp"
#     
#     #make a temp directory
#     if not os.path.exists(temp_dir):
#         os.mkdir(temp_dir)
#         print temp_dir + " created \n"
#     zip_ext = ".zip"
#     receptors_temp_dir = temp_dir + os.sep + "receptors"
#     # if a zip with receptors has been sent, unzip it
#     if receptors.filename.endswith(zip_ext):
#         print receptors.filename + " is a zip file ending with " + zip_ext + " \n"
#         with zipfile.ZipFile(receptors.file) as receptors_zip:
#             receptors_zip.extractall(receptors_temp_dir)
#     
#     
#     # connect to the MongoDB - this could go in another method
#     client = pymongo.MongoClient()      
#     db = client.mdrr_1
#     
#     # 1) calling the AT DeepAlign and AssessDeepAlign
#         
#     # get all receptors from MDRR
#     mdrr_selector = mdrr.selector.Selector(db)
#     all_receptors = mdrr_selector.select_all_receptors()
#     
#     # parse to pdb files and put each into a zip file
#     z_all_receptors_name = "all_receptors.zip"
#     z_all_receptors = zipfile.ZipFile(z_all_receptors_name, "w")
#     parser = mdrr.receptor_parser.Plain() 
#     for mdrr_receptor in all_receptors:
#         # get the structure of the receptor in 'pdb_receptor'
#         pdb_receptor = parser.dict_to_string(mdrr_receptor["structure"])
#         # get the structure_id and make it part of the name, separated by '_' with the receptor name
#         z_all_receptors.writestr(str(mdrr_receptor["structure_id"]) + "_" + mdrr_receptor["name"], pdb_receptor)    
#     z_all_receptors.close()
#     
#     # for each target receptor (receptor that has been used in the insert), usually just 1
#     for receptor_file in os.listdir(receptors_temp_dir):
#         #call the at-deepalign rest api to compare and assess
#         try:
#             target_receptor = receptors_temp_dir + os.sep + receptor_file
#             # get the structure_id of the target receptor from its path
#             target_receptor_structure_id = parser.path_to_structure_id(target_receptor)
#             
#             # the post parameters: target_receptor='receptor' (file), receptors='all receptors'(file), threshold='DeepScore value' (default: 500)
#             pf = [('target_receptor', (pycurl.FORM_FILE, target_receptor)),
#                   ('target_structure_id', target_receptor_structure_id),
#                   ('receptors', (pycurl.FORM_FILE, z_all_receptors_name)), 
#                   ('threshold', thresholdDeepAlign)
#                  ]
#             # create new pycurl object
#             c = pycurl.Curl()
#             # set the parameters: URL, HTTPPOST parameters
#             c.setopt(c.URL, "http://localhost:8091/compareAndAssess")
#             c.setopt(c.HTTPPOST, pf)
#             # ignore SSL error (equivalent to curl --insecure or curl -k)
#             # c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#             # uncomment the next line for verbose (curl -v)  
#             c.setopt(c.VERBOSE, True)
#             #this StringIO is needed to store the response in
#             response_buffer = StringIO()
#             # set the option to write the response into the response_buffer
#             c.setopt(c.WRITEDATA, response_buffer)
#             # send the request
#             c.perform()            
#             # get the HTTP response code, e.g. 200.
#             response_code = c.getinfo(c.RESPONSE_CODE) 
#             if response_code != 200:
#                 print('Response Code: %d' % response_code)
#             c.close()           
#             # this needs to be passed to the DM
#             # {'data': {"similar": [ {"structure_id": aaa, "DeepAlign_result": bbb}, {}, {}, ... ]}, "config": c, "threshold": t }
#             assessed_similar_receptors = json.loads(response_buffer.getvalue()) 
#             
#         except pycurl.error, e:
#             # print the error code and message and raise the error again
#             print "Error code: ", e[0]
#             print "Error message: ", e[1]  
#             raise e
# 
#         # insert into analysis type = structural_alignment, tool = deepalign, config=xxx, target_receptor=xxxx, assessed_similar_receptors["data"]["similar"]
#         mdrr_inserter = mdrr.inserter.Inserter(db)
#         
#         # insert one document per similar receptor in the analisis collection
#         # return a list of the inserted_ids 
#         inserted_similar_receptors = mdrr_inserter.insert_analysis_at(group_id=group_id,at_type="Receptor Structural Alignment",
#                                                                tool="DeepAlign", target=target_receptor_structure_id,
#                                                                results_list=assessed_similar_receptors["data"]["similar"])
#     
#     
#         # insert into analysis type = assess_structural_alignment, threshold, analysis_id=xxx    
#         mdrr_inserter.insert_analysis_at_assessment(group_id=group_id, at_type="Receptor Strucutral Alignment Assessment",
#                                                       assessment_type="User Input Threshold", threshold=thresholdDeepAlign,
#                                                       assessed=inserted_similar_receptors)
# #         
# #         inserted_similar_list = mdrr_inserter.insert_analysis_structural_alignment(group_id=group_id,
# #                                                                                    target_receptor=target_receptor_structure_id,
# #                                                                                    similar_list=assessed_similar_receptors["data"]["similar"])
# #         
# #         
# #         # insert into analysis type = assess_structural_alignment, threshold, analysis_id=xxx    
# #         mdrr_inserter.insert_analysis_structural_alignment_assessment(group_id=group_id,
# #                                                                       assessed_as_similar=inserted_similar_list,
# #                                                                       threshold=thresholdDeepAlign)
#         
#         # 2) calling the AT AssessDockingResults
#         # unless it there are 0 similar receptors        
#         if ( len( assessed_similar_receptors["data"]["similar"] ) > 0):
# #             to_return["data"]["compared"] = {}
# #             to_return["data"]["compared"] = assessed_similar_receptors["data"]
#             
#             # this can be cached, the cache can have id of result and threshold...
#             
#             # get all docking results from MDRR where the id value in the 'receptor' field equals the structure_id of the assessed similar receptors
#             # put all structure_id-s of similar receptors into the array structure_ids_similar
#             structure_ids_similar = []
#             for similar in assessed_similar_receptors["data"]["similar"]:
#                 structure_ids_similar.append( similar["structure_id"] )
#             # get all results from the datbase
#             mdrr_selector = mdrr.selector.Selector(db)
#             docking_results = mdrr_selector.select_results_where_receptor_structure_ids(structure_ids_similar)
# #             docking_results = mdrr_selector.select_results_where_receptor_file(target_receptor)
#             
#             # call the assessor
#             # save the 'all docking results' json as a file on disk
#             all_results_filename = "all_docking_result.json"    
#             with open(all_results_filename, "w") as all_results:
#                 all_results.write(bson.json_util.dumps(docking_results)) 
#             
#             #call the assess-docking rest api to compare and assess
#             try:
#                 
#                 # the post parameters: docking_results='results' (file or zip with many files), [threshold]='affinity value' (default -5.0)
#                 pf = [('docking_results', (pycurl.FORM_FILE, all_results_filename)),
#                       ('threshold', thresholdVinaDocking) 
#                       ]
#                 # create new pycurl object
#                 c = pycurl.Curl()
#                 # set the parameters: URL, HTTPPOST parameters
#                 c.setopt(c.URL, "http://localhost:8092/assess")
#                 c.setopt(c.HTTPPOST, pf)
#                 # ignore SSL error (equivalent to curl --insecure or curl -k)
#                 # c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#                 # uncomment the next line for verbose (curl -v)  
#                 c.setopt(c.VERBOSE, False)
#                 #this StringIO is needed to store the response in
#                 response_buffer = StringIO()
#                 
#                 
#                 # set the option to write the response into the response_buffer
#                 c.setopt(c.WRITEDATA, response_buffer)
#                 #  with open("assesssed_results", 'w') as f:
#                 #     c.setopt(c.WRITEFUNCTION, f.write)
#                 #     c.perform()
#                 # send the request
#                 c.perform()            
#                 # get the HTTP response code, e.g. 200.
#                 response_code = c.getinfo(c.RESPONSE_CODE) 
#                 if response_code != 200:
#                     print('Response Code: %d' % response_code)
#                 c.close()
#                 # this needs to be passed to the DM
#                 assessed_results = json.loads(response_buffer.getvalue())
#             except pycurl.error, e:
#                 # print the error code and message and raise the error again
#                 print "Error code: ", e[0]
#                 print "Error message: ", e[1]  
#                 raise e
#             
#             # insert into analysis type = assess_docking, threshold, assessed_results["data]["good"]: [{model_number, score}, {}...]
#     
#             # insert into analysis type = assess_structural_alignment, threshold, analysis_id=xxx    
#             mdrr_inserter.insert_analysis_at_assessment(group_id=group_id, at_type="AutoDock Vina Docking Result Assessment",
#                                                           assessment_type="User Input Threshold", threshold=thresholdVinaDocking,
#                                                           assessed=assessed_results["data"]["good"])
#             
# #             mdrr_inserter.insert_analysis_docking_assessment(group_id=group_id,
# #                                                              threshold=thresholdVinaDocking,
# #                                                              good_dockings=assessed_results["data"]["good"])
#                    
#             # 3) call the DM with correct parameters - this is a simple decision maker
#             decision_maker = dm.decider.SimpleDecide(assessed_results, assessed_similar_receptors)
#             # append the decision of each target receptor (usually this is only 1 receptor if it is a virtual screening) 
#             to_return["data"]["decisions"] = decision_maker.run()
#     
#         # if there were 0 similar receptors return a message
#         else:
#             to_return["data"]["decisions"] = "No similar receptors, can't suggest the next ligand-receptor pair"
#         to_return["status"] = "success"   
#        
#     # 4) the DM can insert the decision into the MongoDB database - insert into analysis 
#     mdrr_inserter.insert_analysis_decision(group_id=group_id, 
#                                            decision=to_return["data"]["decisions"])
#     
#     # add the group_id value to the response, so that you can see all the 'analysis' documents related to this run
#     to_return["group_id"] = group_id
#     
#     # delete temporary folders where zip files were extracted
#     if os.path.exists(receptors_temp_dir): 
#         for receptor_file in os.listdir(receptors_temp_dir):
#             os.remove(receptors_temp_dir + os.sep + receptor_file)
#         os.removedirs(receptors_temp_dir)
#     
#     print "Goodbye from 'suggestNext'"
#     #return the json with data about all the steps and the final decision
#     return to_return #this one asks bottle to call json.dumps() 
# 
# @bottle.post('/verify')
# def verify():
#     """ Scenario 4
#     1) Find similar receptors to target receptor
#     2) Take all results with these similar receptors, and filter out only results that have similar ligands too
#     3) Take all results with these similar receptors, and filter out only results that have similar configs too
#     4) Decide if there is a similar docking and present to user
#     
#     POST Parameters:
#     receptor -- the  current receptor used in the Molecular Docking
#     ligand -- the current ligand used in the Molecular Docking
#     config -- the current config used in the Molecular Docking
#     thresholdDeepAlign -- user input threshold, value of DeepScore e.g. 750.0
#     thresholdLigsift -- user input threshold, value of ligsift (ShapeSim)
#     threhsoldConfig -- user input threshold, custom value distance of difference between cubes
#         
#     Returns:
#     JSON response containing a recommended protein-ligand pair to dock next 
#     """
#     print "Welcome to 'verify'"
#     # the results from the assessment of the AT deepalign will be stored here 
#     assessed_similar_receptors = None
# 
#     to_return = {}
#     to_return["data"] = {}
#     to_return["data"]["decisions"] = []
#     # read the POST parameters. If any are missing return with a status 'fail' explaining the required parameter  
#     receptors = bottle.request.files.get("receptor")
#     if not receptors:
#         to_return["status"] = "fail"
#         to_return["data"]["receptors"] = "Receptors required as a POST parameter named 'receptors'!"
#         return to_return
#     
#     ligands = bottle.request.files.get("ligand")
#     if not ligands:
#         to_return["status"] = "fail"
#         to_return["data"]["ligands"] = "Ligands required as a POST parameter named 'ligands'!"
#         return to_return
#     
#     configs = bottle.request.files.get("config")
#     if not configs:
#         to_return["status"] = "fail"
#         to_return["data"]["configs"] = "Ligands required as a POST parameter named 'configs'!"
#         return to_return
#     
#     thresholdDeepAlign = bottle.request.params.get("thresholdDeepAlign")
#     thresholdLigsift = bottle.request.params.get("thresholdLigsift")
#     thresholdConfig = bottle.request.params.get("thresholdConfig")
#     group_id = bottle.request.params.get("group_id")
#     
#     if not group_id:
#         group_id = "test-group-id"
#     
#     # declare names of temporary directories where zip files will be unzipped
#     temp_dir = "." + os.sep + "temp"
#     
#     #make a temp directory
#     if not os.path.exists(temp_dir):
#         os.mkdir(temp_dir)
#         print temp_dir + " created \n"
#         
#     zip_ext = ".zip"
#     
#     receptors_temp_dir = temp_dir + os.sep + "receptors"
#     if not os.path.exists(receptors_temp_dir):
#         os.mkdir(receptors_temp_dir)
#         print receptors_temp_dir + " created \n"
#     # if a zip with receptors has been sent, unzip it
#     if receptors.filename.endswith(zip_ext):
#         print receptors.filename + " is a zip file ending with " + zip_ext + " \n"
#         with zipfile.ZipFile(receptors.file) as receptors_zip:
#             receptors_zip.extractall(receptors_temp_dir)
#     else:
#         if not os.path.exists(receptors_temp_dir + os.sep + receptors.filename):
#             receptors.save(receptors_temp_dir + os.sep + receptors.filename)
#     receptors_file_name = receptors_temp_dir + os.sep + os.listdir(receptors_temp_dir)[0] 
#     
#     ligands_temp_dir = temp_dir + os.sep + "ligands"
#     if not os.path.exists(ligands_temp_dir):
#         os.mkdir(ligands_temp_dir)
#         print ligands_temp_dir + " created \n"
#     # if a zip with ligands has been sent, unzip it
#     if ligands.filename.endswith(zip_ext):
#         print ligands.filename + " is a zip file ending with " + zip_ext + " \n"
#         with zipfile.ZipFile(ligands.file) as ligands_zip:
#             ligands_zip.extractall(ligands_temp_dir)
#     else:
#         if not os.path.exists(ligands_temp_dir + os.sep + ligands.filename):
#             ligands.save(ligands_temp_dir + os.sep + ligands.filename)
#         
#     ligands_file_name = ligands_temp_dir + os.sep + os.listdir(ligands_temp_dir)[0]  
#         
#     configs_temp_dir = temp_dir + os.sep + "target_config"
#     if not os.path.exists(configs_temp_dir):
#         os.mkdir(configs_temp_dir)
#         print configs_temp_dir + " created \n"
#     # if a zip with configs has been sent, unzip it
#     if configs.filename.endswith(zip_ext):
#         print configs.filename + " is a zip file ending with " + zip_ext + " \n"
#         with zipfile.ZipFile(configs.file) as configs_zip:
#             configs_zip.extractall(configs_temp_dir)
#     else:
#         if not os.path.exists(configs_temp_dir + os.sep + configs.filename):
#             configs.save(configs_temp_dir + os.sep + configs.filename)
#     
#     config_file_name = configs_temp_dir + os.sep + os.listdir(configs_temp_dir)[0]   
#     config_file_content = open(config_file_name,  "r").read()
#     
#     all_configs_temp_dir = temp_dir + os.sep + "all_configs"
#     if not os.path.exists(all_configs_temp_dir):
#         os.mkdir(all_configs_temp_dir)
#         print all_configs_temp_dir + " created \n"
# 
#     # connect to the MongoDB - this could go in another method
#     client = pymongo.MongoClient()      
#     db = client.mdrr_1
#     
#     # 1) calling the AT DeepAlign and AssessDeepAlign
#         
#     # get all receptors from MDRR
#     mdrr_selector = mdrr.selector.Selector(db)
#     all_receptors = mdrr_selector.select_all_receptors()
#     
#     # parse to pdb files and put each into a zip file
#     z_all_receptors_name = "all_receptors.zip"
#     z_all_receptors = zipfile.ZipFile(z_all_receptors_name, "w")
#     receptor_parser = mdrr.receptor_parser.Plain()
#     for mdrr_receptor in all_receptors:
#         # get the structure of the receptor in 'pdb_receptor'
#         pdb_receptor = receptor_parser.dict_to_string(mdrr_receptor["structure"])
#         # get the structure_id and make it part of the name, separated by '_' with the receptor name
#         z_all_receptors.writestr(str(mdrr_receptor["structure_id"]) + "_" + mdrr_receptor["name"], pdb_receptor)    
#     z_all_receptors.close()
#     
# 
#     #call the at-deepalign rest api to compare and assess
#     try:
#         target_receptor = receptors_file_name
#         # get the structure_id of the target receptor from its path
#         target_receptor_structure_id = receptor_parser.path_to_structure_id(target_receptor)
#         
#         # the post parameters: target_receptor='receptor' (file), receptors='all receptors'(file), threshold='DeepScore value' (default: 500)
#         pf = [('target_receptor', (pycurl.FORM_FILE, target_receptor)),
#               ('target_structure_id', target_receptor_structure_id),
#               ('receptors', (pycurl.FORM_FILE, z_all_receptors_name)), 
#               ('threshold', thresholdDeepAlign)
#              ]
#         # create new pycurl object
#         c = pycurl.Curl()
#         # set the parameters: URL, HTTPPOST parameters
#         c.setopt(c.URL, "http://localhost:8091/compareAndAssess")
#         c.setopt(c.HTTPPOST, pf)
#         # ignore SSL error (equivalent to curl --insecure or curl -k)
#         # c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#         # uncomment the next line for verbose (curl -v)  
#         c.setopt(c.VERBOSE, True)
#         #this StringIO is needed to store the response in
#         response_buffer = StringIO()
#         # set the option to write the response into the response_buffer
#         c.setopt(c.WRITEDATA, response_buffer)
#         # send the request
#         c.perform()            
#         # get the HTTP response code, e.g. 200.
#         response_code = c.getinfo(c.RESPONSE_CODE) 
#         if response_code != 200:
#             print('Response Code: %d' % response_code)
#         c.close()           
#         # this needs to be passed to the DM
#         # {'data': {"similar": [ {"structure_id": aaa, "DeepAlign_result": bbb}, {}, {}, ... ]}, "config": c, "threshold": t }
#         assessed_similar_receptors = json.loads(response_buffer.getvalue()) 
#         
#     except pycurl.error, e:
#         # print the error code and message and raise the error again
#         print "Error code: ", e[0]
#         print "Error message: ", e[1]  
#         raise e
# 
#     # insert into analysis type = structural_alignment, tool = deepalign, config=xxx, target_receptor=xxxx, assessed_similar_receptors["data"]["similar"]
#     mdrr_inserter = mdrr.inserter.Inserter(db)
#     
#     # insert one document per similar receptor in the analisis collection
#     # return a list of the inserted_ids 
#     inserted_similar_receptors = mdrr_inserter.insert_analysis_at(group_id=group_id,at_type="Receptor Structural Alignment",
#                                                                tool="DeepAlign", target=target_receptor_structure_id,
#                                                                results_list=assessed_similar_receptors["data"]["similar"])
#     
#     
#     # insert into analysis type = assess_structural_alignment, threshold, analysis_id=xxx    
#     mdrr_inserter.insert_analysis_at_assessment(group_id=group_id, at_type="Receptor Strucutral Alignment Assessment",
#                                                   assessment_type="User Input Threshold", threshold=thresholdDeepAlign,
#                                                   assessed=inserted_similar_receptors)
#     
#     
#     # ligands can stay .pdbqt, Ligsift will convert them to mol2 with OpenBabel C++ or use them as they are
#     
#     similar_ligands = {}
#     similar_configs = {}
#     # loop through all the similar receptors
#     for similar in assessed_similar_receptors["data"]["similar"]: 
#         
#         similar_receptor_id = similar["structure_id"]
#         # get all configs for 'similar'
#         # call comapre_configs(all_configs.zip, current_config)
#         # if > 0 configs are similar, add
#         
#         
#         # 2) calling the AT Ligsift for each similar receptor + conf
#         # get results from the datbase where this similar receptor is the receptor
#         # the result of this call is a dictionary 
#         # {"ligand_structure_id": {"strucutre":"lorem impsum structure", "configs": ["conf1", "conf2"]}}
#         
#         # connect to the MongoDB - this could go in another method            
#         mdrr_selector = mdrr.selector.Selector(db)
#         ligand_configs_of_similar = mdrr_selector.select_ligand_confs_where_result_has_receptor( similar["structure_id"] )
#         
#         ligand_parser = mdrr.ligand_parser.Plain()        
#         # parse to pdb files and put each into a zip file
#         z_all_ligands_name = ligands_temp_dir + os.sep + "all_ligands.zip"
#         z_all_ligands = zipfile.ZipFile(z_all_ligands_name, "w")
#         ligand_parser = mdrr.ligand_parser.Plain()
#         for ligand_structure_id in ligand_configs_of_similar:
#             # get the structure of the ligand in 'pdb_ligand'
#             pdb_ligand = ligand_parser.dict_to_string(ligand_configs_of_similar[ligand_structure_id]["structure"])
#             # get the structure_id and make it part of the name, separated by '_' with the ligand name
#             z_all_ligands.writestr(str(ligand_structure_id) + "_" + ligand_configs_of_similar[ligand_structure_id]["name"] + ".pdbqt", pdb_ligand)    
#         z_all_ligands.close()
#         
#         # at_ligsift_and_assess( z_current_ligands_name, ligands_of_similar_mol2_filename , thresholdLigsift)
#         # this should return an updated dictionary with only the similar ligands, plus some extra information regarding this similarity
#         # ligsift_similar_dict = ...
#         target_ligand_struct_id = ligand_parser.path_to_structure_id(ligands_file_name)
#         try:
#             
#             # the post parameters: target_receptor='receptor' (file), receptors='all receptors'(file), threshold='DeepScore value' (default: 500)
#             pf = [('ligands', (pycurl.FORM_FILE, z_all_ligands_name)),
#                   ('target_ligand', (pycurl.FORM_FILE, ligands_file_name)), 
#                   ('target_struct_id', target_ligand_struct_id),
#                   ('threshold', thresholdLigsift)
#                  ]
#             # create new pycurl object
#             c = pycurl.Curl()
#             # set the parameters: URL, HTTPPOST parameters - call Ligsift
#             c.setopt(c.URL, "http://localhost:8093/compareAndAssessLigands")
#             c.setopt(c.HTTPPOST, pf)
#             # ignore SSL error (equivalent to curl --insecure or curl -k)
#             # c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#             # uncomment the next line for verbose (curl -v)  
#             c.setopt(c.VERBOSE, True)
#             #this StringIO is needed to store the response in
#             response_buffer = StringIO()
#             # set the option to write the response into the response_buffer
#             c.setopt(c.WRITEDATA, response_buffer)
#             # send the request
#             c.perform()            
#             # get the HTTP response code, e.g. 200.
#             response_code = c.getinfo(c.RESPONSE_CODE) 
#             if response_code != 200:
#                 print('Response Code: %d' % response_code)
#             c.close()           
#             # this needs to be passed to the DM
#             # {'data': {"similar": [ {"structure_id": aaa, "Ligsift_result": bbb}, {}, {}, ... ]}, "config": c, "threshold": t }
#             ligsift_similar_dict = json.loads(response_buffer.getvalue()) 
#             
#         except pycurl.error, e:
#             # print the error code and message and raise the error again
#             print "Error code: ", e[0]
#             print "Error message: ", e[1]  
#             raise e
#         
#         
#         
#         inserted_similar_ligands = mdrr_inserter.insert_analysis_at(group_id=group_id, at_type="Ligand Similarity (Structural Alignment)",
#                                                                tool="Ligsift", target=target_ligand_struct_id,
#                                                                results_list=ligsift_similar_dict["data"]["similar"])
#     
#     
#         # insert into analysis type = assess_structural_alignment, threshold, analysis_id=xxx    
#         mdrr_inserter.insert_analysis_at_assessment(group_id=group_id, at_type="Ligand Similarity (Structural Alignment) Assessment",
#                                                       assessment_type="User Input Threshold", threshold=thresholdLigsift,
#                                                       assessed=inserted_similar_ligands)
#         
#         
#         # 3) calling the AT compare_configs (current_config, ligsift_similar_dict)
#         # this would send some extra information that would not be used by the compare config AT
#         
#         sifted_ligand_configs = {}
#         for similar_ligand in ligsift_similar_dict["data"]["similar"]:
#             lig_struct_id = similar_ligand["similar_ligand_structure_id"]
#             sifted_ligand_configs[ lig_struct_id ] = ligand_configs_of_similar[ lig_struct_id ] 
#         
#         
#         
#         similar_ligands[ similar_receptor_id ] = ligsift_similar_dict 
#         
#             
#             
#         similar_configs [similar_receptor_id] = {}
#         
#         for ligand_id in sifted_ligand_configs:
#             try:
#                 z_all_configs_name = all_configs_temp_dir + os.sep + "configs_of_similar_ligand_" + ligand_id + ".zip"
#                 z_all_configs = zipfile.ZipFile(z_all_configs_name, "w")
#                 config_number = 1
#                 for (result_id, config_for_this_ligand) in sifted_ligand_configs [ ligand_id ]["result_id_configs"].iteritems():
#                     z_all_configs.writestr( str( result_id ) + "_config_" + str(config_number), config_for_this_ligand)
#                     config_number += 1
#                     
#                 z_all_configs.close()
#                 
#                 # the post parameters: target_receptor='receptor' (file), receptors='all receptors'(file), threshold='DeepScore value' (default: 500)
#                 pf = [('configs', (pycurl.FORM_FILE, z_all_configs_name)),
#                       ('target_config', (pycurl.FORM_FILE, config_file_name)), 
#                       ('threshold', thresholdConfig)
#                      ]
#                 # create new pycurl object
#                 c = pycurl.Curl()
#                 # set the parameters: URL, HTTPPOST parameters - call Ligsift
#                 c.setopt(c.URL, "http://localhost:8094/compareConfigs")
#                 c.setopt(c.HTTPPOST, pf)
#                 # ignore SSL error (equivalent to curl --insecure or curl -k)
#                 # c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#                 # uncomment the next line for verbose (curl -v)  
#                 c.setopt(c.VERBOSE, True)
#                 #this StringIO is needed to store the response in
#                 response_buffer = StringIO()
#                 # set the option to write the response into the response_buffer
#                 c.setopt(c.WRITEDATA, response_buffer)
#                 # send the request
#                 c.perform()            
#                 # get the HTTP response code, e.g. 200.
#                 response_code = c.getinfo(c.RESPONSE_CODE) 
#                 if response_code != 200:
#                     print('Response Code: %d' % response_code)
#                 c.close()           
#                 # this needs to be passed to the DM
#                 # {'data': {"similar": [ {"structure_id": aaa, "Ligsift_result": bbb}, {}, {}, ... ]}, "config": c, "threshold": t }
#                 config_similar_dict = json.loads(response_buffer.getvalue()) 
#                 
#             except pycurl.error, e:
#                 # print the error code and message and raise the error again
#                 print "Error code: ", e[0]
#                 print "Error message: ", e[1]  
#                 raise e
#             
#             
#             similar_configs[ similar_receptor_id ] [ligand_id] = config_similar_dict
#             
#             
#             inserted_similar_configs = mdrr_inserter.insert_analysis_at(group_id=group_id, at_type="AutoDock Vina Config Comparison",
#                                                                tool="CompareConfig", target=config_file_content,
#                                                                results_list=config_similar_dict["data"]["similar"])
#     
#     
#             # insert into analysis type = assess_structural_alignment, threshold, analysis_id=xxx    
#             mdrr_inserter.insert_analysis_at_assessment(group_id=group_id, at_type="AutoDock Vina Config Comparison Assessment",
#                                                           assessment_type="User Input Threshold", threshold=thresholdConfig,
#                                                           assessed=inserted_similar_configs)
#             
#                 
#     # 4) the DM sorts the similar_inputs
#     decision_maker = dm.decider.SimilarReceptorsLigandsConfigs(assessed_similar_receptors, similar_ligands, similar_configs)
#     # append the decision of each targer receptor (usually this is only 1 receptor if it is a virtual screening) 
#     to_return["data"]["decisions"].append( decision_maker.decide() )
#     
#     # Insert decision into Analysis
#     mdrr_inserter.insert_analysis_decision(group_id=group_id, 
#                                            decision_type="Similar receptor/ligand/config, sorted by receptor (DeepAlign DeepScore), then ligand (Ligsift ShapeSim), then config (CompareConfig averageDistance)",
#                                            decision=to_return["data"]["decisions"])
# 
# 
# 
#     # Delete the Temp folders
#     # delete temporary folders where zip files were extracted
#     if os.path.exists(configs_temp_dir):
#         for config_file in os.listdir(configs_temp_dir):
#             os.remove(configs_temp_dir + os.sep + config_file)
#         os.removedirs(configs_temp_dir)
#      
#     if os.path.exists(receptors_temp_dir): 
#         for receptor_file in os.listdir(receptors_temp_dir):
#             os.remove(receptors_temp_dir + os.sep + receptor_file)
#         os.removedirs(receptors_temp_dir)
#      
#     if os.path.exists(ligands_temp_dir): 
#         for ligand_file in os.listdir(ligands_temp_dir):
#             os.remove(ligands_temp_dir + os.sep + ligand_file)
#         os.removedirs(ligands_temp_dir)
#     
#     print "Goodbye from 'verify'"
#     return to_return
# 
# 
# @bottle.post('/consult')
# def consult():
#     """ Scenario 2
#     1) Find good docking result out of the currently attempted virtual screening
#     2) Filter the ligands of good docking results, based on the PubChem property selected by the user
#     
#     (you'll need to call consult when call insertMany() )
#     
#     POST Parameters:
#     group_id --
#     inserted -- "True" if the results have been inserted already, "False" otherwise
#     results -- the current virtual screening results (string if 'inserted', file to open otherwise)
#     query -- pubChemProperty + pubChemSign + pubChemValue
#     thresholdVinaDocking -- the threshold for the good docking assessment
#     [ligands] -- if 'inserted' is False, then you must upload the ligands in a zip file
#         
#     Returns:
#     JSON response containing a set of recommended ligands to try in the wet-lab 
#     """
#     print "Welcome to 'consult'"
#     to_return = {}
#     to_return["data"] = {}
#     to_return["data"]["decisions"] = []
#     # read the POST parameters. If any are missing return with a status 'fail' explaining the required parameter  
#     
#     query = bottle.request.params.get("query")
#     if not query:
#         to_return["status"] = "fail"
#         to_return["data"]["query"] = "Query required as a POST parameter named 'query'!"
#         return to_return
#     
#     thresholdVinaDocking = bottle.request.params.get("thresholdVinaDocking")
#         
#     group_id = bottle.request.params.get("group_id")
#     if not group_id:
#         group_id = "test-group-id"
#     
#     # declare names of temporary directories where zip files will be unzipped
#     temp_dir = "." + os.sep + "temp"
#     
#     #make a temp directory
#     if not os.path.exists(temp_dir):
#         os.mkdir(temp_dir)
#         print temp_dir + " created \n"
#     
#     # create results temp dir
#     results_temp_dir = temp_dir + os.sep + "results"
#     if not os.path.exists(results_temp_dir):
#         os.mkdir(results_temp_dir)
#         print results_temp_dir + " created \n"
#         
#     zip_ext = ".zip"    
#     
#     # connect to the MongoDB - this could go in another method
#     client = pymongo.MongoClient()      
#     db = client.mdrr_1
#     
#     mdrr_selector = mdrr.selector.Selector(db)
#     mdrr_inserter = mdrr.inserter.Inserter(db)  
#       
#     ligands_temp_dir = temp_dir + os.sep + "ligands"
#     
#     # process results based on the value of 'inserted'
#     inserted_already = bottle.request.params.get("inserted")    
#     
#     if inserted_already != "True": # if results weren't inserted already
#         results = bottle.request.files.get("results")
#         if not results:
#             to_return["status"] = "fail"
#             to_return["data"]["results"] = "Results required as a POST parameter named 'results'!"
#             return to_return
#         
#         # if a zip with results has been sent, unzip it
#         if results.filename.endswith(zip_ext):
#             print results.filename + " is a zip file ending with " + zip_ext + " \n"
#             with zipfile.ZipFile(results.file) as results_zip:
#                 results_zip.extractall(results_temp_dir)
#         
#         # get the ligands zip from POST
#         ligands = bottle.request.files.get("ligands")
#         if not ligands:
#             to_return["status"] = "fail"
#             to_return["data"]["ligands"] = "Ligands required as a POST parameter named 'ligands'!"
#             return to_return
#         # extract the ligands.zip
#         
#         if not os.path.exists(ligands_temp_dir):
#             os.mkdir(ligands_temp_dir)
#             print ligands_temp_dir + " created \n"
#         # if a zip with ligands has been sent, unzip it
#         if ligands.filename.endswith(zip_ext):
#             print ligands.filename + " is a zip file ending with " + zip_ext + " \n"
#             with zipfile.ZipFile(ligands.file) as ligands_zip:
#                 ligands_zip.extractall(ligands_temp_dir)
#                 
#         # check if a result file is named <receptor-name>_<ligand-name>_out.pdbqt
#         
#         # make sure the order is correct!
#         # get a list of result paths (the ones that end with .pbdqt as in rec_lig_out.pdbqt)
#         list_of_path_to_results = [results_temp_dir + os.sep + r for r in os.listdir(results_temp_dir) if r.endswith(".pdbqt")]
#         # get a list of ligands paths
#         list_of_path_to_ligands = [ligands_temp_dir + os.sep + l for l in os.listdir(ligands_temp_dir) ]
#         # convert Vina results into Python dictionary as stored in the database, then into the 'grouped' format as expected by AssessDockingResult 
#         docking_results = mdrr_inserter.fake_insert_results_grouped_format(list_of_path_to_results, list_of_path_to_ligands)
#         
#     else: # if the results were inserted already
#         results = bottle.request.params.get("results")
#         if not results:
#             to_return["status"] = "fail"
#             to_return["data"]["results"] = "Results required as a POST parameter named 'results'!"
#             return to_return
#         
#         docking_results = mdrr_selector.select_results_grouped_format( ast.literal_eval(results) )
# 
#     all_results_filename = results_temp_dir + os.sep + "all_docking_result.json"
#     with open(all_results_filename, "w") as all_results:
#         all_results.write(bson.json_util.dumps(docking_results))    
# 
#     # now that the results are in goot format, call AssessDockingResult
#     try:
#         # the post parameters: docking_results='results' (file or zip with many files), [threshold]='affinity value' (default -5.0)
#         pf = [('docking_results', (pycurl.FORM_FILE, all_results_filename)),
#               ('threshold', thresholdVinaDocking) 
#               ]
#         # create new pycurl object
#         c = pycurl.Curl()
#         # set the parameters: URL, HTTPPOST parameters
#         c.setopt(c.URL, "http://localhost:8092/assess")
#         c.setopt(c.HTTPPOST, pf)
#         # ignore SSL error (equivalent to curl --insecure or curl -k)
#         # c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
#         # uncomment the next line for verbose (curl -v)  
#         c.setopt(c.VERBOSE, False)
#         #this StringIO is needed to store the response in
#         response_buffer = StringIO()
#         
#         
#         # set the option to write the response into the response_buffer
#         c.setopt(c.WRITEDATA, response_buffer)
#         #  with open("assesssed_results", 'w') as f:
#         #     c.setopt(c.WRITEFUNCTION, f.write)
#         #     c.perform()
#         # send the request
#         c.perform()            
#         # get the HTTP response code, e.g. 200.
#         response_code = c.getinfo(c.RESPONSE_CODE) 
#         if response_code != 200:
#             print('Response Code: %d' % response_code)
#         c.close()
#         # this needs to be passed to the DM
#         assessed_results = json.loads(response_buffer.getvalue())
#     except pycurl.error, e:
#         # print the error code and message and raise the error again
#         print "Error code: ", e[0]
#         print "Error message: ", e[1]  
#         raise e
#     
#     # insert into Analysis after running the AssessDocking AT
#     mdrr_inserter.insert_analysis_at_assessment(group_id=group_id, at_type="AutoDock Vina Docking Result Assessment",
#                                                           assessment_type="User Input Threshold", threshold=thresholdVinaDocking,
#                                                           assessed=assessed_results["data"]["good"])
#         
#     # select the ligands of all 'good' docking results    
#     ligands_of_good_docking = []
#     for assessed in assessed_results["data"]["good"]:
#         ligands_of_good_docking.append( assessed["ligand_structure_id"] )
#     
#     smiles_ligands = []
#     # if already inserted, then select ligands with these ligand_ids
#     # if not already inserted, then these ligand_ids are paths to the ligand file
#     if inserted_already != "True": # if not inserted already, then you must read the ligands from POST - and assume that the result file will be named <receptor-name>_<ligand-name>_out.pdbqt
#         for path_to_ligand in ligands_of_good_docking:
#             smiles_ligands.append( { "_id": path_to_ligand, "canonical_SMILES": mdrr_inserter.canonical_SMILES_from_pdbqt(path_to_ligand) } )
#             
#     else: # if 'inserted' already, then just look up the ligand_id field in the result documents
#         smiles_ligands = mdrr_selector.select_ligands_canonical_SMILES(ligands_of_good_docking)
#     
#     # call the ADS PubChem for each of these ligands and the value of 'query'
#     # how can you find a ligand in PubChem based on what part of the .pdbqt? SMILES
#     # 1) convert pdbqt to canonical SMILES
#     # get PubChem data based on this canonical SMILES
#     # there is a limit of 5 requests per second to the PubChem REST PUG (one every 200ms)
#     # this means 5 lignads can be filtered per second - for 100 000 ligands, it would take 5.55 hours
#     #call the at-deepalign rest api to compare and assess
#     
#     # ADS receive: SMILES, property_name, sign, property_threshold_value. return: SMILES of ones that pass the condition
#     # https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)Nc1ccc(cc1)C(=O)O/property/InChi/txt
#     smiles = [smiles_ligand["canonical_SMILES"] for smiles_ligand in smiles_ligands]
#     query_elements = query.split()
#     pubchem_property = query_elements[0]
#     pubchem_sign = query_elements[1]
#     pubchem_threshold = float( query_elements[2] )
#     
#     filtered_smiles = []
#     
#     for smiles_entry in smiles:
#         rest_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/" + requests.utils.quote(smiles_entry, safe='') + "/property/" + pubchem_property + "/txt"
#         
#         try:
#             r = requests.get(rest_url)            
#             # get the HTTP response code, e.g. 200.
#             response_code = r.status_code 
#             print('Response Code: %d' % response_code)
#             if response_code == 200:
#                 pubchem_value = r.text.strip()
# #                 print pubchem_value, pubchem_sign, pubchem_threshold
#                 if pubchem_value:
#                     if pubchem_sign == "<":
#                         if float(pubchem_value) < pubchem_threshold:
#                             filtered_smiles.append( smiles_entry)
#                     elif pubchem_sign == ">":
#                         if float(pubchem_value) > pubchem_threshold:
#                             filtered_smiles.append( smiles_entry)
#             else:
#                 print r.text
#         except requests.exceptions.RequestException, e:
#             # print the error code and message and raise the error again
#             print e
#             raise e
#         
#         time.sleep(0.2)
# 
#     if inserted_already == "True":
#         smiles_ligands.rewind()
#     filtered_ligands = [ {"ligand_id": str( smiles_ligand["_id"] ) } for smiles_ligand in smiles_ligands if smiles_ligand["canonical_SMILES"] in filtered_smiles ]
# 
#     # this could go in the decision maker...
#     to_return["data"]["decisions"] = filtered_ligands 
#     # Insert decision into Analysis
#     mdrr_inserter.insert_analysis_decision(group_id=group_id, 
#                                            decision_type="Consult Additional Data Source (PubChem) and filter the ligands currently docked based on a user input threshold and property",
#                                            decision=to_return["data"]["decisions"])
#     
#     # Delete the Temp folders
#     # delete temporary folders where zip files were extracted
#     if os.path.exists(ligands_temp_dir): 
#         for ligand_file in os.listdir(ligands_temp_dir):
#             os.remove(ligands_temp_dir + os.sep + ligand_file)
#         os.removedirs(ligands_temp_dir)
#      
#     if os.path.exists(results_temp_dir): 
#         for result_file in os.listdir(results_temp_dir):
#             os.remove(results_temp_dir + os.sep + result_file)
#         os.removedirs(results_temp_dir)
#     
#     print "Goodbye from 'consult'"
#     return to_return
# 
# 
# 
# 
# @bottle.get('/ligand')
# def get_ligand():
#     """ Return full details of the ligand based on the structure id
#     GET Parameters:
#     [structure_id] -- the structure id of the ligand
#     [_id] -- the _id of the ligand
#     Returns:
#     JSON response containing all properties for that ligand in the database 
#     """
#     print "Welcome to 'get_ligand'"
#     to_return = {}
#     to_return["data"] = {}    
#     # read the GET parameters. If any are missing return with a status 'fail' explaining the required parameter  
#     
#     structure_id = bottle.request.query.structure_id
#     if not structure_id:
#         ligand_id = bottle.request.query._id
#         if not ligand_id:
#             to_return["status"] = "fail"
#             to_return["data"] = "structure_id or _id required as a GET parameter named 'structure_id' or '_id'!"
#             return to_return
#         
#         # connect to the MongoDB - this could go in another method
#         client = pymongo.MongoClient()      
#         db = client.mdrr_1
#         
#         mdrr_selector = mdrr.selector.Selector(db)
#         to_return["data"] = bson.json_util.dumps( mdrr_selector.select_ligand_by_id(ligand_id) )
#         
#     else:
#         # connect to the MongoDB - this could go in another method
#         client = pymongo.MongoClient()      
#         db = client.mdrr_1
#         
#         mdrr_selector = mdrr.selector.Selector(db)
#         to_return["data"] = bson.json_util.dumps( mdrr_selector.select_ligand(structure_id) )    
#         
#     return to_return
# 
# @bottle.get('/receptor')
# def get_receptor():
#     """ Return full details of the receptor based on the structure id
#     GET Parameters:
#     [structure_id] -- the structure id of the receptor
#     [_id] -- the _id of the receptor
#     
#     Returns:
#     JSON response containing all properties for that receptor in the database 
#     """
#     print "Welcome to 'get_receptor'"
#     to_return = {}
#     to_return["data"] = {}    
#     # read the GET parameters. If any are missing return with a status 'fail' explaining the required parameter  
#     
#     structure_id = bottle.request.query.structure_id
#     if not structure_id:
#         receptor_id = bottle.request.query._id
#         if not receptor_id:
#             to_return["status"] = "fail"
#             to_return["data"] = "structure_id or _id required as a GET parameter named 'structure_id' or '_id'!"
#             return to_return
#         
#         # connect to the MongoDB - this could go in another method
#         client = pymongo.MongoClient()      
#         db = client.mdrr_1
#         
#         mdrr_selector = mdrr.selector.Selector(db)
#         to_return["data"] = bson.json_util.dumps( mdrr_selector.select_receptor_by_id(receptor_id) )
#         
#     else:
#         # connect to the MongoDB - this could go in another method
#         client = pymongo.MongoClient()      
#         db = client.mdrr_1
#         
#         mdrr_selector = mdrr.selector.Selector(db)
#         to_return["data"] = bson.json_util.dumps( mdrr_selector.select_receptor(structure_id) )    
#         
#     return to_return   
#     
# @bottle.get('/result')
# def get_result_by_id():
#     """ Return full details of the result based on the structure id
#     GET Parameters:
#     [_id] -- the structure id of the result
#     
#     Returns:
#     JSON response containing all properties for that result in the database 
#     """
#     print "Welcome to 'get_result_by_id'"
#     to_return = {}
#     to_return["data"] = {}    
#     # read the GET parameters. If any are missing return with a status 'fail' explaining the required parameter  
#     
#     result_id = bottle.request.query._id
#     if not result_id:
#         to_return["status"] = "fail"
#         to_return["data"]["id"] = "id required as a GET parameter named 'id'!"
#         return to_return
#     
#     # connect to the MongoDB - this could go in another method
#     client = pymongo.MongoClient()      
#     db = client.mdrr_1
#     
#     mdrr_selector = mdrr.selector.Selector(db)
#     to_return["data"] = bson.json_util.dumps( mdrr_selector.select_result_by_id( result_id ) )
#     
#     return to_return
# 
# 
# # @bottle.post('/insertFindSimilarAssess')
# # def insertFindSimilarAssess():
# #     """ 
# #     1) Insert 1..* results made up of 1..* ligands, 1..* receptors and 1..* config files by calling the insert() method
# #     2) Find similar receptors in the MDRR
# #     3) Assess all docking results
# #     4) The results of 2) and 3) are analysed  by the DM
# #     
# #     POST Parameters:
# #     ligands -- ligand(s) (.zip for > 1 ligand, .pdqbt for 1 ligand)
# #     receptors -- receptor(s) (.zip for > 1 ligand, .pdqbt for 1 ligand)
# #     configs -- config file(s) (1-to-1 mapping with receptors, one conf for each receptor, .zip for > 1 ligand, other for 1 ligand)  
# #     results -- results zip file (one or more sets of: recName_ligName_out.pdbqt and recName_ligName_out.pdbqt_log.txt)
# #         
# #     Returns:
# #     JSON response containing a recommended protein-ligand pair to dock next      
# #     """
# #     
# #     # the results from the assessment of the docking results will be stored here
# #     assessed_results = None
# #     # the results from the assessment of the AT deepalign will be stored here 
# #     assessed_similar_receptors = None
# # 
# #     # 1) inserting
# #     to_return = {}
# #     to_return["data"] = {}
# #     # read the POST parameters. If any are missing return with a status 'fail' explaining the required parameter  
# #     ligands = bottle.request.files.get("ligands")
# #     if ligands is None:
# #         to_return["status"] = "fail"
# #         to_return["data"]["ligands"] = "Ligands required as a POST parameter named 'ligands'!"
# #         return to_return
# #     
# #     receptors = bottle.request.files.get("receptors")
# #     if receptors is None:
# #         to_return["status"] = "fail"
# #         to_return["data"]["receptors"] = "Receptors required as a POST parameter named 'receptors'!"
# #         return to_return
# #     
# #     configs = bottle.request.files.get("configs")
# #     if configs is None:
# #         to_return["status"] = "fail"
# #         to_return["data"]["configs"] = "Configs required as a POST parameter named 'configs'!"
# #         return to_return
# #     
# #     results = bottle.request.files.get("results")
# #     if results is None:
# #         to_return["status"] = "fail"
# #         to_return["data"]["results"] = "Results required as a POST parameter named 'results'!"
# #         return to_return
# #     
# #     thresholdDeepAlign = bottle.request.params.get("thresholdDeepAlign")
# #     thresholdVinaDocking = bottle.request.params.get("thresholdVinaDocking")
# #        
# #     # declare names of temporary directories where zip files will be unzipped
# #     temp_dir = "." + os.sep + "temp"
# #     
# #     #make a temp directory
# #     if not os.path.exists(temp_dir):
# #         os.mkdir(temp_dir)
# #         print temp_dir + " created \n"
# #     
# #     results_temp_dir = temp_dir + os.sep + "results"
# #     configs_temp_dir = temp_dir + os.sep + "configs"
# #     ligands_temp_dir = temp_dir + os.sep + "ligands"
# #     receptors_temp_dir = temp_dir + os.sep + "receptors"
# #     
# #     group_id = datetime.now().strftime("%Y-%m-%d_%H:%M:%S%Z") + str(random.random())
# #     
# #     # connect to the MongoDB - this could go in another method
# #     client = pymongo.MongoClient()      
# #     db = client.mdrr_1
# #     
# #     # call the method to insert the data in MongoDB
# #     to_return["status"] = insert(db, ligands, ligands_temp_dir, receptors, receptors_temp_dir, configs, configs_temp_dir, results, results_temp_dir)["status"]
# #     
# # #     to_return["data"]["decisions"] = []
# #     
# #     # 2) calling the AT DeepAlign and AssessDeepAlign
# #         
# #     # get all receptors from MDRR
# #     mdrr_selector = mdrr.selector.Selector(db)
# #     all_receptors = mdrr_selector.select_all_receptors()
# #     
# #     # parse to pdb files and put each into a zip file
# #     z_all_receptors_name = "all_receptors.zip"
# #     z_all_receptors = zipfile.ZipFile(z_all_receptors_name, "w")
# #     parser = mdrr.receptor_parser.Plain() 
# #     for mdrr_receptor in all_receptors:
# #         # get the structure of the receptor in 'pdb_receptor'
# #         pdb_receptor = parser.dict_to_string(mdrr_receptor["structure"])
# #         # get the structure_id and make it part of the name, separated by '_' with the receptor name
# #         z_all_receptors.writestr(str(mdrr_receptor["structure_id"]) + "_" + mdrr_receptor["name"], pdb_receptor)    
# #     z_all_receptors.close()
# #     
# #     # for each target receptor (receptor that has been used in the insert), usually just 1
# #     for receptor_file in os.listdir(receptors_temp_dir):
# #         #call the at-deepalign rest api to compare and assess
# #         try:
# #             target_receptor = receptors_temp_dir + os.sep + receptor_file
# #             
# #             # the post parameters: target_receptor='receptor' (file), receptors='all receptors'(file), threshold='DeepScore value' (default: 500)
# #             pf = [('target_receptor', (pycurl.FORM_FILE, target_receptor)),
# #                   ('receptors', (pycurl.FORM_FILE, z_all_receptors_name)), 
# #                   ('threshold', thresholdDeepAlign)
# #                  ]
# #             # create new pycurl object
# #             c = pycurl.Curl()
# #             # set the parameters: URL, HTTPPOST parameters
# #             c.setopt(c.URL, "http://localhost:8091/compareAndAssess")
# #             c.setopt(c.HTTPPOST, pf)
# #             # ignore SSL error (equivalent to curl --insecure or curl -k)
# #             # c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
# #             # uncomment the next line for verbose (curl -v)  
# #             c.setopt(c.VERBOSE, True)
# #             #this StringIO is needed to store the response in
# #             response_buffer = StringIO()
# #             # set the option to write the response into the response_buffer
# #             c.setopt(c.WRITEDATA, response_buffer)
# #             # send the request
# #             c.perform()            
# #             # get the HTTP response code, e.g. 200.
# #             response_code = c.getinfo(c.RESPONSE_CODE) 
# #             if response_code != 200:
# #                 print('Response Code: %d' % response_code)
# #             c.close()           
# #             # this needs to be passed to the DM
# #             # {'data': {"similar": [ {"structure_id": aaa, "DeepAlign_result": bbb}, {}, {}, ... ]}, "config": c, "threshold": t }
# #             assessed_similar_receptors = json.loads(response_buffer.getvalue()) 
# #             
# #         except pycurl.error, e:
# #             # print the error code and message and raise the error again
# #             print "Error code: ", e[0]
# #             print "Error message: ", e[1]  
# #             raise e
# # 
# #         # insert into analysis type = structural_alignment, tool = deepalign, config=xxx, target_receptor=xxxx, assessed_similar_receptors["data"]["similar"]
# #         mdrr_inserter = mdrr.inserter.Inserter(db)
# #         # get the structure_id of the target receptor from its path
# #         target_receptor_structure_id = parser.path_to_structure_id(target_receptor)
# #         # insert one document per similar receptor in the analisis collection
# #         # return a list of the inserted_ids 
# #         inserted_similar_list = mdrr_inserter.insert_analysis_structural_alignment(group_id=group_id,
# #                                                                                    target_receptor=target_receptor_structure_id,
# #                                                                                    similar_list=assessed_similar_receptors["data"]["similar"])
# #         
# #         
# #         # insert into analysis type = assess_structural_alignment, threshold, analysis_id=xxx    
# #         mdrr_inserter.insert_analysis_structural_alignment_assessment(group_id=group_id,
# #                                                                       assessed_as_similar=inserted_similar_list,
# #                                                                       threshold=thresholdDeepAlign)
# #         
# #         # 3) calling the AT AssessDockingResults
# #         # unless it there are 0 similar receptors        
# #         if ( len( assessed_similar_receptors["data"]["similar"] ) > 0):
# # #             to_return["data"]["compared"] = {}
# # #             to_return["data"]["compared"] = assessed_similar_receptors["data"]
# #             
# #             # this can be cached, the cache can have id of result and threshold...
# #             
# #             # get all docking results from MDRR where the id value in the 'receptor' field equals the structure_id of the assessed similar receptors
# #             # put all structure_id-s of similar receptors into the array structure_ids_similar
# #             structure_ids_similar = []
# #             for similar in assessed_similar_receptors["data"]["similar"]:
# #                 structure_ids_similar.append( similar["structure_id"] )
# #             # get all results from the datbase
# #             mdrr_selector = mdrr.selector.Selector(db)
# #             docking_results = mdrr_selector.select_results_where_receptor_structure_ids(structure_ids_similar)
# # #             docking_results = mdrr_selector.select_results_where_receptor_file(target_receptor)
# #             
# #             # call the assessor
# #             # save the 'all docking results' json as a file on disk
# #             all_results_filename = "all_docking_result.json"    
# #             with open(all_results_filename, "w") as all_results:
# #                 all_results.write(bson.json_util.dumps(docking_results)) 
# #             
# #             #call the assess-docking rest api to compare and assess
# #             try:
# #                 
# #                 # the post parameters: docking_results='results' (file or zip with many files), [threshold]='affinity value' (default -5.0)
# #                 pf = [('docking_results', (pycurl.FORM_FILE, all_results_filename)),
# #                       ('threshold', thresholdVinaDocking) 
# #                       ]
# #                 # create new pycurl object
# #                 c = pycurl.Curl()
# #                 # set the parameters: URL, HTTPPOST parameters
# #                 c.setopt(c.URL, "http://localhost:8092/assess")
# #                 c.setopt(c.HTTPPOST, pf)
# #                 # ignore SSL error (equivalent to curl --insecure or curl -k)
# #                 # c.setopt(pycurl.SSL_VERIFYPEER, False) # equivalent to curl's --insecure
# #                 # uncomment the next line for verbose (curl -v)  
# #                 c.setopt(c.VERBOSE, False)
# #                 #this StringIO is needed to store the response in
# #                 response_buffer = StringIO()
# #                 
# #                 
# #                 # set the option to write the response into the response_buffer
# #                 c.setopt(c.WRITEDATA, response_buffer)
# #                 #  with open("assesssed_results", 'w') as f:
# #                 #     c.setopt(c.WRITEFUNCTION, f.write)
# #                 #     c.perform()
# #                 # send the request
# #                 c.perform()            
# #                 # get the HTTP response code, e.g. 200.
# #                 response_code = c.getinfo(c.RESPONSE_CODE) 
# #                 if response_code != 200:
# #                     print('Response Code: %d' % response_code)
# #                 c.close()
# #                 # this needs to be passed to the DM
# #                 assessed_results = json.loads(response_buffer.getvalue())
# #             except pycurl.error, e:
# #                 # print the error code and message and raise the error again
# #                 print "Error code: ", e[0]
# #                 print "Error message: ", e[1]  
# #                 raise e
# #             
# #             # insert into analysis type = assess_docking, threshold, assessed_results["data]["good"]: [{model_number, score}, {}...]
# #             mdrr_inserter.insert_analysis_docking_assessment(group_id=group_id,
# #                                                              threshold=thresholdVinaDocking,
# #                                                              good_dockings=assessed_results["data"]["good"])
# #                    
# #             # 4) call the DM with correct parameters - this is a simple decision maker
# #             decision_maker = dm.decider.SimpleDecide(assessed_results, assessed_similar_receptors)
# #             # append the decision of each targer receptor (usually this is only 1 receptor if it is a virtual screening) 
# #             to_return["data"]["decisions"] = decision_maker.run()
# #     
# #         # if there were 0 similar receptors return a message
# #         else:
# #             to_return["data"]["decisions"] = "No similar receptors, can't suggest the next ligand-receptor pair"
# #         to_return["status"] = "successD"   
# #        
# #     # 5) the DM can insert the decision into the MongoDB database - insert into analysis 
# #     mdrr_inserter.insert_analysis_decision(group_id=group_id, 
# #                                            decision=to_return["data"]["decisions"])
# #     
# #     # add the group_id value to the response, so that you can see all the 'analysis' documents related to this run
# #     to_return["group_id"] = group_id
# #     
# #     # delete temporary folders where zip files were extracted
# #     if os.path.exists(configs_temp_dir):
# #         for config_file in os.listdir(configs_temp_dir):
# #             os.remove(configs_temp_dir + os.sep + config_file)
# #         os.removedirs(configs_temp_dir)
# #     
# #     if os.path.exists(receptors_temp_dir): 
# #         for receptor_file in os.listdir(receptors_temp_dir):
# #             os.remove(receptors_temp_dir + os.sep + receptor_file)
# #         os.removedirs(receptors_temp_dir)
# #     
# #     if os.path.exists(ligands_temp_dir): 
# #         for ligand_file in os.listdir(ligands_temp_dir):
# #             os.remove(ligands_temp_dir + os.sep + ligand_file)
# #         os.removedirs(ligands_temp_dir)
# #     
# #     if os.path.exists(results_temp_dir): 
# #         for result_file in os.listdir(results_temp_dir):
# #             os.remove(results_temp_dir + os.sep + result_file)
# #         os.removedirs(results_temp_dir)
# #     
# #     #return the json with data about all the steps and the final decision
# #     return to_return #this one asks bottle to call json.dumps() 
# 
# 
# bottle.run(host='localhost', port=8090, debug=True)
