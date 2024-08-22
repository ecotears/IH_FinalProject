import streamlit as st
import pandas as pd
from PIL import Image
import joblib
from textblob import TextBlob

# ------------------------------------------------- Necessary steps for data processing and collection ------------------------
appearance_image = Image.open('appearance.png')

dataset = pd.read_csv('/home/ecotears/Ironhack/Ironhack_all/Ironhack_Final_Project/Dataset/train.csv/train.csv')
breed_dataset = pd.read_csv('/home/ecotears/Ironhack/Ironhack_all/Ironhack_Final_Project/Dataset/BreedLabels.csv')
color_dataset = pd.read_csv('/home/ecotears/Ironhack/Ironhack_all/Ironhack_Final_Project/Dataset/ColorLabels.csv')
max_age_possible = dataset['Age'].max()

def collect_input_data ():
     
     # Since TextBlob doesn't have magnitude like GoogleCloudAPI (for simplicity we use TextBlob), we'll use subjectivity or create our own approximation.
    description_blob = TextBlob(description)
    sentiment_score = description_blob.sentiment.polarity  # Polarity: -1 (negative) to 1 (positive)
    sentiment_magnitude = description_blob.sentiment.subjectivity  # Subjectivity: 0 (objective) to 1 (subjective)

    data_from_user = {
          'AnimalType': Type,
          'Age': age,
          'Gender': gender,
          'HasName?': 'Does_not_have_name' if name == '' else 'Has_Name',
          'Breed1_label' : breed1,
          'Breed2_label' : breed2,
          'Color1_label' : color1,
          'Color2_label' : color2,
          'MaturitySize' : maturity_size,
          'FurLength' : fur_length,
          'Vaccinated_label': vaccinated,
          'Dewormed_label': dewormed,
          'Sterilized_label': sterilized,
          'Health_label': health,
          'PhotoAmt': photo_amt,
          'VideoAmt': video_amt,
          'Sentiment_score': sentiment_score,
          'Sentiment_magnitude': sentiment_magnitude,
          'Fee': fee,
          'Quantity': quantity
          } 
    input_data = pd.DataFrame([data_from_user])
    numerical_columns = input_data.select_dtypes(include=['float64, int64'])
    categorical_columns = input_data.select_dtypes(include=['object'])

    return input_data, numerical_columns, categorical_columns



model_path = '/home/ecotears/Ironhack/Ironhack_all/Ironhack_Final_Project/Streamlit app/final_randomforest_model.joblib'
model = joblib.load(model_path)

# ------------------------------------------------------ Actual app user interface --------------------------------------------

# Defining a function for getting images next to headers
def header_with_image(header, image_url):
    col1, col2 = st.columns([1,11])  

    with col1:
        st.image(Image.open(image_url), width=50)

    with col2:
        st.header(f'{header}')


# This is the banner
st.image(Image.open('/home/ecotears/Ironhack/Ironhack_all/Ironhack_Final_Project/Streamlit app/Banner.jpg'), use_column_width=True)

# Title of the app
st.title("Animal Adoption Speed Prediction")

# Description
st.write("""
    This app allows you to input details about a pet (or a group of animals) that will be given for adoption and predicts an approximate adoption speed.
    Please fill in the information below.
""")

# Input list that end user WILL have to fill out (compulsory)

Type = st.selectbox("Type of Animal", ["Select option", "Dog", "Cat"])
gender = st.selectbox("Gender(if more than 1, choose Mixed)", ["Select option", "Male", "Female", "Mixed"])
age = st.slider("Age of the Pet (months)", 0, max_age_possible, 0)  # Age in months
name = st.text_input("If it has a name, what is it?")

st.markdown("---")
header_with_image("Appearance related", '/home/ecotears/Ironhack/Ironhack_all/Ironhack_Final_Project/Streamlit app/appearance.png')

if Type=='Dog':
    breed_names_available = ['Select Option'] + breed_dataset[breed_dataset['Type'] ==1]['BreedName'].unique().tolist()
else:
    breed_names_available = ['Select Option'] + breed_dataset[breed_dataset['Type'] ==2]['BreedName'].unique().tolist()

breed1 = st.selectbox("Primary Breed", breed_names_available) 
breed2 = st.selectbox("Secondary Breed (if any)", breed_names_available)
color1 = st.selectbox("Primary Color", ['Select Option'] + color_dataset['ColorName'].unique().tolist())
color2 = st.selectbox("Secondary Color (if any)", ['Select Option'] + color_dataset['ColorName'].unique().tolist())
color3 = st.selectbox("Tertiary Color (if any)",['Select Option'] + color_dataset['ColorName'].unique().tolist())
maturity_size = st.selectbox("Maturity Size", ["Select Option", "Small", "Medium", "Large", "Extra Large"])
fur_length = st.selectbox("Fur Length", ["Select Option", "Short", "Medium", "Long"])


