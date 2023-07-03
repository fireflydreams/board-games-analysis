import pandas as pd
import altair as alt
import streamlit as st

df = pd.read_csv('board_games.csv')

st.set_page_config(
    layout='wide',
)

st.sidebar.success('Select a page above.')

st.header("Data Visualization - Continued 📈")

st.markdown("""We've had a look at some initial data analysis, now I'm going to start looking at more indepth 
            analysis.""")

yearly_release = df.groupby(['yearpublished']).size().reset_index(name='count')
yearly_release = yearly_release.drop(yearly_release.index[-1])
yearly_release['yearpublished'] = yearly_release['yearpublished'].astype(int)
yearly_release_limited = yearly_release[(yearly_release['yearpublished'] >= 1950)].copy()

releases_2000 = yearly_release_limited.loc[yearly_release_limited['yearpublished'] == 2000, 'count'].iloc[0]
releases_2020 = yearly_release_limited.loc[yearly_release_limited['yearpublished'] == 2020, 'count'].iloc[0]

df_mechanics = df[['yearpublished', 'mechanics']].copy()
df_mechanics['mechanics'] = df_mechanics['mechanics'].str.replace('Deck, Bag, and Pool Building',
                                                                  'Deck / Bag / Pool Building')
df_mechanics['mechanics'] = df_mechanics['mechanics'].str.replace('Worker Placement, Different Worker Types',
                                                                  'Worker Placement / Different Worker Types')
df_mechanics['mechanics'] = df_mechanics['mechanics'].str.replace('I Cut, You Choose',
                                                                  'I Cut / You Choose')
df_mechanics['yearpublished'] = df_mechanics['yearpublished'].astype(int)
df_mechanics = df_mechanics[(df_mechanics['yearpublished'] >= 1950)]
df_mechanics['mechanics'] = df_mechanics['mechanics'].str.split(',')
df_mechanics = df_mechanics.explode('mechanics')
df_mechanics_2000 = df_mechanics[(df_mechanics['yearpublished'] == 2000)]
df_mechanics_2000 = df_mechanics_2000.groupby(['mechanics'])['mechanics'].count().reset_index(name='2000')
df_most_mechanics_2000 = df_mechanics_2000.sort_values('2000', ascending=False).head(50)
df_most_mechanics_2000['2000'] = df_most_mechanics_2000['2000'].div(releases_2000)*100


df_mechanics_2020 = df_mechanics[(df_mechanics['yearpublished'] == 2020)]
df_mechanics_2020 = df_mechanics_2020.groupby(['mechanics'])['mechanics'].count().reset_index(name='2020')
df_most_mechanics_2020 = df_mechanics_2020.sort_values('2020', ascending=False).head(50)
df_most_mechanics_2020['2020'] = df_most_mechanics_2020['2020'].div(releases_2020)*100

df_most_mechanics = df_most_mechanics_2020.merge(df_most_mechanics_2000, left_on='mechanics',
                                                 right_on='mechanics')
df_most_mechanics = pd.melt(df_most_mechanics, id_vars=['mechanics'], value_vars=['2000', '2020'],
                            var_name='year', value_name='percent')

st.subheader('Mechanics Popularity Change, 2000 -> 2020')

domain = ['2000', '2020']
colors = ['skyblue', 'mediumorchid']

lines = alt.Chart(df_most_mechanics).mark_line(point=True).encode(
    x='percent',
    y='mechanics',
    detail='mechanics',
    color=alt.value('lightskyblue'),
)

points = alt.Chart(df_most_mechanics).mark_circle(size=100).encode(
    x=alt.X('percent', title='Percentage Usage'),
    y=alt.Y('mechanics', title='Mechanic'),
    color=alt.Color('year', scale=alt.Scale(domain=domain, range=colors))
)

st.altair_chart(lines + points, use_container_width=True)

st.markdown("""This is an interesting section to look at. Each mechanic has had the proportion of games it is used in 
            calculated, then the percentage change mapped onto a slope chart. Pale blue is the starting point (ie 2000)
            and purple is the end point (ie 2020). For the most part, mechanics seen an increase in their usage. This
            correlates to the idea that games and combining more and more mechanics together. There are a few that need 
            calling out for their extreme fall from fashion. The first is roll/spin and move. This is a typical 
            mechanic seen in "classic" games such as Monopoly, Game of Life, Snakes & Ladders etc. In 2000 this mechanic 
            was used in over 20% of games released that year, in 2020 it was only used in 4%. This is a huge drop in 
            popularity, meaning alternative methods of movement are being used in games. We can see Grid Movement, 
            Measurement Movement and (to a lesser extent) Point to Point movement increasing in popularity.""")

st.markdown("""Trading, Set Collection, Memory, Hexagon Grid and Auction/Bidding have all also seen a downturn in usage.
            However none of these are as extreme as roll/spin and move.""")

df_categories = df[['yearpublished', 'categories']].copy()
df_categories['yearpublished'] = df_categories['yearpublished'].astype(int)
df_categories = df_categories[(df_categories['yearpublished'] >= 1950)]
df_categories['categories'] = df_categories['categories'].str.split(',')
df_categories = df_categories.explode('categories')
df_categories = df_categories.groupby(['categories'])['categories'].count().reset_index(name='Count')
df_most_categories = df_categories.sort_values('Count', ascending=False).head(50)

