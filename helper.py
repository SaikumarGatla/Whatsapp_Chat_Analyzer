from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji  #--> If not working try with pip install emoji version==1.7.0

def fetch_stats(selected_user, df):

    if selected_user !='Overall':
        df = df[df['user'] == selected_user]

    #1. fetch number of messages
    num_messages = df.shape[0]

    #2. number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #3. fetch number of media messages
    #num_media_messages = df[df['message'] == '<Media omitted\n'].shape[0]
    num_media_messages = df[df['message'].str.contains('<Media omitted>')].shape[0]

    #4. fetch number of links shared
    links = []

    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links) 

    # if selected_user == 'Overall':
    
    #     #1. fetch number of messages
    #     num_messages = df.shape[0]

    #     #2. number of words
    #     words = []
    #     for message in df['message']:
    #         words.extend(message.split())*

    #     return num_messages, len(words)
    # else:
    #     #df[df['user'] == selected_user].shape[0]

    #     new_df = df[df['user'] == selected_user]
    #     num_messages = new_df.shape[0]

    #     words = []
    #     for message in df['message']:
    #         words.extend(message.split())

    #     return num_messages, len(words)

def most_busy_users(df):
    #1. fetching Bar Chart
    # select all rows that contain the value 'group_notification'
    mask = df['user'] == 'group_notification'

    # delete the selected rows using the drop() method
    new_df = df.drop(df[mask].index)

    x = new_df['user'].value_counts().head()

    #2.fetching percent of messages of each user
    percent_df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name', 'user':'percent'})
    return x, percent_df

def create_wordcloud(selected_user, df):

    f = open('stopwords_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user !='Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y) 
  
    wc = WordCloud(width=500, height=500, min_font_size=10, max_font_size=200, background_color='white') #creating object 'wc' of class 'WordCloud'
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    
    return df_wc

def most_common_words(selected_user, df):

    # Stop_words are removed 
    f = open('stopwords_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user !='Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user, df):
    #the goal is to create a string to be put in the function emoji.emoji_list(string)

    words=[]
    for messages in df['message']:
        words.extend(messages.split())

#now we have a list which contains all the words in df['message'] of dataframe
#now the goal is to convert it into a string

    mystr=""
    for x in words:
        mystr=mystr + " "+ x

#now we have to put this string into the emoji function

    myemoji=emoji.emoji_list(mystr)

#myemoji is a list with the following type of elements
#[{'match_start': 5712, 'match_end': 5714, 'emoji': '👍🏻'},
 #{'match_start': 6896, 'match_end': 6897, 'emoji': '👆'},
 #{'match_start': 6897, 'match_end': 6898, 'emoji': '👆'},
 #{'match_start': 8097, 'match_end': 8098, 'emoji': '👆'}]

#now we have to extract each emoji from this type of list

    pre_final_emoji_list=[]
    for i in range(len(myemoji)):
        pre_final_emoji_list.extend(myemoji[i]['emoji'])

#now we have another list which contains all the emojis but it also contains some extra emojis which need to be removed
#we create two new list, one where removal characters are present and another one where final emojis are.

    emojis_to_be_removed=[' ','🏻']
    print(emojis_to_be_removed)

    final_emoji_list=[]
    for items in pre_final_emoji_list:
        if items.strip() not in emojis_to_be_removed:
            final_emoji_list.append(items)
    final_emoji_list
    
    emoji_df = pd.DataFrame(Counter(final_emoji_list).most_common(len(Counter(final_emoji_list))))

    return emoji_df

def monthly_timeline(selected_user, df):

    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['message'].reset_index()

    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['Time'] = time

    return timeline

def daily_timeline(selected_user, df):

    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):

    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):

    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    
    return df['Month'].value_counts()

def activity_heatmap(selected_user, df):

    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    
    activity_heatmap = df.pivot_table(index= 'day_name', columns='period', values='message', aggfunc='count').fillna(0)
    
    return activity_heatmap