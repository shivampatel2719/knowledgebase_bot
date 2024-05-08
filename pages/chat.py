import streamlit as st
from utils.helpers import init_configs
from services.bedrock_agent_runtime import BedRockAgentRuntime

class SimpleChatApp:
    def __init__(self):
        self.messages = []
        self.bedrock_agent_client = BedRockAgentRuntime()
        query_params = st.query_params
        if 'KBId' in query_params:
            self.kb_id = query_params['KBId']
        else:
            raise Exception(f'No Knowledge base Id passed')

    def display_messages(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def accept_user_input(self):
        if prompt := st.chat_input("Ask something here !"):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            response = self.bedrock_agent_client.retrieveAndGenerate(prompt, self.kb_id)
            
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    def run(self):
        init_configs(st=st)
        
        if st.button("Homepage"):
            st.query_params.clear()
            st.switch_page("main.py")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = self.messages
        
        if not len(st.session_state.messages):
            with st.chat_message("assistant"):
                st.markdown('Ask me anything !')

        self.display_messages()
        self.accept_user_input()

if __name__ == "__main__":
    chat_app = SimpleChatApp()
    chat_app.run()
