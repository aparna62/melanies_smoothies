# Import python packages
import requests
import streamlit as st
cnx=st.connection("Snowflake")
session=cnx.session()
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("My Parents New Healthy Diner")


st.write("Breakfast Menu");

name_on_order = st.text_input( 'Name on Smoothie: ')
st.write('The name on your smoothie will be', name_on_order)
cnx=st.connection("Snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME').col('search_on'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Choose up to 5 ingredients:',my_dataframe)

if ingredients_list:
    ingredients_string=''
    for fruit_choosen in ingredients_list:
        ingredients_string+=fruit_choosen+' '
        st.subheader(fruit_chosen+'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
        #st.text(fruityvice_response.json())
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")






