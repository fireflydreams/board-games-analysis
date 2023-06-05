import pandas as pd
import altair as alt
import streamlit as st

from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode

df = pd.read_csv('board_games.csv')

st.set_page_config(
    layout='wide',
)

st.sidebar.success('Select a page above.')

st.header("Data Visualization 📈")

st.markdown("""Now that the initial data exploration has been done, and I'm happy with the results of it, it's time to
            actually look at the data and start visualizing to see what trends I can find. The first thing I'd like to 
            look at is the most owned game according to BGG. Now this has to come with a couple of caveats. First, 
            BGG is only a snapshot of board game owners. Not everyone who owns any board games is on BGG. Second BGG
            is an enthusiasts cataloging/databse system. Enthusiasts often do not own some of the classic childhood
            board games such as Chess, Monopoly, Cluedo (Clue) etc, or do not register them as owned. Many sources cite 
            these as the most owned board games, so lets see what BGG believes to be the most owned:""")

df_most_owners = df.sort_values('total_owners', ascending=False).head(50)

st.subheader('Most owned BGG')
chart = (
    alt.Chart(df_most_owners).mark_bar().encode(
        x=alt.X('name', sort='-y', title='Name'),
        y=alt.Y('total_owners', title='Owner Count'),
        color=alt.Color("name", legend=None),
    )
)
st.altair_chart(chart, use_container_width=True)

st.markdown("""So as I suspected, none of the 'Classic' games are included in the top 50. Yet articles such as 
            \[[1](https://www.fun.com/best-selling-board-games-all-time.html)\], 
            \[[2](https://moneyinc.com/highest-selling-board-games-of-all-time/)\],
            \[[3](https://brandonthegamedev.com/the-10-most-popular-board-games-of-all-time-and-why-they-made-board-gaming-better/)\]
            mostly all agree, that Chess, Checkers, Monopoly, Trivia Persuit etc are among the most popular games. The
            only game from the top 50 on BGG that appears on these top Board Games sites is Catan. Comparative to the
            articles on top board games, where Catan appears quite far down most, it's the most popular on BGG.""")

st.markdown("""Next, I wanted to investigate whether numbers of board games released per year continued to increase, as
            seen by Dinesh Vatvani in 2018, or if there was a tipping point. """)

yearly_release = df.groupby(['yearpublished']).size().reset_index(name='count')
yearly_release = yearly_release.drop(yearly_release.index[-1])
yearly_release['yearpublished'] = yearly_release['yearpublished'].astype(int)
yearly_release_limited = yearly_release[(yearly_release['yearpublished'] >= 1950)].copy()

st.subheader('Yearly Board Game Releases')
chart = (
    alt.Chart(yearly_release_limited).mark_line(point=True).encode(
        x=alt.X('yearpublished', title='Release Year'),
        y=alt.Y('count', title='Count'),
    )
)
st.altair_chart(chart, use_container_width=True)

st.markdown("""Having plotted the releases by year from 1950 onwards, we can see around the 1970s, there is a gradual
            increase in releases, which starts to pick up momentum. By 1990 we are starting to see the releases increase
            rapidly, however by early 2000s we can see the release numbers have doubled since 1990, and this trend 
            continues well into the 2010s. Generally speaking, we are seeing more and more games released every year.
            This appears to hit a peak in 2019, of 1440 games released. This is where we have to start to note global
            events. In early 2020 a virus that seemed to originate in China, spread worldwide and became a pandemic, 
            the likes of which had not been seen for almost a hundred years (influenza pandemic of 1918-1919). """)

st.markdown("""The COVID-19 virus caused a few things to happen:
- China shutdown ***all*** production. Nothing was made, which had a significant impact on board games. Cardboard became in 
short supply, meaning kickstarted projects went on indefinite hold, planned games stopped being produced, and games were
not assembled.
- Shipping became a huge problem. Shipping prices went massively increased due to backlogs, people unable to work due to 
lockdowns etc.
- Companies closed. With little to no income, as products couldn't be made, many companies did not survive the pandemic.
- Oil prices tanked. Once rich countries found themselves unable to sell oil as the world demand decreased due to lack
of requirement for travel etc, meaning individuals found themselves with less disposable income.""")

st.markdown("""Not all of these immediately impacted board game releases, however the impact can be seen in years to 
            come. In 2020 we drop 200 board game releases. This drop continues into 2021 and 2022, with the releases 
            almost halving in 2022. Board game releases are definitely slowing down.""")

st.markdown("""I theorise this could be because of a few different things:
- Kickstarters failing to fund:-
    - Less disposable income due to cost of living crisis, lost jobs due to COVID-19 etc.
    - Shipping costs putting off people from backing from outside their country. 
    - Loss of trust in Kickstarter campaigns as some failed to fulfill (see problems with shipping and China shutdowns).
- Companies liquidating. COVID-19 shutdowns went on some long, some companies ceased trading.
- Market Saturation. Are too many similar games being proposed/coming out causing people to evaluate if their need 
another 'x' mechanic game.
- China backlog. Too many items (not just board games) awaiting production, pushing production dates back, impacting
company profits.""")

