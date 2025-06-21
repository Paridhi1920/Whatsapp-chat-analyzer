import re
import pandas as pd

def preprocess(data):
    # Normalize weird spaces
    data = data.replace('\u202f', ' ').replace('\xa0', ' ')

    # Regex for 12-hour format with optional AM/PM spacing
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}(?:\s?[apAP][mM])\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    if len(messages) != len(dates):
        return pd.DataFrame()

    # Create DataFrame
    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})

    # Remove trailing characters and parse datetime
    df['message_date'] = pd.to_datetime(
        df['message_date'].str.strip(),
        format='%d/%m/%y, %I:%M %p -',
        errors='coerce'
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users, msgs = [], []
    for message in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('group_notifications')
            msgs.append(entry[0])

    df['users'] = users
    df['messages'] = msgs
    df.drop(columns=['user_messages'], inplace=True)

    # Time-based columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['week_day'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute

    # Periods for heatmap
    period = []
    for hour in df['hour']:
        if pd.isna(hour):
            period.append("unknown")
        elif hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")
    df['period'] = period

    return df
