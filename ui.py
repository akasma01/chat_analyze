import streamlit as st
import code1
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue() 
    data=bytes_data.decode("utf-8")
    #st.text(data)

df= code1.preprocess(data)
#st.dataframe(df)

user_list = df["user"].unique().tolist()
user_list.remove("Group Notification")
user_list.sort()
user_list.insert(0,"Overall")
selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)


if st.sidebar.button("Show Analysis"):
   
    st.title("Top Statistics...")
    num_mssg,words,media,links=helper.fetch_stats(selected_user,df)
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.header("Total Messages")
        st.title(num_mssg)
    with col2:
        st.header("Total Words")
        st.title(words)
    with col3:
        st.header("Total Media ")
        st.title(media)
    with col4:
        st.header("Total Links ")
        st.title(links)

    st.title("Monthly Activity")
    timeline=helper.monthly_timeline(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(timeline["time"],timeline["message"],marker="o")
    plt.xticks(rotation=90)
    st.pyplot(fig)

    if selected_user == "Overall":
        st.title("Most Busy Users")
        x,new_df= helper.most_busy_users(df)
        fig,ax=plt.subplots()
        col1,col2=st.columns(2)
        with col1:
            ax.bar(x.index,x.values)
            plt.xticks(rotation=90)
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

#weekly most active user
    st.title("Activity map")
    col1,col2=st.columns(2)
    with col1:
        st.header("Most busy day")
        busy_day=helper.week_activity(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(busy_day["day_name"],busy_day["count"])
        plt.xticks(rotation=90)
        st.pyplot(fig)
#monthly most active user
    with col2:
        st.header("Most busy Month")
        busy_month=helper.month_activity(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(busy_month["month"],busy_month["count"])
        plt.xticks(rotation=90)
        st.pyplot(fig)

#hour activity
    st.title("Hour-wise activity")
    hour_df=helper.hour_activity(selected_user,df)
    fig,ax=plt.subplots()
    ax=sns.heatmap(hour_df)
    st.pyplot(fig)


#wordcloud

    st.title("Wordcloud")
    df_wc=helper.word_cloud(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)


#most comon words

    st.title("Most common Words...")
    cmn_words=helper.most_common_words(selected_user,df)
#st.dataframe(cmn_words)

    fig,ax=plt.subplots()
    ax.barh(cmn_words[0],cmn_words[1])
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.title("Most Used Emoji's")
    em_count=helper.emoji_count(selected_user,df)
    col1,col2=st.columns(2)
    with col1:
        st.header("Most used Emojis list")    
        st.dataframe(em_count)
    with col2:
        st.header("Most used Emojis graph")    
        fig,ax=plt.subplots()
        ax.bar(em_count[0],em_count[1])
        plt.xticks(rotation=90)
        st.pyplot(fig)  



        