/*
  Created by Ed Smythe Sept 2020
  BDA 696 @ SDSU
  Current run time is ~ 12.605s
  New Tables Created:
  player_bat_avg 		-Unique player numbers
  player_bat_avg_all	-Batting Average for all players by game
  REPORT				-Each player with historic and annual averages for all years in data
  hist_calc				-holds historic calculated data
  annual_calc			-holds annual calculated data
*/

-- make unique batter list
drop table if exists player_bat_avg;
create table player_bat_avg as
	select unique batter from atbat_r order by batter;

	alter table player_bat_avg add primary key (batter);

-- make table to pull performance data from
drop table if exists player_bat_avg_all;
create table player_bat_avg_all as
	select batter_counts.game_id , batter , atBat, Hit , left(game.local_date,10) as Game_Date, (Hit/nullif(atBat,0)) as game_bat_avg
	from batter_counts 
	join game using (game_id)-- batter_counts.game_id = game.game_id  
	order by batter, game_id;

	alter table player_bat_avg_all add primary key (batter, game_id);

-- Make Report Table
drop table if exists REPORT;
create table REPORT as select batter from player_bat_avg;
	alter table REPORT 
	  add Historic float
	    after batter,
	  add _2007_ float 
	    after Historic,
	  add _2008_ float 
	    after _2007_,
	  add _2009_ float 
	    after _2008_,
	  add _2010_ float 
	    after _2009_,
	  add _2011_ float 
	    after _2010_,
	  add _2012_ float 
	    after _2011_;

	alter table REPORT add primary key (batter);
  
-- Make Histroic avg table and update REPORT
drop table if exists hist_calc;
create table hist_calc as
	select batter, avg(game_bat_avg) as hist_avg from player_bat_avg_all group by batter;

	update REPORT , hist_calc
	set REPORT.historic = hist_calc.hist_avg
	where REPORT.batter = hist_calc.batter;

-- Make Annual Avg table and update REPORT
drop table if exists annual_calc;
create table annual_calc as
	select batter, left(player_bat_avg_all.Game_Date,4) as Game_Yr, avg(game_bat_avg) as ann_avg from player_bat_avg_all group by batter, Game_Yr;

	update REPORT, annual_calc 
	set report._2007_ = annual_calc.ann_avg
	where REPORT.batter = annual_calc.batter and annual_calc.Game_Yr = '2007';
	update REPORT, annual_calc 
	set report._2008_ = annual_calc.ann_avg
	where REPORT.batter = annual_calc.batter and annual_calc.Game_Yr = '2008';
	update REPORT, annual_calc 
	set report._2009_ = annual_calc.ann_avg
	where REPORT.batter = annual_calc.batter and annual_calc.Game_Yr = '2009';
	update REPORT, annual_calc 
	set report._2010_ = annual_calc.ann_avg
	where REPORT.batter = annual_calc.batter and annual_calc.Game_Yr = '2010';
	update REPORT, annual_calc 
	set report._2011_ = annual_calc.ann_avg
	where REPORT.batter = annual_calc.batter and annual_calc.Game_Yr = '2011';
	update REPORT, annual_calc 
	set report._2012_ = annual_calc.ann_avg
	where REPORT.batter = annual_calc.batter and annual_calc.Game_Yr = '2012';
