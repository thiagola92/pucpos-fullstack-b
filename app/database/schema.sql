DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS persons;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS properties;
DROP TABLE IF EXISTS property_owners;

CREATE TABLE accounts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT UNIQUE NOT NULL,
  phone TEXT UNIQUE
);

CREATE TABLE persons (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER,
  fullname TEXT NOT NULL,
  cpf TEXT,

  FOREIGN KEY(account_id) REFERENCES accounts(id)
);

CREATE TABLE addresses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  country TEXT NOT NULL,
  state TEXT NOT NULL,
  city TEXT NOT NULL,
  street TEXT NOT NULL,
  house_number INTEGER NOT NULL,
  extra TEXT
);

CREATE TABLE properties (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address_id INTEGER,

  FOREIGN KEY(address_id) REFERENCES addresses(id)
);

CREATE TABLE property_owners (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  person_id INTEGER,
  property_id INTEGER,

  FOREIGN KEY(person_id) REFERENCES persons(id),
  FOREIGN KEY(property_id) REFERENCES properties(id)
);

