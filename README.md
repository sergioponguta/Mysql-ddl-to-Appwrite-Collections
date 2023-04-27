# MYSQL DDL TO APPWRITE CONVERTER

![Logo](/img/0.png)

## 📝 Description

This function will take an SQL file with DDL instructions for `MySQL` and convert it to a JSON file that can be used to create collections in [Appwrite](https://github.com/appwrite).

This gonna help you to use your existing database model, or DDL script, to create collections in Appwrite.

At the moment it converts tables, columns, primary keys and unique constraints. Also `NOT NULL` as required fields, also supports numeric types, strings, and dates.

> At this moment, `collections_id` will be the same as the table name in lowercase, and `collection_name` will be the same as the table name in uppercase.

## 🚀 How to use it

Just put your SQL file in the `sql` folder and run the function. The output will be a JSON file in the `json` folder with the same name as the SQL file.

You can also modify `DB_ID` constant in `main.py` to change the id of the database in the JSON file.

**Expected format** (`ALTER TABLE` if present, will be ignored):

```sql

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
```

## 👉 Example

There is already an example inside the `sql` folder. It's a file with the DDL instructions. If you run the function, you will get a JSON file in the `json` folder with the same name as the SQL file.

## 🤖 Recommendations

To create the database model I have use this website [dbdiagram.io](https://dbdiagram.io/home). It's a great tool to create database models and export them to SQL files.

You can upload existing models to the website or create your own. Then you can export the model to a `MySQL` script and use it with this function.

![Download](/img/1.png)

## ✅ TODO

- [x] Convert DDL to JSON
- [x] Add support for MySQL
- [x] Convert single primary keys to indexes
- [x] Convert single unique contraints to indexes
- [x] Not null as required fields
- [ ] Support all datatypes
- [ ] Suport composite primary keys
- [ ] Suport composite unique contraints
- [ ] Add support for other databases
- [ ] Add support for Appwrite relationships
