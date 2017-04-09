# TreeBeard IDS

## Installation  
### Download Project & Install Dependencies
```
git clone https://github.com/iistyler/TreeBeard-IDS.git && cd TreeBeard-IDS  
virtualenv venv && source venv/bin/activate  
pip install -r requirements.txt 
```
  
### Download KDD datasets
Download the data from the KDD website. Note if you don't plan on training the neural networks downloading the training data is sufficient.

Download both files to Database folder

```
curl http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data_10_percent.gz > test.gz 
curl http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data.gz > train.gz

gunzip -k test.gz
gunzip -k train.gz
```

You should now have the data files test & train.

### Set up database
Add database credentials if different from current user to databaseLogin.py & Database/FileToDB.py

```
mysql -e "create database KDD"
mysql KDD < DATABASEFILE.sql

python Database/FileToDB.py
```

## Usage

Trained neural nets are stored in NetBinarySaves/
Schema for tree layout is located in XMLSchema/
Descriptions for neural nets to train are in JSONNetDesc/

The application will go through the tree schema and find any networks not saved in "NetBinarySaves" and train them based on the description located in "JSONNetDesc"

Note: When specifying files in arguments do not include file extensions

### Test tree nodes individually
Note: The number of threads can be changed in this file from the THREADS variable

```
python testingHandlerMultithreaded.py < Schema Name >
```

### Test records running through the entire tree one at a time
```
python singleTestingHandler.py < Schema Name >
```
