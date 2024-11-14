import streamlit as st
import os
from dotenv import load_dotenv
from libraries import ImageModel


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


st.title("Your Personal Nutritional Doctor!!!")
st.write("Enter an image URL to analyze.")

# Input URL from user
image_url = st.text_input("Image URL")

if st.button("Analyze"):
    if image_url:
        try:
            st.image(image_url, caption="Input Image", use_container_width = True)
            print("image input successful")
            inference = ImageModel(azure_endpoint=azure_endpoint, api_key=api_key, deployment=deployment, prompt=prompt)
            print("image model class initiated successfully")
            inf = inference.predict(image_path=image_url, context=None)
            print("got the prediction")
            print(inf)
            st.subheader("Results:")
            st.write(inf)
        except Exception as e:
            st.error(f"Error analyzing image: {e}")
    else:
        st.warning("Please enter a valid image URL.")


