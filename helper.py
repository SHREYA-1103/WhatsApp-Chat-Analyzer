from urlextract import URLExtract
extract=URLExtract()
import matplotlib.pyplot as mpl
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    #calculate total no of messages
    num_messages= df.shape[0]

    #calculate total no of words
    words=[]
    for message in df['message']:
        words.extend(message.split())
    num_words=len(words)

    #calculate media items
    num_media=df[df['message']=='<Media omitted>\n'].shape[0]

    #calculate no of links
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    num_links=len(links)

    #returning desired values
    return num_messages,num_words,num_media,num_links


def most_active_users(selected_user,df):
    if selected_user=='Overall':
            x=df['user'].value_counts().head() #returns the top five users with most activity
            #create a data frame which returns the top five users along with their percentage contribution in the chat
            df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
            return x,df
    

#wordcloud
def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    #applying filtering for removing group notification and media omitted messages
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    #removing stop words
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    
    def remove_stop_words(message):
        words=[] #list of all words
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return "".join(words)    

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


#most common words
def most_common_words(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    #removing unecessary words
    #removing group notifications if present
    temp=df[df['user']!='group_notification']
    #removing media omitted messages
    temp=temp[temp['message']!='<Media omitted>\n']
    #removing stop words (used in sentence formation but has no meaning)
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    
    #finding most common 20 words
    words=[] #list of all words
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    #data frame of most common 20 words
    mcw_df=pd.DataFrame(Counter(words).most_common(20))

    return mcw_df


#emoji analysis
def most_common_emojis(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


#monthly timeline
def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]#finds the month number (earlier we added the month name in the dataframe)
    
    mtimeline_df=df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range(mtimeline_df.shape[0]):
        time.append(mtimeline_df['month'][i]+" - "+str(mtimeline_df['year'][i]))
    
    mtimeline_df['time']=time
    
    return mtimeline_df


#daily timeline
def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    dtimeline_df=df.groupby(['date']).count()['message'].reset_index()
    
    return dtimeline_df


#weekly activity
def weekly_activity(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    wactivity_df=df['day_name'].value_counts()
    return wactivity_df


#monthly activity
def monthly_activity(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    mactivity_df=df['month'].value_counts()
    return mactivity_df


def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    heat_df=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return heat_df