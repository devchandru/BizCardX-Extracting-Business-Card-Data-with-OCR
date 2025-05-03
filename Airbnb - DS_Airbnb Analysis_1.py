import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")
from PIL import Image


def load_data():
    df = pd.read_csv("F:/New folder (4)/New folder/Airbnb_Analysis.csv")
    return df

df = load_data()

# Streamlit part
st.set_page_config(layout="wide")
st.title("AIRBNB DATA ANALYSIS")
st.write("")

with st.sidebar:
    select = option_menu("Main Menu", ["Home", "Data Exploration", "About"])

unique_key_home = "home_select_country"
unique_key_data_exp_price = "data_exp_price"
unique_key_data_exp_availability = "data_exp_availability"
unique_key_data_exp_location = "data_exp_location"
unique_key_data_exp_geospatial = "data_exp_geospatial"
unique_key_data_exp_charts = "data_exp_charts"

if select == "Home":
    image1 = Image.open("F:/New folder (4)/New folder/download.jpg")
    st.image(image1)

    st.header("About Airbnb")
    st.write("""***Airbnb is an online marketplace that connects people who want to rent out
    their property with people who are looking for accommodations, typically for short stays.
    Airbnb offers hosts a relatively easy way to earn some income from their property.
    Guests often find that Airbnb rentals are cheaper and homier than hotels.***""")
    
    st.header("Background of Airbnb")
    st.write("""***Airbnb Inc (Airbnb) operates an online platform for hospitality services.
    The company provides a mobile application (app) that enables users to list, discover, and book
    unique accommodations across the world. The app allows hosts to list their properties for lease,
    and enables guests to rent or lease on a short-term basis, which includes vacation rentals, apartment rentals,
    homestays, castles, tree houses, and hotel rooms. Airbnb is headquartered in San Francisco, California, the US.***""")

    country = st.selectbox("Select the Country", df["country"].unique(), key=unique_key_home)
    df_country = df[df["country"] == country]
    room_type = st.selectbox("Select the Room Type", df_country["room_type"].unique())

elif select == "Data Exploration":
    tab_names = ["***PRICE ANALYSIS***", "***AVAILABILITY ANALYSIS***", "***LOCATION BASED***", "***GEOSPATIAL VISUALIZATION***", "***TOP CHARTS***"]
    tab1, tab2, tab3, tab4, tab5 = st.columns(len(tab_names))
    tabs = [tab1, tab2, tab3, tab4, tab5]


    for i, tab in enumerate(tabs):
        with tab:
            st.title(tab_names[i])

            if i == 0:  # Price Analysis
                country_price = st.selectbox("Select the Country", df["country"].unique(), key=unique_key_data_exp_price)
                df_country = df[df["country"] == country_price]
                room_type = st.selectbox("Select the Room Type", df_country["room_type"].unique())
                df_room_type = df_country[df_country["room_type"] == room_type]

                fig_bar = px.bar(df_room_type, x='property_type', y='price', title='PRICE FOR PROPERTY_TYPES',
                                 hover_data=["number_of_reviews", "review_scores"], color='price',
                                 color_continuous_scale=px.colors.sequential.Redor_r)
                st.plotly_chart(fig_bar)

            elif i == 1:  # Availability Analysis
                df_a = pd.read_csv("F:/New folder (4)/New folder/Airbnb_Analysis.csv")
                country_availability = st.selectbox("Select the Country", df["country"].unique(), key=unique_key_data_exp_availability)
                df_country_a = df_a[df_a["country"] == country_availability]
                property_type_a = st.selectbox("Select the Property Type", df_country_a["property_type"].unique())
                df_property_type_a = df_country_a[df_country_a["property_type"] == property_type_a]

                fig_sunburst_30 = px.sunburst(df_property_type_a, path=["room_type", "bed_type", "is_location_exact"],
                                               values="availability_30", title="Availability_30",
                                               color='availability_30')
                st.plotly_chart(fig_sunburst_30)

            elif i == 2:  # Location Analysis
                country_location = st.selectbox("Select the Country", df["country"].unique(), key=unique_key_data_exp_location)
                df_country_l = df[df["country"] == country_location]
                property_type_l = st.selectbox("Select the Property Type", df_country_l["property_type"].unique())
                df_property_type_l = df_country_l[df_country_l["property_type"] == property_type_l]

                st.dataframe(df_property_type_l)

            elif i == 3:  # Geospatial Visualization
                
                fig_map = px.scatter_mapbox(df, lat='latitude', lon='longitude', color='price', size='accommodates',
                                            color_continuous_scale="rainbow", hover_name='name',
                                            mapbox_style="carto-positron", zoom=1)
                fig_map.update_layout(width=1150, height=800, title='Geospatial Distribution of Listings')
                st.plotly_chart(fig_map)

            elif i == 4:  # Top Charts
                country_charts = st.selectbox("Select the Country", df["country"].unique(), key=unique_key_data_exp_charts)
                df_country_t = df[df["country"] == country_charts]
                property_type_t = st.selectbox("Select the Property Type", df_country_t["property_type"].unique())
                df_property_type_t = df_country_t[df_country_t["property_type"] == property_type_t]

                df_sorted_price = df_property_type_t.sort_values(by="price")
                df_price = pd.DataFrame(df_sorted_price.groupby("host_neighbourhood")["price"].agg(["sum", "mean"]))
                df_price.reset_index(inplace=True)
                df_price.columns = ["host_neighbourhood", "Total_price", "Avarage_price"]

                fig_price = px.bar(df_price, x="Total_price", y="host_neighbourhood", orientation='h',
                                   title="PRICE BASED ON HOST_NEIGHBOURHOOD", width=600, height=800)
                st.plotly_chart(fig_price)

elif select == "About":
    st.header("ABOUT THIS PROJECT")
    st.subheader(":orange[1. Data Collection:]")
    st.write("""***Gather data from Airbnb's public API or other available sources.
    Collect information on listings, hosts, reviews, pricing, and location data.***""")
    
    st.subheader(":orange[2. Data Cleaning and Preprocessing:]")
    st.write("""***Clean and preprocess the data to handle missing values, outliers, and ensure data quality.
    Convert data types, handle duplicates, and standardize formats.***""")
    
    st.subheader(":orange[3. Exploratory Data Analysis (EDA):]")
    st.write("""***Conduct exploratory data analysis to understand the distribution and patterns in the data.
    Explore relationships between variables and identify potential insights.***""")
    
    st.subheader(":orange[4. Visualization:]")
    st.write("""***Create visualizations to represent key metrics and trends.
    Use charts, graphs, and maps to convey information effectively.
    Consider using tools like Matplotlib, Seaborn, or Plotly for visualizations.***""")
    
    st.subheader(":orange[5. Geospatial Analysis:]")
    st.write("""***Utilize geospatial analysis to understand the geographical distribution of listings.
    Map out popular areas, analyze neighborhood characteristics, and visualize pricing variations.***""")