CREATE USER 'bpapp0'@'localhost' IDENTIFIED BY 'conestogahi';
GRANT ALL PRIVILEGES ON bpdb0.* TO 'bpapp0'@'localhost' WITH GRANT OPTION;

-- old approach:
--GRANT ALL PRIVILEGES ON bpdb0.* TO 'bpapp0'@'localhost' IDENTIFIED BY 'conestogahi';

-- and to drop:
--DROP USER 'bpapp0'@'localhost';
