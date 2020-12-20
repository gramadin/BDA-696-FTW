# Created By Ed Smythe
# Dec 2020
# partial from class
# used update feature available in mariadb v 10.3+ to update original table

drop table if exists fix_stealing;
create table fix_stealing as
select * from
	(select -- ateam
			g.game_id
			, g.away_team_id as team_id
			,sum(case when des = 'Stolen Base 2B' then 1 else 0 end) as stolenBase2B
			,sum(case when des = 'Stolen Base 3B' then 1 else 0 end) as stolenBase3B
			,sum(case when des = 'Stolen Base Home' then 1 else 0 end) as stolenBaseHome
			,sum(case when des = 'Caught Stealing 2B' then 1 else 0 end) as caughtStealing2B
			,sum(case when des = 'Caught Stealing 3B' then 1 else 0 end) as caughtStealing3B
			,sum(case when des = 'Caught Stealing Home' then 1 else 0 end) as caughtStealingHome
		from inning i
		join game g on g.game_id = i.game_id 
		where i.half =0 and i.entry ='runner'
		group by g.game_id, g.away_team_id 
	union
	select -- hteam
			g.game_id
			, g.home_team_id as team_id
			,sum(case when des = 'Stolen Base 2B' then 1 else 0 end) as stolenBase2B
			,sum(case when des = 'Stolen Base 3B' then 1 else 0 end) as stolenBase3B
			,sum(case when des = 'Stolen Base Home' then 1 else 0 end) as stolenBaseHome
			,sum(case when des = 'Caught Stealing 2B' then 1 else 0 end) as caughtStealing2B
			,sum(case when des = 'Caught Stealing 3B' then 1 else 0 end) as caughtStealing3B
			,sum(case when des = 'Caught Stealing Home' then 1 else 0 end) as caughtStealingHome
		from inning i
		join game g on g.game_id = i.game_id 
		where i.half =1 and i.entry ='runner'
		group by g.game_id, g.away_team_id 
		) as subTable
	order by game_id , team_id;

create unique index team_game_uidx on fix_stealing(team_id, game_id);	

update team_batting_counts t, fix_stealing f set t.caughtStealing2B = f.caughtStealing2B where t.team_id = f.team_id and t.game_id = f.game_id;
update team_batting_counts t, fix_stealing f set t.caughtStealing3B = f.caughtStealing3B where t.team_id = f.team_id and t.game_id = f.game_id;
update team_batting_counts t, fix_stealing f set t.caughtStealingHome = f.caughtStealingHome where t.team_id = f.team_id and t.game_id = f.game_id;
update team_batting_counts t, fix_stealing f set t.stolenBase2B = f.stolenBase2B where t.team_id = f.team_id and t.game_id = f.game_id;
update team_batting_counts t, fix_stealing f set t.stolenBase3B = f.stolenBase3B where t.team_id = f.team_id and t.game_id = f.game_id;
update team_batting_counts t, fix_stealing f set t.stolenBaseHome = f.stolenBaseHome where t.team_id = f.team_id and t.game_id = f.game_id;
