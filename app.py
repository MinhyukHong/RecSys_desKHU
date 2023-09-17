import streamlit as st
from streamlit_pills import pills
from annotated_text import annotated_text
from sklearn.metrics.pairwise import cosine_similarity
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain import LLMChain
from langchain.embeddings import OpenAIEmbeddings
import tiktoken
import os
import requests
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import openai

st.set_page_config(page_title='desKHU', page_icon='📚')

st.markdown("<h1 style='text-align: center; color: grey;'>desKHU</h1>", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state["history"] = ""

# Sidebar
with st.sidebar:
    with st.form('settings-form'):
        st.subheader('Settings')
        openai_api_key  = st.text_input("Please enter your OpenAI key.", type="password")
        gpt = pills('Please choose GPT model', ['gpt-3.5-turbo', 'gpt-4'])
        k = st.slider('Please select K', 5, 15, 10, 1)
        submit = st.form_submit_button('Apply')

    with st.container():
        st.subheader("History")
        history = st.empty().markdown("- Empty")
    
            # 입력 받은 API 키를 이용
    if submit:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        st.success("API key set successfully.")

# Prompt
with st.form('prompt-form'):
    interest = st.text_area("interest", placeholder="Please enter your interest", key="interest")
    submit_interest = st.form_submit_button("Submit")

def generate_query(interest, gpt):
    chat = ChatOpenAI(model=gpt, temperature=0.7, max_tokens=256)

    system_template = """
    You are an AI trained to generate korean keywords for book titles based on user prompts.
    Your goal is to return a list of unique keywords that are most relevant to the user's interests, specifically focusing on higher education level material. 
    Make sure each keyword is relevant to the topic of interest by combining the topic keyword with other relevant keywords. 
    For example, if the user inputs 'Want to enhance concentration', return a comma-separated string of keywords like 'Enhancement of Concentration, Concentration, Imemersion, Meditation, Stress Management,Productivity, Mindfulness'.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template = f"Generate keywords for the following interest: {interest}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    query = chain.run(interest=interest)

    return query

def embed_doc(text):
    embeddings = OpenAIEmbeddings()
    
    max_tokens = 8191
    encoding_name = 'cl100k_base'

    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)[:max_tokens]
    
    truncated_text = encoding.decode(tokens)

    query_result = embeddings.embed_query(truncated_text)

    return query_result

def recommend_books(student_embedding, book_embedding, top_k=5, similarity_threshold=0.4):
    similarities = [(book_title, cosine_similarity([student_embedding], [book_embedding])) 
                  for book_title, book_embedding in book_embedding.items()]
    similarities.sort(key=lambda x: x[1], reverse=True)

    top_k_books = []
    for book_title, similarity in similarities:
        if similarity >= similarity_threshold and len(top_k_books) < top_k:
            top_k_books.append(book_title)

    return top_k_books, similarities

def book_data(query, display=30):
    naver_url = 'https://openapi.naver.com/v1/search/book.json'

    headers = {"X-Naver-Client-Id" : st.secrets['client_id'], 
               "X-Naver-Client-Secret" : st.secrets['client_secret']}
    
    params = {"query" : query,
              "display" : display}
    
    response = requests.get(naver_url, headers=headers, params=params)

    data = pd.DataFrame(response.json()['items'])

    return data

def get_rent_status(isbn):
    url = f"https://kulis-primo.hosted.exlibrisgroup.com/primo-explore/search?query=any,contains,{isbn},AND&tab=default_tab&search_scope=default_scope&sortby=date&vid=82KHU_GLOBAL&lang=ko_KR&offset=0"

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    rentable = ''

    try:
        items = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.locations-link')))
        for item in items:
            rentable += item.text
    except Exception as e:
        pass
    finally:
        driver.quit()
    
    return rentable

# 관심사를 입력하면 해당 관심사와 관련된 책을 K개 추천.
if submit_interest:
    keywords = [keyword.strip() for keyword in generate_query(interest, gpt).split(",")]
    annotated_text([(keyword, "") for keyword in keywords])

    st.session_state["history"] += f"- {interest}\n"
    history.markdown(st.session_state["history"])

    df = pd.concat([book_data(keyword) for keyword in keywords], ignore_index=True)
    df = df[df['description'] != ''].reset_index(drop=True)
    df['rentable'] = df['isbn'].apply(lambda x : get_rent_status(x))
    df = df[df['rentable'] != '']

    embeddings = OpenAIEmbeddings()

    book_embeddings = {row['title'] : embed_doc(f"{row['description']}") for _, row in df.iterrows()}
    student_embedding = embeddings.embed_query(interest)
    recommend_books, similarities = recommend_books(
        student_embedding,
        book_embeddings,
        top_k = k,
        similarity_threshold=0
    )

    recommendation = df[df['title'].isin(recommend_books)]

    for idx, book in recommendation.iterrows():
        title = book['title']
        image = book['image']
        isbn = book['isbn']
        author = book['author']
        publisher = book['publisher']
        pubdate = book['pubdate']
        rentable = book['rentable']

        with st.form(f"{idx+1}"):
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, width=300)

            with col2:
                st.markdown(f"<h5>{title}</h5>", unsafe_allow_html=True)
                st.write(f"isbn : {isbn}")
                st.write(f'"{author}", {publisher}, {pubdate}')
                #st.form_submit_button("소장 정보", use_container_width=True, disabled=True, type="primary")
                st.form_submit_button(f"{rentable}", use_container_width=True, disabled=True, type="primary")
    