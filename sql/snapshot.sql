-- Create table for destination result
CREATE TABLE IF NOT EXISTS destination (
  "year" INTEGER,
  "month"	INTEGER,
  "branch_id" INTEGER,
  "salary_per_hour" NUMERIC(2)
);

-- Delete existing data
TRUNCATE destination;

-- Find the salary_per_hour
WITH timesheet_work_hour AS (
    SELECT
            employee_id
            ,EXTRACT( HOUR FROM ( checkout - checkin ) ) AS work_hour
            ,date AS record_date
        FROM
            timesheets
)
,month_salary_work_hour AS (
    SELECT
            m.employee_id
            ,e.branch_id
            ,EXTRACT( MONTH FROM record_date ) AS month
            ,EXTRACT( YEAR FROM record_date ) AS year
            ,e.salary
            ,SUM (
                CASE
                    WHEN work_hour IS NULL
                    OR work_hour < 0
                    THEN 8 -- median of the data "SELECT percentile_cont (0.50) within GROUP (ORDER by work_hour ASC) FROM work_hour"
                    ELSE work_hour
                END
            ) AS month_hour
        FROM
            timesheet_work_hour m LEFT JOIN employees e
                ON e.employee_id = m.employee_id
        WHERE
            m.record_date >= e.join_date
            AND (
                m.record_date <= e.resign_date
                OR e.resign_date IS NULL
            )
        GROUP BY
            1
            ,2
            ,3
            ,4
            ,5
)

-- Insert result to destination folder
INSERT INTO destination
SELECT
    year
    ,month
    ,branch_id
    ,SUM (salary) / SUM (month_hour) AS salary_per_hour
FROM
    month_salary_work_hour AS m
GROUP BY
    1
    ,2
    ,3