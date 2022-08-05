import pandas as pd
import streamlit as st
from sms_blast import SMS_Blast


st.header("E-BULK SMS AUTOMATION")

# File upload
phone_numbers = st.file_uploader("Upload file", ["xlsx"])
if phone_numbers is not None:
    try:
        df = pd.read_excel(phone_numbers, dtype={"Phone": str})
        recipients = list(df.Phone)
        unique_recipients = list(df.drop_duplicates(subset="Phone").Phone)
    except AttributeError as error:
        st.error("Failed to locate column 'Phone' in upload.")
        st.stop()

    st.success("Row count: {:,}".format(df.shape[0]))
    st.warning(
        "Unique count: {:,} | {:,} duplicates found.".format(
            len(unique_recipients), (len(recipients) - len(unique_recipients))
        )
    )

st.write("\n")

# Format message with agent phone number to see sample
with st.form("format_message"):
    col1, col2 = st.columns([1, 4])
    with col1:
        code = (
            st.text_input(
                "International Code ", placeholder="234", help="Default is 234"
            )
            or "234"
        )
    with col2:
        agent_numbers = st.text_input(
            "Agent Numbers",
            placeholder="0903 456 4788, 0803 445 5678",
            help="Separate number with commas",
        )

    message_body = st.text_area(
        label="Type Message Here",
        placeholder="""Need quick money? Call/WhatsApp Essential Finance on {} or https://bit.ly/3D6XApL to get a low interest loan & get credit in 3 hours.""",
        help="Please use '{}' in place of where the agent number should be.",
        max_chars=612,
    )

    format = st.form_submit_button("Format message")

if format:
    engine = SMS_Blast(code)
    formatted_message = engine.format_message(agent_numbers, message_body)

    st.write("\n")
    with st.form("bulk_sms"):
        col3, col4 = st.columns([1, 2])
        with col3:
            sender_id = st.text_input("Sender ID", max_chars=11)
        with col4:
            limit = st.number_input("Split On", value=5000)

        st.write("Message Sample:")
        st.info(formatted_message)

        submitted = st.form_submit_button("Submit")

    if submitted:
        with st.spinner("Processing..."):
            response = engine.send_message(
                sender_id, limit, agent_numbers, formatted_message, recipients
            )
        st.info(response)