st.subheader('Most Popular Themes')

chart = (
    alt.Chart(df_most_categories).mark_bar().encode(
        x=alt.X('Count'),
        y=alt.Y('categories', title='Themes', sort='-x'),
        color=alt.Color("categories", legend=None),
    )
)
st.altair_chart(chart, use_container_width=True)

st.markdown("""Possibly unsurprisingly, Card Games are the most popular theme in board games. So many games include
            cards of some description, whether collectable/tradable, or static either way, this is wholly unsurprising.
            As the general view on games if they're for kids and parties, it's also unsurprising that these also feature
            highly in popular themes. Miniatures has been rising in popularity, so it is nice to see these in the top
            half of the table. Many games come with absolutely beautiful miniatures, but an often be underappreciated if
            game-play was sacrificed in favour of the miniatures.""")

df_categories_years = df[['yearpublished', 'name', 'categories']].copy()

df_categories_years['categories'] = df_categories_years['categories'].str.split(',')
df_categories_years = df_categories_years.explode('categories')
df_categories_years = df_categories_years.groupby(['yearpublished', 'name']).count().reset_index()
df_categories_years = df_categories_years[(df_categories_years['yearpublished'] != 'unknown')]
df_categories_years['yearpublished'] = df_categories_years['yearpublished'].astype(int)
df_categories_years = df_categories_years[(df_categories_years['yearpublished'] >= 1950)
                                        & (df_categories_years['yearpublished'] <= 2023)]
df_categories_years = df_categories_years[(df_categories_years['categories'] > 0)]
df_categories_years = df_categories_years.groupby(['yearpublished']).mean(numeric_only=True).reset_index()

st.subheader('Average Number of Themes/Game')

chart = (
    alt.Chart(df_categories_years).mark_circle().encode(
        x=alt.X('yearpublished', title='Release Year', scale=alt.Scale(domain=[1950, 2024])),
        y=alt.Y('categories', title='Themes', scale=alt.Scale(domain=[0, 6])),
    )
)
st.altair_chart(chart, use_container_width=True)

st.markdown("""Unlike board game mechanics, we've barely seen any increase in the number of themes in games increase. 
            Since 1950 there is a marginal increase from an average of 2 themes to an average of 3, but this is 
            different to the increase seen in average mechanics which changed from 1.5 -> more than 5.""")


df_themes = df[['yearpublished', 'categories']].copy()
df_themes['yearpublished'] = df_themes['yearpublished'].astype(int)
df_themes = df_themes[(df_themes['yearpublished'] >= 1950)]
df_themes['categories'] = df_themes['categories'].str.split(',')
df_themes = df_themes.explode('categories')
df_themes_2000 = df_themes[(df_themes['yearpublished'] == 2000)]
df_themes_2000 = df_themes_2000.groupby(['categories'])['categories'].count().reset_index(name='2000')
df_most_categories_2000 = df_themes_2000.sort_values('2000', ascending=False).head(50)
df_most_categories_2000['2000'] = df_most_categories_2000['2000'].div(releases_2000)*100

df_themes_2020 = df_themes[(df_themes['yearpublished'] == 2020)]
df_themes_2020 = df_themes_2020.groupby(['categories'])['categories'].count().reset_index(name='2020')
df_most_categories_2020 = df_themes_2020.sort_values('2020', ascending=False).head(50)
df_most_categories_2020['2020'] = df_most_categories_2020['2020'].div(releases_2020)*100

df_most_categories = df_most_categories_2020.merge(df_most_categories_2000, left_on='categories',
                                                   right_on='categories')
df_most_categories = pd.melt(df_most_categories, id_vars=['categories'], value_vars=['2000', '2020'],
                             var_name='year', value_name='percent')

st.subheader('Themes Popularity Change, 2000 -> 2020')

domain = ['2000', '2020']
colors = ['skyblue', 'mediumorchid']

lines = alt.Chart(df_most_categories).mark_line(point=True).encode(
    x='percent',
    y='categories',
    detail='categories',
    color=alt.value('lightskyblue'),
)

points = alt.Chart(df_most_categories).mark_circle(size=100).encode(
    x=alt.X('percent', title='Percentage Usage'),
    y=alt.Y('categories', title='Themes'),
    color=alt.Color('year', scale=alt.Scale(domain=domain, range=colors))
)

st.altair_chart(lines + points, use_container_width=True)

st.markdown("""Again most themes have increased in use, but games can use multiple themes so not unsurprising. Some
            themes have lost popularity as with mechanics. Most notable are: Trivia, Movies/TV/Radio and Children's.
            Increasing in popularity are Card Games (not just TCG and CCG, just games that use cards), Adventure
            and Print & Play.""")

st.markdown("""Print & Play is an interesting one as generally the creators make no money from creating the game, and
            the game cannot be bought, so "owning" it is relative. In theory everyone and no one owns the game as it's
            freely available.""")
