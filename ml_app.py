import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.title('🤖 Machine Learning App:') 

st.info("This is app builds as machine Learning model!")

with st.expander('Data'):
  st.write('**Raw data**')
  df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')
  df

  st.write('**X**')
  X = df.drop('species', axis=1)
  X

  st.write('**y**')
  y = df.species
  y

with st.expander("Data visualization"): 
    st.header("Bar_chart")
    st.bar_chart(data=df, x='bill_length_mm', y='body_mass_g', color='species')
    st.header("Scatter_chart")
    st.scatter_chart(data=df, x='bill_length_mm', y='body_mass_g', color='species')
    st.header("Line_chart")
    st.line_chart(data=df, x='bill_length_mm', y='body_mass_g', color='species')
    st.header("Area_chart")  
    st.area_chart(data=df, x='bill_length_mm', y='body_mass_g', color='species')  
    
with st.sidebar: 
    st.header('Input features')
    island = st.selectbox('Island' , ('Biscoe', 'Dream', 'Torgersen'))
    gender = st.selectbox('Gender', ('male', "female")) 
    bill_length_mm = st.slider('Bill length (mm)', 32.1, 59.6,43.9)
    bill_depth_mm = st.slider('Bill depth (mm)', 13.1,21.5,17.2)
    flipper_length_mm = st.slider('Flipper length (mm)', 172.0, 231.0, 201.0)
    body_mass_g = st.slider ('Body mass (g)', 2700.0, 6300.0, 4207.0)   
        
data = {'island': island, 
        'bill_length_mm': bill_length_mm,
        'bill_depth_mm': bill_depth_mm,
        'flipper_length_mm': flipper_length_mm,
        'body_mass_g': body_mass_g,
        'sex': gender} 
input_df = pd.DataFrame(data, index=[0])
input_penguins = pd.concat([input_df, X], axis=0)

with st.expander('Input Features'): 
    st.write('**Input Penguin**')
    input_df 
    st.write('**Combined penguins data**') 
    input_penguins 
    
#Data preparation 
#Encode x 
label_encode = ['island','sex']
df_penguins = pd.get_dummies(input_penguins, prefix=label_encode)

df_penguins = df_penguins.fillna(0)  # Fill any NaNs with 0

x = df_penguins[1:]
input_row = df_penguins[:1]

#Encode y 
target_mapper = {'Adelie' :0, 
                 'Chinstrap': 1, 
                  'Gentoo':2} 

def target_encode(val): 
    return target_mapper[val] 

y = y.apply(target_encode)

with st.expander("Data Prepartion"): 
    st.write('**Encode x (input penguin)**')
    input_row
    st.write('**Encoded y**')
    y 
    
#Model training and inference 
clf = RandomForestClassifier() 
clf.fit(x, y) 

prediction = clf.predict(input_row)
prediction_proba = clf.predict_proba(input_row)

df_prediction_proba = pd.DataFrame(prediction_proba)
df_prediction_proba.columns = ['Adelie', 'Chinstrap', 'Gentoo']

st.subheader('Predicted Species')
st.dataframe(df_prediction_proba, 
             column_config={ 
                'Adelie': st.column_config.ProgressColumn(
                   'Adelie',
                   format='%f',
                   width='medium',
                   min_value =0,
                   max_value =1
                ), 
                'Chinstrap': st.column_config.ProgressColumn(
                    'Chinstrap', 
                    format='%f', 
                    width= 'medium', 
                    min_value = 0,
                    max_value = 1
                ), 
                'Gentoo': st.column_config.ProgressColumn( 
                   'Gentoo',
                   format='%f', 
                   width= 'medium', 
                   min_value = 0,
                   max_value = 1
                ),
                }, hide_index=True) 


penguins_species = np.array(['Adelie', 'Chinstrap', 'Gentoo'])
st.success(str(penguins_species[prediction][0])) 
