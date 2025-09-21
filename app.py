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
# ? Can we make any predictions?
# ? Can we make any scenario testing?
# ? Can we make any sensitivity test? Bayesian estimation?
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from copy import deepcopy
import json
from streamlit_option_menu import option_menu

# --- Set page config ---
st.set_page_config(
    # page_title="My App",
    # page_icon="🌿",
    layout="wide",  # <-- sets wide mode
    initial_sidebar_state="expanded"
)


sidebar_items = ["Overview", "Data Vis", "Model"]

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        None,                                       # Title at the top of sidebar
        sidebar_items,                              # Menu items
        icons=["cast", "bar-chart", "activity"],   # Matching icons
        # menu_icon="cast",                         # Icon for the menu title
        default_index=1,                            # Which tab opens first
        # orientation='horizontal'
        styles={
            "icon":{"color": "blue", "font-size": "25px"},
            "nav-link": {"font-size": "18px", "font-weight": "bold"},
            "nav-link-selected": {"background-color": "steelblue"}
        })

##### Expansion on the sidebar ----

# Add something below the radio
# st.sidebar.markdown("---")  # horizontal line
# st.sidebar.write("💡 Tip: You can add instructions, links, or info here.")
# st.sidebar.button("Click Me!")

# with st.sidebar.expander("More Info"):
#     st.write("This content is hidden until you click.")

##### OPTIONAL
# page = st.checkbox("Hit me")

# classical
# st.sidebar.title("Navigation")
# page = st.radio("Go to", ["Home", "Analysis", "Settings"])

# selection tab on top
# page = st.selectbox("Go to", ["Home", "Analysis", "Settings"])

# selection tab (duplicated with pages -> drop)
# tab1, tab2, tab3 = st.tabs(["Home", "Analysis", "Settings"])

# without sidebar
# page = st.segmented_control("Navigation", ["Home", "Analysis", "Settings"])



# ---------------------- HOME PAGE ----------------------
if selected == sidebar_items[0]:
    st.header("Clean Energy App 🫧🇨🇭")
    # st.subheader("Overview")
    st.write(
        "This is a interactive web app (API) to help users explore, analyze, and visualize clean energy scenarios in Switzerland. It provides interactive tools and data-driven insights to inform decisions related to the production of energy at district levels, energy cost for local households, and sustainable practices."
    )
    st.subheader("Data Visualization")
    st.write(
        "A brief geographical summary on clean energy generation in Switzerland among the 26 cantons including the below information:"
    )
    st.markdown(
        """
        - Electrical capacity
        - Tariff
        - Production
        - Facility count
        - Production efficiency
        """
    )
    st.subheader("A simple model for the energy flexibility")
    st.write(
        "To achieve climate neutrality by 2050, the Energy Transition in Switzerland🇨🇭 faces multiple challenges and opportunities. Here, a simple conceptual model shows the basic mechanism of local energy markets in Switzerland, and also shares what kinds of flexibility products the local houeholds have to maximum their profit. The model aims at find an optimal flexibility product based on market information and forecasts (**not applied yet**) to facilitate households' decision-making process."
    )


elif selected == sidebar_items[1]:
    st.header("Production of clean energy in Switzerland")
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
                "Mean electrical capacity was highest in the canton of Uri."  # data description
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
            st.write(
                "The total energy production is dominated by the three cantons with the highest electrical capacity. "
                ) 
        else:
            fig3 = go.Figure(go.Choroplethmapbox(geojson=swiss_geojson, locations=swiss_energy.canton_name, 
                    z=swiss_energy['mean_production'], featureidkey="properties.kan_name", colorscale=colorbar, 
                    zmin=swiss_energy['mean_production'].min(), zmax=swiss_energy['mean_production'].max(),
                    marker_opacity=0.7, marker_line_width=0))
            fig3.update_layout(mapbox_style="carto-positron", mapbox_zoom=6.5, 
                    mapbox_center = {"lat": lat, "lon": lon})
            fig3.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
            fig3.update_layout(title={"text": "Mean production (MWh)", "x": 0.15, "y":0.95, "xanchor": "center","yanchor": "top"})
            st.write(
            "The canton of Uri has the highest mean production. Their very low number of facility (n=64) is noteworthy for such a high level of mean production. Most Swiss cantons have mean production of less than 200 MWh."
            )
        # col1, col2 = st.columns(2)
        # if col1.button("Total", key="tab3_total"):
        #     st.write("Total")
        # if col2.button("Mean", key="tab3_mean")
        st.header(tab_names[2])
        st.plotly_chart(fig3)

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
        st.write(
            "The canton of Bern has the highest number of renewable facilities in Switzerland as of 2020. The other two large cantons, Valais and Graubünden, despite of their high electrical capacity, have much lower number of facilities. "  # data description
        )
        st.header(tab_names[3])
        st.plotly_chart(fig4)



    with tab5:          # production efficiency
        st.write("Production efficiency is obtained by total energy production divided by total electrical capacity.")
        # plot
        fig5 = go.Figure(go.Choroplethmapbox(geojson=swiss_geojson, locations=swiss_energy.canton_name, 
                    z=swiss_energy['Prod_eff'], featureidkey="properties.kan_name", colorscale=colorbar, 
                    zmin=swiss_energy['Prod_eff'].min(), zmax=swiss_energy['Prod_eff'].max(),
                    marker_opacity=0.7, marker_line_width=0))
        fig5.update_layout(mapbox_style="carto-positron", mapbox_zoom=6.5, 
                        mapbox_center = {"lat": lat, "lon": lon})
        fig5.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
        fig5.update_layout(title={"text": "Production efficiency (MW/MWh)", "x": 0.15, "y":0.95, "xanchor": "center","yanchor": "top"}) 
        st.write(
            "The canton of Glarus resulted in the greatest level of efficiency in energy production among other Swiss cantons."  # data description
        )
        st.header(tab_names[4])
        st.plotly_chart(fig5)

