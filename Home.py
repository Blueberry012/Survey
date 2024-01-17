import streamlit as st

tab1, tab2, = st.tabs(["Survey", "Dataset"])

with tab1:
    st.title("Survey")

    name = st.text_input("What is your name?")

    birthday = st.date_input("What is your birthday?")

    nationality = st.checkbox('French Nationality')

    bac = st.selectbox('What Baccalauréat did you take?',['', 'BAC S', 'BAC ES', 'BAC L', 'BAC STMG', 'Other'])

    work = st.slider('How many years have you worked?', 0, 50)

    hobbies = st.multiselect('What are your hobbies?',('Reading','Traveling','Arts and Photography','Cooking','Cinema','Series and Television','Music','Video Games','Sport'))
    hobbies = ', '.join(hobbies)

    contact = st.radio('How would you like to be contacted?',('Email', 'Mobile phone', 'Home phone'))

    if contact == 'Email':
        contact_address = st.text_input("What is your email address?")
        if ("@" not in contact_address) or ("." not in contact_address):
            st.write("This is not a valid email address.")

    elif contact == 'Mobile phone':
        contact_address = st.text_input("What is your mobile phone number?")
        contact_address = contact_address.replace(" ", "")
        if not (contact_address.startswith("06") or contact_address.startswith("07")) or len(contact_address) != 10:
            st.write("This is not a valid mobile phone number.")
        contact_address = ' '.join(contact_address[i:i+2] for i in range(0, len(contact_address), 2))

    elif contact == 'Home phone':
        contact_address = st.text_input("What is your home phone number?")
        contact_address = contact_address.replace(" ", "")
        if not (contact_address.startswith("01")) or len(contact_address) != 10:
            st.write("This is not a valid home phone number.")
        contact_address = ' '.join(contact_address[i:i+2] for i in range(0, len(contact_address), 2))

    if st.button("Send Form"):
        conn = st.connection('survey_db', type='sql')
        with conn.session as s:
            s.execute('CREATE TABLE IF NOT EXISTS dataset (ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, birthday DATE, nationality TEXT, bac TEXT, work TEXT, hobbies TEXT, contact TEXT, contact_address TEXT);')
            s.execute(
                'INSERT INTO dataset (name, birthday, nationality, bac, work, hobbies, contact, contact_address) VALUES (:name, :birthday, :nationality, :bac, :work, :hobbies, :contact, :contact_address);',
                params=dict(name=name, birthday=birthday, nationality=nationality, bac=bac, work=work, hobbies=hobbies, contact=contact, contact_address=contact_address)
            )
            s.commit()

        #st.cache_data.clear()
        #dataset = conn.query("SELECT * FROM dataset")
        #st.dataframe(dataset)

with tab2:
    st.title("Dataset")
    display = st.toggle('Display Data')

    id_delete = st.text_input("Enter the ID to delete:")
    if st.button("Delete") and (id_delete != ""):
        conn = st.connection('survey_db', type='sql')
        with conn.session as s:
                s.execute(
                    'DELETE FROM dataset WHERE ID = :id;',
                    params=dict(id=id_delete)
                )
                s.commit()

    if display:
        conn = st.connection('survey_db', type='sql')
        st.cache_data.clear()
        dataset = conn.query("SELECT * FROM dataset")
        st.dataframe(dataset)