/*
Created by Ed Smythe Sept 2020
BDA 696 @ SDSU

Baseball
Load this dataset into SQL
Calculate the batting average using SQL queries for every player
Annual, Historic
Rolling (over last 100 days)
Look at the last 100 days that player was in prior to this game
Store all these results in their own tables
Hints
Look at the tables already available: batter_counts, battersInGame
Do it for a single batter first
JOIN ing a table with itself may prove helpful
It's ok to make temporary tables for intermediary results
Make it a simple SQL script that will work on a freshly imported copy of the database
Work outside of your master branch and make a PR
Buddy should review PR, after reviewed, send it to me

*/

select * from bb LIMIT 5