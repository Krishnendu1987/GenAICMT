import streamlit as st
import os
from langchain.llms import OpenAI
import json
from tenacity import retry, stop_after_attempt, wait_random_exponential
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
import business_functions  # Import your business functions module


# get parent directory relative to current directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
persona_dir = os.path.join(parent_dir, "personas")

# get persona from the added ones
persona1_json = os.path.join(persona_dir, "Movie_analyst_1.json")
persona2_json = os.path.join(persona_dir, "medical_persona_1.json")

# Load the persona and OpenAI API key
def load_personas():
    with open(persona1_json) as file:
        persona1 = json.load(file)
    with open(persona2_json) as file:
        persona2 = json.load(file)
    
    return persona1, persona2

# Select the persona based on user choice
def select_persona(persona_choice):
    if persona_choice == 'Movie Analyst':
        return persona1
    elif persona_choice == 'Medical Apprentice':
        return persona2


# Format the persona context
def format_persona_context(persona):
    persona_template = """
    You are {name}. {whoami}
    {conversationwith}
    {traits}
    Goal of this conversation for you: {goal}
    Skill of you: {skills}
    Topics you must avoid : {avoided_topics}
    Reply based on conversation history provided in 'Context:'
    Reply with prefix '{chatname}:'
    Respond with {responselength} words max.
    """
    return persona_template.format(**persona['bot'])


# The completion function with retry logic
@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(2))
def get_chatbot_response(messages):
    try:
        llm_response = st.session_state.conversation.run(messages)
        return llm_response
    except Exception as e:
        st.error(f"Error: {e}")
        return None
    
# Initialize session state
def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []

    if "conversation" not in st.session_state:
        llm = OpenAI(
            temperature=0,
            openai_api_key=st.secrets["openai_api_key"],  # Replace with your OpenAI API key from secrets
            model_name="text-davinci-003"
        )
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=ConversationSummaryMemory(llm=llm)
        )


# Load persona and API key
persona1,persona2 = load_personas()
# bot_context = format_persona_context(persona)
# conversation_buffer = []

# Streamlit UI
st.title("Chat with a Bot")
# Persona selection
persona_choice = st.selectbox("Choose a Persona", ['Movie Analyst', 'Medical Apprentice'])
selected_persona = select_persona(persona_choice)
bot_context = format_persona_context(selected_persona)
conversation_buffer = []
user_input = st.text_input("Your message:", key="user_input")



if st.button("Send"):
    if len(conversation_buffer) > 10:
        conversation_buffer = conversation_buffer[-10:]
    user_message = {"role": "user", "content": selected_persona['human']['chatname'] + ":" + user_input}
    system_message = {"role": "system", "content": bot_context}
    context_message = {"role": "system", "content": "Context:\n" + "".join(conversation_buffer)}

    messages = [system_message, context_message, user_message]
    user_input =st.session_state.user_input
    llm_response =st.session_state.conversation.run(user_input)
    st.session_state.history.append(user_input)
    st.session_state.history.append(llm_response)
    bot_response = get_chatbot_response(messages)

    if bot_response:
        conversation_buffer.append("You: " + user_input + "\n")
        conversation_buffer.append("Bot: " + bot_response + "\n")
        st.text_area("Chat", value="\n".join(conversation_buffer), height=300, key="chat_area")

st.sidebar.title("Bot Information")
st.sidebar.text(f"Name: {selected_persona['bot']['name']}")
st.sidebar.text(f"Traits: {selected_persona['bot']['traits']}")

# Initialize session state
initialize_session_state()
