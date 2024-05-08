import streamlit as st
from utils.helpers import init_configs
import utils.css as css
from aws_clients.knowledge_base_client import KnowledgeBaseClient

class MainApp(object):
    def __init__(self) -> None:
        pass
    
    def display_cols(self, knowledge_bases):
        num_columns = len(knowledge_bases) // 3 + (1 if len(knowledge_bases) % 3 != 0 else 0)
        columns = st.columns(num_columns)
        
        
        # Populate each column with clickable cards
        st.markdown(css.custom_css, unsafe_allow_html=True)
        for i, card in enumerate(knowledge_bases):
            with columns[i % num_columns]:
                st.markdown(f"""
                    <div class="glow-on-hover">
                        <h3>{card['name']} </h3>
                        <button disabled style="{css.button_style_success}">{card['status']}</button>
                        <p></p>
                        <a target="_self" href="{card['link']}" style="text-decoration: none; color: inherit;">
                            <button style="{css.button_style_info}">Chat</button>
                        </a>
                        <button style="{css.button_style_info}">Modify Data Source</button>
                    </div>
                    
                """, unsafe_allow_html=True)    
    
    def run(self):
        init_configs(st=st)
        st.title("GroundTruth Knowledge Bases")
        knowledge_base_responses = KnowledgeBaseClient.list_knowledge_base()
        knowledge_bases = []
        for knowledge_base_response in knowledge_base_responses["knowledgeBaseSummaries"]:
            knowledge_base_response["link"] = f'/chat/?KBId={knowledge_base_response.get("knowledgeBaseId")}'
            knowledge_bases.append(knowledge_base_response)
        self.display_cols(knowledge_bases=knowledge_bases)

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()