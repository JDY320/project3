import streamlit as st
import requests
import json

endpoint = st.sidebar.selectbox("Endpoints", ['Assets','Events','Rarity'])
st.header(f"NFT API Explorer {endpoint}")

st.sidebar.subheader("Filters")
collection_input = st.sidebar.text_input("Collection")
owner = st.sidebar.text_input("Owner")


if endpoint == 'Assets':
    collection_name = collection_input
    url = (f"https://testnets-api.opensea.io/api/v1/assets?order_direction=desc&offset=0&collection={collection_name}")

    response = requests.request("GET", url)

    st.write(response.json())