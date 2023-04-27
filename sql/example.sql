CREATE TABLE `CITIES` (
  `id_city` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `city_name` VARCHAR(50) NOT NULL
);

CREATE TABLE `PERSONS` (
  `id_person` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `person_identification` VARCHAR(30) UNIQUE NOT NULL,
  `person_identification_type` ENUM ('CITIZEN', 'FOREIGNER_ID', 'PASSPORT') NOT NULL,
  `first_name` VARCHAR(30) NOT NULL,
  `middle_name` VARCHAR(30),
  `last_name` VARCHAR(30) NOT NULL,
  `second_last_name` VARCHAR(30),
  `phone` VARCHAR(30) NOT NULL,
  `email` VARCHAR(50) UNIQUE NOT NULL,
  `address` VARCHAR(30) NOT NULL,
  `birthdate` DATE,
  `registration_date` DATETIME NOT NULL,
  `id_city` INTEGER NOT NULL,
);
