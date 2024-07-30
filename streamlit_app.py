import streamlit as st
import pandas as pd
import altair as alt


# Define the Likert scale mapping
likert_scale_mapping = {
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5'
}

#################### Let's plot this!!! ###########################

# Read the CSV file into a Pandas DataFrame
df_summary = pd.read_csv('data/Summary_Scale_1_Columns_cleaned.csv', na_filter=False)

# Create a list of unique categories
unique_categories = df_summary['Category'].unique()

# Create a Streamlit sidebar with a selectbox to choose a category
selected_category = st.sidebar.selectbox("Select Category", unique_categories)

# Display the title in the main area of the app
st.title("Survey Results by Category")

# Filter the DataFrame based on the selected category
filtered_df = df_summary[df_summary['Category'] == selected_category].copy()

# Check if the filtered DataFrame is empty
if filtered_df.empty:
    st.warning(f"No data found for Category: {selected_category}")
else:
    # Melt the DataFrame to long format, excluding the 'Blank' column
    melted_df = filtered_df.melt(
        id_vars=['Recommendations'],
        value_vars=list(likert_scale_mapping.keys()),
        var_name='Response',
        value_name='Count'
    )

    # Replace the column names with their corresponding labels
    melted_df['Response'] = melted_df['Response'].replace(likert_scale_mapping)

    # Create a stacked bar chart using Altair
    chart = alt.Chart(melted_df).mark_bar().encode(
        x=alt.X('Recommendations:N', axis=alt.Axis(labelAngle=-45, labelOverlap=False)),
        y=alt.Y('Count:Q'),
        color='Response:N',
        tooltip=['Recommendations', 'Response', 'Count']
    ).properties(
        title=f'Category: {selected_category}'
    ).interactive().properties(width=750)

    # Display the chart in the Streamlit app
    st.altair_chart(chart)