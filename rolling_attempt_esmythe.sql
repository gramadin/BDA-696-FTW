/*
  Created by Ed Smythe Sept 2020
  BDA 696 @ SDSU
  Current run time is ~ ?
  New Tables Created:
  --------------------------------------------
  self_join_test	- Join player game average data on each other
  
  Currently runs longer than 30 min and no reults, but no errors.
*/

/* Comment lines below are from professor feed back*/

-- get a list of all the games and players in those games.
drop table if exists self_join_test;
create table self_join_test as
select distinct batter, game_id, Game_Date, game_bat_avg, date_sub(Game_Date, interval 100 DAY) as look_window from player_bat_avg_all
order by batter ;
-- for each of those rows, (playerid, game_id) join the table to itself 
-- then put a restriction on that join on the dates (you may have to rope in a date table).
select self_join_test.Game_Date, self_join_test.game_bat_avg, avg(rolling_self_join_test.game_bat_avg)
from self_join_test
join self_join_test as rolling_self_join_test
	on rolling_self_join_test.Game_Date between self_join_test.Game_Date - 99 and self_join_test.Game_Date
group by batter, game_id
