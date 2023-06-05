import pandas as pd
import altair as alt
import streamlit as st

from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode

df = pd.read_csv('board_games.csv')

st.set_page_config(
    layout='wide',
)

st.sidebar.success('Select a page above.')

st.header("Data Visualization - Continued 📈")

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


