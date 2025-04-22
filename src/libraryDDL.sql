/*
Author: Blake Carlson
Date 4/14/25
Filename: libraryDDL.sql
Purpose: SQL file containing the DDL for the library database

The tables that will need to be created are:
    Client
    Transaction
    Media_Item
    Book
    Magazine
    Digital_Media

- Blake 4/14/25
    Added the code that would create the relations in the database, with their attributes and associated constraints.
    I am not very confident the syntax is fully correct, but the logic of everything should be pretty clear with some specific things pointed out in comments.

    Does cascading need to be implemented? 
    I'm assuming it doesn't, but lets say a book is damaged and gets removed from the database.
    Should the transaction history of it should remain? And its item_id is still reserved to it?
    Something to consider?
*/

-- Define ENUMs
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'membership_type_enum') THEN
        CREATE TYPE membership_type_enum AS ENUM ('Regular', 'Student', 'Senior Citizen', 'Other');
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'account_status_enum') THEN
        CREATE TYPE account_status_enum AS ENUM ('Active', 'Suspended', 'Inactive');
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'availability_status_enum') THEN
        CREATE TYPE availability_status_enum AS ENUM ('Available', 'Unavailable');
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS Client (
    client_id SERIAL PRIMARY KEY CHECK (client_id > 0),
    name VARCHAR(50) NOT NULL,
    membership_type membership_type_enum NOT NULL,
    account_status account_status_enum NOT NULL,
    email_address VARCHAR(50) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Media_Item (
    item_id SERIAL PRIMARY KEY CHECK (item_id > 0),
    availability_status availability_status_enum NOT NULL
);

CREATE TABLE IF NOT EXISTS Book (
    item_id INT PRIMARY KEY,
    FOREIGN KEY (item_id) REFERENCES Media_Item(item_id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) NOT NULL UNIQUE CHECK (isbn <> '0' AND isbn ~ '[1-9]'),
    genre VARCHAR(50),
    publication_year INT
);

CREATE TABLE IF NOT EXISTS Digital_Media (
    item_id INT PRIMARY KEY,
    FOREIGN KEY (item_id) REFERENCES Media_Item(item_id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) NOT NULL UNIQUE CHECK (isbn <> '0' AND isbn ~ '[1-9]'),
    genre VARCHAR(50),
    publication_year INT
);


CREATE TABLE IF NOT EXISTS Magazine (
    item_id INT PRIMARY KEY,
    FOREIGN KEY (item_id) REFERENCES Media_Item(item_id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    publication_date DATE NOT NULL,
    issue_number INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Transaction (
    transaction_id SERIAL PRIMARY KEY CHECK (transaction_id >= 0),
    client_id INT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Client(client_id),
    item_id INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Media_Item(item_id),
    date_borrowed TIMESTAMP NOT NULL,
    expected_return_date TIMESTAMP NOT NULL CHECK (expected_return_date > date_borrowed),
    returned_date TIMESTAMP CHECK (returned_date IS NULL OR returned_date > date_borrowed)
);