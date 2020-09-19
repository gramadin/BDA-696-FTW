/*
  Created by Ed Smythe Sept 2020
  BDA 696 @ SDSU
*/

-- make unique batter list
drop table if exists player_bat_avg;
create table player_bat_avg as
select unique batter from atbat_r order by batter;

-- make table to pull performance data from
drop table if exists player_bat_avg_all;
create table player_bat_avg_all as
select batter_counts.batter, hit, game.game_id,  game.local_date from batter_counts 
join game on batter_counts.game_id = game.game_id  
order by batter, game_id;

-- Make Report Table
drop table if exists REPORT;
create table REPORT as select distinct batter from player_bat_avg_all where batter = '400284';
alter table REPORT 
  add historic float
    after batter,
  add annual float 
    after historic,
  add rolling float
   after annual;
   
-- get specific batter performance
drop table if exists hist_calc;
create table hist_calc as
select batter, count(case when hit = 0 then 1 end) as hit, count(hit) as bat
from player_bat_avg_all
where batter = '400284';-- chg
/*this will turn into a user entered value in future iteration*/

-- Make report table
alter table hist_calc 
  add hist_avg float;
    
update hist_calc set hist_avg = (hit/bat) where batter = '400284'; -- chg
/*this will turn into a user entered value in future iteration*/

-- send results to report table
update REPORT , hist_calc
set REPORT.historic = hist_calc.hist_avg
where REPORT.batter = hist_calc.batter;

-- Make annual table
drop table if exists annual_calc;
create table annual_calc as
select batter, count(case when hit = 0 then 1 end) as hit_an , count(hit) as bat_an
from player_bat_avg_all
where batter = '400284' and local_date like'2011%';-- chg
/* these will turn into a user entered values in future iteration
   select max(local_date), min(local_date) from game
   Min = 2007-02-26 13:05:00 and max = 2012-06-28 22:15:00	*/

alter table annual_calc 
  add annual float
    after bat_an;

update annual_calc set annual_calc.annual = (hit_an/bat_an);

-- send results to report table
update REPORT , annual_calc
set REPORT.annual = annual_calc.annual
where REPORT.batter = annual_calc.batter;

-- Make rolling table
drop table if exists rolling_calc;
create table rolling_calc as
select batter, count(case when hit = 0 then 1 end) as hit_rol , count(hit) as bat_rol
from player_bat_avg_all
where batter = '400284' and local_date >= (('2012-01-01')- interval 100 day);/* chg */ /*these will turn into a user entered values in future iteration*/

alter table rolling_calc 
  add rolling float
    after bat_rol;

update rolling_calc set rolling_calc.rolling = (hit_rol/bat_rol);

-- send results to report table
update REPORT , rolling_calc
set REPORT.rolling = rolling_calc.rolling
where REPORT.batter = rolling_calc.batter;
select * from report ;