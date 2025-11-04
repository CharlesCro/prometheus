# Standard Libraries
import ast

# Non-Standard Libraries
from dotenv import load_dotenv
import streamlit as st

# Custom Modules
from services.prometheus_service import initialize_adk, run_adk_sync
from services.author_service import invoke
from utils.helpers import convert_to_json
from config.settings import MESSAGE_HISTORY_KEY, get_api_key

load_dotenv()

def login_screen():
    st.header('Welcome to LocaleWeb')
    if st.button("Log in with Google"):
        st.login()

def run_streamlit_app():
    '''
    Sets up and runs the Streamlit web application for the ADK chat assistant.
    '''

    
    st.set_page_config(page_title='Project Prometheus', layout='wide') # Configures the browser tab title and page layout.
   
    

    api_key = get_api_key() # Retrieve the API key from settings.
    if not api_key:
        st.error('Action Required: Google API Key Not Found or Invalid! Please set GOOGLE_API_KEY in your .env file. ⚠️')
        st.stop() # Stop the application if the API key is missing, prompting the user for action.
    # Initialize ADK runner and session ID (cached to run only once).
    adk_runner, current_session_id = initialize_adk()

    # User Info
    with st.sidebar:
        if not st.user.is_logged_in:
            if st.button("Log in with Google"):
                st.login()
            st.stop()

        if st.button("Log out"):
            st.logout()
        st.markdown(f"Welcome, {st.user.name}")


    print(f"DEBUG UI: Using ADK session ID: {current_session_id}")

    
    if st.button('Generate & Send Random Prompt'):
        # 1. Generate the prompt
        generated_prompt = invoke()
        
        # 2. Append user's message to history (simulating user input)
        st.session_state[MESSAGE_HISTORY_KEY].append({'role': 'user', 'content': generated_prompt})
        
        # 3. Process the prompt (get assistant's response)
        print(f"DEBUG UI: Sending generated prompt to ADK with session ID: {current_session_id}")
        agent_response = run_adk_sync(adk_runner, current_session_id, generated_prompt)
        print(f"DEBUG UI: Received response from ADK for generated prompt: {agent_response[:50]}...")
        
        # 4. Append assistant's response to history.
        st.session_state[MESSAGE_HISTORY_KEY].append({'role': 'assistant', 'content': agent_response})
        
        # 5. Rerun the app to refresh the display and show the new messages
        st.rerun()
        

    # Initialize chat message history in Streamlit's session state if it doesn't exist.
    if MESSAGE_HISTORY_KEY not in st.session_state:
        st.session_state[MESSAGE_HISTORY_KEY] = []
    # Display existing chat messages from the session state.
    for message in st.session_state[MESSAGE_HISTORY_KEY]:
        with st.chat_message(message['role']): # Use Streamlit's chat message container for styling.
            st.markdown(message['content'])
    # Handle new user input.
    if prompt := st.chat_input('Enter message'):
        # Append user's message to history and display it.
        st.session_state[MESSAGE_HISTORY_KEY].append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
        # Process the user's message with the ADK agent and display the response.
        with st.chat_message('assistant'):
            message_placeholder = st.empty() # Create an empty placeholder to update with the assistant's response.
            with st.spinner('Assistant is thinking...'): # Show a spinner while the agent processes the request.
                print(f"DEBUG UI: Sending message to ADK with session ID: {current_session_id}")
                agent_response = run_adk_sync(adk_runner, current_session_id, prompt) # Call the synchronous ADK runner.
                print(f"DEBUG UI: Received response from ADK: {agent_response[:50]}...")
                message_placeholder.markdown(agent_response) # Update the placeholder with the final response.
        
        # Append assistant's response to history.
        st.session_state[MESSAGE_HISTORY_KEY].append({'role': 'assistant', 'content': agent_response})
