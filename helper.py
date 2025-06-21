import re
from urlextract import URLExtract
extractor = URLExtract()
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    #1. num of messages
    num_mesages = df.shape[0]

    #2.num_words
    words = []
    for msg in df['messages']:
        words.extend(msg.split())

    #3.num_media
    num_media = df[df['messages'] == '<Media omitted>\n'].shape[0]

    #4.Links shared
    links=[]
    for msg in df['messages']:
        links.extend(extractor.find_urls(msg))
    
    return num_mesages, len(words),num_media,len(links)

def busy_user(df):
    x = df['users'].value_counts().head()
    
    df = round((df['users'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'index':'user', 'users':"percentage"})
    return x ,df

def most_common(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notifications']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    words = []

    for msg in temp['messages']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    common_df = pd.DataFrame(Counter(words).most_common(20))

    return common_df

def emojis(selected_user,df):
    emojis = []

    for msg in df['messages']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
    emoji_counts = pd.DataFrame(Counter(emojis).most_common(5), columns=['Emoji', 'Count'])

    return emoji_counts

def time_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def weekly_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    return df['week_day'].value_counts()

def monthly_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='week_day', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap
