# Created By Ed Smythe
# Dec 2020
# ~6ms load time
# Creates the base circadian rhythm table. non MLB teams are not addressed Thes will only work for Regular season games

drop table if exists circ_rhythm;
create table circ_rhythm (
	city varchar(23) not null,
	t_name varchar(41),
	time_zone int not null
	);

insert into circ_rhythm
	(city, t_name, time_zone)
values
	('Arizona','Arizona Diamondbacks',-2),
	('Atlanta','Atlanta Braves',0),
	('Baltimore','Baltimore Orioles',0),
	('Boston','Boston Red Sox',0),
	('Chi Cubs','Chicago Cubs',-1),
	('Chi White Sox','Chicago White Sox',-1),
	('Cincinnati','Cincinnati Reds',0),
	('Cleveland','Cleveland Indians',0),
	('Colorado','Colorado Rockies',-2),
	('Detroit','Detroit Tigers',0),
	('Houston','Houston Astros',-1),
	('Kansas City','Kansas City Royals',-1),
	('LA Angels','Los Angeles Angels',-3),
	('LA Dodgers','Los Angeles Dodgers',-3),
	('miami','Miami Marlins',0),
	('Milwaukee','Milwaukee Brewers',-1),
	('Minnesota','Minnesota Twins',-1),
	('NY Mets','New York Mets',0),
	('NY Yankees','New York Yankees',0),
	('Oakland','Oakland Athletics',-3),
	('Philadelphia','Philadelphia Phillies',0),
	('Pittsburgh','Pittsburgh Pirates',0),
	('San Diego','San Diego Padres',-3),
	('San Francisco','San Francisco Giants',-3),
	('Seattle','Seattle Mariners',-3),
	('St. Louis','St. Louis Cardinals',-1),
	('Tampa Bay','Tampa Bay Rays',0),
	('Texas','Texas Rangers',-1),
	('Toronto','Toronto Blue Jays',0),
	('Washington','Washington Nationals',0);

alter table circ_rhythm add team_id int(11);
update circ_rhythm cr, team t
set cr.team_id = t.team_id 
where cr.t_name = t.name_full ;

