# import zipfile
# import os
# 
# receptors_filename = "../main/all_receptors.zip"
# print os.path.exists(receptors_filename)
# 
# print zipfile.is_zipfile(receptors_filename)
# 
# with zipfile.ZipFile(receptors_filename) as receptors_zip:
#     
#     print receptors_filename + " works fine"

import pymongo  
import mdrr.selector
import mdrr.ligand_parser

import openbabel


def pdbqt_string_to_mol2(pdbqt_string, path_to_mol2): 
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("pdbqt", "mol2")
     
    mol = openbabel.OBMol()
    obConversion.ReadString(mol, pdbqt_string)
    mol.AddHydrogens()
     
    obConversion.WriteFile(mol, path_to_mol2)

def pdbqt_string_to_mol2_string(pdbqt_string): 
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("pdbqt", "mol2")
     
    mol = openbabel.OBMol()
    obConversion.ReadString(mol, pdbqt_string)
    mol.AddHydrogens()
     
    return obConversion.WriteString(mol)

# connect to the MongoDB - this could go in another method
client = pymongo.MongoClient()      
db = client.mdrr_1

# get all docking results from MDRR
# mdrr_selector = mdrr.selector.Selector(db)
# all_docking_results = mdrr_selector.select_all_results()

mdrr_selector = mdrr.selector.Selector(db)
ligands = mdrr_selector.select_ligands_where_result_has_receptor("d47bcfc8f7c1b91e4f6d451cc11dce07")
many = "";
parser = mdrr.ligand_parser.Plain()
heres_a_string = ""
for l in ligands:
    heres_a_string = parser.dict_to_string( l["structure"] )
    many = many + pdbqt_string_to_mol2_string(heres_a_string)
print many








