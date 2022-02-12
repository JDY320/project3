import streamlit as st
import pandas as pd
import hvplot
import hvplot.pandas
import holoviews as hv
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, mean_squared_error

#IMPORT DATA
data = pd.read_csv("throwdowns_transactions.csv", index_col='Player Name')

#####################################################################
############################## SIDEBAR ##############################
#####################################################################

# SET SELECTION
# UPDATE "sets" WHEN NEW CSV IS UPLOADED, S2 IS JUST A TESTER
sets = ['Throwdowns','S2']
st.sidebar.selectbox('Choose Set',sets)

# Player Selection
players = data.index.drop_duplicates(keep='first')
player_choice = st.sidebar.selectbox('Choose Player', players)



#####################################################################
############################## BODY #################################
#####################################################################

# SET IMAGE
st.image('https://otmnft.com/static/transaction_data/img/sets/co_2_throwdowns_rare.jpg', width=100)

# SELECTED PLAYER DF
player_data = pd.DataFrame(data.loc[data.index==player_choice])

# SELECTED PLAYER SERIAL / PRICE PLOT
player_plot = player_data.hvplot.scatter(x='Serial',
                                         y='Purchase Price',
                                         width=500,
                                         height=200,
                                         xticks=25,
                                         rot=90
)
st.bokeh_chart(hv.render(player_plot, backend='bokeh'))

# LAST TRANSACTION STATS
last_price = data.loc[data.index==player_choice,'Purchase Price'].iloc[0]
last_buyer = data.loc[data.index==player_choice,'Buyer'].iloc[0]
last_seller = data.loc[data.index==player_choice,'Seller'].iloc[0]
last_tx_date = data.loc[data.index==player_choice,'Transaction Date'].iloc[0]

# WRITE TRANSACTION STATS
st.write(f"Last Price: ${last_price}")
st.write(f"Transaction Date: {last_tx_date}")
st.write(f"Last Buyer: {last_buyer}")
st.write(f"Last Seller: {last_seller}")

st.write("Recent Transactions:")
st.write(player_data)


# Add video for each player
st.video('https://assets.nbatopshot.com/editions/2_throwdowns_rare/f3140cd1-8f9e-4483-853d-9bce3d63180d/play_f3140cd1-8f9e-4483-853d-9bce3d63180d_2_throwdowns_rare_capture_Animated_1080_1920_Black.mp4')


#####################################################################
############################## RF MODEL##############################
#####################################################################

st.write("Moment Fair Value:")