elif selected == sidebar_items[2]:
    # model
    @st.cache_data
    def generate_pv_profile(H, sunrise=6, sunset=18, pv_peak=3):
        hours = np.arange(H)                                                    # 60 min
        pv = np.maximum(0, np.sin((hours - sunrise) / (sunset - sunrise) * np.pi))    # roughly sunrise-sunset
        pv *= pv_peak                                                               # scale to average 3 kW peak per household
        return pv   

    @st.cache_data
    def generate_consumption_profile(H, base_use=0.2, am_lv=0.5, noon_lv=0.3, pm_lv=0.7):
        hours = np.arange(H)
        base = base_use + (am_lv * np.exp(-((hours - 7) / 2)**2)) + (noon_lv * np.exp(-((hours - 13) / 2)**2)) + (pm_lv * np.exp(-((hours - 19) / 2.5)**2))       # typical daily demand profile
        base += 0.1 * np.random.randn(H)                                                                            # add some random variability
        return np.maximum(0.1, base)                                                                                # ensure non-negative

    @st.cache_data
    def generate_consumption_profile(H, base_use=0.1, am_lv=0.5, noon_lv=0.3, pm_lv=0.7):
        hours = np.arange(H)
        base = base_use + (am_lv * np.exp(-((hours - 7) / 2)**2)) + (noon_lv * np.exp(-((hours - 13) / 2)**2)) + (pm_lv * np.exp(-((hours - 19) / 2.5)**2))       # typical daily demand profile
            # morning: 0.5 (intermediate), midday: 0.3 (low), evening: 0.7 (high)
        base += 0.1 * np.random.randn(H)                                                                            # add some random variability
        return np.maximum(0.1, base)                                                                                # ensure non-negative

    net_loss = np.minimum(0, generate_pv_profile(24)-generate_consumption_profile(24))*-1
    net_gain = np.maximum(0, generate_pv_profile(24)-generate_consumption_profile(24))

    # tabs -----
    st.title("An energy flexibility model")
    tab_names_model = ["Background", "Flexibility products", "Model", "Scenarios(*WIP*)"]
    tab1, tab2, tab3, tab4 = st.tabs(tab_names_model)
    
    with tab1:              # Background
        # todo: add some literatures? Swiss report?
        # st.subheader("Background")
        st.write(
            "Unlike larger European countries, Switzerland’s grid is heavily interconnected with neighbours but has limited domestic storage capacity. "
            "The rise of Photovoltaic (PV) adaptation of household in Switzerland allow them to become not only energy consumers but also producers (hence known as prosumers)."
        )
        st.write(
            "By offering flexibility, households and businesses can adjust their electricity consumption or generation in response to the market signals. Managing these flexibility products not only stabilize the power grid but also reduce energy costs. "
            "By connecting households, markets, and technology, Switzerland can unlock significant grid stability and decarbonisation benefits while empowering consumers to become active energy participants."
        )
    with tab2:              # Flexibility products
        st.subheader("Flexibility products/strategies")
        st.write(
            "Some of the flexibility strategies includes:"
        )
        st.write("""
        - Feeding electricity back into the local flexibility market (at dynamic market rates)
        - Feeding electricity back into the grid (at standard grid rates)
        - Participating in demand-response programme in response to price or control signals
        - Storing surplus PV generation in household batteries or electric vehicle batteries
        - Adjusting consumption patterns (e.g., shifting morning peak to afternoon peak)
        """)
        st.image("Model.png")
    with tab3:
        st.subheader("Introduction")
        st.write(
            "This is a conceptual model for displaying and understanding the basic mechanism of the energy input and output of a single household. "
            "The model shows hourly values (a 24-hour timestep) based on theoretical parameters and profiles. "
        )
        st.write(
            "By assuming buying electricity from grid at 0.26 CHF/kWh and feeding in surplus energy to the grid at 0.04 CHF/kWh, this model focuses on showing factors that affect PV generation and energy cost."
        )

        st.subheader("Baseline")
        st.write(
            """
            - Regular sunrise at 6am and sunset at 6pm.
            - Maximum PV generation at 3 kWh.
            - Randomly generated consumption pattern.
            """
        )
        st.write()
        fig, axs = plt.subplots(2, 1, sharex=True)
        axs[0].plot(np.arange(24), generate_pv_profile(24), label='PV generation', color='green')
        axs[0].plot(np.arange(24), generate_consumption_profile(24), label='Consumption', color='orange')
        axs[0].plot(np.arange(24), generate_pv_profile(24)-generate_consumption_profile(24), label='Net', color='steelblue')
        axs[0].set_xlim(0, 23)
        axs[0].set_ylabel('Energy (kWh)')
        axs[0].legend()
        axs[1].set_ylabel('Payment/Profit (CHF)')
        axs[1].plot(np.arange(24), net_gain*0.04-net_loss*0.26, color='k', lw=0.8)
        axs[1].set_xlabel('Hours')
        axs[1].fill_between(np.arange(24), y1=0, y2=np.maximum(0, net_gain*0.04-net_loss*0.26), color='blue', alpha=0.7, lw=0, label='Profit')
        axs[1].fill_between(np.arange(24), y1=0, y2=np.minimum(0, net_gain*0.04-net_loss*0.26), color='r', alpha=0.7, lw=0, label='Payment')
        axs[1].legend()
        axs[1].set_xticks(np.arange(24))
        st.pyplot(fig)

        

