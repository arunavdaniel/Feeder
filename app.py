import streamlit as st
import pandas as pd
import os

df_final = pd.read_csv('rss_feed_with_content_and_sentiment.csv')

st.title("Feeder")

search_term = st.text_input("Enter term(s) to search in the content:")

if st.button("Search"):
    if search_term:
        search_results = df_final[df_final['content'].str.contains(search_term, case=False, na=False)]
        
        if not search_results.empty:
            st.write(f"Found {len(search_results)} articles containing the term '{search_term}':")
            for index, row in search_results.iterrows():
                st.write(f"**Title:** {row['title']}")
                st.write(f"**Link:** {row['link']}")
                st.write(f"**Sentiment Score:** {row['sentiment']}")
                st.write(f"**Content Snippet:** {row['content'][:200]}...")
                st.write("---")
        else:
            st.write(f"No articles found containing the term '{search_term}'.")
    else:
        st.error("Please enter a term to search.")

if st.checkbox("Show full DataFrame"):
    st.write(df_final)

st.header("Manage RSS Feeds")

new_feed_url = st.text_input("Enter new RSS feed URL:")

if st.button("Add RSS Feed"):
    if new_feed_url:
        try:
            rss_df = pd.read_csv('rss_feeds.csv', header=None)
        except FileNotFoundError:
            rss_df = pd.DataFrame(columns=[0])

        rss_df = rss_df.append({0: new_feed_url}, ignore_index=True)
        rss_df.to_csv('rss_feeds.csv', index=False, header=False)

        st.success(f"RSS feed '{new_feed_url}' added successfully!")
    else:
        st.error("Please enter a valid RSS feed URL.")

st.subheader("Delete RSS Feed")

try:
    rss_df = pd.read_csv('rss_feeds.csv', header=None)
    delete_feed_url = st.selectbox("Select RSS feed to delete:", rss_df[0].tolist())

    if st.button("Delete RSS Feed"):
        if delete_feed_url:
            rss_df = rss_df[rss_df[0] != delete_feed_url]
            rss_df.to_csv('rss_feeds.csv', index=False, header=False)
            st.success(f"RSS feed '{delete_feed_url}' deleted successfully!")
        else:
            st.error("Please select a valid RSS feed to delete.")
except FileNotFoundError:
    st.write("No RSS feeds found.")

if st.button("Update"):
    os.system('python main.py')
    st.write("main.py script has been executed.")
