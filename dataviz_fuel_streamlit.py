from bokeh.plotting import figure
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import pydeck as pdk 

#My infos
st.write('Louis Le Breton 20190760, BIA2')
st.title('Fuel Prices in France (2022) - Data Analysis')

#Reading the file
df = pd.read_csv('fuel_france_2022.csv', delimiter= ';')

#Data treatment
df = df.dropna()
df[['lat','lon']]=df.geom.str.split(',',expand=True)
df['lat'] = df['lat'].astype(float, errors = 'raise')
df['lon'] = df['lon'].astype(float, errors = 'raise')


df["prix_maj"]= pd.to_datetime(df["prix_maj"])

#Info of the dataset ?

if st.button('Infos of the dataset'):
    st.dataframe(df)
else:
    st.write('Button not clicked')

# Creation of 3 sub datasets which will be easier to work with.
prices = df.groupby(["dep_code"],as_index= False).mean(["prix_valeur"])
prices.drop(["cp", "id", "prix_id", "epci_code", "reg_code"], axis=1)

df2 = df[['dep_code','prix_valeur','prix_nom']]

type_fuel = df.groupby(["prix_nom"],as_index= False).mean(["prix_valeur"])
type_fuel.drop(["cp", "id", "prix_id", "epci_code", "reg_code"], axis=1)

#Ploting each graph

st.header('Mean price by county')
st.write('Done w/ Altair')
chart = alt.Chart(prices).mark_circle().encode(
    x="dep_code", y="prix_valeur", size="prix_valeur", color='dep_code', tooltip=['dep_code',"prix_valeur"])
st.altair_chart(chart, use_container_width=True)

st.write("Another representation w/ Bokeh")
p = figure(
    title='Value by county',
    x_axis_label="County",
    y_axis_label="Value")
p.line(prices['dep_code'], prices['prix_valeur'], legend_label='Trend', line_width=2)
st.bokeh_chart(p, use_container_width=True)


st.header('Gas station in France in 2022')
st.write('Done w/ streamlit')
st.map(df)

st.header("Gas Station prices.")
st.write('Done w/ streamlit')
# plot the slider that selects gas station according to the price 
price_station = st.slider("Min. Price", float(df["prix_valeur"].min()), float(df["prix_valeur"].max()))
st.map(df.query("prix_valeur >= @price_station"))


fig = px.pie(
    labels = df.prix_nom,
    names = df.prix_nom,
)
st.header("Distribution of fuel types in France")
st.write('Done w/ streamlit')
st.plotly_chart(fig)


st.header("Mean price of the different type of fuel.")
st.write('Done w/ streamlit')
st.bar_chart(data=type_fuel, x='prix_nom', y='prix_valeur', width=0, height=0, use_container_width=True)


st.header("Prices of the different type of fuel.")
st.write('Done w/ Vega')
st.vega_lite_chart(df2, {
    'mark': {'type': 'circle', 'tooltip': True},
    'encoding': {
        'x': {'field': 'dep_code'},
        'y': {'field': 'prix_nom'},
        'size': {'field': 'prix_valeur', 'type': 'quantitative'},
        'color': {'field': 'prix_valeur', 'type': 'quantitative'},
    },
})




