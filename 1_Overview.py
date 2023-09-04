import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout='wide',
)

st.sidebar.success('Select a page above.')

st.sidebar.divider()

st.write("# Welcome to my Board Games Analysis! 👋")

st.markdown("""I've always had an enjoyment of boardgames, and being a data analyst by trades lead me to considering 
            what could be looked at in terms of boardgames, and where to get the information. BoardGameGeek is a 
            treasure trove of information, and because of this I have stood on the shoulders of those before me, and 
            gathered my own set of data to analyse. There is BGG data on Kaggle, but this is now very out of date 
            (5+ years old), and doesn't include the full data set available.""")
st.markdown("""Both Dinesh Vatvani and Markus Shepherd's scraping of Board Game Geek inspired me to start my own 
            analysis. I initially tried to update code I found that scraped BGG however I discovered Markus' 
            prescraped data contained much of the information I was interested in, so updated the scraper to pull the 
            last few bits from his public data.""")
st.markdown("""Some of the questions posed to the data include:
- What games are the most popular?
- Have releases of boardgames peaked, or do they continue to rise yearly?
- How have yearly releases been rated?
- How has the complexity (number on mechanics) changed in recent years?
- What is the most used mechanic in games?
- What is the average number of mechanics in games by yearly release?
- How have mechanics popularity changed? 2000 vs 2020
- What are the most prevalent themes in games?
- What are the average number of themes by game by year?
- How have the popularity of themes changed? 2000 vs 2020""")
