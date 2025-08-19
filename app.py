# An app for clean energy data in Europe (starts with Switzerland)
# Layout of UI
#   Graphs showing data
#       changing variables
#       show data bar
#       data filters: which year to show? what data to show?
#   Visualization
#       geographical map
#       any statistical inferences/metrics? (comparing between countries? between regions?)
#           boxplots
# 
#       
# ? Can we make any predictions?
# ? Can we make any scenario testing?
# ? Can we make any sensitivity test? Bayesian estimation?

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from copy import deepcopy
import json


st.header("Production of renewable energy in Switzerland")
st.write(
    "Clean energy is a primary source of electricity in Switzerland, which generates the majority of its power from renewable methods. The country aims to reduce carbon emissions and achieve climate neutrality by 2050."
)

st.write(
    "Here displays how different factors related to the development of renewable energy vary in the 26 Swiss cantons. The data is adapted from Open Power System Data platform for the year of 2020. (https://doi.org/10.25832/renewable_power_plants/2020-08-25)"
)

st.link_button("Data", "https://data.open-power-system-data.org/renewable_power_plants/")


# data -----
data_path = "Data/swiss_energy.csv"  # for curation details, please see: 
geojson_path = "Data/georef-switzerland-kanton.geojson"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

# load dataframe and curate data -----
swiss_energy = load_data(data_path)

@st.cache_data
def load_geojson(path):
    with open(path) as f:
        geojson = json.load(f)
    return geojson

swiss_geojson = load_geojson(geojson_path)

# tabs -----
tab_names = ["Electrical capacity", "Tariff", "Production", "Facility count", "Production efficiency"]
tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_names)


# plots -----
colorbar = "jet"
lat, lon = 47.13495-0.25, 8.02+0.2      # obtained from the median lat and lon of energy data for switzerland 
items = ["electrical_capacity", "tariff", "production", "count", "Prod_eff"]
titles = ["Total electrical capacity (MW)", "Tariff (CHF)", "Production (MWh)", "Facility count (nos)", 
        "Production efficiency (MW/MWh)"]



with tab1:
    # col1, col2 = st.columns(2)
    # col1.button("Total", key="tab1_total")
    # col2.button("Mean", key="tab1_mean")
    st.write("Electrical capacity refers to the installed electrical capacity in megawatts.")
    show_values = st.radio("Show values", ["Total", "Mean"], key="tab1_radio")
    if show_values == "Total":
        fig1 = go.Figure(go.Choroplethmapbox(geojson=swiss_geojson, locations=swiss_energy.canton_name, 
                z=swiss_energy['electrical_capacity'], featureidkey="properties.kan_name", colorscale=colorbar, 
                zmin=swiss_energy['electrical_capacity'].min(), zmax=swiss_energy['electrical_capacity'].max(),
                marker_opacity=0.7, marker_line_width=0))
        fig1.update_layout(mapbox_style="carto-positron", mapbox_zoom=6.5, 
                  mapbox_center = {"lat": lat, "lon": lon})
        fig1.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
        fig1.update_layout(title={"text": "Total electrical capacity (MW)", "x": 0.15, "y":0.95, "xanchor": "center","yanchor": "top"}) 
        st.write(
            "Total electrical capacity was led by three largest canton, Bern, Valais, and Graubünden, who share large area of Switzerland. Smaller cantons like Basel-Stadt and Obwalden result in lower electrical capacity."  # data description
        )
    else:
        fig1 = go.Figure(go.Choroplethmapbox(geojson=swiss_geojson, locations=swiss_energy.canton_name, 
                z=swiss_energy['mean_electrical_capacity'], featureidkey="properties.kan_name", colorscale=colorbar, 
                zmin=swiss_energy['mean_electrical_capacity'].min(), zmax=swiss_energy['mean_electrical_capacity'].max(),
                marker_opacity=0.7, marker_line_width=0))
        fig1.update_layout(mapbox_style="carto-positron", mapbox_zoom=6.5, 
                  mapbox_center = {"lat": lat, "lon": lon})
        fig1.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
        fig1.update_layout(title={"text": "Mean electrical capacity (MW)", "x": 0.15, "y":0.95, "xanchor": "center","yanchor": "top"})
        st.write(
            ""  # data description
        )
    st.header(tab_names[0])
    st.plotly_chart(fig1)   


