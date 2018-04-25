from pymongo import MongoClient    
from mdrr.inserter import Inserter
from mdrr.selector import Selector
import os
import ntpath
import bson.json_util

client = MongoClient()      
db = client.mdrr_1

ligands = db.ligandsSmall.find()
receptors = db.receptorsSmall.find()
ligand_ids = []
receptor_ids = []
for l in ligands:
    ligand_ids.append(str(l["structure_id"]))
for r in receptors:
    receptor_ids.append(str(r["structure_id"]))
print ligand_ids
print receptor_ids
# results = db.results.find({"ligand": {"$in": ligand_ids}, "receptor": {"$in": receptor_ids} })
# print len(results)
#test_pybel insert methods
# i = Inserter(db)
# result = i.insert_receptor("/home/damjan/Documents/Docking/result data/results/rec.pdbqt", "ribokinase", "TV")
# result = i.insert_ligand("/home/damjan/Documents/Docking/result data/results/ligands/ZINC00000036.pdbqt", "(S)-(+)-Mandelic acid")
# result = i.insert_result(receptor_path="/home/damjan/Documents/Docking/result data/results/rec.pdbqt", receptor_name="ribokinase", receptor_species="TV", 
#                          ligand_path="/home/damjan/Documents/Docking/result data/results/ligands/ZINC00000036.pdbqt", ligand_name="(S)-(+)-Mandelic acid",
#                          result_path="/home/damjan/Documents/Docking/result data/results/rec/rec_ZINC00000036_out.pdbqt",
#                          config_path="/home/damjan/Documents/Docking/conf.txt")
# print "ObjectId: "
# print result

#read through all results in this folder
# root_folder = "/home/damjan/Documents/Docking/result data/results"
# config_file="/home/damjan/Documents/Docking/conf.txt"
# ligands = []
# for f in os.listdir(root_folder):
#     if f.endswith(".pdbqt"):
#         receptor = root_folder + "/" + f
#   
# for f in os.listdir(root_folder + "/ligands"):
#     ligands.append(root_folder + "/ligands/" + f)
#      
# receptor_basename = ntpath.basename(receptor).split(".")[0] 
# for ligand in ligands:     
#     ligand_basename = ntpath.basename(ligand).split(".")[0]
#     result = root_folder + "/" + receptor_basename + "/" + receptor_basename + "_" + ligand_basename + "_out.pdbqt"
#     result_id = i.insert_result(receptor, "ribokinase", "TV", ligand, "(S)-(+)-Mandelic acid", result, config_file)

#test_pybel selector methods
# s = Selector(db)
# results = [bson.ObjectId("59522cc4c831de0e7c524636"), "59522cc4c831de0e7c524639", "5952217cc831de0e7c52461a", "59998c29c831de10b17eed58", "592f2cfac831de25fe46f1d7"]
# results = ["5a5cc8e8c831de11a5d80a79", "5a5cc8e8c831de11a5d80aca", "5a5cc8e8c831de11a5d80a9a", "5a5cc8e8c831de11a5d80a91"]
# cursor = s.select_results_grouped_format(results)
# print "lala"
# print bson.json_util.dumps(cursor)
# similar_structure_ids = ["1f64a6e0a4f0a8588f40ad3dab7eafde", "15e7679635b2001077b825d9b6311268"]
# cursor = s.select_results_where_receptor_structure_ids(similar_structure_ids)
# print bson.json_util.dumps(cursor)
