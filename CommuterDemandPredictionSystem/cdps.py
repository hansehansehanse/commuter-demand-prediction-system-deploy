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

    # Handle categorical data
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
        'is_saturday',

        # Newly added features
        'is_university_event',
        'is_local_event',
        'is_others',
        'is_local_holiday',
        'is_within_ay',
        'is_start_of_sem',
        'is_day_before_end_of_sem',
        'is_week_before_end_of_sem',
        'is_end_of_sem',
        'is_day_after_end_of_sem',
        'is_2days_after_end_of_sem',
        'is_week_after_end_of_sem'
    ]

    # Only include rows that have all required fields (in case of legacy data)
    df = df.dropna(subset=features + ['num_commuters'])

    X = df[features]
    y = df['num_commuters']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict for next 14 days
    today = datetime.today()
    prediction_dates = [today + timedelta(days=i) for i in range(14)]
    ride_hours = [5, 13, 18]  # 5 AM, 1 PM, 6 PM

    predictions = []

    for date in prediction_dates:
        for hour in ride_hours:
            # Placeholder logic for the new fields – you’ll want to implement real checks later
            date_info = {
                'hour': hour,
                'route_code': 0,
                'month_code': date.month - 1,  # -1 because cat.codes starts from 0
                'day_of_week_code': date.weekday(),
                'is_holiday': 0,
                'is_day_before_holiday': 0,
                'is_day_before_long_weekend': 0,
                'is_friday': 1 if date.weekday() == 4 else 0,
                'is_long_weekend': 0,
                'is_saturday': 1 if date.weekday() == 5 else 0,

                # New fields defaulting to 0 unless actual logic is added
                'is_university_event': 0,
                'is_local_event': 0,
                'is_others': 0,
                'is_local_holiday': 0,
                'is_within_ay': 0,
                'is_start_of_sem': 0,
                'is_day_before_end_of_sem': 0,
                'is_week_before_end_of_sem': 0,
                'is_end_of_sem': 0,
                'is_day_after_end_of_sem': 0,
                'is_2days_after_end_of_sem': 0,
                'is_week_after_end_of_sem': 0
            }

            input_data = pd.DataFrame([date_info])
            predicted_commuters = model.predict(input_data)[0]

            predictions.append({
                'date': date.strftime('%Y-%m-%d'),
                'hour': hour,
                'predicted_commuters': round(predicted_commuters)
            })

    return predictions


#---



