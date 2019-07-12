# Stanley-Cup-Champs-1927-2019
This project is broken into three parts:
* A [VBA script](https://github.com/cwils021/Stanley-Cup-Champs-1927-2019/blob/master/StanleyCupChamp1927_2019_VBAScript.md) that pulls the data from a table on Wikipedia
* A [Python script](https://github.com/cwils021/Stanley-Cup-Champs-1927-2019/blob/master/SCC1927-2019-v2.py) that cleans the data, primarily with the use of the Pandas library
* A [Juypter Notebook](https://github.com/cwils021/Stanley-Cup-Champs-1927-2019/blob/master/Stanley%20Cup%20Champions%201927-2019.ipynb) walkthrough of cleaning the data as well as basic exploratory analysis using primarily the Matplotlib library

 ## Data Dictionary
 <dl>
<dt>team_win</dt>
<dd>Name of winning team</dd>
<dt>coach_win</dt>
<dd>Name of winning coach</dd>
<dt>Games</dt>
<dd>Series record of winning team</dd>
<dt>team_lose</dt>
<dd>Name of losing team</dd>
<dt>coach_lose</dt>
<dd>Name of losing coach</dd>
<dt>win_gs</dt>
<dd>Name of Cup winning goal scorer</dd>
<dt>wcon</dt>
<dd>Winning Teams Conference -- this column was ignored due to data gap from 1932 - 1967</dd>
<dt>wt_app2d</dt>
<dd>Winning team's Cup final appearances to date</dd>
<dt>wt_rec2d</dt>
<dd>Winning teams's Cup Final record to date</dd>
<dt>lcon</dt>
<dd>Losing Teams Conference -- this column was ignored due to data gap from 1932 - 1967</dd>
<dt>lt_app2d</dt>
<dd>Losing team's Cup final appearances to date</dd>
<dt>lt_rec2d</dt>
<dd>Losing teams's Cup Final record to date</dd>
<dt>goal_time</dt>
<dd>Time of period game winning goal was scored</dd>
<dt>period</dt>
<dd>Period in which game winning goal was scored</dd>
<dt>gt_cat</dt>
<dd>Time category of game winning goal</dd>
<dt>game_end</dt>
<dd>Categorization of whether the game went to overtime or ended in regulation</dd>











 </dl>
