USE bpdb0;

CREATE TABLE Measurements
(
    id INT NOT NULL AUTO_INCREMENT,
    systolic INT NOT NULL,
    diastolic INT NOT NULL,
    time_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

