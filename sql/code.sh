#!/bin/sh

sleep 10

# Insert in the raw SQL data
if ! mysql -h db-container -uroot -psecret -e 'use baseball'; then
  mysql -h db-container -uroot -psecret -e "create database baseball;"
  mysql -h db-container -uroot -psecret -D baseball < /data/baseball.sql
fi

# Run your scripts
mysql -h db-container -uroot -psecret baseball < /scripts/sql_commands.sql

# Get results
mysql -h db-container -uroot -psecret baseball -e '
  SELECT * FROM rolling_100;' > /results/rolling.txt
