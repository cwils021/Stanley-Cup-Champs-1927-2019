import pandas as pd
from collections import Counter
data = pd.read_csv("C:/Users/chris/Documents/GitHub Repos/Stanley-Cup-Champs-1927-2019/_data/SCC1927-2019.csv",
                   header=0)

# Pandas options for better viewing of data frame

pd.set_option('max_rows', 100) # set max rows printed to 10
pd.set_option('expand_frame_repr', False)  # expand frame by row width
# truncate data frame when rows > max rows above
pd.set_option('large_repr', 'truncate')

print('Shape')
print('=======================')
print(data.shape)

print('Type')
print('=======================')
print(type(data))

print('Info')
print('=======================')
print(data.info())

print('Head')
print('=======================')
print(data.head())

print('Tail')
print('=======================')
print(data.tail())

print('Describe')
print('=======================')
print(data.describe())

print('Describe winning_team')
print('=======================')
print(data['Winning team'].describe())

# the above code shows something interesting, clearly the winning team column will need to be further investigated
# as it shows 93 unique winning teams of the cup where as we know teams have one multiple times before

print(data[data[
               "Year"] == 2005])  # this was the year of the lockout and no playoffs were played, therefore it is
# good to drop

data = data.set_index("Year")
data = data.drop(2005, axis=0)

print(data.info())
data = data.rename(columns={"Winning team": "team_win",
                            "Coach": "coach_win",
                            "Losing team": "team_lose",
                            "Coach.1": "coach_lose",
                            "Winning goal\n": "win_gs"
                            })

print(data.team_win)
# after printing the team_win col we can see that it actually holds multiple feilds of information
# winning team, winning team conference, winning team record in playoffs to date
# we will need to split these into new columns

data[['win_team', 'wt_conf', 'wt_rec2d']] = data.team_win.str.split(
    "(", expand=True)
# split team_win into 3 new cols,
# need to clean wt_conf & wt_rec2d further
data[['wt_cup_app2d', 'wt_cupfin_rec2d']
] = data.wt_rec2d.str.split(",", expand=True)
# split cup final appearances from cup final record of winning team
data['wt_cupfin_rec2d'] = data['wt_cupfin_rec2d'].map(
    lambda x: str(x)[:-1])  # drops unwanted ) from cup final records
# used -2 as there was a space after the )
data['wt_conf'] = data['wt_conf'].map(lambda x: str(x)[:-2])
data['win_team'] = data['win_team'].map(lambda x: str(x)[:-1])
# now that winning team cols are cleaned, we drop the unwanted cols before cleaning losing team cols

data = data.drop(columns=['team_win', 'wt_rec2d'])

data[['lose_team', 'lt_conf', 'lt_rec2d']
] = data.team_lose.str.split("(", expand=True)
data[['lt_cup_app2d', 'lt_cupfin_rec2d']
] = data.lt_rec2d.str.split(",", expand=True)
data['lt_cupfin_rec2d'] = data['lt_cupfin_rec2d'].map(lambda x: str(x)[:-1])
data['lt_conf'] = data['lt_conf'].map(lambda x: str(x)[:-2])
data['lose_team'] = data['lose_team'].map(lambda x: str(x)[:-1])
data = data.drop(columns=['team_lose', 'lt_rec2d'])

# now we need to clean the winning goal-scorer, for simplicity we only care about who scored the goal, not when

data[['win_goal_scorer', 'DROP']] = data.win_gs.str.split("(", expand=True)
data['win_goal_scorer'] = data['win_goal_scorer'].map(lambda x: str(x)[:-1])
data = data.drop(columns=['win_gs', 'DROP'])

print(data)
print(data.info(
))

print(data.win_team.value_counts())

print(data.wt_conf.value_counts())

# since conferences have been changed so much over the years it does not provide much info so we will drop


data_cleaned = data.drop(columns=['wt_conf', 'wt_cup_app2d',
                                     'lt_conf', 'lt_cup_app2d'])
print(data_cleaned
      )
cols = list(data_cleaned.columns.values)
print(cols)

data_cleaned = data_cleaned[['Games', 'win_team', 'coach_win',
                        'win_goal_scorer','wt_cupfin_rec2d','lose_team', 'coach_lose','lt_cupfin_rec2d']]
print(data_cleaned)
#ata_cleaned.to_excel('SCC1927-2019-clean.xlsx')
win_dic = Counter(data_cleaned['win_team'])
lose_dic = Counter(data_cleaned['lose_team'])
print(win_dic)
print(lose_dic)
Total_apps = win_dic + lose_dic
print(Total_apps)
Total_Cup_App_by_team = pd.DataFrame.from_dict(Total_apps, orient='index',columns=['Number of Cup Appearances'])
Total_Cup_App_by_team = Total_Cup_App_by_team.sort_values('Number of Cup Appearances',ascending=False)
print(Total_Cup_App_by_team)