st.markdown("""So, having looked at most popular (according to BGG) and releases/year... what's next?""")

rating_year = df[['yearpublished', 'average_rating', 'users_rated', 'name']].copy()
rating_year = rating_year[(rating_year['yearpublished'] != 'unknown')]
rating_year['yearpublished'] = rating_year['yearpublished'].astype(int)
rating_year = rating_year[(rating_year['yearpublished'] >= 1990)]
enough_ratings = rating_year[(rating_year['users_rated'] >= 150)].copy()

st.subheader('Yearly Rankings')

stripplot = alt.Chart(enough_ratings).mark_circle(size=8).encode(
    x=alt.X(
        'jitter:Q',
        title=None,
        axis=alt.Axis(ticks=True, grid=False, labels=False),
        scale=alt.Scale(),
    ),
    y=alt.Y('average_rating:Q', title='Rating'),
    color=alt.Color('yearpublished:N', legend=None),
).transform_calculate(
    # Generate Gaussian jitter with a Box-Muller transform
    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
)
meanplot = alt.Chart(enough_ratings).mark_point(size=30).encode(
    y=alt.Y('mean(average_rating):Q'),
    color=alt.value('#ffff99'),
)
fullplot = (stripplot+meanplot).properties(
    width=27,
).facet(
    column=alt.Column(
        'yearpublished', title=None,
        header=alt.Header(
            labelColor='white',
            labelFontSize=12,
            labelAngle=0,
            titleOrient='top',
            labelOrient='bottom',
            labelAlign='center',
            labelPadding=25,
        ),
    ),
).configure_facet(
    spacing=5
).configure_view(
    stroke=None
)

st.altair_chart(fullplot)

st.markdown("""Looking at this chart, we can see that every year more and more reviews are submitted for games (which
            is consistent with increased releases) but also as of 2019 on average games are rated over 7/10. This is 
            despite some significantly low rated games:""")

low_rated = enough_ratings[(enough_ratings['average_rating'] <= 4) & (enough_ratings['yearpublished'] >= 2015)].copy()
low_rated = low_rated.sort_values('yearpublished')

mean_ratings = enough_ratings.groupby(['yearpublished']).mean(numeric_only=True).reset_index()
mean_ratings = mean_ratings.drop('users_rated', axis=1)
ratings = low_rated.merge(mean_ratings, on=['yearpublished'])
ratings = ratings.rename(columns={'average_rating_x': 'game_average',
                                  'average_rating_y': 'year_average'})
ratings['difference'] = ratings['year_average'] - ratings['game_average']
columnsTitles = ['yearpublished', 'users_rated', 'name', 'game_average', 'year_average', 'difference']
ratings = ratings.reindex(columns=columnsTitles)
ratings = ratings.rename(columns={'yearpublished': 'Publication Year',
                                  'users_rated': 'Users Rated',
                                  'name': 'Name',
                                  'game_average': 'Game Rating',
                                  'year_average': 'Yearly Average Rating',
                                  'difference': 'Difference'})


gb = GridOptionsBuilder.from_dataframe(ratings)
gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
gridOptions1 = gb.build()
st.caption('Low Rated Games, Published After 2015')
AgGrid(ratings, gridOptions=gridOptions1, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
       allow_unsafe_jscode=True)

st.markdown("""Without looking at further criteria for why these games are so low rated, it is hard to quantify the
            reasons behind it, however compared to the yearly average, these are very low rated games.""")
st.markdown("""Going back to the original graph, it does appear at face value games are getting better. Ratings are 
            increasing year on year, and have hit an all time high. This increase has been quite steady since 2004. 
            Going back to the BGG website and looking at the current top 100 games, you can see some of the most popular
            games are several years old. Within the top 10 there are none from 2022, and only one from 2021. Most are 
            from 2017-2020. Has their popularity come from lockdown when people were stuck at home and turned to long
            campaign boardgames to occupy time? Or indepth games that can take hours to complete? Or games you can play 
            solo? I believe many of these to be contributing factors to more people getting into boardgames and therefor
            discovering Board Game Geek and rating games.""")

complexity = df[['yearpublished', 'average_weight', 'total_weights', 'name']].copy()
complexity_year = complexity[(complexity['yearpublished'] != 'unknown')].copy()
complexity_year['yearpublished'] = complexity_year['yearpublished'].astype(int)
complexity_year = complexity_year[(complexity_year['yearpublished'] >= 1990)]
enough_weights = complexity_year[(complexity_year['total_weights'] >= 150)].copy()
# st.table(enough_weights)
st.subheader('Yearly Weightings (Complexity)')

