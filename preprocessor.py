import re
import pandas as pd

def preprocess(data):
    # Fix for non-breaking space (e.g., between time and "pm") using \s? and accept both "am" and "pm"
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}(?:\s?[ap]m)\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    if len(messages) != len(dates):
        print("⚠️ Mismatch in messages and dates. Possibly wrong format.")
        return pd.DataFrame()

    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})

    # Convert message_date datatype
    df['message_date'] = pd.to_datetime(df['message_date'].str.replace('\u202f', ' ').str.strip(), 
                                        format='%d/%m/%y, %I:%M %p - ', errors='coerce')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages
    users = []
    messages = []

    for message in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notifications')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['week_day'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute

    # Create time periods for heatmap
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")
    df['period'] = period

    return df
