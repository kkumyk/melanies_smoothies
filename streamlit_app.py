# Fetch fruit name and search term from the table
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'), col('SEARCH_ON')
).to_pandas()

# Create a dictionary for lookup later
fruit_lookup = dict(zip(my_dataframe['FRUIT_NAME'], my_dataframe['SEARCH_ON']))

# User selection
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        search_term = fruit_lookup[fruit_chosen]
        ingredients_string += fruit_chosen + ' '
        st.subheader(f"{fruit_chosen} Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_term)
        st.dataframe(data=smoothiefroot_response.json()) 

    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')"""

    st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



# # Import python packages
# import streamlit as st
# from snowflake.snowpark.functions import col
# import requests

# # Write directly to the app
# st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write(
#   """
#   Choose the fruits you want in your custom Smoothie!
#   """)

# name_on_order = st.text_input('Name on Smoothie:')
# st.write('The name on your Smoothie will be:', name_on_order)


# cnx = st.connection("snowflake")
# session = cnx.session()

# # session = get_active_session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# # st.dataframe(data=my_dataframe, use_container_width=True)

# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients:',
#     my_dataframe,
#     max_selections=5
# )

# if ingredients_list:
#     ingredients_string = ''
#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '
#         st.subheader(fruit_chosen + ' Nutrition Information')
#         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
#         sf_df = st.dataframe(data=smoothiefroot_response.json()) 

#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
#             values ('""" + ingredients_string + """', '""" +name_on_order+ """' )"""

#     st.write(my_insert_stmt)
#     #st.stop()
    
#     time_to_insert = st.button('Submit Order')

#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")
