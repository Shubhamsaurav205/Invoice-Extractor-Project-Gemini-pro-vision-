from dotenv import load_dotenv
load_dotenv() # Load all the environment  variables from .env
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
 
 #Function to load Gemini pro vision
model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type": uploaded_file.type, #Get the mime type of the upload_fiels
                "data": bytes_data 
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError
    

#Initialize Our streamlit app
st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.header("Multilanguage Invoice Extractor")
input=st.text_input("Input Prompt:",key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Upload Image.", use_column_width=True)
    
Submit=st.button("Tell me about invoice")

input_prompt="""
You are an expert in understanding invoice. We will upload image and images and you have to answers based on the invoice image 
"""    
#If submit button is click
if Submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is")
    st.write(response)