st.markdown("---")
header_with_image('Health related', '/home/ecotears/Ironhack/Ironhack_all/Ironhack_Final_Project/Streamlit app/health.png')
vaccinated = st.selectbox("Vaccinated", ["Select Option", "Yes", "No", "Not Sure"])
dewormed = st.selectbox("Dewormed", ["Select Option", "Yes", "No", "Not Sure"])
sterilized = st.selectbox("Sterilized", ["Select Option", "Yes", "No", "Not Sure"])
health = st.selectbox("Health Condition", ["Select Option", "Healthy", "Minor Injury", "Serious Injury"])

st.markdown("---")
header_with_image('Informational', '/home/ecotears/Ironhack/Ironhack_all/Ironhack_Final_Project/Streamlit app/informational.png')
photo_amt = st.slider("Number of Photos you plan to include", 0, 30, 1)
video_amt = st.slider("Number of Videos you plan to include", 0, 30, 1)
description = st.text_area("Description of the Pet")

st.markdown("---")
header_with_image('Miscellaneous','/home/ecotears/Ironhack/Ironhack_all/Ironhack_Final_Project/Streamlit app/miscellaneous.png')
quantity = st.number_input("Choose 1 if it is just one animal, if group choose appropriate number", min_value=1, max_value=100000, value=1)
fee = st.number_input("Adoption Fee", min_value=0, max_value=100000, value=0)


st.markdown("---")

# Submit button
if st.button("Predict Adoption Speed"):
    input_data, numerical_columns, categorical_columns = collect_input_data()
    prediction = model.predict(input_data)[0]

    if prediction == 0:
        prediction_output = 'The pet will probably be adopted within the first week!'
    elif prediction == 1:
        prediction_output = 'It will probably take between 8 to 30 days for the pet to get adopted'
    elif prediction == 2:
        prediction_output = 'It will probably take between 31 to 90 days for the pet to get adopted'
    elif prediction == 3:
        prediction_output = 'It might take more than 100 days or the pet might not get adopted :(. Please work on the description/video/photoes more to increase chances!'

    st.write("**Input values**:")
    st.write(f"**Type:** {Type}")
    st.write(f"**Age:** {age} months")
    st.write(f"**Primary Breed:** {breed1}")
    st.write(f"**Secondary Breed:** {breed2}")
    st.write(f"**Gender:** {gender}")
    st.write(f"**Primary Color:** {color1}")
    st.write(f"**Secondary Color:** {color2}")
    st.write(f"**Tertiary Color:** {color3}")
    st.write(f"**Maturity Size:** {maturity_size}")
    st.write(f"**Fur Length:** {fur_length}")
    st.write(f"**Vaccinated:** {vaccinated}")
    st.write(f"**Dewormed:** {dewormed}")
    st.write(f"**Sterilized:** {sterilized}")
    st.write(f"**Health Condition:** {health}")
    st.write(f"**Adoption Fee:** ${fee}")
    st.write(f"**Number of Photos:** {photo_amt}")
    st.write(f"**Description:** {description}")

    # Display the prediction
    st.write(f"Predicted Adoption Speed:")
    st.markdown(f'<p style="color:green; font-weight:bold;">{prediction_output}</p>', unsafe_allow_html=True)

st.image(Image.open('/home/ecotears/Ironhack/Ironhack_all/Ironhack_Final_Project/Streamlit app/Banner2.jpg'), use_column_width=True)

st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #4CAF50; /* Green background */
        color: white; /* White text */
        border: none; /* Remove borders */
        padding: 15px 32px; /* Some padding */
        text-align: center; /* Center text */
        text-decoration: none; /* Remove text underline */
        display: inline-block; /* Inline block for alignment */
        font-size: 16px; /* Set font size */
        margin: 4px 2px; /* Margins for spacing */
        cursor: pointer; /* Pointer cursor on hover */
        border-radius: 4px; /* Rounded corners */
        transition: background-color 0.3s; /* Smooth transition for background color */
    }
    .stButton > button:hover {
        background-color: #45a049; /* Darker green on hover */
    }
    .stButton > button:active {
        background-color: #388e3c; /* Even darker green on click */
        color: white; /* Ensure text color remains white */
    }
    </style>
    """,
    unsafe_allow_html=True
)