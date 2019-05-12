# NB: Supplementary Data
The Supplementary Data extracted from my PhD thesis are located in the branch `mdrr-dm`, in the folder SupplementaryData. The remainder of that branch and the other branches contain the code, as described below.

# mdrr-scenarios
The needed elements for three scenarios that use the MDRR. In all scenarios the element MDE is the extended version of Raccoon2 which can be found in the repository named Raccoon2 branch `mdrr`: https://github.com/damjanmk/Raccoon2.


## Description

This repository contains the implementations of elements (apart from MDE) required to run three scenarios:
- Scenario_1: Suggest a ligand-protein pair that should be used in the next molecular docking, based on protein similarity and previous results
- Scenario_2: Filter results which are suitable for laboratory experiments, based on ligand properties
- Scenario_4: Enable verication of the simulation methodology and learning from previous docking


## Prerequisits

The elements are grouped into servers with the help of the Python library called Bottle (http://bottlepy.org/docs/dev/). In order to install Bottle you can use pip:
`pip install bottle`

The Python library for HTTP communication called Requests (http://docs.python-requests.org/en/master/user/install/) is also needed:
`python -m pip install requests`

The MDRR uses MonogDB as the database where it stores docking results, input files and keeps track of all the steps in a scenario. In order to install MongoDB please consult https://docs.mongodb.com/manual/installation/. To install it on Ubuntu you may use
`sudo apt-get install mongodb-org`

Then in order to start the mongod service you may use
`sudo service mongod start`
To stop it, you may use 
`sudo service mongod stop`

The MDRR requires the PyMongo Python library (http://api.mongodb.com/python/current/installation.html), which can be installed using
`python -m pip install pymongo`

The example database full of docking results can be downloaded from the mdrr-dm branch: `testMDRR/mongodb-small-2018-25-04_13-14.archive.gz`

Once you have donwloaded this file, you may load the data into the MongoDB. You need to open the terminal, change directory to ...testMDRR, and then from the OS terminal (not the mongo console) run:
`mongorestore db=mdrr_small mongodb-small-2018-25-04_13-14.archive.gz`




## User Manual

This repository contains 5 unrelated branches (a.k.a. orphan branches). Each branch represents a separate bottle server:

* mdrr-dm: Server containing the MDRR (folder 'main/mdrr') and DM (folder 'main/dm'). The logic for running the elements on the server is in 'main/controller.py'
* assess-docking: Server containing the AT AssessDocking (folder 'main/at_assess'). The logic for running the element on the server is in 'main/controller.py'
* compare-config: Server containing the AT CompareConfig (folder 'main/at_assess'). The logic for running the element on the server is in 'main/controller.py'
* deep-align: Server containing the AT DeepAlign (folder 'main/at') and the AT AssessDeepAlign (folder 'main/at_assess'). The logic for running the elements on the server is in 'main/controller.py'
* ligsift: Server containing the AT LIGSIFT (folder 'main/at') and the AT AssessLIGSIFT (folder 'main/at_assess'). The logic for running the elements on the server is in 'main/controller.py'

To test each of the servers on Linux firstly clone all branches in this repository using
```bash
mkdir test-damjans-implementations
cd test-damjans-implementations
git clone -b mdrr-dm https://github.com/damjanmk/mdrr-scenarios.git
mv mdrr-scenarios/ mdrr-dm/
```
```bash
git clone -b assess-docking https://github.com/damjanmk/mdrr-scenarios.git
mv mdrr-scenarios/ assess-docking/
```
```bash
git clone -b compare-config https://github.com/damjanmk/mdrr-scenarios.git
mv mdrr-scenarios/ compare-config/
```
```bash
git clone -b deep-align https://github.com/damjanmk/mdrr-scenarios.git
mv mdrr-scenarios/ deep-align/
```
```bash
git clone -b ligsift https://github.com/damjanmk/mdrr-scenarios.git
mv mdrr-scenarios/ ligsift/
```

You may want to run tests on each branch. The procedure for this is the same in all branches (apart from the branch mdrr-dm). You can firstly:
```bash
cd ...assess-docking/
python main/controller.py
```
Secondly, in another terminal window:
```bash
cd ...assess-docking/test/
python testREST.py
```
You may use an equivalent method for the other branches as they all contain the file test/testREST.py

The branch mdrr-dm is a little different. It contains the folder testMDRR/ where you will find the files 
- `testREST_scenario1_SuggestNext.py`
- `testREST_scenario2_Consult_A.py`
- `testREST_scenario2_Consult_B.py`
- `testREST_scenario4_Verify.py`

Running each of these will test each scenario (there are two versions for scenario 2, A if the docking results have been inserted into the MongoDB database before, and B if they have not been inserted). Before you run these scripts you have to have an active server for each branch that is needed based on the scenario. Namely you will need to run:

- `assess-docking, deep-align` for scenario 1
- `assess-docking` for scenario 2
- `assess-docking, deep-align, ligsift` for scenario 4

To be safe, you could run a server per each branch in a separate terminal window using `python main/controller.py` as explained above. Once you all the needed servers are active run

```bash
cd ...mdrr-dm/testMDRR/
python testREST_scenario1_SuggestNext.py
```
or analogously for the other scenarios.


The code snippets to help you install the implementations have been tested in the Ubuntu 17.04 flavour of GNU/Linux. If you need help with other operating systems, please let me know.

Please feel free to write an issue if you have any problems or suggestions.

Regards,
Damjan
