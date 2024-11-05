import streamlit as st
import pandas as pd
import google.generativeai as genai

# Set up Google API key and configure the client
google_api_key = "AIzaSyD2_oxzOQQtcGDmW_Ul8E7mREi_LYYJO9I"  # Replace with your actual Google API key
genai.configure(api_key=google_api_key)

# Function to predict gender based on name
def generate_text(name): 
    prompt = f"Based on common naming conventions, predict the likely gender of the person with the name '{name}'. Please respond with just 'Male' or 'Female'."
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit user interface
st.title("Gender Prediction Based on Name")
st.write("Upload a CSV file with a column named 'Name' to predict the likely gender for each name.")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Check if 'Name' column exists in the uploaded CSV
    if 'Name' in df.columns:
        # Predict gender for each name in the 'Name' column
        df['Predicted Gender'] = df['Name'].apply(generate_text)
        
        # Show the DataFrame with predictions
        st.write("Predicted Genders:")
        st.write(df)
        
        # Download the result as a new CSV file
        output_csv = df.to_csv(index=False)
        st.download_button("Download Predictions as CSV", data=output_csv, file_name="gender_predictions.csv", mime="text/csv")
    else:
        st.error("The uploaded CSV file must contain a column named 'Name'.")
