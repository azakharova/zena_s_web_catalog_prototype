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
streamlit.write(df)