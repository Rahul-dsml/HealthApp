import streamlit as st
import os
from libraries import ImageModel, ImageModelUploader
from PIL import Image

# Load environment variables from .toml file


azure_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]
deployment = st.secrets["AZURE_OPENAI_CHATGPT_DEPLOYMENT"]                           
api_key = st.secrets["AZURE_OPENAI_KEY"]

prompt = """"You are an expert in food and nutrition and you are on a mission to aware people about the so-called healthy snacks. Analyze the nutritional information and ingredients from the attached product label image(s). Provide a structured analysis with the following sections:

1. Overall Product Assessment: Give an overview of the product’s nutritional profile, including calories, fat, protein, fiber, sodium, and sugar content. 
   Highlight any significant health benefits or concerns.
2. Please flag any ingrediants which are harmful, like palm oil, malodextrin, any regulators which are not great to be consume
 
3. Suitability for Different Dietary Needs: Assess the product’s suitability for the following dietary needs and health conditions:
 
    - General Consumption: Is this product suitable for regular use?
 
    - Vegetarian and Vegan Diets: Comment on the suitability based on ingredients.
    - Gut health: Mention what could be the potential impact based on the ingredients 
    - Kids Health: Mention what could be the potential impact based on the ingredients on kids health and any specific ingredients which 
      do not suit well with their health and growth
 
    - Heart Health: Mention any potential concerns related to fat, cholesterol, and sodium.
 
    - Weight Management: Evaluate whether this product would be beneficial or concerning for those trying to manage weight.
 
    - Diabetes Management: Provide insights on the product’s carbohydrate and sugar content and its impact on blood sugar levels.
    - Special mention on people who might have food allergies like lactose intolerance, peanuts, gluten intolerance, etc.
 
4. Final Recommendation: Based on the nutritional analysis, provide a recommendation on the frequency of consumption (e.g., daily, occasional, or avoid). 
   Include any portion control advice if relevant.
 
5. Final Score: Based on your analysis and pretrained knowledge of Indian people food habits and patterns, give a final score on the scale of 10. Be conservative on the scoring 
as people will take 5/10 a good score to occasionaly enjoy products which are not great 
Add emojis for personalized touch.
Please output each section in clear, structured text and add emojis for each section and sub-section wherever it is required for friendly and personalized touch"""

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

