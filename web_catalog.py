import streamlit
import snowflake.connector
import pandas

streamlit.title("Zena's Amazing Athleisure Catalog")

# connect to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

# run a snowflake query and put it all in a var called my_catalog
my_cur.execute("select distinct color_or_style from catalog_for_website")
my_catalog = my_cur.fetchall()

# put the dafta into a dataframe
df = pandas.DataFrame(my_catalog)
# streamlit.write(df)

# put the first column into a list
color_list = df[0].values.tolist()
# print(color_list)

# color picker
with streamlit.form("color_picker_form", clear_on_submit=True, border=False):
    option = streamlit.selectbox('Pick a sweatsuit color or style:', list(color_list))
    submit_button = streamlit.form_submit_button(label='Submit')
    if submit_button:
        # image caption
        product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

        # return information about selected option
        my_cur.execute("select direct_url, price, size_list, upsell_product_desc from catalog_for_website where color_or_style = '" + option + "';")
        product_info = my_cur.fetchone()

        streamlit.image(product_info[0], caption=product_caption, width=400)
        streamlit.write('Price: $' + str(product_info[1]))
        streamlit.write('Available sizes: ' + product_info[2])
        streamlit.write(product_info[3])