import numpy as np
from fontTools.subset import subset


def medal_telly(df):
    medal_telly = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_telly = medal_telly.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_telly['total']=medal_telly['Gold']+medal_telly['Silver']+medal_telly['Bronze']

    medal_telly['Gold']=medal_telly['Gold'].astype('int')
    medal_telly['Silver'] = medal_telly['Silver'].astype('int')
    medal_telly['Bronze'] = medal_telly['Bronze'].astype('int')
    medal_telly['total'] = medal_telly['total'].astype('int')
    return medal_telly

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    countries=np.unique(df['region'].dropna().values).tolist()
    countries.sort()

    countries.insert(0,"Overall")

    return years,countries

def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year=='Overall' and country=='Overall':
        temp_df=medal_df
    if year=='Overall' and country!='Overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==year]
    if year!='Overall' and country!='Overall':
        temp_df=medal_df[(medal_df['region']==country) & (medal_df['Year']==year)]

    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['Total']=x['Gold']+x['Silver']+x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')
    return x

def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col]).groupby('Year').count()[[col]].reset_index()
    nations_over_time.rename(columns={'Year': 'Edition', col: 'count'}, inplace=True)
    return nations_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Ensure 'value_counts()' returns a proper DataFrame with correct column names
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']  # Rename columns explicitly

    # Merge with original dataframe to get additional details
    x = medal_counts.head(15).merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')

    return x

def year_wise_medal(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    # Rename columns explicitly after reset_index()
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']  # Ensure correct column names

    # Merge using the correct column name
    x = medal_counts.head(10).merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

    return x

