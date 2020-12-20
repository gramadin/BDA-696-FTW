#!/usr/bin/env bash

FILE=baseball.sql
if [ -f "$FILE" ]; then
    echo "$FILE loading..."
else
  echo "$FILE getting..."
  curl -O https://teaching.mrsharky.com/data/baseball.sql.tar.gz
  tar -xvzf baseball.sql.tar.gz
fi

sleep 10

# Insert in the raw SQL data
if ! mysql -h db-container -uuser -ppass -e 'use baseball'; then			# pragma: allowlist secret
  mysql -h db-container -uuser -ppass -e "create database baseball;"		# pragma: allowlist secret
  mysql -h db-container -uuser -ppass -D baseball < /data/baseball.sql		# pragma: allowlist secret
fi

# Run your scripts
mysql -h db-container -uuser -ppass baseball < /fix_stolen_bases.sql.sql	# pragma: allowlist secret
mysql -h db-container -uuser -ppass baseball < /circadian.sql				# pragma: allowlist secret
mysql -h db-container -uuser -ppass baseball < /net_jet_lag.sql				# pragma: allowlist secret
mysql -h db-container -uuser -ppass baseball < /team_rolling_14.sql			# pragma: allowlist secret
mysql -h db-container -uuser -ppass baseball < /team_rolling_30.sql			# pragma: allowlist secret
mysql -h db-container -uuser -ppass baseball < /team_rolling_90.sql			# pragma: allowlist secret
mysql -h db-container -uuser -ppass baseball < /team_rolling_180.sql		# pragma: allowlist secret


# Get results running python code
mysql -h db-container -uuser -ppass baseball -e 							# pragma: allowlist secret

echo This dosen\'t work\, but have a nice day \:\) 