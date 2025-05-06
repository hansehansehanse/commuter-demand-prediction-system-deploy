# Inside cdps.py (or wherever you define prediction functions)

from datetime import datetime
import pandas as pd
from .models import Dataset
from sklearn.ensemble import RandomForestRegressor

def train_and_predict_random_forest_single(route, time_str, date_str):
    data = Dataset.objects.all().values()
    df = pd.DataFrame(data)

    df['date'] = pd.to_datetime(df['date'])
    # df['hour'] = pd.to_datetime(df['time'].astype(str)).dt.hour
    df['hour'] = pd.to_datetime(df['time'].astype(str), format="%H:%M:%S", errors='coerce').dt.hour

    df['route'] = df['route'].astype('category')
    df['month'] = df['month'].astype('category')
    df['day_of_week'] = df['day_of_week'].astype('category')

    df['route_code'] = df['route'].cat.codes
    df['month_code'] = df['month'].cat.codes
    df['day_of_week_code'] = df['day_of_week'].cat.codes

    X = df[[
        'hour', 'route_code', 'month_code', 'day_of_week_code',
        'is_holiday', 'is_day_before_holiday', 'is_day_before_long_weekend',
        'is_friday', 'is_long_weekend', 'is_saturday'
    ]]
    y = df['num_commuters']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # selected_date = datetime.strptime(date_str, "%Y-%m-%d")
    # selected_time = datetime.strptime(time_str, "%I:%M%p")
    selected_date = date_str  # Already a datetime.date
    selected_time = time_str  # Already a datetime.time


    route_code = df[df['route'] == route]['route_code'].iloc[0]

    input_data = pd.DataFrame([{
        'hour': selected_time.hour,
        'route_code': route_code,
        'month_code': selected_date.month,
        'day_of_week_code': selected_date.weekday(),
        'is_holiday': 0,
        'is_day_before_holiday': 0,
        'is_day_before_long_weekend': 0,
        'is_friday': 1 if selected_date.weekday() == 4 else 0,
        'is_long_weekend': 0,
        'is_saturday': 1 if selected_date.weekday() == 5 else 0
    }])

    prediction = model.predict(input_data)[0]
    return prediction


