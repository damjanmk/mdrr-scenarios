'''
Created on May 19, 2017

@author: damjan
'''

import bottle
import zipfile
import os
import at_assess.assess_docking


@bottle.post('/assess')
def assess():
    """ Assess the AutoDock Vina docking results, using a threshold value of the vina score provided by the user
    
    POST Parameters:    
    docking_results -- vina docking results to assess (must contain receptor name/id). This is one example result in JSON (expect an array of results!):  
      
    {
    "_id" : ObjectId("58cee528c831de230925a53b"),
    "random_seed" : "800072252",
    "ligand" : ObjectId("58cee528c831de230925a53a"),
    "models" : [ 
        {
            "rmsd_from_best" : [ 
                "0.000", 
                "0.000"
            ],
            "model" : [ 
                "MODEL 1\n", 
                "REMARK VINA RESULT:      -5.2      0.000      0.000\n", 
                "REMARK  Name = ZINC00000411\n", 
                "REMARK                            x       y       z     vdW  Elec       q    Type\n", 
                "REMARK                         _______ _______ _______ _____ _____    ______ ____\n", 
                "ROOT\n", 
                "ATOM      1  C   LIG    1       -6.256  -2.325  -0.264  0.00  0.00    +0.240 C \n", 
                "ATOM      2  O   LIG    1       -6.398  -3.552  -0.117  0.00  0.00    -0.287 OA\n", 
                "ENDROOT\n", 
                "BRANCH   1   3\n", 
                "ATOM      3  C   LIG    1       -7.369  -1.318   0.060  0.00  0.00    +0.189 C \n", 
                "ATOM      4  C   LIG    1       -7.983  -0.710  -1.207  0.00  0.00    +0.046 C \n", 
                "BRANCH   3   5\n", 
                "ATOM      5  O   LIG    1       -7.019  -0.342   1.045  0.00  0.00    -0.369 OA\n", 
                "BRANCH   5   7\n", 
                "ATOM      6  C   LIG    1       -6.685   2.048   1.092  0.00  0.00    +0.034 C \n", 
                "ATOM      7  C   LIG    1       -7.687   0.914   0.934  0.00  0.00    +0.157 C \n", 
                "ENDBRANCH   5   7\n", 
                "ENDBRANCH   3   5\n", 
                "ENDBRANCH   1   3\n", 
                "BRANCH   1   8\n", 
                "ATOM      8  C   LIG    1       -4.920  -1.732  -0.764  0.00  0.00    +0.419 C \n", 
                "BRANCH   8   9\n", 
                "ATOM      9  O   LIG    1       -3.814  -2.568  -0.483  0.00  0.00    -0.502 OA\n", 
                "ATOM     10  H   LIG    1       -4.154  -3.239   0.138  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8   9\n", 
                "BRANCH   8  11\n", 
                "ATOM     11  O   LIG    1       -4.629  -0.480  -0.191  0.00  0.00    -0.502 OA\n", 
                "ATOM     12  H   LIG    1       -4.778   0.164  -0.904  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8  11\n", 
                "ENDBRANCH   1   8\n", 
                "TORSDOF 6\n", 
                "ENDMDL\n"
            ],
            "affinity" : "-5.2",
            "model_number" : "1"
        }, 
        {
            "rmsd_from_best" : [ 
                "9.032", 
                "10.327"
            ],
            "model" : [ 
                "MODEL 2\n", 
                "REMARK VINA RESULT:      -4.8      9.032     10.327\n", 
                "REMARK  Name = ZINC00000411\n", 
                "REMARK                            x       y       z     vdW  Elec       q    Type\n", 
                "REMARK                         _______ _______ _______ _____ _____    ______ ____\n", 
                "ROOT\n", 
                "ATOM      1  C   LIG    1      -11.644   4.609  -7.922  0.00  0.00    +0.240 C \n", 
                "ATOM      2  O   LIG    1      -12.029   4.588  -9.106  0.00  0.00    -0.287 OA\n", 
                "ENDROOT\n", 
                "BRANCH   1   3\n", 
                "ATOM      3  C   LIG    1      -10.708   3.542  -7.337  0.00  0.00    +0.189 C \n", 
                "ATOM      4  C   LIG    1      -11.228   2.121  -7.582  0.00  0.00    +0.046 C \n", 
                "BRANCH   3   5\n", 
                "ATOM      5  O   LIG    1      -10.315   3.777  -5.982  0.00  0.00    -0.369 OA\n", 
                "BRANCH   5   7\n", 
                "ATOM      6  C   LIG    1       -9.466   2.901  -3.899  0.00  0.00    +0.034 C \n", 
                "ATOM      7  C   LIG    1      -10.315   2.630  -5.132  0.00  0.00    +0.157 C \n", 
                "ENDBRANCH   5   7\n", 
                "ENDBRANCH   3   5\n", 
                "ENDBRANCH   1   3\n", 
                "BRANCH   1   8\n", 
                "ATOM      8  C   LIG    1      -12.074   5.744  -6.966  0.00  0.00    +0.419 C \n", 
                "BRANCH   8   9\n", 
                "ATOM      9  O   LIG    1      -10.980   6.520  -6.518  0.00  0.00    -0.502 OA\n", 
                "ATOM     10  H   LIG    1      -11.132   7.411  -6.886  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8   9\n", 
                "BRANCH   8  11\n", 
                "ATOM     11  O   LIG    1      -12.725   5.268  -5.812  0.00  0.00    -0.502 OA\n", 
                "ATOM     12  H   LIG    1      -13.471   5.877  -5.676  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8  11\n", 
                "ENDBRANCH   1   8\n", 
                "TORSDOF 6\n", 
                "ENDMDL\n"
            ],
            "affinity" : "-4.8",
            "model_number" : "2"
        }, 
        {
            "rmsd_from_best" : [ 
                "8.727", 
                "10.252"
            ],
            "model" : [ 
                "MODEL 3\n", 
                "REMARK VINA RESULT:      -4.7      8.727     10.252\n", 
                "REMARK  Name = ZINC00000411\n", 
                "REMARK                            x       y       z     vdW  Elec       q    Type\n", 
                "REMARK                         _______ _______ _______ _____ _____    ______ ____\n", 
                "ROOT\n", 
                "ATOM      1  C   LIG    1      -11.354   5.021  -4.813  0.00  0.00    +0.240 C \n", 
                "ATOM      2  O   LIG    1      -11.241   6.259  -4.752  0.00  0.00    -0.287 OA\n", 
                "ENDROOT\n", 
                "BRANCH   1   3\n", 
                "ATOM      3  C   LIG    1      -11.284   4.248  -6.138  0.00  0.00    +0.189 C \n", 
                "ATOM      4  C   LIG    1      -10.265   3.103  -6.083  0.00  0.00    +0.046 C \n", 
                "BRANCH   3   5\n", 
                "ATOM      5  O   LIG    1      -11.151   5.071  -7.299  0.00  0.00    -0.369 OA\n", 
                "BRANCH   5   7\n", 
                "ATOM      6  C   LIG    1      -12.310   4.832  -9.402  0.00  0.00    +0.034 C \n", 
                "ATOM      7  C   LIG    1      -12.366   5.375  -7.983  0.00  0.00    +0.157 C \n", 
                "ENDBRANCH   5   7\n", 
                "ENDBRANCH   3   5\n", 
                "ENDBRANCH   1   3\n", 
                "BRANCH   1   8\n", 
                "ATOM      8  C   LIG    1      -11.549   4.176  -3.535  0.00  0.00    +0.419 C \n", 
                "BRANCH   8   9\n", 
                "ATOM      9  O   LIG    1      -12.617   3.255  -3.649  0.00  0.00    -0.502 OA\n", 
                "ATOM     10  H   LIG    1      -12.743   3.129  -4.608  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8   9\n", 
                "BRANCH   8  11\n", 
                "ATOM     11  O   LIG    1      -11.819   4.960  -2.397  0.00  0.00    -0.502 OA\n", 
                "ATOM     12  H   LIG    1      -11.528   5.857  -2.636  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8  11\n", 
                "ENDBRANCH   1   8\n", 
                "TORSDOF 6\n", 
                "ENDMDL\n"
            ],
            "affinity" : "-4.7",
            "model_number" : "3"
        }, 
        {
            "rmsd_from_best" : [ 
                "12.493", 
                "13.884"
            ],
            "model" : [ 
                "MODEL 4\n", 
                "REMARK VINA RESULT:      -4.7     12.493     13.884\n", 
                "REMARK  Name = ZINC00000411\n", 
                "REMARK                            x       y       z     vdW  Elec       q    Type\n", 
                "REMARK                         _______ _______ _______ _____ _____    ______ ____\n", 
                "ROOT\n", 
                "ATOM      1  C   LIG    1        3.377  -9.662  -3.152  0.00  0.00    +0.240 C \n", 
                "ATOM      2  O   LIG    1        3.283  -8.500  -3.588  0.00  0.00    -0.287 OA\n", 
                "ENDROOT\n", 
                "BRANCH   1   3\n", 
                "ATOM      3  C   LIG    1        3.022 -10.035  -1.705  0.00  0.00    +0.189 C \n", 
                "ATOM      4  C   LIG    1        4.099  -9.581  -0.712  0.00  0.00    +0.046 C \n", 
                "BRANCH   3   5\n", 
                "ATOM      5  O   LIG    1        2.620 -11.395  -1.524  0.00  0.00    -0.369 OA\n", 
                "BRANCH   5   7\n", 
                "ATOM      6  C   LIG    1        0.495 -10.979  -0.458  0.00  0.00    +0.034 C \n", 
                "ATOM      7  C   LIG    1        1.850 -11.661  -0.353  0.00  0.00    +0.157 C \n", 
                "ENDBRANCH   5   7\n", 
                "ENDBRANCH   3   5\n", 
                "ENDBRANCH   1   3\n", 
                "BRANCH   1   8\n", 
                "ATOM      8  C   LIG    1        3.838 -10.820  -4.065  0.00  0.00    +0.419 C \n", 
                "BRANCH   8   9\n", 
                "ATOM      9  O   LIG    1        2.755 -11.546  -4.613  0.00  0.00    -0.502 OA\n", 
                "ATOM     10  H   LIG    1        2.607 -12.287  -3.996  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8   9\n", 
                "BRANCH   8  11\n", 
                "ATOM     11  O   LIG    1        4.646 -11.757  -3.392  0.00  0.00    -0.502 OA\n", 
                "ATOM     12  H   LIG    1        5.312 -11.224  -2.925  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8  11\n", 
                "ENDBRANCH   1   8\n", 
                "TORSDOF 6\n", 
                "ENDMDL\n"
            ],
            "affinity" : "-4.7",
            "model_number" : "4"
        }, 
        {
            "rmsd_from_best" : [ 
                "8.084", 
                "9.714"
            ],
            "model" : [ 
                "MODEL 5\n", 
                "REMARK VINA RESULT:      -4.6      8.084      9.714\n", 
                "REMARK  Name = ZINC00000411\n", 
                "REMARK                            x       y       z     vdW  Elec       q    Type\n", 
                "REMARK                         _______ _______ _______ _____ _____    ______ ____\n", 
                "ROOT\n", 
                "ATOM      1  C   LIG    1      -11.346   4.960  -4.918  0.00  0.00    +0.240 C \n", 
                "ATOM      2  O   LIG    1      -11.654   6.160  -4.804  0.00  0.00    -0.287 OA\n", 
                "ENDROOT\n", 
                "BRANCH   1   3\n", 
                "ATOM      3  C   LIG    1      -10.927   4.336  -6.257  0.00  0.00    +0.189 C \n", 
                "ATOM      4  C   LIG    1      -11.396   5.171  -7.454  0.00  0.00    +0.046 C \n", 
                "BRANCH   3   5\n", 
                "ATOM      5  O   LIG    1      -11.228   2.944  -6.383  0.00  0.00    -0.369 OA\n", 
                "BRANCH   5   7\n", 
                "ATOM      6  C   LIG    1      -11.158   0.978  -7.781  0.00  0.00    +0.034 C \n", 
                "ATOM      7  C   LIG    1      -11.428   2.473  -7.715  0.00  0.00    +0.157 C \n", 
                "ENDBRANCH   5   7\n", 
                "ENDBRANCH   3   5\n", 
                "ENDBRANCH   1   3\n", 
                "BRANCH   1   8\n", 
                "ATOM      8  C   LIG    1      -11.344   4.019  -3.692  0.00  0.00    +0.419 C \n", 
                "BRANCH   8   9\n", 
                "ATOM      9  O   LIG    1      -10.249   3.124  -3.695  0.00  0.00    -0.502 OA\n", 
                "ATOM     10  H   LIG    1       -9.463   3.682  -3.545  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8   9\n", 
                "BRANCH   8  11\n", 
                "ATOM     11  O   LIG    1      -12.506   3.227  -3.609  0.00  0.00    -0.502 OA\n", 
                "ATOM     12  H   LIG    1      -12.735   3.022  -4.532  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8  11\n", 
                "ENDBRANCH   1   8\n", 
                "TORSDOF 6\n", 
                "ENDMDL\n"
            ],
            "affinity" : "-4.6",
            "model_number" : "5"
        }, 
        {
            "rmsd_from_best" : [ 
                "11.473", 
                "13.163"
            ],
            "model" : [ 
                "MODEL 6\n", 
                "REMARK VINA RESULT:      -4.4     11.473     13.163\n", 
                "REMARK  Name = ZINC00000411\n", 
                "REMARK                            x       y       z     vdW  Elec       q    Type\n", 
                "REMARK                         _______ _______ _______ _____ _____    ______ ____\n", 
                "ROOT\n", 
                "ATOM      1  C   LIG    1        3.253  -9.561  -3.345  0.00  0.00    +0.240 C \n", 
                "ATOM      2  O   LIG    1        3.978  -8.768  -2.717  0.00  0.00    -0.287 OA\n", 
                "ENDROOT\n", 
                "BRANCH   1   3\n", 
                "ATOM      3  C   LIG    1        2.224  -9.096  -4.386  0.00  0.00    +0.189 C \n", 
                "ATOM      4  C   LIG    1        1.463 -10.272  -5.009  0.00  0.00    +0.046 C \n", 
                "BRANCH   3   5\n", 
                "ATOM      5  O   LIG    1        2.734  -8.174  -5.353  0.00  0.00    -0.369 OA\n", 
                "BRANCH   5   7\n", 
                "ATOM      6  C   LIG    1        1.324  -6.468  -4.388  0.00  0.00    +0.034 C \n", 
                "ATOM      7  C   LIG    1        1.880  -7.074  -5.668  0.00  0.00    +0.157 C \n", 
                "ENDBRANCH   5   7\n", 
                "ENDBRANCH   3   5\n", 
                "ENDBRANCH   1   3\n", 
                "BRANCH   1   8\n", 
                "ATOM      8  C   LIG    1        3.367 -11.086  -3.128  0.00  0.00    +0.419 C \n", 
                "BRANCH   8   9\n", 
                "ATOM      9  O   LIG    1        2.967 -11.482  -1.830  0.00  0.00    -0.502 OA\n", 
                "ATOM     10  H   LIG    1        3.780 -11.807  -1.401  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8   9\n", 
                "BRANCH   8  11\n", 
                "ATOM     11  O   LIG    1        4.678 -11.567  -3.304  0.00  0.00    -0.502 OA\n", 
                "ATOM     12  H   LIG    1        4.695 -12.423  -2.844  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8  11\n", 
                "ENDBRANCH   1   8\n", 
                "TORSDOF 6\n", 
                "ENDMDL\n"
            ],
            "affinity" : "-4.4",
            "model_number" : "6"
        }, 
        {
            "rmsd_from_best" : [ 
                "8.117", 
                "9.474"
            ],
            "model" : [ 
                "MODEL 7\n", 
                "REMARK VINA RESULT:      -4.4      8.117      9.474\n", 
                "REMARK  Name = ZINC00000411\n", 
                "REMARK                            x       y       z     vdW  Elec       q    Type\n", 
                "REMARK                         _______ _______ _______ _____ _____    ______ ____\n", 
                "ROOT\n", 
                "ATOM      1  C   LIG    1      -11.378   5.093  -5.777  0.00  0.00    +0.240 C \n", 
                "ATOM      2  O   LIG    1      -11.371   6.284  -5.414  0.00  0.00    -0.287 OA\n", 
                "ENDROOT\n", 
                "BRANCH   1   3\n", 
                "ATOM      3  C   LIG    1      -11.555   3.929  -4.792  0.00  0.00    +0.189 C \n", 
                "ATOM      4  C   LIG    1      -11.205   4.331  -3.354  0.00  0.00    +0.046 C \n", 
                "BRANCH   3   5\n", 
                "ATOM      5  O   LIG    1      -10.941   2.705  -5.204  0.00  0.00    -0.369 OA\n", 
                "BRANCH   5   7\n", 
                "ATOM      6  C   LIG    1       -9.865   0.903  -4.011  0.00  0.00    +0.034 C \n", 
                "ATOM      7  C   LIG    1       -9.755   2.340  -4.498  0.00  0.00    +0.157 C \n", 
                "ENDBRANCH   5   7\n", 
                "ENDBRANCH   3   5\n", 
                "ENDBRANCH   1   3\n", 
                "BRANCH   1   8\n", 
                "ATOM      8  C   LIG    1      -11.232   4.715  -7.267  0.00  0.00    +0.419 C \n", 
                "BRANCH   8   9\n", 
                "ATOM      9  O   LIG    1      -12.192   3.762  -7.683  0.00  0.00    -0.502 OA\n", 
                "ATOM     10  H   LIG    1      -12.786   4.246  -8.287  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8   9\n", 
                "BRANCH   8  11\n", 
                "ATOM     11  O   LIG    1       -9.971   4.168  -7.571  0.00  0.00    -0.502 OA\n", 
                "ATOM     12  H   LIG    1       -9.977   4.046  -8.536  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8  11\n", 
                "ENDBRANCH   1   8\n", 
                "TORSDOF 6\n", 
                "ENDMDL\n"
            ],
            "affinity" : "-4.4",
            "model_number" : "7"
        }, 
        {
            "rmsd_from_best" : [ 
                "12.768", 
                "13.904"
            ],
            "model" : [ 
                "MODEL 8\n", 
                "REMARK VINA RESULT:      -4.3     12.768     13.904\n", 
                "REMARK  Name = ZINC00000411\n", 
                "REMARK                            x       y       z     vdW  Elec       q    Type\n", 
                "REMARK                         _______ _______ _______ _____ _____    ______ ____\n", 
                "ROOT\n", 
                "ATOM      1  C   LIG    1        3.875  -9.951  -2.283  0.00  0.00    +0.240 C \n", 
                "ATOM      2  O   LIG    1        4.395  -9.131  -1.505  0.00  0.00    -0.287 OA\n", 
                "ENDROOT\n", 
                "BRANCH   1   3\n", 
                "ATOM      3  C   LIG    1        2.372 -10.265  -2.272  0.00  0.00    +0.189 C \n", 
                "ATOM      4  C   LIG    1        1.966 -11.097  -1.049  0.00  0.00    +0.046 C \n", 
                "BRANCH   3   5\n", 
                "ATOM      5  O   LIG    1        1.864 -10.782  -3.504  0.00  0.00    -0.369 OA\n", 
                "BRANCH   5   7\n", 
                "ATOM      6  C   LIG    1        1.711  -9.006  -5.131  0.00  0.00    +0.034 C \n", 
                "ATOM      7  C   LIG    1        0.949  -9.936  -4.199  0.00  0.00    +0.157 C \n", 
                "ENDBRANCH   5   7\n", 
                "ENDBRANCH   3   5\n", 
                "ENDBRANCH   1   3\n", 
                "BRANCH   1   8\n", 
                "ATOM      8  C   LIG    1        4.722 -10.693  -3.340  0.00  0.00    +0.419 C \n", 
                "BRANCH   8   9\n", 
                "ATOM      9  O   LIG    1        4.270 -12.014  -3.571  0.00  0.00    -0.502 OA\n", 
                "ATOM     10  H   LIG    1        5.076 -12.563  -3.567  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8   9\n", 
                "BRANCH   8  11\n", 
                "ATOM     11  O   LIG    1        6.079 -10.794  -2.980  0.00  0.00    -0.502 OA\n", 
                "ATOM     12  H   LIG    1        6.236 -11.746  -2.856  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8  11\n", 
                "ENDBRANCH   1   8\n", 
                "TORSDOF 6\n", 
                "ENDMDL\n"
            ],
            "affinity" : "-4.3",
            "model_number" : "8"
        }, 
        {
            "rmsd_from_best" : [ 
                "7.235", 
                "8.937"
            ],
            "model" : [ 
                "MODEL 9\n", 
                "REMARK VINA RESULT:      -4.3      7.235      8.937\n", 
                "REMARK  Name = ZINC00000411\n", 
                "REMARK                            x       y       z     vdW  Elec       q    Type\n", 
                "REMARK                         _______ _______ _______ _____ _____    ______ ____\n", 
                "ROOT\n", 
                "ATOM      1  C   LIG    1      -11.307   4.178  -5.549  0.00  0.00    +0.240 C \n", 
                "ATOM      2  O   LIG    1      -11.508   5.142  -6.310  0.00  0.00    -0.287 OA\n", 
                "ENDROOT\n", 
                "BRANCH   1   3\n", 
                "ATOM      3  C   LIG    1      -10.684   2.859  -6.029  0.00  0.00    +0.189 C \n", 
                "ATOM      4  C   LIG    1      -11.231   2.427  -7.394  0.00  0.00    +0.046 C \n", 
                "BRANCH   3   5\n", 
                "ATOM      5  O   LIG    1      -10.691   1.811  -5.057  0.00  0.00    -0.369 OA\n", 
                "BRANCH   5   7\n", 
                "ATOM      6  C   LIG    1      -10.797  -0.532  -4.488  0.00  0.00    +0.034 C \n", 
                "ATOM      7  C   LIG    1      -10.484   0.495  -5.566  0.00  0.00    +0.157 C \n", 
                "ENDBRANCH   5   7\n", 
                "ENDBRANCH   3   5\n", 
                "ENDBRANCH   1   3\n", 
                "BRANCH   1   8\n", 
                "ATOM      8  C   LIG    1      -11.655   4.265  -4.046  0.00  0.00    +0.419 C \n", 
                "BRANCH   8   9\n", 
                "ATOM      9  O   LIG    1      -10.521   4.113  -3.215  0.00  0.00    -0.502 OA\n", 
                "ATOM     10  H   LIG    1      -10.879   3.958  -2.321  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8   9\n", 
                "BRANCH   8  11\n", 
                "ATOM     11  O   LIG    1      -12.579   3.283  -3.642  0.00  0.00    -0.502 OA\n", 
                "ATOM     12  H   LIG    1      -12.695   2.712  -4.421  0.00  0.00    +0.288 HD\n", 
                "ENDBRANCH   8  11\n", 
                "ENDBRANCH   1   8\n", 
                "TORSDOF 6\n", 
                "ENDMDL\n"
            ],
            "affinity" : "-4.3",
            "model_number" : "9"
        }
    ],
    "CPUs" : "1",
    "filename" : "rec_ZINC00000411_out.pdbqt",
    "docking_tool" : "AutoDock Vina",
    "receptor" : ObjectId("58cee516c831de22e1139792"),
    "date" : "2017-03-19",
    "config" : {
        "center_z" : "1.11111111111",
        "center_x" : "0.625",
        "center_y" : "0.541666666667",
        "size_x" : "3.01398888889",
        "size_y" : "1.18065555556",
        "size_z" : "1.7501",
        "exhaustiveness" : "8"
    }
}
    
    
    threshold -- threshold value (default -5.0)
            
    Returns:
    JSON response of the assessment including a flag: SUCCESSFUL or NOT_SUCCESSFULL     
    """
    # the json response
    to_return = {}
    to_return["data"] = {}
    # read the POST parameters. If any are missing return with a status 'fail' explaining the required parameter  
        
    docking_results = bottle.request.files.get("docking_results")
    if docking_results is None:
        to_return["status"] = "fail"
        to_return["data"]["docking_results"] = "Docking results required as a file, a POST parameter named 'docking_results'!"
        return to_return
    
    threshold = bottle.request.forms.get("threshold")
    if threshold is None:
        # threshold is optional default value is -5.0
        threshold = -5.0
        print "Threshold value hasn't been specified - using the default: -5.0"
    else:
        threshold = float(threshold)
        
    to_return["data"]["good"] = []
    
    # declare common file extensions
    zip_ext = ".zip"
    
    # if the docking results sent by POST are in the form of a zip file, extract it in 'docking_results_temp_dir'
    if docking_results.filename.endswith(zip_ext):
        
        # declare names of temporary directories where zip files will be unzipped
        temp_dir = "." + os.sep + "temp"    
        # make a temp directory first
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
            print temp_dir + " created \n"        
            
        docking_results_temp_dir = temp_dir + os.sep + "docking_results"
        
        # empty any temporary folder where the docking results will be unzipped (if one with this name exists)
        if os.path.exists(docking_results_temp_dir):    
            for receptor_file in os.listdir(docking_results_temp_dir):
                os.remove(docking_results_temp_dir + os.sep + receptor_file)        
        
        # if a directory with this name ('docking_results_temp_dir') doesn't exist, create it
        if not os.path.exists(docking_results_temp_dir):
            os.mkdir(docking_results_temp_dir)
            print docking_results_temp_dir + " created \n"
        
        print docking_results.filename + " is one file ending with " + zip_ext + " \n"
        with zipfile.ZipFile(docking_results.file) as docking_results_zip:
            docking_results_zip.extractall(docking_results_temp_dir)
            print docking_results.filename + " extracted in " + docking_results_temp_dir + " \n"
    
        # loop through all docking results stored on disk (can be 1 or more)
        for saved_results in os.listdir(docking_results_temp_dir):
            # run the docking assessor and store the results in to_return[data][assessed]
            assessor = at_assess.assess_docking.AssessDockingWithThreshold(docking_results_temp_dir + os.sep + saved_results, threshold)            
            to_return["data"]["good"].append( assessor.run() )
            
    #otherwise, the POST parameter is one json file (an array of json docking results)
    else:
        print docking_results.filename + " is one file containing all the docking results. \n"
        # save the file on the file system
#         docking_results.save(docking_results_temp_dir + os.sep + docking_results.filename)
#         print docking_results.filename + " saved as " + docking_results_temp_dir + os.sep + docking_results.filename + " \n"
        assessor = at_assess.assess_docking.AssessDockingWithThreshold(docking_results.file, threshold)            
        to_return["data"]["good"] = assessor.runFile() 
    
    
    
    # return the result of 'insert()' as json
    return to_return
    
bottle.run(host='localhost', port=8092, debug=True)
