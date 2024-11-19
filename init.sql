CREATE TABLE IF NOT EXISTS meter_readings (
    personal_account INTEGER PRIMARY KEY, 
    address VARCHAR(255),               
    meter INTEGER                 
);

INSERT INTO meter_readings
VALUES
(1, 'Советская, 1', 12),
(2, 'Советская, 2', 45),
(3, 'Советская, 3', 34)
