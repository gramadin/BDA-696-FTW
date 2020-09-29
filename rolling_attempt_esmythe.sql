/*
  Created by Ed Smythe Sept 2020
  BDA 696 @ SDSU
  Current run time is ~ ? one month is < 10 seconds
  New Tables Created:
  --------------------------------------------
  prejoin	- Join player game average data on each other
  final_t	- Rolling table
  
  Currently runs longer than 30 min and no reults, but no errors.
*/

/* Comment lines below are from professor feed back*/

-- get a list of all the games and players in those games.
drop table if exists prejoin;
create table prejoin as
	select batter, game_id, Game_Date, game_bat_avg, date_sub(Game_Date, interval 100 DAY) as look_window 
	from player_bat_avg_all 
--    where Game_Date between cast('2009-08-01' as date) and cast('2009-09-01' as date) -- use to get a quick calc check
	order by batter;
-- for each of those rows, (playerid, game_id) join the table to itself 
-- then put a restriction on that join on the dates (you may have to rope in a date table).
drop table if exists final_t;
create table final_t as
	select prejoin.batter, prejoin.game_id, prejoin.Game_Date, prejoin.game_bat_avg, avg(rolling.game_bat_avg) as rolling_avg
	from prejoin
	join prejoin as rolling
		on prejoin.batter = rolling.batter and rolling.Game_Date between prejoin.look_window and prejoin.Game_Date
	group by prejoin.batter, game_id;
