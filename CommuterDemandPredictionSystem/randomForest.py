# randomForest.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from .models import HistoricalDataset
import numpy as np

# def train_random_forest_model():
#     # Query the database for the dataset
#     queryset = HistoricalDataset.objects.all()  # You can filter by date or other criteria if needed
    
#     # Convert queryset to a pandas DataFrame
#     data = pd.DataFrame(list(queryset.values('date', 'route', 'time', 'num_commuters', 
#                                               'is_holiday', 'is_friday', 'is_saturday', 
#                                               'is_local_event', 'is_others', 'is_flagged')))  
    
#     # Perform feature engineering (if needed)
#     data['hour'] = data['time'].apply(lambda x: x.hour)
#     data['day_of_week'] = data['date'].apply(lambda x: x.weekday())
    
#     # Features (independent variables)
#     X = data[['hour', 'day_of_week', 'is_holiday', 'is_friday', 'is_saturday', 
#               'is_local_event', 'is_others', 'is_flagged']]

#     # Target (dependent variable)
#     y = data['num_commuters']
    
#     # Split the dataset into training and testing sets (80% train, 20% test)
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
#     # Train the model
#     model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
#     model.fit(X_train, y_train)
    
#     # Make predictions
#     y_pred = model.predict(X_test)
    
#     # Calculate Mean Squared Error
#     mse = mean_squared_error(y_test, y_pred)

#     # Manually compute RMSE
#     rmse = np.sqrt(mse)
    
#     # Calculate Mean Absolute Error
#     mae = mean_absolute_error(y_test, y_pred)
    
#     # Save the model and evaluation results
#     save_model_and_results(model, rmse, mae)
    
#     return rmse, mae


# def train_random_forest_model():
#     queryset = HistoricalDataset.objects.all()
#     data = pd.DataFrame(list(queryset.values()))

#     # Feature engineering
#     data['hour'] = data['time'].apply(lambda x: x.hour)
#     data['day_of_week'] = data['date'].apply(lambda x: x.weekday())

#     features_to_use = [
#         'day_of_week', 'is_holiday', 'is_friday', 'is_saturday', 'is_local_event',
#         'is_others', 'is_flagged', 'is_day_before_holiday', 'is_long_weekend', 
#         'is_day_before_long_weekend', 'is_end_of_sem', 'is_day_before_end_of_sem', 
#         'is_day_after_end_of_sem', 'is_2days_after_end_of_sem', 'is_local_holiday', 
#         'is_start_of_sem', 'is_week_after_end_of_sem', 'is_week_before_end_of_sem', 
#         'is_within_ay'
#     ]


#     X = data[features_to_use]
#     y = data['num_commuters']

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
#     model.fit(X_train, y_train)

#     # Evaluate
#     y_pred = model.predict(X_test)
#     mse = mean_squared_error(y_test, y_pred)
#     rmse = np.sqrt(mse)
#     mae = mean_absolute_error(y_test, y_pred)

#     # Save the model
#     save_model_and_results(model, rmse, mae)
#     return model

####################

# def train_random_forest_model():
#     queryset = HistoricalDataset.objects.all()
#     data = pd.DataFrame(list(queryset.values()))

#     # Feature engineering
#     data['hour'] = data['time'].apply(lambda x: x.hour)
#     data['day_of_week'] = data['date'].apply(lambda x: x.weekday())

#     # Ensure 'num_commuters' column exists and doesn't have missing values
#     if 'num_commuters' not in data.columns:
#         print("❌ 'num_commuters' column is missing")
#         return None
    
#     # Check for any missing values
#     if data.isnull().any().any():
#         print("❌ Data contains missing values. Here's the summary of missing values:")
#         print(data.isnull().sum())
#         return None

#     features_to_use = [
#         'day_of_week', 'is_holiday', 'is_friday', 'is_saturday', 'is_local_event',
#         'is_others', 'is_flagged', 'is_day_before_holiday', 'is_long_weekend', 
#         'is_day_before_long_weekend', 'is_end_of_sem', 'is_day_before_end_of_sem', 
#         'is_day_after_end_of_sem', 'is_2days_after_end_of_sem', 'is_local_holiday', 
#         'is_start_of_sem', 'is_week_after_end_of_sem', 'is_week_before_end_of_sem', 
#         'is_within_ay'
#     ]

