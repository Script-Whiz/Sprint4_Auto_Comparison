import streamlit as st
import pandas as pd
import plotly.express as px


# Load the data from the CSV file
autos = pd.read_csv('autos_data.csv')

# Create a header
st.header("Comparison of Auto Sales from 1908-2019")

# Add a checkbox
show_only_automatic = st.checkbox("Show Only Automatic Transmissions")

# Create a filtered DataFrame based on the checkbox
if 'transmission' in autos.columns:
    if show_only_automatic:
        filtered_autos = autos[autos['transmission'] == 'automatic']
    else:
        filtered_autos = autos
    # Get counts of each transmission type from the filtered dataset
    transmission_counts = filtered_autos['transmission'].value_counts().reset_index()
    transmission_counts.columns = ['transmission', 'count']
    
    # Ensure transmission counts are not empty
    if not transmission_counts.empty:
        # Create a histogram using Plotly
        fig = px.bar(transmission_counts, x='transmission', y='count', title='Counts of Each Transmission Type')
        
        # Display histogram in Streamlit
        st.write("Here is a histogram of the counts of each transmission type:")
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected transmission types.")
else:
    st.error("The 'transmission' column is missing from the data.")
    
# Create a scatter plot using Plotly Express
def create_scatter_plot(auto_data):
    try:
        fig = px.scatter(
            auto_data,
            x='model',
            y='price',
            title='Scatter Plot of Car Models vs Price',
            labels={'model': 'Car Model', 'price': 'Price ($)'},
            hover_data=['transmission']
        )
        return fig
    except Exception as e:
        st.error(f"Error creating scatter plot: {e}")
        return None
    
# Initial unfiltered scatter plot
if not filtered_autos.empty:
    fig = create_scatter_plot(filtered_autos)
    if fig:
        # Display the scatter plot with Streamlit
        st.write("Car models compared to their prices:")
        st.plotly_chart(fig)
        
# Add a button to filter models starting with "Chevrolet"
if st.button('Show Chevrolet Models'):
    if not filtered_autos.empty:
        chevrolet_autos = filtered_autos[filtered_autos['model'].str.lower().str.startswith('chevrolet')]
        if not chevrolet_autos.empty:
            chevy_fig = create_scatter_plot(chevrolet_autos)
            if chevy_fig:
                st.write("Below are the cars starting with 'Chevrolet':")
                st.plotly_chart(chevy_fig)
            else:
                st.write("Error creating Chevrolet scatter plot.")
        else:
            st.write("No Chevrolet models found.")