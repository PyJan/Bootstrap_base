sudo apt-get install postgresql

sudo su postgres # postgres is default user for postgresql

psql -d postgres -U postgres # log in the DB

CREATE USER myuser WITH PASSWORD 'mypassword';

ALTER USER myuser WITH PASSWORD 'newpassword';

CREATE DATABASE myapp;

\c myapp

REVOKE ALL ON DATABASE myapp FROM PUBLIC; # remove access 

REVOKE ALL ON SCHEMA public FROM PUBLIC;

du # database users

GRANT CONNECT ON DATABASE myapp to app_ro; 

\l # access privilages

GRANT SELECT ON ALL TABLES IN SCHEMA public to app_ro;

GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public to app_rw;

CREATE TABLE test(id serial, name varchar(40));

GRANT SELECT ON ALL SEQUENCES IN SCHEMA public to app_rw;

GRANT USAGE ON SCHEMA public to app_rw;

\z

