import streamlit as st
from services.bedrock_agent import BedRockAgent
from aws_clients.s3_client import S3Client

class CreateKnowledgeBase:
    def run(self):
        if st.button("Go to Homepage"):
            st.switch_page("main.py")
        st.title("Create Knowledge base")
        
        kb_title = st.text_input("Enter title of knowledge base *")
        kb_description = st.text_area("Enter description of knowledge base", height=100)
        uploaded_files = st.file_uploader("Upload files", type=['csv', 'txt', 'xlsx', 'pdf'], accept_multiple_files=True)

        if st.button(label="Submit"):
            bedrock_agent = BedRockAgent()
            response = bedrock_agent.create_knowledge_base(title=kb_title)
            print(response)
            st.write(response)
        # if uploaded_file is not None:
        #     st.success("File uploaded successfully!")
        #     if st.button("Submit"):
        #         # Perform processing or action on the uploaded file here
        #         st.info("File submitted!")


if __name__=='__main__':
    create_knowledge_base = CreateKnowledgeBase()
    create_knowledge_base.run()