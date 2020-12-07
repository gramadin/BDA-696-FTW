# Created By Ed Smythe
# Dec 2020
# Used from class demo
# ~2m3s
use baseball;

drop table if exists rolling_030;
create table rolling_030 as	
select
	tbc1.team_id
	, t.name_full as Home_Team
	, (select name_full from team t2  where tbc1.opponent_team_id = t2.team_id) as Away_Team
	, tbc1.game_id
	, gl.local_date
	, COUNT (*) AS Cnt
	, SUM(tbc2.plateApperance) AS plateApperance
	, SUM(tbc2.atBat) AS atBat
	, SUM(tbc2.Hit) AS Hit
	, SUM(tbc2.caughtStealing2B) AS caught5tealing2B
	, SUM(tbc2.caughtStealing3B) AS caughtStealing3B
	, SUM(tbc2.caughtStealingHome) AS caughtStealingHome
	, SUM(tbc2.stolenBase2B) AS stolenBase2B
	, SUM(tbc2.stolenBase3B) AS stolenBase3B
	, SUM(tbc2.stolenBaseHome) AS stolenBaseHome
	, ((SUM(tbc2.stolenBase2B)+SUM(tbc2.stolenBase3B)+SUM(tbc2.stolenBaseHome))/nullif((SUM(tbc2.caughtStealing2B)+SUM(tbc2.caughtStealing3B)+SUM(tbc2.caughtStealingHome)+SUM(tbc2.stolenBase2B)+SUM(tbc2.stolenBase3B)+SUM(tbc2.stolenBaseHome)),0)) as SB_pct
	, SUM(tbc2.toBase) AS toBase
	, SUM(tbc2.atBat)/nullif(SUM(tbc2.Home_Run),0) AS AB_HR
	, SUM(tbc2.Hit)/nullif(SUM(tbc2.atBat),0) as Bat_Avg
	, SUM(tbc2.Batter_Interference) AS Batter_Interference
	, SUM(tbc2.Walk)/nullif(SUM(tbc2.Strikeout),0) AS BB_K
	, SUM(tbc2.Bunt_Ground_Out) + SUM(tbc2.Bunt_Groundout) AS Bunt_Ground_Out
	, SUM(tbc2.Bunt_Pop_Out) AS Bunt_Pop_Out
	, SUM(tbc2.Catcher_Interference) AS Catcher_Interference
	, SUM(tbc2.`Double`) AS Duhble # Used ` instead of ' due to local system. If you have issues change this for your system
	, SUM(tbc2.Double_Play) AS Double_Play
	, SUM(tbc2.Fan_interference) AS Fan_interference
	, SUM(tbc2.Field_Error) AS Field_Error
	, SUM(tbc2.Fielders_Choice) AS Fielders_Choice
	, SUM(tbc2.Fielders_Choice_Out) AS Fielders_Choice_Out
	, SUM(tbc2.Fly_Out) + SUM(tbc2.Flyout) AS Fly_Out
	, SUM(tbc2.Force_Out) + SUM(tbc2.Forceout) AS Force_Out
	, ((SUM(tbc2.Ground_Out) + SUM(tbc2.Groundout))/nullif(SUM(tbc2.Fly_Out) + SUM(tbc2.Flyout),0)) AS GO_AO
	, (1.8*(((SUM(tbc2.toBase)/nullif(SUM(tbc2.atBat)+SUM(tbc2.Walk)+SUM(tbc2.Hit_By_Pitch)+SUM(tbc2.Sac_Fly),0))+(SUM(tbc2.Hit)/nullif(SUM(tbc2.atBat),0)))/4)) AS GPA
	, SUM(tbc2.Ground_Out) + SUM(tbc2.Groundout) AS Ground_Out
	, SUM(tbc2.Grounded_Into_DP) AS Grounded_Into_DP
	, SUM(tbc2.Hit_By_Pitch) AS Hit_By_Pitch
	, SUM(tbc2.Home_Run) AS Home_Run
	, SUM(tbc2.Home_Run)/nullif(SUM(tbc2.Hit),0) AS HR_H
	, SUM(tbc2.Intent_Walk) AS Intent_Walk
	, SUM(tbc2.Strikeout)/nullif(SUM(tbc2.Walk),0) as K_BB
	, SUM(tbc2.Line_Out) + SUM(tbc2.Lineout) AS Line_Out
	, SUM(tbc2.toBase)/nullif(SUM(tbc2.atBat)+SUM(tbc2.Walk)+SUM(tbc2.Hit_By_Pitch)+SUM(tbc2.Sac_Fly),0) AS OBP
	, SUM(tbc2.toBase)/nullif(SUM(tbc2.atBat)+SUM(tbc2.Walk)+SUM(tbc2.Hit_By_Pitch)+SUM(tbc2.Sac_Fly),0) + SUM(tbc2.Hit)/nullif(SUM(tbc2.atBat),0) AS OPS
	, SUM(tbc2.plateApperance)/nullif(SUM(tbc2.Strikeout),0) AS PA_SO
	, SUM(tbc2.Pop_Out ) AS Pop_Out
	, SUM(tbc2.Runner_Out ) AS Runner_Out
	, SUM(tbc2.finalScore) AS Runs
	, SUM(tbc2.Sac_Bunt) AS Sac_Bunt
	, SUM(tbc2.Sac_Fly) AS Sac_Fly
	, SUM(tbc2.Sac_Fly_DP) AS Sac_Fly_DP
	, SUM(tbc2.Sacrifice_Bunt_DP) AS Sacrifice_Bunt_DP
	, SUM(tbc2.Single) AS Single
	, SUM(tbc2.Strikeout) as Strickout
	, SUM(tbc2.`Strikeout_-_DP`) AS Strikeout_DP # Used ` instead of ' due to local system. If you have issues change this for your system
	, SUM(tbc2.`Strikeout_-_TP`) AS Strikeout_TP # Used ` instead of ' due to local system. If you have issues change this for your system
	, SUM(tbc2.Triple) AS Triple
	, SUM(tbc2.Triple_Play) AS Triple_Play
	, SUM(tbc2.Walk) AS Walk
	, SUM(tbc2.`Double`)+SUM(tbc2.Triple)+SUM(tbc2.Home_Run) AS XBH
	, (1/(1+power(nullif(SUM(tbc2.opponent_finalScore)/nullif(SUM(tbc2.finalScore),0),0),1.83))) as pathag_v1
	, (1/(1+power(nullif(SUM(tbc2.opponent_finalScore)/nullif(SUM(tbc2.finalScore),0),0),((1.50*(log(((SUM(tbc2.finalScore)+SUM(tbc2.opponent_finalScore))/(count(tbc1.game_id)/2)))))+.045)))) as pathag_v2
	, (1/(1+power(nullif(SUM(tbc2.opponent_finalScore)/nullif(SUM(tbc2.finalScore),0),0),power(((SUM(tbc2.finalScore)+SUM(tbc2.opponent_finalScore))/(count(tbc1.game_id)/2)),0.287)))) as pathag_v3
	FROM team_batting_counts tbc1
	JOIN team t ON tbc1.team_id = t.team_id 
	JOIN game gl ON gl.game_id = tbc1.game_id AND gl.type IN ("R")
	JOIN team_batting_counts tbc2 ON tbc1.team_id = tbc2.team_id
	JOIN game g2 ON g2.game_id = tbc2.game_id AND
		g2.type IN ("R") AND
		g2.local_date < gl.local_date AND
		g2.local_date >= DATE_ADD(gl.local_date, INTERVAL -30 DAY)
	GROUP BY tbc1.team_id, tbc1.game_id , gl.local_date
	ORDER BY gl.local_date, tbc1.team_id;
# Establish Index
CREATE UNIQUE INDEX team_game ON rolling_030 (team_id, game_id);