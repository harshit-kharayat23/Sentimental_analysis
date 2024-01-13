import streamlit as st 
import base64
import SentimentAnalysisFlipkart

def add_bg(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: wide
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def main():
    st.set_page_config(page_title="FLIPKART",page_icon=":tada:",layout="wide")
    #st.title("Sentimental Analysis of Products")
    # Adding color to the title using Markdown syntax
    st.markdown("<h1 style='color: #000000; font-family: Italic, MONOSPACE;'>Sentimental Analysis of Products</h1>", unsafe_allow_html=True)
    add_bg("D:/Mini/image.png")
    
    url = st.text_input("Enter the URL:")
    
    
    if st.button("Analyze"):
        data = SentimentAnalysisFlipkart.webScrapingReviews(url)
        SentimentAnalysisFlipkart.sentimentAnalysis(data)
        st.markdown(
            '<div style="background-color: #FFD700; padding: 10px; border-radius: 10px;">'
            '<h3 style="color: black; text-align: center;">Here is the overall analysis:</h3>'
            '</div>',
            unsafe_allow_html=True
        )
        SentimentAnalysisFlipkart.visualization()

    

   
if __name__=='__main__':
    main()

# streamlit run "c:/Users/Saumya Bagri/Workspace/Machine Learning/Mini Project 4/app.py"

#samples:

# reviews2.xlsx file saved at: C:\Users\Saumya Bagri\Workspace\Machine Learning\reviews2.xlsx
# sentiment_result.xlsx file saved at C:\Users\Saumya Bagri\Workspace\Machine Learning\sentiment_result.xlsx