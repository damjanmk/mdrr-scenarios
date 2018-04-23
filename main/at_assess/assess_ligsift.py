

class Assess():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
# example:
#  ********************************************************************************************* 
#  * LIGSIFT (v1.3): An open-source tool for ligand structural alignment and virtual screening * 
#  * Ambrish Roy & Jeffrey Skolnick                                                            * 
#  * Please mail your comments to Ambrish Roy (ambrish.roy@gmail.com)                          * 
#  ********************************************************************************************* 
# No. of molecules read from query file : 1
# No. of molecules read from database   : 1
# Using -opt 2 (default) Chemical similarity for finding the best overlap.
# Database_name      Query_name         ShapeTanimoto  ChemTanimoto    ShapeSim   ChemSim   ShapeSimPval  ChemSimPval   TverskyShape  TverskyChem  
# STI                STI                   1.000          1.000         1.000      1.000    4.957569e-09  5.256640e-09    1.000         1.000 


    def ShapeSim(self, LigsiftResult, threshold):
        lines = LigsiftResult.split("\n")
        this_line = False
        ShapeSim = 0.0
        for line in lines:            
            if this_line:
                line_values = line.split()
                ShapeSim = float(line_values[4]) # the fifth element is the ShapeSim
                break
            if line.startswith("Database_name"):
                this_line = True
            
        if ShapeSim > threshold:
            # if similar return True
            return ShapeSim
        else:
            # if deemed not similar return False
            return False