INSERT INTO Users (email_address, username, password) VALUES
	('pmadziak@conestogac.on.ca','sjones','pwd1'),
	('peter.madziak@gmail.com','lsmith','pwd2'),
	('bjulius5513@conestogac.on.ca','precious','pbkdf2:sha256:150000$7Xa8c3RT$3ff3560884c15b6cc8dfb21bf66d70d0cf399dd5553e50e13273d3a7494bff19');


INSERT INTO Patients (firstName, lastName) VALUES ('Anna', 'Jones');
INSERT INTO Patients (firstName, lastName) VALUES ('Allan', 'Smith');
INSERT INTO Patients (firstName, lastName) VALUES ('Alex', 'Smith');
INSERT INTO Patients (firstName, lastName) VALUES ('Allan', 'Smith');
INSERT INTO Patients (firstName, lastName) VALUES ('Andrea', 'Smith');
INSERT INTO Patients (firstName, lastName) VALUES ('Albie', 'Jones');
INSERT INTO Patients (firstName, lastName) VALUES ('Albie', 'Jones');
INSERT INTO Patients (firstName, lastName) VALUES ('Ahmed', 'Fahad');

INSERT INTO Measurements (systolic,diastolic,pulse,patient_id) VALUES (120,80,90,1);
INSERT INTO Measurements (systolic,diastolic,pulse,patient_id) VALUES (122,78,90,1);
