import streamlit as st
import snowflake.connector
import pandas

st.title("Zena's Amazing Athleisure Catalog")

# Connect to snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()

# Run a snowflake query and put it all in a var called my_catalog
my_cur.execute("select distinct color_or_style from catalog_for_website order by color_or_style;")
my_catalog = my_cur.fetchall()

# Put the data into a dataframe
df = pandas.DataFrame(my_catalog)

# Put the first column into a list
color_list = df[0].values.tolist()
print(color_list)

# Initialize session state
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

# Color picker
with st.form("color_picker_form", clear_on_submit=True, border=False):
    # Use session_state for the selected option
    option = st.selectbox('Pick a sweatsuit color or style:', list(color_list), index=color_list.index(st.session_state.selected_option) if st.session_state.selected_option else 0)
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Save the selected option to session_state
        st.session_state.selected_option = option

        # Image caption
        product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

        # Return information about the selected option
        my_cur.execute("select direct_url, price, size_list, upsell_product_desc from catalog_for_website where color_or_style = '" + option + "';")
        product_info = my_cur.fetchone()

        st.image(product_info[0], caption=product_caption, width=400)
        st.write('Price: $' + str(product_info[1]))
        st.write('Available sizes: ' + product_info[2])
        st.write(product_info[3])
