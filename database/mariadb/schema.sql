USE bpdb0;

DROP TABLE IF EXISTS Measurements;

CREATE TABLE Measurements(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    systolic INT NOT NULL,
    diastolic INT NOT NULL,
    pulse INT NOT NULL,
    time_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

