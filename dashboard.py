import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    data = data.drop(15870)
    data = data.drop_duplicates(subset=['id'])

    return data

@st.cache(allow_output_mutation=True)
def set_feature(data):
    data['price_m2'] = data['price'] / (data['sqft_lot'] * 0.092903)
    data['waterfront_bin'] = data['waterfront'].apply(lambda x: 'yes' if x == 1 else 'no')
    data['built'] = data['yr_built'].apply(lambda x: '<1955' if x < 1955 else '>=1955')
    data['basement'] = data['sqft_basement'].apply(lambda x: 'yes' if x > 0 else 'no')
    data['renovated'] = data['yr_renovated'].apply(lambda x: '>=2000' if x >= 2000 else
    '<2000' if 0 < x < 2000 else 'not renovated')
    data['renovated_bin'] = data['yr_renovated'].apply(lambda x: 'no' if x == 0 else 'yes')


    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data[['bathrooms', 'floors']] = data[['bathrooms', 'floors']].astype(int)



    data['season'] = data['month'].apply(lambda x: 'spring' if (3 <= x <= 5) else
                                                   'summer' if (6 <= x <= 8) else
                                                   'fall' if (9 <= x <= 11) else
                                                   'winter')

    return data

@st.cache(allow_output_mutation=True)
def purchase_house(data):
    zipcode = data[['zipcode', 'waterfront', 'price']].groupby(['zipcode', 'waterfront']).median().reset_index()
    zipcode = zipcode.rename(columns = {'price' : 'median_price_by_zip'})
    data = pd.merge(data, zipcode, how='inner', on=['zipcode', 'waterfront'])

    for i in range(len(data)):
        if (data.loc[i, 'price'] <= data.loc[i, 'median_price_by_zip']) & (data.loc[i, 'condition'] > 2):
            data.loc[i, 'status'] = 'buy'
        else:
            data.loc[i, 'status'] = 'dont_buy'

    return data

def purchase_season(data):
    purchase = data[data['status'] == 'buy']

    season = purchase[['zipcode', 'waterfront', 'season', 'price']].groupby(['zipcode', 'waterfront', 'season']).median().reset_index()
    season = season.rename(columns = {'price' : 'median_price_by_season'})
    season = pd.merge(purchase, season, how='inner', on=['zipcode', 'waterfront', 'season'])
    season = season.rename(columns = {'price' : 'buying_price'})


    for i in range(len(season)):
        if (season.loc[i, 'buying_price'] < season.loc[i, 'median_price_by_season']):
            season.loc[i, 'profit%'] = 0.3
            season.loc[i, 'selling_price'] = (1 + season.loc[i, 'profit%']) * season.loc[i, 'buying_price']
            season.loc[i, 'profit_$'] = season.loc[i, 'profit%'] * season.loc[i, 'buying_price']
        else:
            season.loc[i, 'profit%'] = 0.1
            season.loc[i, 'selling_price'] = (1 + season.loc[i, 'profit%']) * season.loc[i, 'buying_price']
            season.loc[i, 'profit_$'] = season.loc[i, 'profit%'] * season.loc[i, 'buying_price']

    opportunities = season[['id', 'zipcode', 'buying_price', 'selling_price', 'season', 'profit%', 'profit_$', 'price_m2', 'yr_built', 'bedrooms', 'bathrooms', ]]

    f_attributes = st.multiselect('Enter columns you want to analyze', opportunities.columns.sort_values())

    if (f_attributes != []):
        opportunities = opportunities.loc[:, f_attributes]
    else:
        opportunities = opportunities.copy()

    st.dataframe(opportunities, height=300)


    return season

def profit(data):
    c1, c2 = st.columns(2)

    display1 = c1.checkbox("Display to see maximum possible profits by zipcode")

    maximum_profit1 = data[['zipcode', 'profit_$']].groupby('zipcode').sum('profits_$').sort_values('profit_$', ascending=False).reset_index()
    maximum_profit1 = maximum_profit1.rename(columns = {'profit_$' : 'maximum_profit'})

    display2 = c2.checkbox("Display to see maximum possible profits by season")

    maximum_profit2 = data[['season', 'profit_$']].groupby('season').sum('profits_$').sort_values('profit_$', ascending=False).reset_index()
    maximum_profit2 = maximum_profit2.rename(columns = {'profit_$' : 'maximum_profit'})


    if display1:
        c1.subheader("Possible profits by zipcode")
        c1.dataframe(maximum_profit1, height=300)

    if display2:
        c2.subheader("Possible profits by season")
        c2.dataframe(maximum_profit2, height=300)

    return None

