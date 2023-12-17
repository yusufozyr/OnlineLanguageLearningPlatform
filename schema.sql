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
-- Learner tablosu
CREATE TABLE Learner (
    U_id VARCHAR(255) PRIMARY KEY,
    learning_style VARCHAR(255),
    learning_objective TEXT,
    FOREIGN KEY (U_id) REFERENCES User(U_id)
);

-- Teacher tablosu
CREATE TABLE Teacher (
    U_id VARCHAR(255) PRIMARY KEY,
    fee_per_hour DECIMAL(10, 2) NOT NULL,
    experience VARCHAR(255),
    FOREIGN KEY (U_id) REFERENCES User(U_id)
);

-- Administrator tablosu
CREATE TABLE Administrator (
    U_id VARCHAR(255) PRIMARY KEY,
    FOREIGN KEY (U_id) REFERENCES User(U_id)
);

CREATE TABLE Language (
    Language_id INT AUTO_INCREMENT PRIMARY KEY,
    Language_name VARCHAR(255) NOT NULL,
    Language_level VARCHAR(2) NOT NULL
);

CREATE TABLE Current_Level (
    Language_id INT,
    U_id VARCHAR(255),
    PRIMARY KEY (Language_id, U_id),
    FOREIGN KEY (Language_id) REFERENCES Language(Language_id),
    FOREIGN KEY (U_id) REFERENCES User(U_id)
);
CREATE TABLE Goal_Level (
    Language_id INT,
    U_id VARCHAR(255),
    PRIMARY KEY (Language_id, U_id),
    FOREIGN KEY (Language_id) REFERENCES Language(Language_id),
    FOREIGN KEY (U_id) REFERENCES User(U_id)
);

-- Inserting a new User (Learner)
INSERT INTO User (U_id, full_name, email, password, nationality, date_of_birth)
VALUES ('learner1', 'Learner One', 'learner1@example.com', 'password123', 'NationalityLearner', '2000-01-01');

-- Inserting a new User (Teacher)
INSERT INTO User (U_id, full_name, email, password, nationality, date_of_birth)
VALUES ('teacher1', 'Teacher One', 'teacher1@example.com', 'password456', 'NationalityTeacher', '1980-01-01');

-- Inserting a new User (Administrator)
INSERT INTO User (U_id, full_name, email, password, nationality, date_of_birth)
VALUES ('admin1', 'Administrator One', 'admin1@example.com', 'admin123', 'NationalityAdmin', '1970-01-01');

-- Inserting a new Learner
INSERT INTO Learner (U_id, learning_style, learning_objective) 
VALUES ('learner1', 'Visual Learning', 'Improve problem-solving skills');

-- Inserting a new Teacher
INSERT INTO Teacher (U_id, fee_per_hour, experience) 
VALUES ('teacher1', 30.00, '5 years ');

-- Inserting a new Administrator
INSERT INTO Administrator (U_id)
VALUES ('admin1');


-- Language table


-- Insert data into Language table
INSERT INTO Language (Language_name, Language_level) VALUES
    ('English', 'A1'),
    ('English', 'A2'),
    ('English', 'B1'),
    ('English', 'B2'),
    ('English', 'C1'),
    ('English', 'C2'),
    ('German', 'A1'),
    ('German', 'A2'),
    ('German', 'B1'),
    ('German', 'B2'),
    ('German', 'C1'),
    ('German', 'C2'),
    ('Italian', 'A1'),
    ('Italian', 'A2'),
    ('Italian', 'B1'),
    ('Italian', 'B2'),
    ('Italian', 'C1'),
    ('Italian', 'C2'),
    ('Japanese', 'A1'),
    ('Japanese', 'A2'),
    ('Japanese', 'B1'),
    ('Japanese', 'B2'),
    ('Japanese', 'C1'),
    ('Japanese', 'C2'),
    ('Spanish', 'A1'),
    ('Spanish', 'A2'),
    ('Spanish', 'B1'),
    ('Spanish', 'B2'),
    ('Spanish', 'C1'),
    ('Spanish', 'C2'),
    ('Arabic', 'A1'),
    ('Arabic', 'A2'),
    ('Arabic', 'B1'),
    ('Arabic', 'B2'),
    ('Arabic', 'C1'),
    ('Arabic', 'C2'),
    ('Turkish', 'A1'),
    ('Turkish', 'A2'),
    ('Turkish', 'B1'),
    ('Turkish', 'B2'),
    ('Turkish', 'C1'),
    ('Turkish', 'C2'),
    ('French', 'A1'),
    ('French', 'A2'),
    ('French', 'B1'),
    ('French', 'B2'),
    ('French', 'C1'),
    ('French', 'C2'),
    ('Russian', 'A1'),
    ('Russian', 'A2'),
    ('Russian', 'B1'),
    ('Russian', 'B2'),
    ('Russian', 'C1'),
    ('Russian', 'C2');
