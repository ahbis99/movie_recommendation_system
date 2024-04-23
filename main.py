import streamlit as st
import base64
from recommender import Recommender
from chat_bot import chatbot
import streamlit.components.v1 as components

config = {
    "page_title": "Baklava Film Gourmet",
    "page_icon": "👨‍🍳",
    "layout": "centered",
    "initial_sidebar_state": "auto",
    "button_background_color": "#a1b0ff",
    "button_text_color": "black",
    "reset_button_name": "Home",
    "random_button_name": "Serendipity Surprise!",
    "category_button_name": "Tailored Taste",
    "category_results_loading_text": "Cooking...",
    "category_results_name": "Voilà",
    "category_submit_button_name": "Cook",
}

@st.cache_resource()
def get_base64_of_bin_file(bin_file):
    """
    Encodes a file to base64 to be inserted inline inside an HTML file.

    Parameters:
    -----------
    bin_file : str
        The path to the file to be encoded.
    
    Returns:
    --------
    : str
        The base64 encoded file.
    
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    """
    Sets a PNG file as the background of the page.

    Parameters:
    -----------
    png_file : str
        The path to the PNG file to be used as the background.
    """
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
	* {
	font-family: "VT323", monospace;
	}
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    .reportview-container {
    margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
    }
    </style>
    """ % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


@st.cache_data()
def read_network_file():
    """
    Read the network file and return the NetworkX graph object.

    Returns:
    --------
    G : nx.Graph
        The NetworkX graph object.
    """
    rec = Recommender()
    rec = rec.read_pajek('movies_graph.net')
    cats = rec.get_category_list(rec.G)

    return rec, cats

def activate_chatbot(movie_name):
    """
    Activate the chatbot with the given movie name.

    Parameters:
    -----------
    movie_name : str
        The name of the movie for which the chatbot will be activated.
    """
    st.session_state.mode = 'chatbot'
    st.session_state.movie_name = movie_name


def filter_categories(categories):
    """
    Filter the recommendations based on the selected categories.

    Parameters:
    -----------
    categories : Set[str]
        The set of categories to filter the recommendations.

    Returns:
    --------
    filtered : List[str]
        The list of filtered recommendations.
    """
    filtered = [n.replace('m-', '') for n in categories if n != "m-N/A"]
    return filtered

def remove_loading_image():
    """Remove the loading image from the page after loading is complete.
    """
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('img');
            for (var i = 0; i < elements.length; ++i) {{ 
                    elements[i].remove();
            }}
        </script>
        """
    components.html(f"{htmlstr}", height=0, width=0)

def remove_buttons():
    """Remove the buttons from the page after loading is complete. Excludes the reset button.
    """
    global config
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText != '{config['reset_button_name']}') {{
                        elements[i].remove();
                    }}
            }}
        </script>
        """
    components.html(f"{htmlstr}", height=0, width=0)

def main():
    global config

    set_png_as_page_bg('webb.png')

    st.markdown(f"<h1 style='text-align: center; color: black;'>{config['page_title']} {config['page_icon']}</h1>", unsafe_allow_html=True)
    rec, cats = read_network_file()

    if st.session_state.get('mode') is None:
        col1, col2 = st.columns(2)
        if col1.button(config['random_button_name'], use_container_width=True):
            st.session_state.mode = 'random'
            st.rerun()

        if col2.button(config['category_button_name'], use_container_width=True):
            st.session_state.mode = 'category_selection'
            st.rerun()

    elif st.session_state.mode == 'random':
        _,col1,col2,__ = st.columns([0.2,0.2,0.2,0.2])
        lst = rec.get_random_list(rec.G, k=10)
        for i in range(int(len(lst)/2)):
            col1.button(lst[i], on_click=activate_chatbot, args=(lst[i],))
            col2.button(lst[i+5], on_click=activate_chatbot, args=(lst[i+5],))      

    elif st.session_state.mode == 'category_selection':
        _,col,__ =st.columns([0.2,0.6,0.2])
        cats_filtered = filter_categories(cats)
        values = col.multiselect('Ingredients', cats_filtered, max_selections=3)
        values = ["m-"+c for c in values if "m-"+c in cats] + [c for c in values if "m-"+c not in cats]
        st.session_state.categories = set(values)
        if col.button(config['category_submit_button_name']):
            st.session_state.mode = 'category_results'
            st.rerun()
    elif st.session_state.mode == 'category_results':
        st.markdown(f"<h2 style='text-align: center; color: black;'>{config['category_results_name']}</h2>", unsafe_allow_html=True)
        file_ = open("./travolta.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        
        st.markdown(
            f"""<img style="display: block;margin-left: auto;margin-right: auto;width: 50%;" src="data:image/gif;base64,{data_url}" alt="travolta gif">""",
            unsafe_allow_html=True,
        )

        lst = rec.get_recommendations(st.session_state.categories, k=10)
        remove_loading_image()
        _,col1,col2,__ = st.columns([0.2,0.2,0.2,0.2])
        for i in range(int(len(lst)/2)):
            col1.button(lst[i], on_click=activate_chatbot, args=(lst[i],))
            col2.button(lst[i+5], on_click=activate_chatbot, args=(lst[i+5],))

    elif st.session_state.mode == 'chatbot':
        remove_buttons()
        chatbot(st.session_state.movie_name)
    else:
        st.write('Invalid mode')
    
    if st.session_state.get('mode') is not None:
        st.button(config['reset_button_name'], on_click=lambda: st.session_state.clear())

main()