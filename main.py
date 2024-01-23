import argparse
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine


def process_data(start_date):
    # Load and preprocess data
    employees = pd.read_csv("./data/employees.csv")
    employees["join_date"] = pd.to_datetime(employees["join_date"])
    employees["resign_date"] = pd.to_datetime(employees["resign_date"])

    # Load and preprocess data
    timesheets = pd.read_csv("./data/timesheets.csv")
    timesheets["checkin"] = pd.to_datetime(timesheets["checkin"])
    timesheets["checkout"] = pd.to_datetime(timesheets["checkout"])
    timesheets["month"] = pd.to_datetime(timesheets["date"]).dt.month
    timesheets["year"] = pd.to_datetime(timesheets["date"]).dt.year

    # Fill na or negative value to median
    timesheets["work_hour"] = (
        timesheets["checkout"] - timesheets["checkin"]
    ).dt.components["hours"]
    median_value = timesheets["work_hour"].median()

    timesheets["work_hour"] = timesheets["work_hour"].fillna(median_value)
    timesheets["work_hour"][timesheets["work_hour"] < 0] = median_value

    # Merged two dataset and find the correct answer
    df_merged = pd.merge(
        timesheets, employees, how="left", left_on="employee_id", right_on="employe_id"
    )

    # Edge case if date is before join_date
    df_merged = df_merged[
        (df_merged["date"] >= df_merged["join_date"])
        & (df_merged["date"] >= start_date)
    ]
    # TODO: filter for edge case resign_date

    df_processed = (
        df_merged[["employee_id", "year", "month", "branch_id", "work_hour", "salary"]]
        .groupby(["month", "year", "branch_id", "salary"])
        .sum()
        .reset_index()
    )
    df_processed = (
        df_processed[["year", "month", "branch_id", "salary", "work_hour"]]
        .groupby(["year", "month", "branch_id"])
        .sum()
        .reset_index()
    )
    df_processed["salary_per_hour"] = (
        df_processed["salary"] / df_processed["work_hour"]
    )

    return df_processed.drop(columns=["salary", "work_hour"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="Database username", default="user")
    parser.add_argument("--password", help="Database password", default="password")
    parser.add_argument("--host", help="Database host", default="localhost")
    parser.add_argument("--port", help="Database port", default="5432")
    parser.add_argument("--database", help="Database database", default="default")
    parser.add_argument(
        "--start-date",
        help="Filter start date",
        default=datetime.now().strftime("%Y-%m-%d"),
    )

    args = parser.parse_args()

    username = args.username
    password = args.password
    host = args.host
    port = args.port
    database = args.database
    start_date = args.start_date

    result = process_data(start_date)

    engine = create_engine(
        f"postgresql://{username}:{password}@{host}:{port}/{database}"
    )

    result.to_sql(name="destination", con=engine, index=False, if_exists="append")
