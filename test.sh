docker-compose up -d
echo Please wait...
docker container exec -i db-container mysql bbdb < baseball.sql -ppass
echo Complete
mysqld -u root -ppass -e "drop table if exists rolling_100;"
mysqld -u root -ppass -e "create table rolling_100 as

	select 
		g.game_id
		, g.local_date
		, bc.batter
		, sum(bc.atBat) as atbats
		, sum(bc.Hit) as Hits
		, count(*) as chk
		
	from batter_counts bc
	join game g on g.game_id = bc.game_id
	join batter_counts bc1 on bc.batter = bc1.batter
	join game g1 on g1.game_id = bc1.game_id and
		g.local_date >= date_add(g.local_date, interval -100 day) 
	where g.local_date < '2011-04-04 15:05:00' and bc.batter in (select batter from batter_counts bc2 where game_id = '12560')
	group by batter, g.game_id
	order by batter;"
	
docker exec -it db-container bash -c 'mysqld -h . -u root -ppass --database sample --batch -e "select 
	batter
	,(sum(Hits)/sum(atbats)) as batavg
from rolling_100 
group by batter 
order by batter;"'   > sed 's/\t/","/g;s/^/"/;s/$/"/;s/\n//' > report.csv
