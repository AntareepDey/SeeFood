import streamlit as st  
import torch 
from PIL import Image, ImageOps
import numpy as np

# hide deprication warnings which directly don't affect the working of the application
import warnings
warnings.filterwarnings("ignore")

# set some pre-defined configurations for the page, such as the page title, logo-icon, page loading state (whether the page is loaded automatically or you need to perform some action for loading)
st.set_page_config(
    page_title="SeeFood",
    page_icon = ":pizza:",
    initial_sidebar_state = 'auto'
)


def load_model():
    model=torch.load('detection.pt', map_location=torch.device('cpu'))
    model.eval()
    return model
with st.spinner('Model is being loaded..'):
    model=load_model()


# hide the part of the code, as this is just for adding some custom CSS styling but not a part of the main idea 
hide_streamlit_style = """
	<style>
  #MainMenu {visibility: hidden;}
	footer {visibility: hidden;}
  </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) # hide the CSS code from the screen as they are embedded in markdown text. Also, allow streamlit to unsafely process as HTML


with st.sidebar:
        st.image('dog.jpg')
        st.title("SeeFood")
        st.subheader("Shazam for Food")

st.write("""
         # Upload the image of your food!
         """
         )

file = st.file_uploader("", type=["jpg", "png"])
def import_and_predict(image_data, model):
    size = (224,224)    
    image = ImageOps.fit(image_data, size, Image.LANCZOS)
    img = np.asarray(image)
    img = img / 255
    img = torch.from_numpy(img).float().unsqueeze(0)
    img = img.permute(0, 3, 1, 2) 
    prediction = torch.sigmoid(model(img))
    return prediction.detach().numpy()

        
if file is None:
    st.text("Please upload theimage of the food you would like to know about.")
else:
    image = Image.open(file)
    st.image(image, use_column_width=True)
    predictions = import_and_predict(image, model)
    if predictions[0]<0.5:
        st.balloons()
        st.sidebar.success("It's a hotdog !!")
    else:
        st.sidebar.error("It is not a hotdog")

