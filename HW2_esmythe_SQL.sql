/* Create a table to assign binary values to events */
create table event_val as
select unique event 
from atbat_r;

/* add value cloumn */
/* check for new values after fiurst run to force review of event _val:value*/

alter table event_val 
  add value int
    after event;
	
/* marke events that are hits */
update event_val
set value = 1
where event = 'Single'
or event = 'Double'
or event = 'Home Run'
or event = 'Walk'
or event = 'Hit By Pitch'
or event = 'Field Error'
or event = 'Triple'
or event = 'Catcher Interference'
or event = 'Intent Walk'
or event = 'Fan interference';

update event_val 
set value = 0
where value is null;

 /* make a batter performance table for unique batter ids */
create table player_bat_avg as
select unique batter from atbat_r ar order by batter

alter table player_bat_avg
  add on_base int
    after batter,
  add bats int
    after on_base,
  add bat_avg float
    after bats;
   