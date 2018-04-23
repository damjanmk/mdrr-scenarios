'''
Created on Mar 19, 2017

@author: damjan
'''
# import subprocess
# try:
# #     obprop_stdout = subprocess.check_output(['obprop', '/home/damjan/Documents/Docking/result data/results/ligands/ZINC00000226.pdbqt'])
#     obprop_stdout = subprocess.check_output(['ls'])
# except Exception as e:
#     print e

import pybel
import binascii
# import openbabel
#  
# obConversion = openbabel.OBConversion()
# obConversion.SetInAndOutFormats("pdbqt", "mol2")
# obmol = openbabel.OBMol()
# obConversion.ReadFile(obmol, '/home/damjan/Documents/Docking/result data/results/ligands/ZINC00000226.pdbqt')   # Open Babel will uncompress automatically
# obmol.AddHydrogens()
 
# print mol.NumAtoms()
# print mol.NumBonds()

 
# print [method for method in dir(mol) if callable(getattr(mol, method))]
mol = pybel.readfile("pdbqt", 'workspace/DockingResultRepositoryAPI/main/temp/ligands/ZINC00000125.pdbqt').next()
# mol = pybel.readfile("pdbqt", '/home/damjan/Documents/Docking/result data/results/ligands/ZINC00000226.pdbqt').next()
# mol = pybel.readfile("pdbqt", '/home/damjan/Documents/Docking/result data/results/ligands/ZINC00000384.pdbqt').next()
mol = pybel.readfile("pdbqt", '../main/temp/ligands/ZINC00000125.pdbqt').next()
# if not mol.OBMol.HasHydrogensAdded():
mol.OBMol.AddHydrogens()
    
descvalues = mol.calcdesc()
# In Python, the update method of a dictionary allows you
# to add the contents of one dictionary to another
# for key in descvalues.keys():
#     print key + ": "
#     print descvalues[key]

# for key in pybel.outformats.keys():
#     print key + ": " + pybel.outformats[key]

mol.data.update(descvalues)
 
# for key in mol.data.keys():
#     print key + ": " + mol.data[key]

print "name\t" + mol.title
print "formula\t" + mol.formula
print "mol_weight\t" + str(mol.molwt)
print "exact_mass\t" + str(mol.exactmass)
print "canonical_SMILES\t" + mol.write("can").split()[0]
print "InChI\t" + mol.write("inchi")
print "num_atoms\t" + str(len(mol.atoms))
print "num_bonds\t" + str(mol.OBMol.NumBonds())
num_residues = mol.OBMol.NumResidues()
print "num_residues\t" + str(num_residues)
print "num_rotors\t" + str(mol.OBMol.NumRotors())
seq = ""
for i in range(num_residues):
    seq += mol.OBMol.GetResidue(i).GetName() + '-'
seq = seq.strip('-')    
print "sequence\t" + seq
print "num_rings\t" + str(len(mol.sssr))
print "logP\t" + str(mol.data['logP'])
print "PSA\t" + str(mol.data['TPSA'])
print "MR\t" + str(mol.data['MR'])
print mol.calcfp(pybel.fps[1])
print mol.calcfp().bits

print binascii.hexlify(str(mol.calcfp(pybel.fps[0])))# hexlify("512")
# for b in mol.calcfp().bits:
#     print binascii.hexlify(str(b))
# for f in mol.calcfp().fp:
#     print binascii.hexlify(str(f))

# print [method for method in dir(mol.OBMol) if callable(getattr(mol.OBMol, method))]
# print "num_bonds\t" + 
# name             ZINC00000226
# formula          C9H9NO3
# mol_weight       179.173
# exact_mass       179.058
# canonical_SMILES CC(=O)Nc1ccc(cc1)C(=O)O    ZINC00000226
# 
# InChI            InChI=1S/C9H9NO3/c1-6(11)10-8-4-2-7(3-5-8)9(12)13/h2-5H,1H3,(H,10,11)(H,12,13)
# 
# num_atoms        22
# num_bonds        22
# num_residues     1
# num_rotors       3
# sequence         LIG
# num_rings        1
# logP             1.4162
# PSA              66.4
# MR               47.714

