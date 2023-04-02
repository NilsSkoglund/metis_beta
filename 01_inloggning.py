from deta import Deta
import streamlit as st
import time
from tools import test_login_page
from tools import test_init_session_state_vars
from tools import google_oauth
import extra_streamlit_components as stx
cm = stx.CookieManager(key="init2")
st.write(cm.get_all(key="blabla"))

test_init_session_state_vars.init_session_state()

if st.session_state["authentication_status"] == None and "random_cookie_name" not in cm.get_all():

    client_id = "836432242434-a1mg70bs9s2g83llpvd6jmidstkgovtt.apps.googleusercontent.com"
    client_secret = "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"
    uri = 'http://localhost:8501'
    login_info = google_oauth.login(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=uri,
            logout_button_text="Logga ut"
        )

    if login_info:
        test_login_page.custom_authenticate_oauth()

test_login_page.custom_authenticate()


if st.session_state["authentication_status"]:
    # litet hack för bättre ui/ux
    time.sleep(1)
    # frontend
    if "google" not in st.session_state:
        st.session_state["authenticator"].logout('Logout', 'main')
    else:
        google_oauth.logout_button("Logga ut")
    # litet hack för bättre ui/ux
    time.sleep(1)
    st.write(f'Inloggad med email: {st.session_state["name"]}')

    # backend
    # connect to database
    # database name based on username - new session state variable
    st.session_state["db"] =\
    st.session_state["deta"].Base(st.session_state["username"])

    test_login_page.custom_user_logged_in()

# frontend
    # fel inloggningsuppgifter
if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')

    # frontend/backend
    # användare väljar att registrera ny profil
    # widget - new session state variable
    st.checkbox("Registrera", key="register_user_v1")
    if st.session_state["register_user_v1"]:
        test_login_page.custom_register_user()
# frontend
    # ej angett inloggningsuppgifter
if st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')

    # frontend/backend
    # användare väljar att registrera ny profil
    # widget - new session state variable
    st.checkbox("Registrera", key="register_user_v2")
    if st.session_state["register_user_v2"]:
        test_login_page.custom_register_user()
