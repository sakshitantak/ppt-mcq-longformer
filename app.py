# Imports
import re

import streamlit as st
import textractplus as tp
from qa import QuestionAnsweringModel

st.set_page_config(layout='wide')
st.title('PowerPoint Presentation Q&A')

if 'i' not in st.session_state:
    st.session_state['i'] = 0

if 'choices' not in st.session_state:
    st.session_state['choices'] = []

def clean_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text

if 'file' not in st.session_state:
    st.session_state['file'] = st.file_uploader('Upload ppt')
    with open('tmp.pptx', 'wb') as f:
        f.write(st.session_state['file'].getbuffer())
    f.close()
else:
    text = tp.process()
    text = tp.process('tmp.pptx', input_encoding='utf-8').decode()
    text = clean_text(text)
    print(f'i = {st.session_state.i}')
    for i, choice in enumerate(st.session_state.choices):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input(label='', value=f"Choice {i}", disabled=True)
        with col2:
            st.text_area(label='', value=choice, disabled=True)
    t = st.text_input(f'Choice {st.session_state["i"]}', key = f'choice{str(st.session_state["i"])}')
    print('type : ', type(t))
    def add_choice(choice):
        print(f'Inside add_choice .')
        st.session_state['choices'].append(choice)
        st.session_state['i'] += 1
    print('choices : ', st.session_state['choices'])
    print('text input : ', t)
    submit = st.button('Add choice', on_click = add_choice, kwargs = dict(choice=t))
    process = st.button('Find answers')
    if process:
        if 'model' not in st.session_state:
            with st.spinner('Loading Model ...'):
                st.session_state['model'] = QuestionAnsweringModel()
        st.success('Model Loaded successfully!')
        with st.spinner('Finding the best answer ...'):
            answer = st.session_state['model'].get_answer(text, st.session_state.choices)
        st.success(f'Choice{answer} : {st.session_state["choices"][answer]}')