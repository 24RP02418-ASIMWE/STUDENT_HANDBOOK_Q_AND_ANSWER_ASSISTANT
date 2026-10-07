import streamlit as st
from rag_engine import answer_question

st.set_page_config(page_title='RP Student Handbook Q&A', page_icon='🎓', layout='wide')
st.title('🎓 RP Student Handbook Q&A Assistant')
st.caption('RAG-based question answering system using the Rwanda Polytechnic Student Handbook.')
st.info('Ask about attendance, assessments, student ID, fees, library rules, registration, or other handbook information.')
question = st.text_input('Enter your question', placeholder='Ask question here')
if st.button('Ask', type='primary'):
    if not question.strip():
        st.warning('Please enter a question.')
    else:
        with st.spinner('Searching the handbook...'):
            result = answer_question(question)
        st.subheader('Answer')
        st.write(result['answer'])
        st.subheader('Sources')
        for source in result['sources']:
            st.write(f"📄 Handbook page {source['page']} — relevance: {source['score']:.3f}")
        with st.expander('Retrieved evidence'):
            for item in result['retrieved']:
                st.markdown(f"**Page {item['page']} | score {item['score']:.3f}**")
                st.write(item['text'])
st.divider()
st.caption('Responsible use: if the handbook does not support an answer, the system should say so rather than invent information.')
