import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('WhatsApp Chat Analyzer')

#upload_file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    #fetch unique user
    user_list = df['users'].unique().tolist()
    if 'group_notifications' in user_list:
        user_list.remove('group_notifications')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt",user_list)

    #show analysis
    if st.sidebar.button("Show Analysis"):
        col_1, col_2, col_3, col_4 = st.columns(4)

        num_mesages, num_word, num_media, num_url = helper.fetch_stats(selected_user,df)

        with col_1:
            st.header("Total message")
            st.title(num_mesages)

        with col_2:
            st.header("Total words")
            st.title(num_word)

        with col_3:
            st.header("Media shared")
            st.title(num_media)

        with col_4:
            st.header("Links shared")
            st.title(num_url)

        #time analysis
        st.title("Monthly Time Analysis")
        timeline = helper.time_analysis(selected_user,df)
        if timeline.shape[0] < 2:
            st.warning("Not enough data to show Monthly Time Analysis.")
        else:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(timeline['time'], timeline['messages'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        #activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            week_day = helper.weekly_activity(selected_user, df)
            if week_day.empty:
                st.warning("Not enough data to show Most Busy Day chart.")
            else:
                fig, ax = plt.subplots()
                ax.bar(week_day.index, week_day.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)


        with col2:
            st.header("Most Busy Month")
            month_name = helper.monthly_activity(selected_user, df)
            if month_name.empty:
                st.warning("Not enough data to show Most Busy Month chart.")
            else:
                fig, ax = plt.subplots()
                ax.bar(month_name.index, month_name.values, color='pink')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)


        # heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        # Check if heatmap is valid (non-empty, numeric)
        if user_heatmap.empty or not user_heatmap.select_dtypes(include='number').any().any():
            st.warning("Not enough data to generate heatmap.")
        else:
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, annot=False, fmt="g", cmap="YlGnBu")
            st.pyplot(fig)

        #finding the busiest user in the group(Group level)
        if selected_user =='Overall':
            st.title("Most Active Users")
            x, new_df = helper.busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color= 'purple')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        #most common words
        most_common_df = helper.most_common(selected_user,df)
        st.title('Most Common Words')
        fig,ax = plt.subplots(figsize=(9,5))
        ax.barh(most_common_df[0], most_common_df[1], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #emoji analysis
        common_emojis = helper.emojis(selected_user,df)
        st.title("Emoji Analysis")
        fig, ax = plt.subplots()
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(common_emojis)
        with col2:
            ax.pie(common_emojis.iloc[:, 1], labels=common_emojis.iloc[:, 0], autopct='%0.2f%%')
            st.pyplot(fig)

        

