import streamlit as st
import preprocessor as pp
import helper as hp
import matplotlib.pyplot as mpl
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

#create the column for uploading the file
uploaded_file=st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    #obtain the data of the uploaded file
    bytes_data=uploaded_file.getvalue()
    #convert the data of the uploaded file into string in order to make it ready for pre processing
    data=bytes_data.decode("utf-8")
    df=pp.preprocess(data)

    # st.dataframe(df) #prints the entire dataframe

    #fetch unique users and create their list - for analysis per user
    user_list=df['user'].unique().tolist()
    if 'group_notification' in user_list: 
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall") #for group analysis

    #column for selecting the user for printing the analysis
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        #printing the total statistics
        num_messages,num_words,num_media,num_links=hp.fetch_stats(selected_user,df)
        
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.subheader(num_messages)

        with col2:
            st.header("Total Words")
            st.subheader(num_words)

        with col3:
            st.header("Media items")
            st.subheader(num_media)

        with col4:
            st.header("Total Links")
            st.subheader(num_links)


        #monthly analysis
        st.title("Monthly Timeline")
        mtimeline_df=hp.monthly_timeline(selected_user,df)
        fig,ax=mpl.subplots()
        ax.plot(mtimeline_df['time'],mtimeline_df['message'],color='red')
        mpl.xticks(rotation='vertical')
        st.pyplot(fig)


        #daily analysis
        st.title("Daily Timeline")
        dtimeline_df=hp.daily_timeline(selected_user,df)
        fig,ax=mpl.subplots()
        ax.plot(dtimeline_df['date'],dtimeline_df['message'],color='red')
        mpl.xticks(rotation='vertical')
        st.pyplot(fig)


        #activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy days")
            wactivity_df=hp.weekly_activity(selected_user,df)
            fig,ax=mpl.subplots()
            ax.barh(wactivity_df.index,wactivity_df.values,color='red')
            mpl.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy months")
            mactivity_df=hp.monthly_activity(selected_user,df)
            fig,ax=mpl.subplots()
            ax.barh(mactivity_df.index,mactivity_df.values,color='red')
            mpl.xticks(rotation='vertical')
            st.pyplot(fig)



        #user activity heatmap
        st.title("Activity Heat Map")
        heat_df=hp.activity_heatmap(selected_user,df)
        fig,ax=mpl.subplots()
        ax=sns.heatmap(heat_df)
        st.pyplot(fig)


        #finding the most active user in the group
        if selected_user=='Overall':
            st.title("Most Active Users")
            x,new_df=hp.most_active_users(selected_user,df)
            fig,ax=mpl.subplots()
            col1,col2=st.columns(2)
            
            #printing the bar plot showing users activity
            with col1:
                ax.bar(x.index,x.values,color='red')
                mpl.xticks(rotation='vertical')
                st.pyplot(fig)
            
            #printing the dataframe showing the stats of users's activity
            with col2:
                st.dataframe(new_df)
        


        #wordcloud
        st.title("Wordcloud")
        df_wc=hp.create_wordcloud(selected_user,df)
        fig,ax=mpl.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #most common words        
        st.title("Most Commonly Used Words in the chat")
        mcw_df=hp.most_common_words(selected_user,df)
        fig,ax=mpl.subplots()
        ax.barh(mcw_df[0],mcw_df[1],color='red') #horizontal bar chart
        mpl.gca().invert_yaxis() #reversing the horizontal bar chart
        mpl.xticks(rotation='vertical')
        st.pyplot(fig)


        #emoji analysis
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)
        emoji_df=hp.most_common_emojis(selected_user,df)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=mpl.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)


        
