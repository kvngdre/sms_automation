import pandas as pd
import streamlit as st
import engine

st.header('E-BULK SMS AUTOMATION')

phone_numbers = st.file_uploader('Upload file', ['xlsx'])
if phone_numbers is not None:
    try:
        df = pd.read_excel(phone_numbers, dtype={'Phone': str})
        recipients = list(df.Phone)
    except AttributeError as error:
        st.error("Failed to locate column 'Phone' in upload")
        st.stop()

    st.success('Row count: {:,}'.format(df.shape[0]))

st.write('\n')
with st.form('format_message'):
    agent_numbers = st.text_input('Agent Numbers', placeholder='0903 456 4788, 0803 445 5678', help='Split number with commas')

    message_body = st.text_area('Type message here', max_chars=612)

    format = st.form_submit_button('Format message')


if format:
    pass

    
    st.write('\n')
    with st.form('bulk_sms'):
        col1, col2 = st.columns([1, 2])
        with col1:
            sender_id = st.text_input('Sender ID', max_chars=11)
        with col2:
            limit = st.number_input('Split On', value=5000)

        # st.write(formatted_message)

        submitted = st.form_submit_button('Format message')

    # if format_message:
    #     pass

    if submitted:
        with st.spinner('Processing...'):
            response = engine.send_message(sender_id, limit, agent_numbers, message_body, recipients)
        st.info(response)
        