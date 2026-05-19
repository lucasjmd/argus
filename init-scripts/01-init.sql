CREATE DATABASE IF NOT EXISTS paysim;
USE paysim;

CREATE TABLE IF NOT EXISTS transactions (
    step INT,
    type VARCHAR(20),
    amount DECIMAL(15,2),
    nameOrig VARCHAR(20),
    oldbalanceOrg DECIMAL(15,2),
    newbalanceOrig DECIMAL(15,2),
    nameDest VARCHAR(20),
    oldbalanceDest DECIMAL(15,2),
    newbalanceDest DECIMAL(15,2),
    isFraud TINYINT(1),
    isFlaggedFraud TINYINT(1)
);

LOAD DATA INFILE '/var/lib/mysql-files/paysim_dataset.csv'
INTO TABLE transactions
FIELDS TERMINATED BY ','
IGNORE 1 LINES;
