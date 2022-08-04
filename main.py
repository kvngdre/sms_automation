from nbformat import write
import pandas as pd
import streamlit as st
import engine

st.header('EBULK SMS AUTOMATION')

phone_numbers = st.file_uploader('Upload file', ['xlsx'])
if phone_numbers is not None:
    try:
        df = pd.read_excel(phone_numbers, dtype={'Phone': str})
        numbers_list = list(df.Phone)
    except AttributeError as error:
        st.error(error)
        st.stop()

    col1, col2, col3 = st.columns([1, 3, 4])
    with col1:
        st.write('Row count:')
    with col2:
        st.write(df.shape[0])


st.write('\n')
with st.form('bulk_sms'):
    col3, col4 = st.columns([1, 3])

    with col3:
        sender_id = st.text_input('Enter sender id:')

    message_body = st.text_area('Type message here', max_chars=612)


    submitted = st.form_submit_button('Submit')

if submitted:
    with st.spinner():
        response = engine.send_message(sender_id, message_body, numbers_list)
    st.info(response)
    