def available(data):
    display = st.checkbox("Display all available houses with their infos and status (Buy or Don't Buy).")

    if display:
        st.subheader("King County's available houses")
        st.dataframe(data, height=300)

    return None

@st.cache(allow_output_mutation=True)
def opportunities_map(data):
    fig = px.scatter_mapbox(data,
                            lat ='lat',
                            lon = 'long',
                            color = 'status',
                            size = 'price',
                            size_max = 15,
                            zoom = 10,
                            color_discrete_sequence=px.colors.qualitative.G10)

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(height=600, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

    return fig

def hipotesis1_2(data):
    # hipotesis 1
    wtfrnt = data[['waterfront_bin', 'price']].groupby('waterfront_bin').mean().reset_index()
    wtfrnt['YoY'] = wtfrnt['price'].pct_change()

    difference1 = wtfrnt.iloc[1, 2] * 100

    fig1 = px.bar(wtfrnt, x='waterfront_bin', y='price', color='waterfront_bin',
                 title='Waterfront average price', color_discrete_sequence=px.colors.qualitative.G10, labels = {'price': 'Average price', 'waterfront_bin':'Waterfront'})

    # hipotesis 2
    built = data[['built', 'price']].groupby('built').mean().reset_index()
    built['YoY'] = built['price'].pct_change()

    difference2 = built.iloc[1, 2] * 100

    fig2 = px.bar(built, x='built', y='price', color='built', title='Built year average price',
                 color_discrete_sequence=px.colors.qualitative.G10,
                 labels={'price': 'Average price', 'built': 'Year built'})


    c1, c2 = st.columns(2)

    c1.subheader('Hipotesis 1 - Waterfront properties, are 30% more expensive, in average.')
    c1.plotly_chart(fig1, use_container_width=True)
    c1.write(f"Hipotesis 1 answer: TRUE - The waterfront properties' price is {round(difference1, 2)}% higher, in average")

    c2.subheader('Hipotesis 2 - Properties built before 1955 are 50% cheaper, in average')
    c2.plotly_chart(fig2, use_container_width=True)
    c2.write(f"Hipotesis 2 answer - FALSE - Properties built before 1955 are {round(difference2, 2)}% cheaper, in average")

    return None

def hipotesis3_4(data):
    # hipotesis 3
    basement = data[['basement', 'sqft_lot']].groupby('basement').mean().reset_index().sort_values('basement', ascending=False)
    basement['YoY'] = basement['sqft_lot'].pct_change()

    difference1 = basement.iloc[1, 2] * 100

    fig1 = px.bar(basement, x='basement', y='sqft_lot', color='basement',
                 title='Building with basements average total area', color_discrete_sequence=px.colors.qualitative.G10,
                 labels={'sqft_lot': 'Average area', 'basement': 'Basement'})

    # hipotesis 4
    year = data[['year', 'price']].groupby('year').mean().reset_index()
    year['YoY'] = year['price'].pct_change()

    difference2 = year.iloc[1, 2] * 100

    year['year'] = year['year'].astype(str)  # converting from int64 to str for the plotly axis X format
    fig2 = px.bar(year, x='year', y='price', color='year', title='Average price by year',
                 color_discrete_sequence=px.colors.qualitative.G10, labels={'year': 'Year', 'price': 'Average price'})

    c1, c2 = st.columns(2)

    c1.subheader('Hipotesis 3 - Properties without basement have 40% bigger total area, in average ')
    c1.plotly_chart(fig1, use_container_width=True)
    c1.write(f"Hipotesis 3 answer - FALSE - Properties with basement are {round(difference1, 2)}% bigger, in average")

    c2.subheader('Hipotesis 4 - The YoY (Year over Year) price increasing is 10%')
    c2.plotly_chart(fig2, use_container_width=True)
    c2.write(f"Hipotesis 4 answer - FALSE - The price YoY increasing is {round(difference2, 2)}%, in average")

    return None

def hipotesis5_6(data):
    # hipotesis 5
    bathroom = data[data['bathrooms'] == 3]
    bathroom = bathroom[['year', 'month', 'price']].groupby(['year', 'month']).mean().reset_index()
    bathroom['year'] = bathroom['year'].astype(str)
    bathroom['month'] = bathroom['month'].astype(str)
    bathroom['period'] = bathroom['month'] + '-' + bathroom['year']

    bathroom['MoM'] = bathroom['price'].pct_change()

    fig1 = px.bar(bathroom, x='period', y='MoM', color='period', title='MoM average price',
                 color_discrete_sequence=px.colors.qualitative.Dark24,
                 labels={'price': 'Average price', 'period': 'Period'})

    # hipotesis 6
    ren = data[data['renovated_bin'] == 'yes'][['renovated', 'price']].groupby('renovated').mean().reset_index()

    ren['%'] = ren['price'].pct_change()
    difference2 = ren.iloc[1, 2] * 100

    fig2 = px.bar(ren, x='renovated', y='price', color='renovated', title='Buildings renovated before or after 2000',
                  color_discrete_sequence=px.colors.qualitative.G10,
                  labels={'price': 'Average price', 'renovated': 'Year renovated'})


    c1, c2 = st.columns(2)

    c1.subheader('Hipotesis 5 - Properties with 3 bathrooms have 15% increasing of MoM (Month over Month)  ')
    c1.plotly_chart(fig1, use_container_width=True)
    c1.write(f"Hipotesis 5 answer - FALSE - As it is seen, none of the historical MoM is over 15%")

    c2.subheader('Hipotesis 6 - Properties renovated after 2000 are 60% more expensive, in average, than renovated before 2000')
    c2.plotly_chart(fig2, use_container_width=True)
    c2.write(f"Hipotesis 6 answer - FALSE - The price of properties built after 2000 is {round(difference2, 2)}% more expensive than those built before 2000, in average")


def hipotesis7_8(data):
    # hipotesis 7
    renovated = data[['renovated_bin', 'price']].groupby('renovated_bin').mean().reset_index()

    renovated['%'] = renovated['price'].pct_change()
    difference1 = renovated.iloc[1, 2] * 100

    fig1 = px.bar(renovated, x='renovated_bin', y='price', color='renovated_bin',
                 title='Average price by renovated buildings', color_discrete_sequence=px.colors.qualitative.G10,
                 labels={'price': 'Average price', 'renovated_bin': 'Renovated'})


    # hipotesis 8
    data = data[(data['season'] == 'summer') | (data['season'] == 'winter')]
    season = data[['season', 'price']].groupby('season').mean().reset_index().sort_values('season', ascending=False)

    season['%'] = season['price'].pct_change()
    difference2 = season.iloc[1, 2] * 100

    fig2 = px.bar(season, x='season', y='price', color='season', title='Average price by season',
                 color_discrete_sequence=px.colors.qualitative.G10,
                 labels={'price': 'Average price', 'season': 'Season'})


    c1, c2 = st.columns(2)

    c1.subheader('Hipotesis 7 - Properties with 3 bathrooms have 15% increasing of MoM (Month over Month)  ')
    c1.plotly_chart(fig1, use_container_width=True)
    c1.write(f"Hipotesis 7 answer - TRUE - The price of renovated properties is {round(difference1, 2)}% more expensive than not renovated buildings, in average")

    c2.subheader('Hipotesis 8 - Properties renovated after 2000 are 60% more expensive, in average, than renovated before 2000')
    c2.plotly_chart(fig2, use_container_width=True)
    c2.write(f"Hipotesis 8 answer - FALSE - Properties price in summer is {round(difference2, 2)}% more expensive than in winter, in average")


if __name__ == '__main__':
    path = 'kc_house_data.csv'

    st.title('Real State Case - Seeking Opportunities in King County US-WA')
    st.subheader('Some assumptions')
    st.text('- If “condition” column =< 2 then "bad";\n- If “condition” column =  3 or 4 then "regular";\n- If “condition” column = 5 then "good".\n\n\n ')
    st.write("If price is minor than median price by zipcode, condition is regurlar or good and there is waterfront, then buy else don't buy")

    st.sidebar.title('About')
    st.sidebar.markdown('House Rocket is a real state company located in King County - Settle, WA - USA. Its core business is based on purchasing properties at lower prices compared to the market, renovating and selling them in order to make a profit.')
    st.sidebar.header('Business questions:')
    st.sidebar.markdown('1. Which properties House Rocket should buy and which price?')
    st.sidebar.markdown('2. Once bought, when should be the the best time to sell it and which price?')

    df = get_data(path)

    df = set_feature(df)

    house = purchase_house(df)

    fig = opportunities_map(house)
    st.plotly_chart(fig)

    st.subheader('Opportunities')
    season = purchase_season(house)

    st.write('')
    st.subheader('Maximum possible profits')
    profit(season)

    st.write('')
    st.write('If you wish to see all available houses and its attributes, display the box bellow')

    available(house)

    hipotesis1_2(house)
    hipotesis3_4(house)
    hipotesis5_6(house)
    hipotesis7_8(house)