with tab2:
    st.write("Tariff is shown in CHF for the year of 2016.")
    # plot
    fig2 = go.Figure(go.Choroplethmapbox(geojson=swiss_geojson, locations=swiss_energy.canton_name, 
                z=swiss_energy['tariff'], featureidkey="properties.kan_name", colorscale=colorbar, 
                zmin=swiss_energy['tariff'].min(), zmax=swiss_energy['tariff'].max(),
                marker_opacity=0.7, marker_line_width=0))
    fig2.update_layout(mapbox_style="carto-positron", mapbox_zoom=6.5, 
                    mapbox_center = {"lat": lat, "lon": lon})
    fig2.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    fig2.update_layout(title={"text": "Tariff (CHF)", "x": 0.15, "y":0.95, "xanchor": "center","yanchor": "top"}) 
    st.header(tab_names[1])
    st.plotly_chart(fig2)
    st.write(
        ""  # data description
    )

with tab3:
    st.write("Production is based on annual total production in MWh.")
    show_values = st.radio("Show values", ["Total", "Mean"], key="tab3_radio")
    if show_values == "Total":
        fig3 = go.Figure(go.Choroplethmapbox(geojson=swiss_geojson, locations=swiss_energy.canton_name, 
                z=swiss_energy['production'], featureidkey="properties.kan_name", colorscale=colorbar, 
                zmin=swiss_energy['production'].min(), zmax=swiss_energy['production'].max(),
                marker_opacity=0.7, marker_line_width=0))
        fig3.update_layout(mapbox_style="carto-positron", mapbox_zoom=6.5, 
                  mapbox_center = {"lat": lat, "lon": lon})
        fig3.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
        fig3.update_layout(title={"text": "Total production (MWh)", "x": 0.15, "y":0.95, "xanchor": "center","yanchor": "top"}) 
    else:
        fig3 = go.Figure(go.Choroplethmapbox(geojson=swiss_geojson, locations=swiss_energy.canton_name, 
                z=swiss_energy['mean_production'], featureidkey="properties.kan_name", colorscale=colorbar, 
                zmin=swiss_energy['mean_production'].min(), zmax=swiss_energy['mean_production'].max(),
                marker_opacity=0.7, marker_line_width=0))
        fig3.update_layout(mapbox_style="carto-positron", mapbox_zoom=6.5, 
                  mapbox_center = {"lat": lat, "lon": lon})
        fig3.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
        fig3.update_layout(title={"text": "Mean production (MWh)", "x": 0.15, "y":0.95, "xanchor": "center","yanchor": "top"})
    # col1, col2 = st.columns(2)
    # if col1.button("Total", key="tab3_total"):
    #     st.write("Total")
    # if col2.button("Mean", key="tab3_mean")
    st.header(tab_names[2])
    st.plotly_chart(fig3)
    st.write(
        ""  # data description
    )

with tab4:
    st.write("The number of renewable facilities in each canton .")
    # plot
    fig4 = go.Figure(go.Choroplethmapbox(geojson=swiss_geojson, locations=swiss_energy.canton_name, 
                z=swiss_energy['count'], featureidkey="properties.kan_name", colorscale=colorbar, 
                zmin=swiss_energy['count'].min(), zmax=swiss_energy['count'].max(),
                marker_opacity=0.7, marker_line_width=0))
    fig4.update_layout(mapbox_style="carto-positron", mapbox_zoom=6.5, 
                    mapbox_center = {"lat": lat, "lon": lon})
    fig4.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    fig4.update_layout(title={"text": "Facility count (nos)", "x": 0.15, "y":0.95, "xanchor": "center","yanchor": "top"}) 
    st.header(tab_names[3])
    st.plotly_chart(fig4)
    st.write(
        ""  # data description
    )


with tab5:          # production efficiency
    st.write("The number of renewable facilities in each canton.")
    # plot
    fig5 = go.Figure(go.Choroplethmapbox(geojson=swiss_geojson, locations=swiss_energy.canton_name, 
                z=swiss_energy['Prod_eff'], featureidkey="properties.kan_name", colorscale=colorbar, 
                zmin=swiss_energy['Prod_eff'].min(), zmax=swiss_energy['Prod_eff'].max(),
                marker_opacity=0.7, marker_line_width=0))
    fig5.update_layout(mapbox_style="carto-positron", mapbox_zoom=6.5, 
                    mapbox_center = {"lat": lat, "lon": lon})
    fig5.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    fig5.update_layout(title={"text": "Production efficiency (MW/MWh)", "x": 0.15, "y":0.95, "xanchor": "center","yanchor": "top"}) 
    st.header(tab_names[4])
    st.plotly_chart(fig5)
    st.write(
        ""  # data description
    )