import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_csv("C:/Users/chris/Documents/GitHub Repos/Stanley-Cup-Champs-1927-2019/_data/SCC1927-2019.csv",
                   header=0)

# Pandas options for better viewing of data frame

pd.set_option('max_rows', 100) # set max rows printed to 10
pd.set_option('expand_frame_repr', False)  # expand frame by row width
# truncate data frame when rows > max rows above
pd.set_option('large_repr', 'truncate')

data = data.set_index('Year')
data = data.drop(2005, axis= 0)
data = data.rename(columns={"Winning team": "team_win",
                            "Coach": "coach_win",
                            "Losing team": "team_lose",
                            "Coach.1": "coach_lose",
                            "Winning goal\n": "win_gs"
                            })

#print(data)
print(data.team_win.str.rpartition('(').head())
#split record and appearances from win_team
data[['team_win','DROP','WREC']] = data.team_win.str.rpartition('(')
data = data.drop('DROP', axis=1)
data['team_win'] = data.team_win.str.rstrip()

#create temp df to split conf from win_team
temp = data.team_win.str.rsplit("(",1).to_frame()
temp[['win_team','wcon']] = pd.DataFrame(temp.team_win.values.tolist(),index=temp.index)
temp = temp.drop('team_win',axis=1)

#print(temp)

#add team_Win and wcon to df
data[['team_win','wcon']] = temp[['win_team','wcon']]

data['wcon'] = data.wcon.str.rstrip(')')
data['wcon'] = data.wcon.str.lstrip()

#clean WREC col by splitting apperances to date and record to date
data[['wt_app2d','DROP','wt_rec2d']] = data.WREC.str.partition(',')
data = data.drop(['WREC','DROP'],axis=1)
data['wt_rec2d'] = data.wt_rec2d.str.rstrip(')')


#split record and appearances from lose_team
data[['team_lose','DROP','LREC']] = data.team_lose.str.rpartition('(')
data = data.drop('DROP', axis=1)
data['team_lose'] = data.team_lose.str.rstrip()

#create temp df to split conf from lose_team
temp = data.team_lose.str.rsplit("(",1).to_frame()
temp[['lose_team','lcon']] = pd.DataFrame(temp.team_lose.values.tolist(),index=temp.index)
temp = temp.drop('team_lose',axis=1)

#add team_lose and lcon to df
data[['team_lose','lcon']] = temp[['lose_team','lcon']]

data['lcon'] = data.lcon.str.rstrip(')')
data['lcon'] = data.lcon.str.lstrip()

#clean LREC col by splitting apperances to date and record to date
data[['lt_app2d','DROP','lt_rec2d']] = data.LREC.str.partition(',')
data = data.drop(['LREC','DROP'],axis=1)
data['lt_rec2d'] = data.lt_rec2d.str.rstrip(')')

#clean winning goal scorer col
data['win_gs'] = data.win_gs.str.rstrip()
data[['win_gs','DROP','goal_time']] = data.win_gs.str.partition('(')
data = data.drop('DROP',axis=1)
data[['goal_time','DROP','period']] = data.goal_time.str.partition(', ')
data = data.drop('DROP',axis=1)
data['period'] = data.period.str.rstrip(')')

data['game_end'] = np.where(data['period'] == 'first','Regulation',np.where(data['period'] == 'second','Regulation',np.where(data['period'] == 'third','Regulation','Overtime')))

cols = list(data.columns.values)

cols = ['Games','team_win', 'wcon', 'coach_win', 'win_gs',  'wt_app2d', 'wt_rec2d', 'team_lose', 'coach_lose', 'lcon', 'lt_app2d', 'lt_rec2d', 'goal_time', 'period', 'game_end']
data = data[list(cols)]



data['team_win'] = data.team_win.str.strip()
data['team_lose'] = data.team_lose.str.strip()
#print(data)
data.replace({'team_win' : {'Chicago Black Hawks':'Chicago Blackhawks'}},inplace=True)
data.replace({'team_lose' : {'Chicago Black Hawks':'Chicago Blackhawks'}},inplace=True)

#create dictionaries of team appearances in cup final (win + lose)

win_dic = Counter(data['team_win'])
lose_dic = Counter(data['team_lose'])
Total_dic = win_dic + lose_dic


#create df from above dictionary
total_cup_app = pd.DataFrame.from_dict(Total_dic, orient='index',columns=['Number of Cup Appearances'])
total_cup_app = total_cup_app.sort_values('Number of Cup Appearances',ascending=False)
total_cup_app.index.names = ['Team']
#print(total_cup_app)

#convert to time object and categorize time of goal
data['goal_time'] = pd.to_datetime(data['goal_time'],format='%M:%S').dt.time
temp = pd.DataFrame(data['goal_time'],columns=['goal_time'])

temp[['goal_hour_DROP','goal_min','goal_sec']] = temp['goal_time'].astype(str).str.split(':', expand=True).astype(int)

temp = temp.drop('goal_hour_DROP',axis=1)
temp['gt_in_s'] = (temp['goal_min']*60) + temp['goal_sec']
temp['gt_cat'] = np.where(temp['gt_in_s'] <= 300, 'First 5',np.where(temp['gt_in_s'] >= 900, 'Final 5', 'Middle 10'))
data['gt_cat'] = temp['gt_cat']
#print(data.head())

