#!/bin/bash
docker-compose up -d
echo Please wait... Loading bbdb
sleep 10s
docker container exec -i db-container mysql bbdb < baseball.sql -ppass
echo Complete
docker exec -i db-container mysql bbdb -u root -ppass -e "drop table if exists rolling_100;"
echo Making rolling table
docker exec -i db-container mysql bbdb -u root -ppass -e ""
echo exporting
docker exec -it db-container bash -c 'mysql -h localhost -u root -ppass --database bbdb --batch -e "select batter,(sum(Hits)/sum(atbats)) as batavg from rolling_100 group by batter order by batter;"'  > report.txt
sed -e 's/\s\+/,/g' report.txt > report.csv
echo report.csv \&.txt created
echo shutting down
docker-compose down
sleep 5s
echo cleaning up
docker system prune -a
sleep 1s
y
echo have a nice day \:\)
