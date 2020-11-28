docker-compose up -d
echo Please wait...
docker container exec -i db-container mysql bbdb < baseball.sql -ppass
echo Complete