import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8") 
    #st.text(data)         #To display text data
    df = preprocessor.preprocess(data) 
    st.dataframe(df)          #To diaplay DataFrame

    #Creating a Dropdown List , Fetching unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Analysis Area
        num_messages, num_words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write("<span style='font-size: 25px;'>Total Messages</span>", unsafe_allow_html=True)
            st.write(f"<span style='font-size: 25px;'>{num_messages}</span>", unsafe_allow_html=True)
            #Syntax only for reference purpose
            #st.write(f"<span style='font-size: 25px;'>{num_words}</span>", unsafe_allow_html=True)
                                        #or
            #st.write("<span style='font-size: 25px;'>{}</span>".format(num_words), unsafe_allow_html=True)



        with col2:
            st.write("<span style='font-size: 25px;'>Total Words</span>", unsafe_allow_html=True)
            st.write(f"<span style='font-size: 25px;'>{num_words}</span>", unsafe_allow_html=True)
            
        with col3:
            st.write("<span style='font-size: 25px;'>Total Shared Media</span>", unsafe_allow_html=True)
            st.write(f"<span style='font-size: 25px;'>{num_media_messages}</span>", unsafe_allow_html=True)

        with col4:
            st.write("<span style='font-size: 25px;'>Total Links Shared</span>", unsafe_allow_html=True)
            st.write(f"<span style='font-size: 25px;'>{num_links}</span>", unsafe_allow_html=True)

        #col1, col2, col3, col4 = st.beta_columns(4)

        # with col1:
        #     st.header('Total Messages')

        # with col1:
        #     st.header('Total Words')

        # with col3:
        #     st.header("Shared Media")
                      
        # with col4:
        #     st.header('Links Shared')

        #Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['Time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily TImeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title("Activity Map")
        col1, col2  = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity HeatMap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest user in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, percent_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                st.write("<span style='font-size: 25px;'>Bar Chart of Users' Messages</span>", unsafe_allow_html=True)
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.write("<span style='font-size: 25px;'>Percentage of Messages</span>", unsafe_allow_html=True)
                st.dataframe(percent_df)
            
    # WordCloud
    st.title("Word Cloud")
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    # Most common words
    most_common_df = helper.most_common_words(selected_user, df)

    fig, ax = plt.subplots()
    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation = 'vertical')

    st.title('Most Common Words')
    st.pyplot(fig)

    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("<span style='font-size: 25px;'>Emojis Frequency Table</span>", unsafe_allow_html=True)
        st.dataframe(emoji_df)
    with col2:
        st.write("<span style='font-size: 25px;'>Emojis Pie Chart</span>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        st.pyplot(fig)