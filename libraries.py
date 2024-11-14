import base64

from openai import AzureOpenAI
import json
from typing import Any


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

class ImageModel:
    def __init__(self, azure_endpoint, api_key, deployment, prompt):
        self.azure_endpoint = azure_endpoint
        self.api_key = api_key
        self.deployment = deployment
        self.prompt = prompt
        self.client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version="2024-02-01")
        

    def encode_image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string

    def call_model(self, image_path):
        # base64_image = self.encode_image_to_base64(image_path)
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=[{"role": "user", 
                       "content": [{"type": "text", 
                                    "text": f"""{self.prompt}"""},
                                   {"type": "image_url",
                                    "image_url": {"url": image_path, "detail": "high"}}]
                                        # {"url": f"data:image/jpeg;base64,{base64_image}", "detail": "high"}}]
                            }],
        )
        return completion.choices[0].message.content
    
    def load_context(self, context):
        self.client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version="2024-02-01"
        )

    def predict(self, image_path, context):
        # image_path = model_input["image_path"]
        ans = self.call_model(image_path)
        return ans


class ImageModelUploader:

    def __init__(self, azure_endpoint, api_key, deployment, prompt):
        self.azure_endpoint = azure_endpoint
        self.api_key = api_key
        self.deployment = deployment
        self.prompt = prompt
        self.client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version="2024-02-01"
        )

    def encode_image_to_base64(self, image_file):
        # Convert image file to base64 string
        image_file.seek(0)
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        print(f"Encoded image string (truncated): {encoded_string[:50]}...")  # Debug print
        return encoded_string

    def call_model(self, image_file):
        # Encode the image in base64 format
        base64_image = self.encode_image_to_base64(image_file)

        # Construct the data URI with correct MIME type
        data_uri = f"data:image/jpeg;base64,{base64_image}"
        print(f"Data URI (truncated): {data_uri[:100]}...")  # Debug print

        try:
            # Prepare the message for the multimodal GPT model
            completion = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": data_uri,
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ]
            )

            # Return the model's response content
            return completion.choices[0].message.content  #completion.choices[0].message["content"]

        except Exception as e:
            print(f"Error in call_model: {e}")
            raise e

    def predict(self, image_file, context=None):
        # Call the model with the provided image file and context
        ans = self.call_model(image_file)
        return ans
