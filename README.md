# Code Challenge: Salary per hour

Mekari Data Engineer submission

## How to setup database
1. Deploy postgresql instance with docker. It will create new database `employee` with `user:password` as credential
```sh
docker compose -f docker-compose.yaml up -d
```
2. Download the sample data, it will download the csv file and save to `data/` folder
```sh
./prepare_data.sh
```
3. Ingest the initial data
```sh
psql -1 -U user -d employee -h localhost -W -a -f ./sql/ingest_data.sql
```
Command explanation:
- `-1` for single transaction
- `-U user` for select user as username
- `-d employee` for select database employee
- `-W` for using password
- `-a` for print the query to stdout
- `-f` for select sql file

## SQL Task
1. Run this command to get snapshot from table
```sh
psql -1 -U user -d employee -h localhost -W -a -f ./sql/snapshot.sql
```

## Python Task
1. Run this command to calculate and save data to db
```sh
python3 main.py --start-date 2019-01-01 --database employee
```
Note: `start-date` params can be used as parameter for daily pipeline