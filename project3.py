import streamlit as st
import pandas as pd
import hvplot
import hvplot.pandas
import holoviews as hv
from datetime import datetime


#IMPORT DATA
data = pd.read_csv("throwdowns_transactions.csv", index_col='Player Name')
fair_value_df = pd.read_csv("pred_df.csv", index_col = 'Player Name')

#####################################################################
############################## SIDEBAR ##############################
#####################################################################

# SET SELECTION
# UPDATE "sets" WHEN NEW CSV IS UPLOADED, S2 IS JUST A TESTER

sets = ['Throwdowns','S2']
set_choice = st.sidebar.selectbox('Choose Set',sets)

# Player Selection
players = data.index.drop_duplicates(keep='first').sort_values(ascending=True)
player_choice = st.sidebar.selectbox('Choose Player', players)
circulation_count = data.loc[data.index==player_choice,'Circulation Count'].iloc[0]

# ADD PLAYER JPGs to DF, REFERENCE DF IN IF STATEMENT
if player_choice == 'Blake Griffin':
    st.sidebar.image('https://otmnft.com/static/transaction_data/img/moments/GettyImages-1232169410.jpeg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")


#####################################################################
############################## BODY #################################
#####################################################################
# TITLE
st.markdown("# :basketball: NBA TopShot Evaluator :basketball:")
# SET IMAGE
st.subheader(f"{set_choice}:  {player_choice}")
st.write(f"Moment Count: {circulation_count}")
st.write('\n')
st.image('https://otmnft.com/static/transaction_data/img/sets/co_2_throwdowns_rare.jpg', width=100)
st.write('\n')
st.write('\n')

# SELECTED PLAYER DF
player_data = pd.DataFrame(data.loc[data.index==player_choice])


#CONVERT TRANSACTION DATE TO DATETIME
player_data['Date'] = pd.to_datetime(player_data['Transaction Date'])
player_data.sort_values(by='Date', ascending=False)




# LAST TRANSACTION STATS

last_price = data.loc[data.index==player_choice,'Purchase Price'].iloc[-1]
second_price = data.loc[data.index==player_choice, 'Purchase Price'].iloc[-2]
pct_chg = round((last_price - second_price)/second_price*100,2)

last_buyer = data.loc[data.index==player_choice,'Buyer'].iloc[-1]
last_seller = data.loc[data.index==player_choice,'Seller'].iloc[-1]
last_tx_date = data.loc[data.index==player_choice,'Transaction Date'].iloc[-1]
last_serial = data.loc[data.index==player_choice,'Serial'].iloc[-1]

#FAIR VALUE CALCS
last_fair_value = fair_value_df.loc[fair_value_df.index==player_choice,'Fair Value'].iloc[-1].astype(int)
second_fair_value = fair_value_df.loc[fair_value_df.index==player_choice,'Fair Value'].iloc[-2].astype(int)
fv_pct_chg = round((last_fair_value - second_fair_value)/second_fair_value*100,2)

# WRITE TRANSACTION STATS
st.subheader("Last Transaction Details:")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Last Price", value=f"${last_price}", delta= f"{pct_chg}%")

    st.write(f"Last Serial: #{last_serial}")
    st.write(f"Transaction Date: {last_tx_date}")
    st.write(f"Last Buyer: {last_buyer}")
    st.write(f"Last Seller: {last_seller}")

with col2:
    st.metric(label="Estimated Fair Value", value=f"${last_fair_value}", delta= f"{fv_pct_chg}%")

with col3:
    link = data.loc[data.index==player_choice,'Top Shot Link'].iloc[0]
    
    st.write("Recommendation")
    if last_price < last_fair_value*.90:
        if st.button("BUY"):
            st.markdown(f"Buy Moment here: [{player_choice}](%s)" % link)
    elif last_price > last_fair_value*1.1:
        if st.button("SELL"):
            st.markdown(f"Sell Moment here: [{player_choice}](%s)" % link)
    else:
        st.write("HOLD")

    


# SELECTED PLAYER SERIAL / PRICE PLOT
charts = ["Serial/Price", "Player Price History", "Moment Correlation"]

# CHARTING
# SERIAL/PRICE
serial_price_plot = player_data.hvplot.scatter(x='Serial',
                                         y='Purchase Price',
                                         width=750,
                                         height=250,
                                         xticks=10,
                                         rot=0
)

# PLAYER PRICE HISTORY
player_price_history = player_data.hvplot.line(x='Date',
                                               y = 'Purchase Price',
                                               width=750,
                                               height=250,
                                               xticks=10,
                                               rot=45
)

# FEATURE CORRELATION

correlation_df = data.filter(['Purchase Price', 'Serial', 'Circulation Count'], axis=1).corr()['Purchase Price'][:]


corr_plot = correlation_df.hvplot.bar(rot=0,
                                      ylim = [-0.5,1]
)


chart_select = st.selectbox("Select Chart",charts)

if chart_select == "Serial/Price":
    st.bokeh_chart(hv.render(serial_price_plot, backend='bokeh'))

if chart_select == "Player Price History":
    st.bokeh_chart(hv.render(player_price_history, backend='bokeh'))

if chart_select =="Moment Correlation":
    st.bokeh_chart(hv.render(corr_plot, backend='bokeh'))




# RECENT TRANSACTIONS DF

st.subheader("Recent Transactions:")
with st.expander("See Recent Transactions"):
    st.dataframe(player_data)


