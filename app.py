import streamlit as st
import numpy as np

model = np.load('weight.npz')
x_mean = model['x_mean']
x_std = model['x_std']
theta = model['theta']


@st.cache_resource
# Define the prediction function
def predict(carat, cut, color, clarity, depth, table, x, y, z, x_mean, x_std, theta):
    # Mapping for cut
    cut_mapping = {'Fair': 0, 'Good': 1,
                   'Ideal': 2, 'Premium': 3, 'Very Good': 4}
    # Mapping for color
    color_mapping = {'E': 0, 'G': 1, 'F': 2, 'I': 3, 'D': 4, 'J': 5, 'H': 6}
    # Mapping for clarity
    clarity_mapping = {'VVS1': 0, 'VVS2': 1, 'I1': 2,
                       'VS1': 3, 'VS2': 4, 'IF': 5, 'SI1': 6, 'SI2': 7, }

    # Transform the categorical variables to numerical values
    cut = cut_mapping.get(cut, 0)
    color = color_mapping.get(color, 0)
    clarity = clarity_mapping.get(clarity, 0)

    input = np.array(
        [[carat, cut, color, clarity, depth, table, x, y, z]], dtype='float')
    input = (input - x_mean)/x_std
    b = np.array([[1.0]])
    input = np.concatenate((b, input), axis=1)
    prediction = input.dot(theta)
    return prediction


# Add title for my app
st.title('💎DIAMOND PRICE PREDICTION💎')

st.header('Vui long nhap cac dac trung cua vien kim cuong ma ban muon mua: ')
carat = st.number_input('Carat weight:', min_value=0.1,
                        max_value=10.0, value=1.0)
cut = st.selectbox(
    'Cut rating:', ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'])
color = st.selectbox('Color rating:', ['J', 'I', 'H', 'G', 'F', 'E', 'D'])
clarity = st.selectbox('Clarity rating:', [
                       'VVS1', 'VVS2', 'I1', 'VS1', 'VS2', 'IF', 'SI1', 'SI2'])
depth = st.number_input('Diamond depth percentage:',
                        min_value=0.1, max_value=100.0, value=1.0)
table = st.number_input('Diamond table percentage:',
                        min_value=0.1, max_value=100.0, value=1.0)
x = st.number_input('Diamond Length (X) in mm:',
                    min_value=0.1, max_value=100.0, value=1.0)
y = st.number_input('Diamond width (Y) in mm:',
                    min_value=0.1, max_value=100.0, value=1.0)
z = st.number_input('Diamond height (Z) in mm:',
                    min_value=0.1, max_value=100.0, value=1.0)
if st.button('Predict Price'):
    out = predict(carat, cut, color, clarity, depth,
                  table, x, y, z, x_mean, x_std, theta)
    st.success(f'Gia du doan cua vien kim cuong la: ${out[0, 0]:.2f} USD')
