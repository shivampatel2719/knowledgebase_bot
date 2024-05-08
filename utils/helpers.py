import random
import string

def generate_unique_name(resource_name, title):
    unique_id = ''.join(random.choice(string.digits) for i in range(5))
    unique_name = f"{resource_name}-{title}-{unique_id}"
    return unique_name

def init_configs(st):
    st.set_page_config(layout="wide")
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
    # st.markdown(hide_st_style, unsafe_allow_html=True)