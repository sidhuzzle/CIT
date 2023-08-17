import streamlit as st

import openai
from streamlit_chat import message


openai.api_key = st.secrets["api_key"]

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
if 'time' not in st.session_state:
    st.session_state['time'] = []
if 'utensils' not in st.session_state:
    st.session_state['utensils'] = []

if 'servings' not in st.session_state:
    st.session_state['servings'] = 0.0

st.sidebar.title("Filters")
time = st.sidebar.slider('Cooking time', 0, 100,key = 'one')

utensils =  st.sidebar.multiselect('MAJOR APPLIANCES',['Stove or cooking range','Mixer or food processor','Grinder','Refrigerator','Microwave Oven','Induction stove','Rice cooker'])
utensils = ' '.join([str(elem) for elem in utensils])
servings = st.sidebar.slider('No of Servings', 1, 10,key = 'two')


if time == 0 & len(utensils) == 0  & servings == 0:
    message = 'recipe' + ' ' + 'with' + " " + 'ingredients' + " " + 'and' + " " + 'instruction'
else:
    message = 'recipe' + " " +  'within' + "  " + str(time)  + "  " + 'minutes' + "   " + 'using' + "  " + utensils + "  " + 'for' + "  "  + str(servings) +  "  "  + 'people'
 

   
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})
    return response

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
        s = ['how much','gm','gram','kilogram','what does','quantity','color','colour','kg','tablespoon','teaspoon','boil','heat','freeze','required']
        for i in s:
            if i in prompt.split():
                user_input = prompt
            else:
                user_input = str(prompt) +  " " + str(message)
        #s = pd.unique(list(user_input))
        #userinput = ''.join(s)
        print(user_input)
        #st.write(user_input)

        output = generate_response(user_input)
        st.write(output)
        print(len(output))
       
        
