import streamlit as st
import requests as rq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import re
import nltk
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")    #earlier used "agg" backend that didnt work with streamlit
import string
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer


def clean_text(text):
    cleaned_text = re.sub('<.*?>', '', text)   
    cleaned_text = cleaned_text.translate(str.maketrans('', '', string.punctuation))   
    cleaned_text = re.sub(r'\d+', '', cleaned_text)   
    cleaned_text = ' '.join(cleaned_text.split())    
    cleaned_text = cleaned_text.lower()       
    return cleaned_text

def webScrapingReviews(url):
    reviews = []
    link = []
    
    r1 = rq.get(url)
    sleep(2)
    soup1 = BeautifulSoup(r1.text, 'html.parser')
    
    f_url = ''
    for i in soup1.findAll('a', attrs={'href': re.compile("/product-review")}):
        q = i.get('href')
        link.append(q)
        for j in link:
            if 'LSTMOBF3HZ2H9YZSYRYTFKW51' in j:
                aa = i
        f_url = 'https://www.flipkart.com' + str(j)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f_url)
    
    i = 1
    while i < 3:
        ss = driver.get(f_url + "&page=" + str(i))
        qq = driver.current_url
        r2 = rq.get(qq)
        soup = BeautifulSoup(r2.text, 'html.parser')
        reviews_container = soup.find('div', {'class': '_1YokD2 _3Mn1Gg col-9-12'})
        reviews_divs = reviews_container.find_all('div', {'class': 't-ZTKy'})
        for child in reviews_divs:
            third_div = child.div.div
            text = third_div.text.strip()
            cleaned_text = clean_text(text)
            reviews.append(cleaned_text)
        sleep(1)
        i += 1
    
    driver.quit()  # Close the browser
    file_path='reviews2.xlsx'
    data = pd.DataFrame({'review': reviews})
    data.to_excel(file_path, index=False)
    
    
    return data

def sentimentAnalysis(data):
    sid = SentimentIntensityAnalyzer()
    def sentiment_vader(text):
        over_all_polarity = sid.polarity_scores(text)
        if over_all_polarity['compound'] >= 0.05:
            return 'positive'
        elif over_all_polarity['compound'] < -0.05:
            return 'negative'
        else:
            return 'neutral'
    file_path='sentiment_result.xlsx'
    data['polarity'] = data['review'].apply(lambda review: sentiment_vader(review))
    data.to_excel('sentiment_result.xlsx', index=False)
    

def visualization():
    file = pd.read_excel('sentiment_result.xlsx')
    
    total_labels = len(file['polarity'])
    label_counts = pd.Series(file['polarity']).value_counts()
    percentages = (label_counts / total_labels) * 100
    print(percentages)

    fig, ax = plt.subplots()
    ax.pie(percentages, labels=percentages.index)
    ax.set_aspect('equal')  # Ensure pie is drawn as a circle
    st.pyplot(fig)
