import streamlit
import snowflake.connector

streamlit.title("Zena's Amazing Athleisure Catalog")

# color's list for picker
# def get_colors():
#     with my_cnx.cursor() as cur:
#         my_cur.execute("select distinct color_or_style from zenas_athleisure_db.products.catalog_for_website")
#         return my_cur.fetchall()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select distinct color_or_style from catalog_for_website")
my_colors = my_cur.fetchall()
color_selected = streamlit.selectbox("Pick a sweatsuit color or style:", list(my_colors))