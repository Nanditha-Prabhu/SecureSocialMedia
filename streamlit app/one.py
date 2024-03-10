import streamlit as st
import pandas as pd
import numpy as np

import streamlit as st

tabs = st.sidebar.radio("Select Tab", ["Fake Account Detection", "Trustworthiness"])

# Main app content
st.markdown('<h1 style = "color : #0079B1;text-decoration: underline; font-size : 46px; text-align: center;font-family: Courier New">Are We Sure??</h1>', unsafe_allow_html = True)
if tabs=="Fake Account Detection":
    import streamlit as st
    import pandas as pd
    import numpy as np
    import tensorflow as tf
    from sklearn.preprocessing import StandardScaler
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout
    from sklearn.metrics import classification_report, confusion_matrix
    import matplotlib.pyplot as plt
   

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
            st.write("The algorithm predicts that this account is FAKE. BE AWARE!!")
        
        
        
        
elif tabs == "Trustworthiness":
    import streamlit as st
    def trust():    
        import pandas as pd
        import numpy as np

        # Load train and test datasets
        train_data_path = 'train.csv'
        test_data_path = 'test.csv'

        # Load the training dataset
        train = pd.read_csv(train_data_path)

        # Load the testing dataset
        test = pd.read_csv(test_data_path)

        # Define weights for each attribute
        weights = {
        'profile pic':0.8,
        'nums/length username':0.4,
        'fullname words':0.8,
        'nums/length fullname':0.8,
        'name==username':0.6,
        'description length':0.2,
        'external URL':0.05,
        'private':0.05,
        '#posts':0.8,
        '#followers':0.8,
        '#follows':0.1,
        'fake':0.9
        }
        def calculate_trustworthiness_score(row):
            trustworthiness_score = sum(row[attr] * weights[attr] for attr in weights.keys())
            return trustworthiness_score

        # Calculate Trustworthiness Score for each user in train dataset
        train['trustworthiness_score'] = train.apply(calculate_trustworthiness_score, axis=1)

        # Calculate Trustworthiness Score for each user in test dataset
        test['trustworthiness_score'] = test.apply(calculate_trustworthiness_score, axis=1)
        import pandas as pd

        # Define weights for each attribute
        weights = {
        'profile pic':0.8,
        'nums/length username':0.4,
        'fullname words':0.8,
        'nums/length fullname':0.8,
        'name==username':0.6,
        'description length':0.2,
        'external URL':0.05,
        'private':0.05,
        '#posts':0.8,
        '#followers':0.8,
        '#follows':0.1,
        'fake':0.9# Importance of number of accounts followed
        }

        # Load your dataset
        data = pd.read_csv("train.csv")

        # Normalize the features (assuming Min-Max normalization)
        normalized_data = (data - data.min()) / (data.max() - data.min())

        # Apply the weights to each feature
        weighted_data = normalized_data.copy()
        for feature in weights:
            weighted_data[feature] *= weights[feature]
        # Calculate trustworthiness score for each instance
        trustworthiness_scores = weighted_data.sum(axis=1)
        # Adjust trustworthiness score based on the 'fake' attribute
        trustworthiness_scores = trustworthiness_scores - (data['fake'] * 10)
        # Scale trustworthiness scores to range from 0 to 100
        scaled_trustworthiness_scores = (trustworthiness_scores * 100).astype(int)
        # Clip scores to be within the range of 0 to 100
        scaled_trustworthiness_scores = scaled_trustworthiness_scores.clip(0, 100)
        import pandas as pd
        from sklearn.discriminant_analysis import StandardScaler
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.metrics import mean_squared_error
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression

        # Load your dataset
        data = pd.read_csv("train.csv")

        # Define weights for each attribute
        weights = {
            'profile pic': 0.8,
            'nums/length username': 0.4,
            'fullname words': 0.8,
            'nums/length fullname': 0.8,
            'name==username': 0.6,
            'description length': 0.2,
            'external URL': 0.05,
            'private': 0.05,
            '#posts': 0.8,
            '#followers': 0.8,
            '#follows': 0.1,
            'fake': 0.9
        }

        # Normalize the features (assuming Min-Max normalization)
        normalized_data = (data - data.min()) / (data.max() - data.min())

        # Apply the weights to each feature
        weighted_data = normalized_data.copy()
        for feature in weights:
            weighted_data[feature] *= weights[feature]

        # Calculate trustworthiness score for each instance
        trustworthiness_scores = weighted_data.sum(axis=1)

        # Adjust trustworthiness score based on the 'fake' attribute
        trustworthiness_scores = trustworthiness_scores - (data['fake'] * 10)

        # Scale trustworthiness scores to range from 0 to 100
        scaled_trustworthiness_scores = (trustworthiness_scores * 100).astype(int)

        # Clip scores to be within the range of 0 to 100
        scaled_trustworthiness_scores = scaled_trustworthiness_scores.clip(0, 100)

        # Add the scaled trustworthiness scores column to the dataset
        data['scaled_trustworthiness_scores'] = scaled_trustworthiness_scores
        import tensorflow as tf
        X_train = data.drop(columns = ['scaled_trustworthiness_scores'])
        X_test = data.drop(columns = ['scaled_trustworthiness_scores'])

        print(X_train,X_test)
        # Training and testing dataset (Outputs)
        y_train = data['scaled_trustworthiness_scores']
        y_test = data['scaled_trustworthiness_scores']

        
        # Scale the data before training the model
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        # Initialize the Random Forest Regressor model
        model = RandomForestRegressor(random_state=42)
        # Train the model
        model.fit(X_train, y_train)
        # Make predictions on the test set
        y_pred = model.predict(X_test)
        # Calculate the Mean Squared Error (MSE) of the predictions
        mse = mean_squared_error(y_test, y_pred)
        import tensorflow.keras
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Dropout

        # Define the model
        model = Sequential()
        model.add(Dense(50, input_dim=12, activation='relu'))  # Adjust input_dim to 12
        model.add(Dense(150, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(150, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(25, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(2, activation='softmax'))

        # Compile the model
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
        # 1. Prepare your input data
        input_data = pd.DataFrame({
        'profile pic': [1],
        'nums/length username': [12],
        'fullname words': [15],
        'nums/length fullname': [12],
        'name==username': [0],
        'description length': [53],
        'external URL': [0],
        'private': [0],
        '#posts': [50],
        '#followers': [1000],
        '#follows': [95],
        'fake': [0]
        
        })
        from sklearn.preprocessing import StandardScaler


    # 2. Scale the input data using the same scaler
        scaled_input_data = scaler.transform(input_data)

    # 3. Use the trained model to predict the trustworthiness score
        trustworthiness_score = model.predict(scaled_input_data)


        return trustworthiness_score[0][0]*100

    st.markdown("<h2 style='text-align: center;'>The Trustworthiness Calculated : </h2>", unsafe_allow_html=True)
    import plotly.graph_objs as go

    # Define gauge parameters
    min_value = 0
    max_value = 100
    target_value = trust()

    # Create the gauge trace
    import plotly.graph_objs as go

    # Define gauge parameters
    min_value = 0
    max_value = 100
    target_value = trust()

    # Create the gauge trace
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=target_value,
        mode="gauge+number",
        gauge={
            'shape': "angular",  # Use bullet shape for a rounded gauge
            'bgcolor': 'rgba(255, 255, 255, 0)',  # Transparent background
            'borderwidth': 2,
            'bordercolor': "gray",
            'axis': {'range': [min_value, max_value], 'tickwidth': 2, 'tickcolor': "gray", 'showticklabels': False},  # Customized axis
            'steps': [
                {'range': [min_value, 25], 'color': "rgba(255, 99, 71, 0.5)"},  # Red gradient
                {'range': [25, 50], 'color': "rgba(255, 165, 0, 0.5)"},  # Orange gradient
                {'range': [50, 75], 'color': "rgba(255, 255, 0, 0.5)"},  # Yellow gradient
                {'range': [75, max_value], 'color': "rgba(144, 238, 144, 0.5)"}  # Green gradient
            ],
            'threshold': {
                'line': {'color': "gray", 'width': 4}  # Black needle at target value
            }
        }
    ))

    # Remove extra space around the gauge
    fig.update_layout(margin={'t': 0, 'b': 0, 'l': 0, 'r': 0})



    st.plotly_chart(fig)

