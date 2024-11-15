import streamlit as st
import os
from dotenv import load_dotenv
from libraries import ImageModel, ImageModelUploader
from PIL import Image

# Load environment variables from .env file
load_dotenv(override=True)

azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT")                           
api_key = os.getenv("AZURE_OPENAI_KEY")

prompt = """"Analyze the nutritional information and ingredients from the attached product label image. Provide a structured analysis with the following sections:

1. Overall Product Assessment: Give an overview of the product’s nutritional profile, including calories, fat, protein, fiber, sodium, and sugar content. Highlight any significant health benefits or concerns.

2. Suitability for Different Dietary Needs: Assess the product’s suitability for the following dietary needs and health conditions:

    - General Consumption: Is this product suitable for regular use?

    - Vegetarian and Vegan Diets: Comment on the suitability based on ingredients.

    - Heart Health: Mention any potential concerns related to fat, cholesterol, and sodium.

    - Weight Management: Evaluate whether this product would be beneficial or concerning for those trying to manage weight.

    - Diabetes Management: Provide insights on the product’s carbohydrate and sugar content and its impact on blood sugar levels.

3. Final Recommendation: Based on the nutritional analysis, provide a recommendation on the frequency of consumption (e.g., daily, occasional, or rarely). Include any portion control advice if relevant.
Please output each section in clear, structured text."""

st.title("Your Personal Nutritional Doctor!")
st.write("Upload an image of the product label to analyze.")

# Image upload from user
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if st.button("Analyze"):
    if uploaded_image is not None:
        try:
            # Display the uploaded image
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Initialize ImageModel and make a prediction
            inference = ImageModelUploader(azure_endpoint=azure_endpoint, api_key=api_key, deployment=deployment, prompt=prompt)

            # Pass the uploaded image file-like object to predict
            inf = inference.predict(image_file=uploaded_image)
            
            # Display the results
            st.subheader("Results:")
            st.write(inf)
        except Exception as e:
            st.error(f"Error analyzing image: {e}")
    else:
        st.warning("Please upload a valid image file.")

