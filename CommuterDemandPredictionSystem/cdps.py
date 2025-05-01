# # cdps.py

# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from .models import Dataset
# import pandas as pd

# def train_and_predict_random_forest():
#     # Load all records from the DB
#     data = Dataset.objects.all().values()

#     # Convert to DataFrame
#     df = pd.DataFrame(data)

#     # Ensure correct datetime conversion
#     df['date'] = pd.to_datetime(df['date'])
#     df['hour'] = pd.to_datetime(df['time'].astype(str)).dt.hour

#     # Handle categorical data (convert strings to categories)
#     df['route'] = df['route'].astype('category')
#     df['month'] = df['month'].astype('category')
#     df['day_of_week'] = df['day_of_week'].astype('category')

#     # Convert categories to numeric codes
#     df['route_code'] = df['route'].cat.codes
#     df['month_code'] = df['month'].cat.codes
#     df['day_of_week_code'] = df['day_of_week'].cat.codes

#     # Features and target
#     features = [
#         'hour',
#         'route_code',
#         'month_code',
#         'day_of_week_code',
#         'is_holiday',
#         'is_day_before_holiday',
#         'is_day_before_long_weekend',
#         'is_friday',
#         'is_long_weekend',
#         'is_saturday'
#     ]

#     X = df[features]
#     y = df['num_commuters']

#     # Train/test split
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     # Train model
#     model = RandomForestRegressor(n_estimators=100, random_state=42)
#     model.fit(X_train, y_train)

#     # Define the specific times to predict (5:00 AM, 1:00 PM, 6:00 PM)
#     prediction_times = [5, 13, 18]  # 5:00 AM, 1:00 PM, 6:00 PM
    
#     predictions = []
#     for time in prediction_times:
#         # Example prediction for each of these times
#         prediction_data = {
#             'hour': time,
#             'route_code': df['route_code'].iloc[0],  # Use a sample route code (modify if needed)
#             'month_code': df['month_code'].iloc[0],  # Use a sample month (modify as needed)
#             'day_of_week_code': df['day_of_week_code'].iloc[0],  # Use a sample day (modify if needed)
#             'is_holiday': 0,  # Example value (change based on data)
#             'is_day_before_holiday': 0,  # Example value (change based on data)
#             'is_day_before_long_weekend': 0,  # Example value (change based on data)
#             'is_friday': 0,  # Example value (change based on data)
#             'is_long_weekend': 0,  # Example value (change based on data)
#             'is_saturday': 0,  # Example value (change based on data)
#         }

#         # Convert to DataFrame to match input format for the model
#         prediction_df = pd.DataFrame([prediction_data])

#         # Predict the number of commuters
#         predicted_commuters = model.predict(prediction_df[features])

#         predictions.append({
#             'time': f'{time}:00',  # Time as a string (5:00, 13:00, 18:00)
#             'num_commuters': predicted_commuters[0]
#         })

#     return predictions

# cdps.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
from .models import Dataset


def train_and_predict_random_forest():
    # Load all records from the DB
    data = Dataset.objects.all().values()

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Ensure correct datetime conversion
    df['date'] = pd.to_datetime(df['date'])
    df['hour'] = pd.to_datetime(df['time'].astype(str)).dt.hour

    # Handle categorical data (convert strings to categories)
    df['route'] = df['route'].astype('category')
    df['month'] = df['month'].astype('category')
    df['day_of_week'] = df['day_of_week'].astype('category')

    # Convert categories to numeric codes
    df['route_code'] = df['route'].cat.codes
    df['month_code'] = df['month'].cat.codes
    df['day_of_week_code'] = df['day_of_week'].cat.codes

    # Features and target
    features = [
        'hour',
        'route_code',
        'month_code',
        'day_of_week_code',
        'is_holiday',
        'is_day_before_holiday',
        'is_day_before_long_weekend',
        'is_friday',
        'is_long_weekend',
        'is_saturday'
    ]

    X = df[features]
    y = df['num_commuters']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Get the current date and the next two weeks
    today = datetime.today()
    prediction_dates = [today + timedelta(days=i) for i in range(14)]  # Next 2 weeks

    # Possible ride hours (5:00 AM, 1:00 PM, 6:00 PM)
    ride_hours = [5, 13, 18]

    predictions = []

    # Generate predictions for each day and each ride
    for date in prediction_dates:
        for hour in ride_hours:
            # Prepare the input data for prediction
            date_info = {
                'hour': hour,
                'route_code': 0,  # Assuming route A to B has route_code 0
                'month_code': date.month,
                'day_of_week_code': date.weekday(),
                'is_holiday': 0,  # Modify with actual logic
                'is_day_before_holiday': 0,  # Modify with actual logic
                'is_day_before_long_weekend': 0,  # Modify with actual logic
                'is_friday': 1 if date.weekday() == 4 else 0,  # Check if Friday
                'is_long_weekend': 0,  # Modify with actual logic
                'is_saturday': 1 if date.weekday() == 5 else 0,  # Check if Saturday
            }

            # Convert to a DataFrame for prediction
            input_data = pd.DataFrame([date_info])

            # Make the prediction
            predicted_commuters = model.predict(input_data)[0]

            predictions.append({
                'date': date.strftime('%Y-%m-%d'),
                'hour': hour,
                'predicted_commuters': round(predicted_commuters)
            })

    return predictions

