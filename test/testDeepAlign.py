'''
Created on Feb 19, 2018

@author: damjan
'''
import subprocess
import os

DEEPALIGN_PATH = "/home/damjan/Documents/StructAlign/DeepAlign/DeepAlign"
for receptor_file in os.listdir("../main/temp/receptors/"):
    try:
        DeepAlignResult = subprocess.check_output([DEEPALIGN_PATH, "../main/temp/target/rec.pdbqt", "../main/temp/receptors/" + receptor_file], stderr=subprocess.STDOUT) #, stdout=redirect_to_file)
        print DeepAlignResult
        print "\n\n"
    except subprocess.CalledProcessError as e:
        # if it is a non-zero result
        print("DeepAlign stdout output on error:\n" + e.output)
        print "\n\n"
        pass 