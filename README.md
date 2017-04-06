# TreeBeard IDS

## Installation  
### Download Project & Install Dependencies
```
git clone https://github.com/iistyler/TreeBeard-IDS.git && cd TreeBeard-IDS  
virtualenv venv && source venv/bin/activate  
pip install -r requirements.txt 
```
  
### Download KDD datasets:  
Download the data from the KDD website. Note if you don't plan on training the neural networks downloading the 
training data is sufficient.  

```
curl http://kdd.ics.uci.edu/databases/kddcup99/corrected.gz > test.gz
curl http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data.gz > train.gz

gunzip -k test.gz
gunzip -k train.gz
```  

You should now have the data files test & train.

### Set up database
```
mysql -e "create database KDD"
mysql KDD < DATABASEFILE.sql
TODO: ADD AUTOMATED SCRIPT
```

## Usage  