# print "atoms len: " 
# print len(mol.atoms)
# print "charge: "  
# print mol.charge
# print "conformers: "  
# # for c in mol.conformers:
# #     print c
# print "data: "   
# print mol.data.keys()
# print "dim: "   
# print mol.dim
# print "energy: "   
# print mol.energy
# print "exactmass: "   
# print mol.exactmass
# print "molwt: "   
# print mol.molwt
# print "spin: "   
# print mol.spin
# print "sssr: "   
# for s in mol.sssr:
#     print s
# print "title: "   
# print mol.title
# print "unitcell: "   
# print mol.unitcell




#         print mol.calcfp(pybel.fps[1])
#         print mol.calcfp().bits        
#         obprop_stdout = subprocess.check_output(['obprop', ligand])
#         obprop_dict = {}
#         obprop_keys = ["name", "formula", "mol_weight", "exact_mass", "canonical_SMILES", "InChI", "num_atoms",
#                        "num_bonds", "num_residues", "num_rotors", "sequence", "num_rings", "logP", "PSA"]
#         for line in obprop_stdout.splitlines():
#             if line.startswith(obprop_keys[0]):
#                 obprop_dict[obprop_keys[0]] = line.split()[1]
#             elif line.startswith(obprop_keys[1]):
#                 obprop_dict[obprop_keys[1]] = line.split()[1]
#             elif line.startswith(obprop_keys[2]):
#                 obprop_dict[obprop_keys[2]] = line.split()[1]
#             elif line.startswith(obprop_keys[3]):
#                 obprop_dict[obprop_keys[3]] = line.split()[1]
#             elif line.startswith(obprop_keys[4]):
#                 obprop_dict[obprop_keys[4]] = line.split()[1]
#             elif line.startswith(obprop_keys[5]):
#                 obprop_dict[obprop_keys[5]] = line.split()[1]
#             elif line.startswith(obprop_keys[6]):
#                 obprop_dict[obprop_keys[6]] = line.split()[1]
#             elif line.startswith(obprop_keys[7]):
#                 obprop_dict[obprop_keys[7]] = line.split()[1]
#             elif line.startswith(obprop_keys[8]):
#                 obprop_dict[obprop_keys[8]] = line.split()[1]
#             elif line.startswith(obprop_keys[9]):
#                 obprop_dict[obprop_keys[9]] = line.split()[1]
#             elif line.startswith(obprop_keys[10]):
#                 obprop_dict[obprop_keys[10]] = line.split()[1]
#             elif line.startswith(obprop_keys[11]):
#                 obprop_dict[obprop_keys[11]] = line.split()[1]
#             elif line.startswith(obprop_keys[12]):
#                 obprop_dict[obprop_keys[12]] = line.split()[1]
#             elif line.startswith(obprop_keys[13]):
#                 obprop_dict[obprop_keys[13]] = line.split()[1]
#         return obprop_dict



#         ob2fps_stdout = subprocess.check_output(['ob2fps', ligand])
#         ob2fps_dict = {}
#         ob2fps_keys = ["num_bits", "type", "software", "source", "date"]
#         first_line = True
#         for line in ob2fps_stdout.splitlines():
#             if first_line:
#                 ob2fps_dict["format"] = line.trim("#")
#                 first_line = False
#             elif line.startswith(ob2fps_keys[0]):
#                 ob2fps_dict[ob2fps_keys[0]] = line.split("=")[1]
#             elif line.startswith(ob2fps_keys[1]):
#                 ob2fps_dict[ob2fps_keys[1]] = line.split("=")[1]
#             elif line.startswith(ob2fps_keys[2]):
#                 ob2fps_dict[ob2fps_keys[2]] = line.split("=")[1]
#             elif line.startswith(ob2fps_keys[3]):
#                 ob2fps_dict[ob2fps_keys[3]] = line.split("=")[1]
#             else:
#                 ob2fps_dict["fingerprint"] = line
#         return ob2fps_dict
