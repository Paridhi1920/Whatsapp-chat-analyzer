import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages' : messages, 'message_date': dates})

    # convert message_date datatype
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')

    #renaming the column
    df.rename(columns ={'message_date' : 'date'}, inplace = True)

    #separate users and messages
    users =[]
    messages = []

    for message in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:    #user name (also write as - if len(entry) > 2 : )
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notifications')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace = True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['week_day'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute

    period = []
    for hour in df[['week_day', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df