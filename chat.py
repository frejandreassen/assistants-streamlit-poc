import streamlit as st
from openai import OpenAI
import time 

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Define the assistant (Do this once outside of your main app logic to avoid creating multiple assistants)
# if 'assistant_id' not in st.session_state:
#     assistant = client.beta.assistants.create(
#         name="Math tutor",
#         instructions="You are a personal math tutor. Write and run code to answer math questions.",
#         tools=[{"type": "code_interpreter"}],
#         model="gpt-4-1106-preview"
#     )
#     st.session_state.assistant_id = assistant.id
# else:
#     assistant_id = st.session_state.assistant_id

assistant_id = "asst_PY4qXn12WRdBxMnaUcMgZ4sz"
# Create a new thread for the conversation


# Initialize the messages state if not already present
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'thread' not in st.session_state:
    st.session_state.thread = client.beta.threads.create()
thread = st.session_state.thread

st.write(thread.id)
st.title("Math Tutor Chat")

# Display the chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Handle user input
user_input = st.chat_input("Ask a math question:")
if user_input:
    
    # Add user input to messages and display
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add message to the thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions="Please address the user as Frej Andreassen. The user has a premium account."
    )

    # Wait for the assistant to respond
    polls = 0
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status in ['completed', 'failed']:
            break
        polls += 1
        if (polls > 20): break
        time.sleep(0.5)  # Sleep for half a second before checking again

    # Display the assistant's response
    if run_status.status == 'completed':
        # Get the messages here:
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        # Display each new message from the assistant
        message = messages.data[0]
        if message.role == "assistant":
            content = message.content[0].text.value
            st.session_state.messages.append({"role": "assistant", "content": content})
            with st.chat_message("assistant"):
                st.markdown(content)