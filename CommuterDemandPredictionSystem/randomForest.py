# randomForest.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from .models import HistoricalDataset
import numpy as np

def train_random_forest_model():
    # Query the database for the dataset
    queryset = HistoricalDataset.objects.all()  # You can filter by date or other criteria if needed
    
    # Convert queryset to a pandas DataFrame
    data = pd.DataFrame(list(queryset.values('date', 'route', 'time', 'num_commuters', 
                                              'is_holiday', 'is_friday', 'is_saturday', 
                                              'is_local_event', 'is_others', 'is_flagged')))  
    
    # Perform feature engineering (if needed)
    data['hour'] = data['time'].apply(lambda x: x.hour)
    data['day_of_week'] = data['date'].apply(lambda x: x.weekday())
    
    # Features (independent variables)
    X = data[['hour', 'day_of_week', 'is_holiday', 'is_friday', 'is_saturday', 
              'is_local_event', 'is_others', 'is_flagged']]

    # Target (dependent variable)
    y = data['num_commuters']
    
    # Split the dataset into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)

    # Manually compute RMSE
    rmse = np.sqrt(mse)
    
    # Calculate Mean Absolute Error
    mae = mean_absolute_error(y_test, y_pred)
    
    # Save the model and evaluation results
    save_model_and_results(model, rmse, mae)
    
    return rmse, mae

def save_model_and_results(model, rmse, mae):
    import joblib
    import os
    from datetime import datetime
    
    # Directory to save model and results
    model_dir = os.path.join(os.path.dirname(__file__), 'model')
    os.makedirs(model_dir, exist_ok=True)
    
    # Save the trained model
    model_filename = os.path.join(model_dir, 'random_forest_model.pkl')
    joblib.dump(model, model_filename)
    
    # Save the evaluation results in a text file
    results_filename = os.path.join(model_dir, 'model_results.txt')
    with open(results_filename, 'w') as f:
        f.write(f"Random Forest Model Evaluation Results\n")
        f.write(f"RMSE: {rmse:.2f}\n")
        f.write(f"MAE: {mae:.2f}\n")
        f.write(f"Date of Training: {datetime.now()}\n")