#     # Ensure all features exist in the dataset
#     missing_features = [feature for feature in features_to_use if feature not in data.columns]
#     if missing_features:
#         print(f"❌ Missing features in data: {missing_features}")
#         return None

#     X = data[features_to_use]
#     y = data['num_commuters']

#     # Split data
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     # Train the model
#     model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
#     model.fit(X_train, y_train)

#     # Evaluate
#     y_pred = model.predict(X_test)
#     mse = mean_squared_error(y_test, y_pred)
#     rmse = np.sqrt(mse)
#     mae = mean_absolute_error(y_test, y_pred)

#     # Save the model and results
#     save_model_and_results(model, rmse, mae)

#     return model



# import joblib
# import os
# from datetime import datetime

# def save_model_and_results(model, rmse, mae):
    
#     # Directory to save model and results
#     model_dir = os.path.join(os.path.dirname(__file__), 'model')
#     os.makedirs(model_dir, exist_ok=True)
    
#     # Save the trained model
#     model_filename = os.path.join(model_dir, 'random_forest_model.pkl')
#     joblib.dump(model, model_filename)
    
#     # Save the evaluation results in a text file
#     results_filename = os.path.join(model_dir, 'model_results.txt')
#     print("-------------------------------Successfully saved the model and results.")
#     with open(results_filename, 'w') as f:
#         f.write(f"Random Forest Model Evaluation Results\n")
#         f.write(f"RMSE: {rmse:.2f}\n")
#         f.write(f"MAE: {mae:.2f}\n")
#         f.write(f"Date of Training: {datetime.now()}\n")

import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from .models import HistoricalDataset  # adjust import if needed

def train_random_forest_model():
    queryset = HistoricalDataset.objects.all()
    data = pd.DataFrame(list(queryset.values()))

    # Feature engineering
    data['hour'] = data['time'].apply(lambda x: x.hour)
    data['day_of_week'] = data['date'].apply(lambda x: x.weekday())

    # Ensure 'num_commuters' column exists and doesn't have missing values
    if 'num_commuters' not in data.columns:
        print("❌ 'num_commuters' column is missing")
        return None
    
    # Check for any missing values
    if data.isnull().any().any():
        print("❌ Data contains missing values. Here's the summary of missing values:")
        print(data.isnull().sum())
        return None

    features_to_use = [
        'day_of_week', 'is_holiday', 'is_friday', 'is_saturday', 'is_local_event',
        'is_others', 'is_flagged', 'is_day_before_holiday', 'is_long_weekend', 
        'is_day_before_long_weekend', 'is_end_of_sem', 'is_day_before_end_of_sem', 
        'is_day_after_end_of_sem', 'is_2days_after_end_of_sem', 'is_local_holiday', 
        'is_start_of_sem', 'is_week_after_end_of_sem', 'is_week_before_end_of_sem', 
        'is_within_ay'
    ]

    # Check all required features are present
    missing_features = [feature for feature in features_to_use if feature not in data.columns]
    if missing_features:
        print(f"❌ Missing features in data: {missing_features}")
        return None

    X = data[features_to_use]
    y = data['num_commuters']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)

    # Save model and metadata
    save_model_and_results(model, rmse, mae, features_to_use)

    return model


def save_model_and_results(model, rmse, mae, features_to_use):
    model_dir = os.path.join(os.path.dirname(__file__), 'model')
    os.makedirs(model_dir, exist_ok=True)

    # Save model
    model_path = os.path.join(model_dir, 'random_forest_model.pkl')
    joblib.dump(model, model_path)

    # Save features used during training
    features_path = os.path.join(model_dir, 'features_used.pkl')
    joblib.dump(features_to_use, features_path)

    # Save metrics
    results_path = os.path.join(model_dir, 'model_results.txt')
    with open(results_path, 'w') as f:
        f.write("Random Forest Model Evaluation Results\n")
        f.write(f"RMSE: {rmse:.2f}\n")
        f.write(f"MAE: {mae:.2f}\n")
        f.write(f"Date of Training: {datetime.now()}\n")

    print("✅ Successfully saved model, features, and evaluation results.")
