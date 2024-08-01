from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import pandas as pd
extract=URLExtract()

f=open("stop_hinglish.txt","r")
stop_words=f.read()

def fetch_stats(selected_user,df):

    if selected_user !="Overall":
        df = df[df["user"]==selected_user]

    num_mssg = df.shape[0]
    words=[]
    for i in df.message:
        words.extend(i.split())
    

    media = df[df["message"]=="<Media omitted>\n"].shape[0]

    links=[]
    for i in df["message"]:
        links.extend(extract.find_urls(i))

    return num_mssg,len(words),media,len(links)

def most_busy_users(df):
    x=df["user"].value_counts().head()
    df=round((df["user"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"user":"User","count":"Percentage"})
    return x,df


def word_cloud(selected_user,df):

    if selected_user !="Overall":
        df = df[df["user"]==selected_user]

    temp=df[df['user'] != 'Group Notification']
    temp=temp[temp['message'] !='<Media omitted>\n']
    temp=temp[~temp['message'].str.contains('deleted', case=False, na=False)]

    def remove_stop(mssg):
        w=[]
        for word in mssg.lower().split():
            if word not in stop_words:
                w.append(word)
        return " ".join(w)
    


    wc = WordCloud(width=500,height=500,min_font_size=10,background_color="yellow")
    temp["message"]=temp["message"].apply(remove_stop)

    df_wc=wc.generate(temp["message"].str.cat(sep=" "))

    return df_wc



def most_common_words(selected_user,df):
    if selected_user !="Overall":
        df = df[df["user"]==selected_user]

    temp=df[df['user'] != 'Group Notification']
    temp=temp[temp['message'] !='<Media omitted>\n']
    temp=temp[~temp['message'].str.contains('deleted', case=False, na=False)]



    words=[]
    for i in temp.message:
        for word in i.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))
    

def emoji_count(selected_user,df):
    if selected_user !="Overall":
        df = df[df["user"]==selected_user]
    emojis=[]

    for i in df["message"]:
        emojis.extend([e['emoji'] for e in emoji.emoji_list(i)])
    em_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return em_df.head(10)


def monthly_timeline(selected_user,df):
    if selected_user !="Overall":
        df = df[df["user"]==selected_user]
    time=[]
    timeline= df.groupby(["year","month"]).count()["message"].reset_index()
    for i in range(timeline.shape[0]):
        time.append( timeline["month"][i] + "-" + str(timeline["year"][i]))
    timeline["time"]=time
    return timeline



def week_activity(selected_user,df):
    if selected_user !="Overall":
        df = df[df["user"]==selected_user]

    return df["day_name"].value_counts().reset_index()

def month_activity(selected_user,df):
    if selected_user !="Overall":
        df = df[df["user"]==selected_user]

    return df["month"].value_counts().reset_index()

def hour_activity(selected_user,df):
    if selected_user !="Overall":
        df = df[df["user"]==selected_user]

    return df.pivot_table(index="day_name",columns="period",values="message",aggfunc="count").fillna(0)








    # if selected_user=="Overall":
    #     num_mssg = df.shape[0]
    #     words=[]
    #     for i in df.message:
    #         words.extend(i.split())
    #     return num_mssg,len(words)
    # else:
    #     new_df = df[df["user"]==selected_user]
    #     num_mssg = new_df.shape[0]
    #     words=[]
    #     for i in new_df.message:
    #         words.extend(i.split())
    #     return num_mssg,len(words)

    
    