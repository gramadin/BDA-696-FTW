# Created By Ed Smythe
# Dec 2020
# Establish net jet lag value for taveling team
# Future consideration to multi day series resulting in deminishing effect of circadian offset
# Should also make a cumulative internal clock values thorugh out season

drop table if exists team_circ;
create table team_circ as
select g2.game_id
		, local_date
		, (select name_full from team t2  where tbc.team_id = t2.team_id) as Home_Team 
		, (select name_full from team t2  where tbc.opponent_team_id = t2.team_id) as Away_Team
		, (select time_zone from circ_rhythm cr where tbc.opponent_team_id = cr.team_id) as Away_TZ -- home team is always 0
		, (0-(select time_zone from circ_rhythm cr where tbc.opponent_team_id = cr.team_id)) as Net_Jet_Lag -- positive values are travel east negative values are travel west
from team_batting_counts tbc 
join team t3 on tbc.team_id = t3.team_id
join game g2 on tbc.game_id = g2.game_id 
where tbc.homeTeam = 1
order by home_team_id;