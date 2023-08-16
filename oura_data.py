import requests
import shutil
import pandas as pd
import os
from dotenv import load_dotenv


# Load api from dotenv
load_dotenv()

# Define API endpoints and headers
url_daily_activity = 'https://api.ouraring.com/v2/usercollection/daily_activity'
url_daily_readiness = 'https://api.ouraring.com/v2/usercollection/daily_readiness'
url_daily_sleep = 'https://api.ouraring.com/v2/usercollection/sleep'

# Folder for saving
folder_path = 'data/csv'


# Get API key from user
oura_api_key = os.getenv("OURA_API_KEY") #input("Enter your Oura API key: ")
headers = {
    'Authorization': f'Bearer {oura_api_key}'
}
params = {
    'start_date': '2023-06-02',
    'end_date': '2023-07-03'
}

# Define column names
activity_column_names = ["Activity ID", "Activity Day", "Activity Score", "Active Calories", "Resting Time", "Steps"]
readiness_column_names = ["Readiness Level ID", "Day", "Score", "Temperature Deviation", "Temperature Trend Deviation", "Activity Balance", "Body Temperature", 
                          "HRV Balance", "Previous Day Activity", "Previous Night", "Recovery Index", "Resting Heart Rate", "Sleep Balance"]
sleep_column_names = ["Sleep Info ID", "Day", "Average Heart Rate", "Deep Sleep Duration", "Efficiency", "Latency", "Light Sleep Duration", "Lowest Heart Rate", 
                      "Restless Periods", "Bedtime End", "Bedtime Start" , "Movement 30 Sec", "Period", "Readiness Score Delta", 
                        "REM Sleep Duration", "Sleep Phase 5 Min", "Sleep Score Delta", "Time in Bed", "Total Sleep Duration", "Type"]

# Function to fetch and return activity info
def fetch_and_return_activity_info():
    response_daily_activity = requests.request("GET", url_daily_activity, headers=headers, params=params)
    if response_daily_activity.status_code == 200:
        activity_data = response_daily_activity.json()['data']
        activity_df = pd.DataFrame(columns=activity_column_names)
        for day_values in activity_data:
            activity_df = activity_df.append({
                "Activity ID": day_values["id"],
                "Activity Day": day_values['day'],
                "Activity Score": day_values['score'],
                "Active Calories": day_values['active_calories'],
                "Resting Time": day_values['resting_time'],
                "Steps": day_values['steps']
            }, ignore_index=True)
        activity_df.to_csv(folder_path + '/activity_data.csv', index=False)
        print("Activity data saved to CSV")

# Function to fetch and return readiness info
def fetch_and_return_readiness_info():
    response_daily_readiness = requests.request("GET", url_daily_readiness, headers=headers, params=params)
    if response_daily_readiness.status_code == 200:
        readiness_data = response_daily_readiness.json()['data']
        readiness_df = pd.DataFrame(columns=readiness_column_names)
        for day_values in readiness_data:
            readiness_df = readiness_df.append({
                "Readiness Level ID": day_values['id'],
                "Day": day_values['day'],
                "Score": day_values['score'],
                "Temperature Deviation": day_values['temperature_deviation'],
                "Temperature Trend Deviation": day_values['temperature_trend_deviation'],
                "Timestamp":day_values["timestamp"],
                "Activity Balance": day_values['contributors'].get('activity_balance', 0),
                "Body Temperature": day_values['contributors'].get('body_temperature', 0),
                "HRV Balance": day_values['contributors'].get('hrv_balance', 0),
                "Previous Day Activity": day_values['contributors'].get('previous_day_activity', 0),
                "Previous Night": day_values['contributors'].get('previous_night', 0),
                "Recovery Index": day_values['contributors'].get('recovery_index', 0),
                "Resting Heart Rate": day_values['contributors'].get('resting_heart_rate', 0),
                "Sleep Balance": day_values['contributors'].get('sleep_balance', 0)
            }, ignore_index=True)
        readiness_df.to_csv(folder_path + '/readiness_data.csv', index=False)
        print("Readiness data saved to CSV")

# Function to fetch and return sleep info
def fetch_and_return_sleep_info():
    response_daily_sleep = requests.get(url_daily_sleep, headers=headers, params=params)
    if response_daily_sleep.status_code == 200:
        sleep_data = response_daily_sleep.json()['data']
        sleep_df = pd.DataFrame(columns=sleep_column_names)
        for day_values in sleep_data:
            sleep_df = sleep_df.append({
                "Sleep Info ID": day_values['id'],
                "Day": day_values['day'],
                "Average Heart Rate": day_values['average_heart_rate'],
                "Deep Sleep Duration": day_values['deep_sleep_duration'],
                "Efficiency": day_values['efficiency'],
                "Latency": day_values['latency'],
                "Light Sleep Duration": day_values['light_sleep_duration'],
                "Lowest Heart Rate": day_values['lowest_heart_rate'],
                "Restless Periods": day_values['restless_periods'],
                "Bedtime End": day_values['bedtime_end'],
                "Bedtime Start": day_values['bedtime_start'],
                # "Heart Rate Interval": day_values['heart_rate'].get('interval',None),
                "Movement 30 Sec": day_values['movement_30_sec'],
                "Period": day_values['period'],
                "Readiness Score Delta": day_values['readiness_score_delta'],
                "REM Sleep Duration": day_values['rem_sleep_duration'],
                "Sleep Phase 5 Min": day_values['sleep_phase_5_min'],
                "Sleep Score Delta": day_values['sleep_score_delta'],
                "Time in Bed": day_values['time_in_bed'],
                "Total Sleep Duration": day_values['total_sleep_duration'],
                "Type": day_values['type']
            }, ignore_index=True)
        sleep_df.to_csv(folder_path + '/sleep_data.csv', index=False)
        print("Sleep data saved to CSV")

def create_csv_files():
    #check if folder exists
    if os.path.exists(folder_path):
        overwrite = input("Folder already exists do you want to override? (y/n): ")
        if overwrite.lower() == 'y':
            shutil.rmtree(folder_path)
        else:
            print("Folder were not override exiting...")
            return
    else:
        os.makedirs(folder_path)
    fetch_and_return_activity_info()
    fetch_and_return_readiness_info()
    fetch_and_return_sleep_info()
    print("All data saved to CSV files")

if __name__ == "__main__":
    create_csv_files()
