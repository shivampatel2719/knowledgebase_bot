import time
import boto3
import streamlit as st
from aws_clients.s3_client import S3Client
from aws_clients.knowledge_base_client import KnowledgeBaseClient

class ModifyDataSourcePage:
    def __init__(self):
        self.client = boto3.client('bedrock-agent')
        self.s3_client = S3Client()
        self.knowledge_base_client = KnowledgeBaseClient()
        query_params = st.query_params
        if 'KBId' in query_params:
            self.kb_id = query_params['KBId']
        else:
            raise Exception(f'No Knowledge base Id passed')
    
    def run(self):
        if st.button("Go to Homepage"):
            st.switch_page("main.py")
        st.title("Modify Data Source Files")
        s3_objects = self._get_s3_objects(knowledgeBaseId=self.kb_id)
        
        with st.form("my-form", clear_on_submit=True):
            uploaded_files = st.file_uploader("Upload files", type=['csv', 'txt', 'xlsx', 'pdf'], accept_multiple_files=True)
            submitted = st.form_submit_button("Upload to S3")
            
            if submitted and len(uploaded_files) == 0:
                st.error("No Files Selected !")
                time.sleep(3)
                st.rerun()

            if submitted and uploaded_files is not None and len(uploaded_files) != 0:
                for uploaded_file in uploaded_files:
                    response, message = self.s3_client.upload_to_s3(bucket_name=self.bucket_name, uploaded_file=uploaded_file, prefix=self.prefix)
                    if response != 200:
                        st.error(message)
                    else:
                        st.success(f"File : {uploaded_file.name} Uploaded Successfully !")
                response, message = self.knowledge_base_client.sync_data_source(dataSourceId=self.dataSourceId, knowledgeBaseId=self.kb_id)
                if response != 200:
                    st.error(message)
                else:
                    st.success("Data Source Synced Successfully !") 
            
                time.sleep(5) 
                st.rerun()
        self.display_s3_objects(s3_objects=s3_objects)
    
    def _get_s3_objects(self, knowledgeBaseId):
        data_sources = self.client.list_data_sources(
            knowledgeBaseId = knowledgeBaseId
        )
        for data_source_summary in data_sources["dataSourceSummaries"]:
            self.dataSourceId = data_source_summary["dataSourceId"]
            data_source = self.client.get_data_source(
                dataSourceId = self.dataSourceId,
                knowledgeBaseId = knowledgeBaseId
            )
            data_source_s3_configuration = data_source.get("dataSource").get("dataSourceConfiguration").get("s3Configuration")
            data_source_bucket_arn = data_source_s3_configuration.get("bucketArn")
            self.prefix = data_source_s3_configuration.get("inclusionPrefixes")[0].split("/")[0]
            self.bucket_name = data_source_bucket_arn.split(":::")[1]
            # as of now we only upload to single prefix
            s3_objects = self.s3_client.get_s3_objects(bucket_arn = self.bucket_name, prefix=self.prefix)
        return s3_objects

    def display_s3_objects(self, s3_objects):
        st.divider()
        for s3_object in s3_objects:
            col1, col2 = st.columns([3, 1])  # Adjust column ratios as needed
            object_key = s3_object.get("Key")
            with col1:
                st.write(object_key)
            with col2:
                if st.button("🗑️", key=object_key):
                    self.s3_client.delete_s3_object(bucket_name=self.bucket_name, key=object_key)
                    self.knowledge_base_client.sync_data_source(dataSourceId=self.dataSourceId, knowledgeBaseId=self.kb_id)
                    st.rerun()
                    st.write(s3_objects)
            st.divider()
    
if __name__=='__main__':
    modify_data_source_page = ModifyDataSourcePage()
    modify_data_source_page.run()