#create dic like team but for coaches
wc_dic = Counter(data['coach_win'])
lc_dic = Counter(data['coach_lose'])
coach_total_dic = wc_dic + lc_dic

#create df from above dictionary
total_coach_app = pd.DataFrame.from_dict(coach_total_dic, orient='index',columns=['Number of Cup Appearances'])
total_coach_app = total_coach_app.sort_values('Number of Cup Appearances',ascending=False)
total_coach_app.index.names = ['Coach']

cols = list(data.columns.values)
#print(cols) #to get list of column names to copy
cols = ['Games', 'team_win', 'wcon', 'coach_win', 'win_gs', 'wt_app2d', 'wt_rec2d', 'team_lose', 'coach_lose', 'lcon', 'lt_app2d', 'lt_rec2d', 'goal_time', 'gt_cat', 'period', 'game_end']
data = data[list(cols)]
print(data.head())
#print(data.win_gs.value_counts().head(10))
writer = pd.ExcelWriter('SCC1927-2019-clean-v2.xlsx', engine='xlsxwriter')
data.to_excel(writer,sheet_name='cleaned_data')
total_coach_app.to_excel(writer,sheet_name='total_apps_coach')
total_cup_app.to_excel(writer,sheet_name='total_apps_team')
writer.save()



plt.figure(num=1,figsize=(15,6))
team_wins = data.team_win.value_counts(ascending=True).plot.barh()
team_wins.set_xlabel('Frequency')
team_wins.set_ylabel('Team')
team_wins.set_title('Stanley Cup Finals Wins')
team_wins.grid(True,which='major',axis='x')
for i,v in enumerate(data.team_win.value_counts(ascending=True)):
    team_wins.text(v,i," "+str(v), color='black',va='center',fontweight='bold')
plt.tight_layout()
#plt.savefig('team_wins.png')
#plt.show()
plt.close()

plt.figure(num=2, figsize=(15,6))
team_loses = data.team_lose.value_counts(ascending=True).plot.barh()
team_loses.set_xlabel('Frequency')
team_loses.set_ylabel('Team')
team_loses.set_title('Number of Stanley Cup Finals Loses')
team_loses.grid(True,which='major',axis='x')
for i,v in enumerate(data.team_lose.value_counts(ascending=True)):
    team_loses.text(v,i," "+str(v), color='black',va='center',fontweight='bold')
plt.tight_layout()
#plt.savefig('team_loses.png')
#plt.show()
plt.close()

plt.figure(num=3,figsize=(15,10))
coach_wins = data.coach_win.value_counts(ascending=True).plot.barh()
coach_wins.set_xlabel('Frequency')
coach_wins.set_ylabel('Coach')
coach_wins.set_title('Number of Stanley Cup Finals Wins')
coach_wins.grid(True,which='major',axis='x')
for i,v in enumerate(data.coach_win.value_counts(ascending=True)):
    coach_wins.text(v,i," "+str(v), color='black',va='center',fontweight='bold')
#plt.yticks(rotation=45)
plt.tight_layout()
#plt.savefig('coach_wins.png')
#plt.show()
plt.close()

plt.figure(num=4,figsize=(15,10))
coach_loses = data.coach_lose.value_counts(ascending=True).plot.barh()
coach_loses.set_xlabel('Frequency')
coach_loses.set_ylabel('Coach')
coach_loses.set_title('Number of Stanley Cup Finals Loses')
coach_loses.grid(True,which='major',axis='x')
for i,v in enumerate(data.coach_lose.value_counts(ascending=True)):
    coach_loses.text(v,i," "+str(v), color='black',va='center',fontweight='bold')
plt.tight_layout()
#plt.savefig('coach_loses.png')
#plt.show()
plt.close()

plt.figure(num=5)
goal_timedis = data.gt_cat.value_counts(ascending=True).plot.bar()
#plt.show()
plt.close()

plt.figure(num=6)
goal_scorer = data.win_gs.value_counts(ascending=True).plot.barh()
#plt.show()
plt.close()

plt.figure(num=7,figsize=(6,6))
game_end = data.game_end.value_counts().plot.bar()
for i,v in enumerate(data.game_end.value_counts()):
    game_end.text(i,v + 1,str(v),color='black',ha='center',fontweight='bold')
game_end.set_ylabel('Frequency')
game_end.set_title('Frequency of Cup Winning Games\nEnding in OT')
plt.xticks(rotation=0)
#plt.savefig('game_end.png')
#plt.show()
plt.close()



plt.figure(num=8, figsize=(10,6))
t5c = data.coach_win.value_counts().head()
print(t5c)
top5_coach = t5c.plot.bar(color='dodgerblue')
plt.xticks(rotation=0)
top5_coach.set_title('Top 5 Coaches by\nStanley Cup Final Wins',fontweight='bold')
top5_coach.set_ylabel('Number of Cups')
top5_coach.set_xlabel('Coach')
for i,v in enumerate(t5c):
    top5_coach.text(i,v+0.05,str(v),color='black',ha='center',fontweight='bold')
#plt.savefig('t5win_coach.png')
#plt.show()
plt.close()

