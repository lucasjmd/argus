-- Database initialisation for argus transaction validator engine
CREATE DATABASE IF NOT EXISTS paysim;
USE paysim;

-- Transaction records to be populated with pipeline
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

-- Adding indexing to optimise API lookup performance
ALTER TABLE transactions ADD INDEX idx_name_orig (nameOrig);

-- User accounts for API JWT auth
CREATE TABLE IF NOT EXISTS api_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL
);