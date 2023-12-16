CREATE TABLE User (
    U_id VARCHAR(255) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nationality VARCHAR(255),
    date_of_birth DATE
);
INSERT INTO User (U_id, full_name, email, password, nationality, date_of_birth)
VALUES ('john_doe', 'John Doe', 'john@example.com', 'password123', 'USA', '1990-01-01');
 
CREATE TABLE Learner (
    U_id VARCHAR(255) PRIMARY KEY,
    learning_style VARCHAR(255),
    learning_objective TEXT,
    FOREIGN KEY (U_id) REFERENCES User(U_id)
);

-- Teacher tablosu
CREATE TABLE Teacher (
    U_id INT PRIMARY KEY,
    fee_per_hour DECIMAL(10, 2) NOT NULL,
    experience VARCHAR(255),
    FOREIGN KEY (U_id) REFERENCES User(U_id)
);

-- Administrator tablosu
CREATE TABLE Administrator (
    U_id INT PRIMARY KEY,
    FOREIGN KEY (U_id) REFERENCES User(U_id)
);

-- Learner tablosu