import requests
import csv
import pandas as pd

# Define API endpoints
url_daily_activity = 'https://api.ouraring.com/v2/usercollection/daily_activity'
url_personal_info = 'https://api.ouraring.com/v2/usercollection/personal_info'
url_daily_readiness = 'https://api.ouraring.com/v2/usercollection/daily_readiness'
url_sleep = 'https://api.ouraring.com/v2/usercollection/sleep'
url_daily_sleep = 'https://api.ouraring.com/v2/usercollection/daily_sleep'
url_session = 'https://api.ouraring.com/v2/usercollection/session'

# Define user headers and params such as date
headers = {
    'Authorization': 'Bearer PHJQUPJUO7X3OQERAOHEXC3FT4V4QY5Z'
}

params = {
    'start_date': '2023-01-02',
    'end_date': '2023-01-04'
}


column_names = ("Personal ID", "Email", "Age", "Weight", "Height", "Sex", "Activity ID", "Activity Day", "Activity Score", "Active Calories", "Resting Time", "Steps",
                         "Readiness Level ID", "Day", "Score", "Temperature Deviation", "Temperature Trend Deviation", "Activity Balance", "Body Temperature", "HRV Balance", 
                         "Previous Day Activity", "Previous Night", "Recovery Index", "Resting Heart Rate", "Sleep Balance",
                         "Sleep Info ID", "Day", "Average Heart Rate", "Deep Sleep Duration", "Efficiency", "Latency", "Light Sleep Duration", "Lowest Heart Rate", "Restless Periods",
                         "Bedtime End", "Bedtime Start", "Heart Rate Interval", "Movement 30 Sec", "Period", "Readiness Score Delta", "REM Sleep Duration", "Sleep Phase 5 Min", 
                         "Sleep Score Delta", "Time in Bed", "Total Sleep Duration", "Type")

df = pd.DataFrame(columns=column_names)

# Function to fetch personal info
def fetch_personal_info(day):
    date = {'start_date': day, 'end_date': day}
    response_personal_info = requests.request("GET",url_personal_info, headers=headers, params=date)
    personal_info = response_personal_info.json()
    return personal_info

# Function to fetch and print activity info
def fetch_and_return_activity_info():
    response_daily_activity = requests.request("GET",url_daily_activity, headers=headers, params=params)
    
    if response_daily_activity.status_code == 200:
        activity_data = response_daily_activity.json()['data']
        
        
        for day_values in activity_data:
            user_activity_id = day_values["id"]
            day = day_values['day']
            score = day_values['score']
            active_calories = day_values['active_calories']
            resting_time = day_values['resting_time']
            steps = day_values['steps']
            
            personal_info = fetch_personal_info(day)
            user_personal_id = personal_info['id']
            age = personal_info['age']
            email = personal_info['email']
            weight = personal_info['weight']
            height = personal_info['height']
            sex = personal_info['biological_sex']
            
            df = df.append({
                "Personal ID":user_personal_id,
                "Email": email,
                "Age": age,
                "Height":height,
                "Weight":weight,
                "Sex":sex,
                "Activity ID": user_activity_id,
                "Day":day,
                "Activity Score": score,
                "Active Calories": active_calories,
                "Resting Time": resting_time,
                "Steps":steps
            })
    else:
        print("Request failed with status code:", response_daily_activity.status_code)


# Function to fetch and return readiness info
def fetch_and_return_readiness_info():
    response_daily_readiness = requests.request("GET", url_daily_readiness, headers=headers, params=params)
    
    if response_daily_readiness.status_code == 200:
        readiness_data = response_daily_readiness.json()['data']

        for day_values in readiness_data:
            id = day_values['id']
            day = day_values['day']
            score = day_values['score']
            temp_deviation = day_values['temperature_deviation']
            temp_trend_deviation = day_values['temperature_trend_deviation']
            
            # Selected contributors
            contributors = day_values['contributors']
            activity_balance = contributors.get('activity_balance', 0)
            body_temperature = contributors.get('body_temperature', 0)
            hrv_balance = contributors.get('hrv_balance', 0)
            previous_day_activity = contributors.get('previous_day_activity', 0)
            previous_night = contributors.get('previous_night', 0)
            recovery_index = contributors.get('recovery_index', 0)
            resting_heart_rate = contributors.get('resting_heart_rate', 0)
            sleep_balance = contributors.get('sleep_balance', 0)
            
            df = df.append({
                "Readiness Level ID": id,
                "Day": day,
                "Readiness Score": score,
                "Temperature Deviation": temp_deviation,
                "Temperature Trend Deviation": temp_trend_deviation,
                "Activity Balance": activity_balance,
                "Body Temperature": body_temperature,
                "HRV Balance": hrv_balance,
                "Previous Day Activity": previous_day_activity,
                "Previous Night": previous_night,
                "Recovery Index": recovery_index,
                "Resting Heart Rate": resting_heart_rate,
                "Sleep Balance": sleep_balance
            })
    else:
        print("Request failed with status code:", response_daily_readiness.status_code)

# Function to fetch and return sleep info
def fetch_and_return_sleep_info():
    response_daily_sleep = requests.get(url_sleep, headers=headers, params=params)
    
    if response_daily_sleep.status_code == 200:
        sleep_data = response_daily_sleep.json()['data']
        
        for day_values in sleep_data:
            id = day_values['id']
            day = day_values['day']
            average_heart_rate = day_values['average_heart_rate']
            deep_sleep_duration = day_values['deep_sleep_duration']
            efficiency = day_values['efficiency']
            latency = day_values['latency']
            light_sleep_duration = day_values['light_sleep_duration']
            lowest_heart_rate = day_values['lowest_heart_rate']
            restless_periods = day_values['restless_periods']
            time_in_bed = day_values['time_in_bed']
            total_sleep_duration = day_values['total_sleep_duration']
            
            bedtime_end = day_values['bedtime_end']
            bedtime_start = day_values['bedtime_start']
            
            heart_rate_interval = day_values['heart_rate']['interval']
            movement_30_sec = day_values['movement_30_sec']
            period = day_values['period']
            
            readiness_score_delta = day_values['readiness_score_delta']
            rem_sleep_duration = day_values['rem_sleep_duration']
            sleep_phase_5_min = day_values['sleep_phase_5_min']
            sleep_score_delta = day_values['sleep_score_delta']
            
            sleep_type = day_values['type']
            
            df = df.append({
                "Sleep Info ID": id,
                "Day": day,
                "Average Heart Rate": average_heart_rate,
                "Deep Sleep Duration": deep_sleep_duration,
                "Efficiency": efficiency,
                "Latency": latency,
                "Light Sleep Duration": light_sleep_duration,
                "Lowest Heart Rate": lowest_heart_rate,
                "Restless Periods": restless_periods,
                "Bedtime End": bedtime_end,
                "Bedtime Start": bedtime_start,
                "Heart Rate Interval": heart_rate_interval,
                "Movement 30 Sec": movement_30_sec,
                "Period": period,
                "Readiness Score Delta": readiness_score_delta,
                "REM Sleep Duration": rem_sleep_duration,
                "Sleep Phase 5 Min": sleep_phase_5_min,
                "Sleep Score Delta": sleep_score_delta,
                "Time in Bed": time_in_bed,
                "Total Sleep Duration": total_sleep_duration,
                "Type": sleep_type
            })
    else:
        print("Request failed with status code:", response_daily_sleep.status_code)

fetch_and_return_activity_info()
fetch_and_return_readiness_info()
fetch_and_return_sleep_info()

#Opening csv file
with open('oura_info.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(df.to_csv())
print("Data saved to oura_info.csv")