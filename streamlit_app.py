# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)
cnx=st.connection("snowflake")
session=cnx.session()

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Covert the snowpark dataframe to a pandas dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pf_df)
#st.stop()


ingredients_list=st.multiselect(
    'Choose up to 5 ingredients:'
      , my_dataframe
      , max_selections=5
     )
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    INGREDIENTS_STRING=''

    for fruit_chosen in ingredients_list:
        INGREDIENTS_STRING += fruit_chosen + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" +search_on)
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #st.write(INGREDIENTS_STRING)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + INGREDIENTS_STRING + """', '""" +name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

#new section to display smoothiefruit nutrition information





