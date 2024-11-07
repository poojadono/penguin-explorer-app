# 1. Import Libraries and Setup

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image

# 2. Display Header and Load Data
# Set page config to widen the layout and add a title and icon
st.set_page_config(page_title="Penguin Explorer", page_icon=":penguin:", layout="wide")

# Display the app logo and title
logo = Image.open('penguin-logo.png')
st.image(logo, width=800)
st.title("Penguin Explorer")
st.write("""
Explore the Palmer Archipelago Penguin dataset interactively. Use the sidebar widgets to filter data and visualize penguin statistics.
""")

@st.cache_data
def load_data():
    data = pd.read_csv('penguins_size.csv')
    # Assuming 'body_mass_g' might have NaN, fill NaN with the median or drop NaN values
    data['body_mass_g'] = data['body_mass_g'].fillna(data['body_mass_g'].median())
    return data

data = load_data()

# 3. Sidebar for Data Filtering
# Sidebar for species selection
species = st.sidebar.selectbox('Select Species', data['species'].unique())
filtered_data = data[data['species'] == species]

# Sidebar for island selection
island = st.sidebar.multiselect('Select Island(s)', data['island'].unique())
filtered_data = filtered_data[filtered_data['island'].isin(island)] if island else filtered_data

# Slider for selecting body mass range
# Ensure all values are integers and there are no NaN values before setting up the slider
min_mass = int(data['body_mass_g'].min())
max_mass = int(data['body_mass_g'].max())
mass_range = st.sidebar.slider('Body Mass Range (g)', min_mass, max_mass, (min_mass, max_mass))
filtered_data = filtered_data[(filtered_data['body_mass_g'] >= mass_range[0]) & (filtered_data['body_mass_g'] <= mass_range[1])]


# 4. Data Visualization Section
# Display filtered data and count of records
st.write(f"Filtered Data for {species} on {', '.join(island) if island else 'All Islands'}:")
st.dataframe(filtered_data)
st.write("Total records:", len(filtered_data))

# Plotly scatter plot
st.write("Interactive Scatter Plot of Flipper Length vs. Culmen Length")
fig = px.scatter(filtered_data, x='flipper_length_mm', y='culmen_length_mm', color='species',
                 size='body_mass_g', hover_data=['island'])
st.plotly_chart(fig, use_container_width=True)

# Seaborn pair plot
st.write("Pair Plot of Measurements")
pair_plot = sns.pairplot(filtered_data, hue='species', palette='bright')
st.pyplot(pair_plot)

# 5. Conclusion and Instructions for Deployment
st.write('Your app is ready to be deployed!')
st.write("Ready to share your insights? Follow along to deploy this app on Streamlit Sharing and make your data analysis accessible to the world!")

