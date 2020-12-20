# Created By Ed Smythe
# Dec 2020
# ~6ms load time
# Creates the world series winners of previous year table, In reality this Would be created at the end of the year for use in the next year and could include all stats

drop table if exists ws_win_stats;
create table ws_win_stats (
	win_yr year
	,BB_pct float
	,K_pct float
	,OBP Float
	);

insert into ws_win_stats
	(win_yr, BB_pct, K_pct, OBP)
values
	(2006,0.085,0.1480,0.337)
	, (2007,0.1070,0.1620,0.362)
	, (2008,0.0930,0.1780,0.332)
	, (2009,0.1030,0.1570,0.362)
	, (2010,0.0790,0.1790,0.321)
	, (2011,0.0870,0.1570,0.341);


