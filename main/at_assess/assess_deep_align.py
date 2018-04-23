

class Assess():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
# example:

# #------------------------------------------------------#
# #                    DeepAlign                         #
# # Protein structure alignment beyond spatial proximity #
# # Reference:     S. Wang, J. Ma, J. Peng and J. Xu.    #
# #                Scientific Reports, 3, 1448, (2013)   #
# #------------------------------------------------------#
# 
# 1st input protein: 1pazA    length=  120 
# 2nd input protein: 1p53    length=  250 
# 
# #----- Normalization length for TMscore, MAXSUB, GDT_TS, and GDT_HA is  120
# #----- Distance cutoff value is 9.807331
# # BLOSUM CLESUM DeepScore SeqID LALI RMSD(A) TMscore MAXSUB GDT_TS GDT_HA
#      -13     63    116.86     5   67   3.028   0.403  0.321  0.369  0.242
# #----- Please see http://raptorx.uchicago.edu/DeepAlign/documentation/ for explanation of these scores 
# 
# #----- Transformation to superpose the 1st protein onto the 2nd ---#
# # i          t(i)         u(i,1)         u(i,2)         u(i,3) 
#   1         -2.538736    0.127876243   -0.267021811    0.955168582
#   2        163.166395   -0.673404225   -0.730425687   -0.114039751
#   3         42.311049    0.728130769   -0.628631584   -0.273217708
# 
# 
# T 1pazA            15 AMVFEPAY-IKANPGDTVTFIPVDK---------GHNVESIKDMIPEGAEKFKSKI-------NENYVLTVT--QPGAYL   75 (120)
# RMSD                  412124   101101211013454          74411355       4445364       442100011  201110           
# S 1p53              7 PPQLVS--PRVLEVDTQGTVVCSL-DGLFPVSEAQVHLALGD-------QRLNPTVTYGNDSFSAKASVSVTAEDEGTQR   76 (250)
# 
# 
# T 1pazA            76 VKCTPHY-----AMGMIALIAVG   93 (120)
# RMSD                  11021       64412200001           
# S 1p53             77 LTCAV--ILGNQSQETLQTVTIY   97 (250)

    def run(self, deepAlignResult, threshold):
        lines = deepAlignResult.split("\n")
        this_line = False
        deepScore = 0.0
        for line in lines:
            if this_line:
                line_values = line.split() 
                deepScore = float(line_values[2]) # the third element is the DeepScore
                break
            if line.startswith("# BLOSUM CLESUM DeepScore"):
                this_line = True
               
        if deepScore > threshold:
            # if similar return True
            return deepScore
        else:
            # if deemed not similar return False
            return False