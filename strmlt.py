import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

scaler_x = StandardScaler()

def prepare_data(Train, Test):
    train = pd.read_csv(Train)
    test = pd.read_csv(Test)
    # Training and testing dataset (inputs)
    X_train = train.drop(columns=['fake'])
    X_test = test.drop(columns=['fake'])

    # Training and testing dataset (Outputs)
    y_train = train['fake']
    y_test = test['fake']

    # Scale the data before training the model
    
    X_train = scaler_x.fit_transform(X_train)
    X_test = scaler_x.transform(X_test)

    y_train = tf.keras.utils.to_categorical(y_train, num_classes=2)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes=2)

    return X_train, X_test, y_train, y_test

def build_and_train_model(X_train, y_train):
    model = Sequential()
    model.add(Dense(50, input_dim=11, activation='relu'))
    model.add(Dense(150, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(150, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(25, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(2, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    epochs_hist = model.fit(X_train, y_train, epochs=50, verbose=1, validation_split=0.1)

    return model, epochs_hist

# def show_performance(X_test, y_test, model):
#     predicted = model.predict(X_test)

#     predicted_value = []
#     test = []
#     for i in predicted:
#         predicted_value.append(np.argmax(i))

#     for i in y_test:
#         test.append(np.argmax(i))

#     st.write(classification_report(test, predicted_value))

#     plt.figure(figsize=(10, 10))
#     cm = confusion_matrix(test, predicted_value)
#     sns.heatmap(cm, annot=True)
#     st.pyplot()

#     st.write("Keys in epoch history:", epochs_hist.history.keys())
def predict_fake_account(model):
    # Prepare the input data
    input_data = pd.DataFrame({
        'profile pic': [0],
        'nums/length username': [6],
        'fullname words': [5],
        'nums/length fullname': [4],
        'name==username': [0],
        'description length': [10],
        'external URL': [0],
        'private': [0],
        '#posts': [0],
        '#followers': [1],
        '#follows': [95]
    })
        # Scale the input data using the same scaler
    scaled_input_data = scaler_x.fit_transform(input_data)
    scaled_input_data = scaler_x.transform(input_data)

    model, epochs_hist = build_and_train_model(X_train, y_train)
    # Use the trained model to predict
    predicted_probabilities = model.predict(scaled_input_data)
    predicted_label = np.argmax(predicted_probabilities)

    return predicted_label
# # Streamlit UI
# st.title('Deep Learning Model Training with Streamlit')
# model = tf.keras.Sequential()
# # train_data_path = st.text_input('Enter path to train data CSV file:')
# # test_data_path = st.text_input('Enter path to test data CSV file:')

# if st.button('Train Model'):
#     X_train, X_test, y_train, y_test = prepare_data("train.csv", "test.csv")
#     model, epochs_hist = build_and_train_model(X_train, y_train)
#     # st.write(type(model))
#     st.success('Model training completed successfully!')
    # show_performance(X_test, y_test, model)

# Streamlit UI
st.title('Fake Account Detection')

# Assuming model and scaler_x are already defined and loaded

if st.button('Undergo Check for this account'):
    X_train, X_test, y_train, y_test = prepare_data("train.csv", "test.csv")
    model, epochs_hist = build_and_train_model(X_train, y_train)
    # st.write(type(model))
    st.success('Model training completed successfully!')
    # show_performance(X_test, y_test, model)
    predicted_label = predict_fake_account(model)
    if predicted_label == 0:
        st.write("The algorithm predicts that this account is NOT FAKE. NOTHING TO WORRY.")
    else:
        st.write("The algorithm predicts that this account is FAKE. BE AWARE!!")