import streamlit as st
import pandas as pd
import base64
import plotly_express as px
from bs4 import BeautifulSoup
import requests
import json
import time

#WebScraping coinmarketcap.com#
#-----------------------------#

#Getting the coin values
#-----------------------------#
cmc = requests.get('https://coinmarketcap.com')
soup = BeautifulSoup(cmc.content, 'html.parser')
data = soup.find('script', id='__NEXT_DATA__', type='application/json')
coins = {}
coin_data = json.loads(data.contents[0])
listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
for i in listings:
    coins[str(i['id'])] = i['slug']

#Initializing the variables
#-----------------------------#
coin_name = []
coin_symbol = []
market_cap = []
percent_change_1h = []
percent_change_24h = []
percent_change_7d = []
price = []
volume_24h = []

#Getting the values to the variables
#----------------------------------#
for i in listings:
    coin_name.append(i['slug'])
    coin_symbol.append(i['symbol'])
    price.append(i['quote'])

json_DF = pd.json_normalize(price)
df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
df['coin_name'] = coin_name
df['coin_symbol'] = coin_symbol
df['price'] = json_DF['USD.price']
df['percent_change_1h'] = json_DF['USD.percent_change_1h']
df['percent_change_24h'] = json_DF['USD.percent_change_24h']
df['percent_change_7d'] = json_DF['USD.percent_change_7d']
df['market_cap'] = json_DF['USD.market_cap']
df['volume_24h'] = json_DF['USD.volume_24h']

# Function to Download CSV data
#-----------------------------#
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

#Function to Plot pie chart
#--------------------------#
def plot_pie(options,view_options):
    fig = px.pie(df.head(10), values=options, names='coin_symbol', title=view_options)
    st.plotly_chart(fig)
    
#Dashboaard Layout
#----------------#
st.markdown("<h1 style='text-align: center; color: green;'>Crypto Currency Dashboard</h1><br>", unsafe_allow_html=True)
sidebar = st.sidebar

#Display Options
#---------------#
sidebar.write('Display Options')
view_All = sidebar.selectbox('View Dataset?', ['Yes','No'])
if view_All == 'Yes':
    view_options = sidebar.selectbox('Choose your option', ['Top 100 CryptoCurrencies', 'Historical Data for Bitcoin'])
    if view_options == 'Top 100 CryptoCurrencies':
        view = sidebar.slider("Select the top N values", 10, 1,100)
        st.write(view_options)
        st.write(df.head(view))
        st.markdown(filedownload(df.head(view)), unsafe_allow_html=True);
    else:
        st.write(view_options)
        df_hist = pd.read_csv('Nomics-CurrencyHistory-BTC-USD-1d-2021-01-04T15_20_18.559Z.csv')
        st.write(df_hist)
        st.markdown(filedownload(df_hist), unsafe_allow_html=True);
   
st.markdown("<h2 style='text-align: center; color: green;'>Pie plot for Top 10 currencies</h2>", unsafe_allow_html=True)
sidebar.subheader('Graph Options')
view_options = sidebar.selectbox('View Options', ['Market_Cap', 'Price', 'Percentage_Change_1h', 'Percentage_Change_24h', 'Percentage_Change_7d', 'Volume_24h'])
if view_options== 'Market_Cap':
    plot_pie(df['market_cap'].head(10),view_options);
elif view_options== 'Price':
    plot_pie(df['price'].head(10),view_options);
elif view_options== 'Percentage_Change_1h':
    plot_pie(df['percent_change_1h'].head(10),view_options);
elif view_options== 'Percentage_Change_24h':
    plot_pie(df['percent_change_24h'].head(10),view_options);
elif view_options== 'Percentage_Change_7d':
    plot_pie(df['percent_change_7d'].head(10),view_options);
else:
    plot_pie(df['volume_24h'].head(10),view_options); 

