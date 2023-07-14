import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date column to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    #(1) An Error will be thrown if the datetime string '13/02/23, 12:42 - ' does not match the expected format '%d/%m/%Y, %H:%M - '.
    #(2) For example, if the year is only represented by the last two digits, the format string should use '%y' instead of '%Y'. 
    #Similarly, if there are spaces before or after the hyphen in the datetime string, 
    #the format string should include spaces around the hyphen as well.
    # '20/02/23, 09:34 - ' --> '%d/%m/%y, %H:%M - '  AND  '20/02/2023, 09:34 - ' --> '%d/%m/%Y, %H:%M - '
    #(3) Also this project works only for 24hrs date format.
    #Not for 12 hrs date format(For it to work in 12hrs date format convert the pattern created accordingly by studying its regular expression)
    # rename message_date to date column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:# user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
        
    df['user']  = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['Year'] = df['date'].dt.year
    df['Month_num'] = df['date'].dt.month
    df['Month'] = df['date'].dt.month_name()
    df['Day'] = df['date'].dt.day
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['Hour'] = df['date'].dt.hour
    df['Minutes'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period

    return df
