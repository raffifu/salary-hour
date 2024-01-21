-- Create table for employees data
CREATE TABLE employees (
  "employee_id" INTEGER NOT NULL,
  "branch_id" INTEGER NOT NULL,
  "salary" INTEGER NOT NULL,
  "join_date" DATE NOT NULL,
  "resign_date" DATE
);

-- Create table for timesheets
CREATE TABLE timesheets (
  "timesheet_id" INTEGER NOT NULL,
  "employee_id"	INTEGER NOT NULL, 
  "date" DATE NOT NULL,
  "checkin" TIME,
  "checkout" TIME
);

-- Ingest Data Employees client side
\copy employees("employee_id", "branch_id", "salary", "join_date", "resign_date") from 'data/employees.csv' with csv header delimiter ',';

-- Ingest Data timesheets client side
\copy timesheets("timesheet_id", "employee_id", "date", "checkin", "checkout") from 'data/timesheets.csv' with csv header delimiter ',';