stripplot = alt.Chart(enough_weights).mark_circle(size=8).encode(
    x=alt.X(
        'jitter:Q',
        title=None,
        axis=alt.Axis(ticks=True, grid=False, labels=False),
        scale=alt.Scale(),
    ),
    y=alt.Y('average_weight:Q', title='Rating'),
    color=alt.Color('yearpublished:N', legend=None),
).transform_calculate(
    # Generate Gaussian jitter with a Box-Muller transform
    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
)
meanplot = alt.Chart(enough_weights).mark_point(size=30).encode(
    y=alt.Y('mean(average_weight):Q'),
    color=alt.value('#ffff99'),
)
fullplot = (stripplot+meanplot).properties(
    width=27,
).facet(
    column=alt.Column(
        'yearpublished', title=None,
        header=alt.Header(
            labelColor='white',
            labelFontSize=12,
            labelAngle=0,
            titleOrient='top',
            labelOrient='bottom',
            labelAlign='center',
            labelPadding=25,
        ),
    ),
).configure_facet(
    spacing=5
).configure_view(
    stroke=None
)

st.altair_chart(fullplot)

st.markdown("""Is it that more complex games are prompting people to feel a greater sense of reward and enjoyment? Or 
            are simpler games popular? Time to take a look. The data for this has been limited to 1950 onwards, which is 
            likely to remain the same for all future exploration as this is when games start to pick up popularity on 
            releases. A description of mechanics according to the BGG community can be found here: 
            \[[mechanisms](https://boardgamegeek.com/wiki/page/mechanism)\]""")

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
df_mechanics = df_mechanics.groupby(['mechanics'])['mechanics'].count().reset_index(name='Count')
df_most_mechanics = df_mechanics.sort_values('Count', ascending=False).head(50)

st.subheader('Most Popular Mechanics')

chart = (
    alt.Chart(df_most_mechanics).mark_bar().encode(
        x=alt.X('Count'),
        y=alt.Y('mechanics', sort='-x'),
        color=alt.Color("mechanics", legend=None),
    )
)
st.altair_chart(chart, use_container_width=True)

st.markdown("""The top mechanics (Dice Rolling, and Roll or Spin to Move) are not inherently particularly complicated 
            mechanics. Hand Management and Set Collection are more so, but still individually not overly complex. This 
            has then lead to the question: 'Are the amount of mechanics in games becoming higher?' The chart below will 
            explore this question.""")

df_mechanics_years = df[['yearpublished', 'name', 'mechanics']].copy()
df_mechanics_years['mechanics'] = df_mechanics_years['mechanics'].str.replace('Deck, Bag, and Pool Building',
                                                                              'Deck / Bag / Pool Building')
df_mechanics_years['mechanics'] = df_mechanics_years['mechanics'].str.\
    replace('Worker Placement, Different Worker Types',
            'Worker Placement / Different Worker Types')
df_mechanics_years['mechanics'] = df_mechanics_years['mechanics'].str.replace('I Cut, You Choose',
                                                                              'I Cut / You Choose')
df_mechanics_years['mechanics'] = df_mechanics_years['mechanics'].str.split(',')
df_mechanics_years = df_mechanics_years.explode('mechanics')
df_mechanics_years = df_mechanics_years.groupby(['yearpublished', 'name']).count().reset_index()
df_mechanics_years = df_mechanics_years[(df_mechanics_years['yearpublished'] != 'unknown')]
df_mechanics_years['yearpublished'] = df_mechanics_years['yearpublished'].astype(int)
df_mechanics_years = df_mechanics_years[(df_mechanics_years['yearpublished'] >= 1950)]
df_mechanics_years = df_mechanics_years[(df_mechanics_years['mechanics'] > 0)]
df_mechanics_years = df_mechanics_years.groupby(['yearpublished']).mean(numeric_only=True).reset_index()

st.subheader('Average Number of Mechanics/Game')

chart = (
    alt.Chart(df_mechanics_years).mark_circle().encode(
        x=alt.X('yearpublished', title='Release Year', scale=alt.Scale(domain=[1950, 2030])),
        y=alt.Y('mechanics'),
    )
)
st.altair_chart(chart, use_container_width=True)

st.markdown("""Until 2013 we remain at around a 2.5 average amount of mechanics per game. Not too high. After 2014 we 
            start to see the complexity creep begin, with a sharp rise seen 2019 onwards. This means that it does look
            like games are getting more complex, which was also shown by the complexity rating increasing also. With the
            increase in ratings, seen in 
            \[[the weightings chart](/Part_2_-_Data_Visualization_%F0%9F%93%88#yearly-weightings-complexity)\] 
            it does appear people are starting to favour more complex games.""")
