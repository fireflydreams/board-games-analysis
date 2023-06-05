import io
import pandas as pd
import streamlit as st

from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode

df = pd.read_csv('board_games.csv')

st.set_page_config(
    layout='wide',
)

st.sidebar.success('Select a page above.')

st.header("Data Exploration 🗺️")

st.markdown("To start this project, as with any project, some initial data exploration is needed.")

buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()

st.text(s)

st.markdown("""First df.info() was run on the data and this is shown above. It shows there are some null values in 
            3 columns, but these three are ones that while are interesting to analyse, are not integral to the 
            initial work. Therefor I will not be dropping the rows with nulls in Categories, Mechanics or Designer.""")

st.write(df.describe())

st.markdown("""Next df.describe() was run on the data to ensure no columns have values that appear to be out of the 
            realm of acceptable. Ignoring the ID column, as this one is the ID assigned to the game by BGG, most 
            columns appear to have values within normal limits.""")

st.markdown("""There are four that this does not apply to:
- playtime
- maxplaytime
- minplaytime and 
- maxplayers.""")

st.markdown("""Each of the play times columns appears to have a very large max value (60000-84000 minutes). While this 
            could be due to long campaign games; such as ISS Vanguard, Middara, Sword and Sorcery and the likes, this 
            does need looking at further just to sense check these numbers.""")

df_size_check = df[(df['playingtime'] >= 1440)].copy()
gb = GridOptionsBuilder.from_dataframe(df_size_check)
gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
gridOptions = gb.build()
st.caption('Games over 24 hours long')
AgGrid(df_size_check, gridOptions=gridOptions, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
       allow_unsafe_jscode=True)

st.markdown("""Loading the above list, I was surprised to see very few long campaign games. Digging into the games I 
            could identify as long campaign, I searched BGG for them and it appears their playtime is measured by 
            session time, rather than full game time. The games that did show up appear to mostly be wargames. These 
            simulation games are heavily skewing numbers and are going to be dropped for the purposes of this 
            analysis. Filtering these games out left 30 games (filtering was done on category, removing everything 
            referencing any type of war related game.""")

st.markdown("""These remaining 30 games had some similar categories appear. Party was a common theme, as co-operative
            and dice rolling. Without digging into each and every game to see why the game time is so high, it's hard to
             make generalizations, however I would like to believe many of these are 'real life' games. ie games you 
            play while going about everyday life.""")

st.markdown("""The last column to investigate is the max players. Board games with over 10 players sounds to me like
            a exercise that would decend into chaos. So a table of games with more than 10 max players was created to
            investigate these games.""")

df_players_check = df[(df['maxplayers'] > 10)].copy()
gb = GridOptionsBuilder.from_dataframe(df_players_check)
gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
gridOptions1 = gb.build()
st.caption('Games with over 10 max players')
AgGrid(df_players_check, gridOptions=gridOptions1, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
       allow_unsafe_jscode=True)

st.markdown("""517 of the 863 games are tagged as party games in the categories. This shows how the max number of 
            players can be so high. The remaining 346 have a couple of tags in common, such as 'Word Games', 'Dice', 
            'Trivia' each of which can explain a higher max player count. For this reason I do not believe any to 
            require removal from the data set.""")
st.markdown("""With this initial data exploration complete, and all potentially erroneous data investigated, it
            is time to move onto visualizing the data to see what meaningful information can be pulled form this
            dataset.""")
