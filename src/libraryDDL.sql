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
CREATE TYPE membership_type_enum AS ENUM ('Regular', 'Student', 'Senior Citizen', 'Other');
CREATE TYPE account_status_enum AS ENUM ('Active', 'Inactive');
CREATE TYPE availability_status_enum AS ENUM ('Available', 'Unavailable');

CREATE TABLE Client (
    -- Serial keyword handles both auto-increment and not null together.
    client_id SERIAL PRIMARY KEY CHECK (client_id > 0),
    -- Name is highlighted for me in VSCode as if its a keyword?
    name VARCHAR(50) NOT NULL,
    membership_type membership_type_enum NOT NULL,
    -- Enum isnt a default keyword. Whats a possible workaround?
    account_status account_status_enum NOT NULL,
    email_address VARCHAR(50) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE Media_Item (
    item_id SERIAL PRIMARY KEY CHECK (item_id > 0),
    -- This is definitely wrong as ENUM isnt defined, but it would resemble something like this.
    availability_status availability_status_enum NOT NULL
);

CREATE TABLE Book (
    item_id INT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn BIGINT NOT NULL UNIQUE CHECK (isbn >= 0),
    genre VARCHAR(50),
    publication_year INT,
    FOREIGN KEY (item_id) REFERENCES Media_Item(item_id) ON DELETE CASCADE
);

CREATE TABLE Digital_Media (

    /*
    NOTE: Exact copy of Book. If any changes are made to book, they should also be made here!
    */

    item_id INT PRIMARY KEY,
    FOREIGN KEY (item_id) REFERENCES Media_Item(item_id),
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    -- Would "bigint" or a "larger" int make sense? Is "int" large enough?
    isbn BIGINT NOT NULL UNIQUE CHECK (isbn >= 0),
    genre VARCHAR(50),
    publication_year INT
);

CREATE TABLE Magazine (
    item_id INT PRIMARY KEY,
    FOREIGN KEY (item_id) REFERENCES Media_Item(item_id),
    title VARCHAR(100) NOT NULL,
    -- DATE follows "yyyy-mm-dd" structure.
    publication_date DATE NOT NULL,
    issue_number INT NOT NULL
);

CREATE TABLE Transaction (
    transaction_id SERIAL PRIMARY KEY CHECK (transaction_id >= 0),
    date_borrowed TIMESTAMP NOT NULL,
    -- Not sure if the comparison of timestamps can be made in this manner, but thats the logic it should follow.
    expected_return_date TIMESTAMP NOT NULL CHECK (expected_return_date > date_borrowed),
    -- Ensures the return date of the item is either NULL or is after the date borrowed.
    returned_date TIMESTAMP CHECK (returned_date IS NULL OR returned_date > date_borrowed),
    client_id INT NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Client(client_id),
    FOREIGN KEY (item_id) REFERENCES Media_Item(item_id)
);