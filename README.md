# Visualizing Team 888 Attendance Data

This is a Streamlit web app for visualizing attendance/hour logging data from a Firebase Realtime DB. The web app will
update in real time, thus all the statistics should be up-to-date.

## Usage

To run this on your local machine:
```commandline
git clone https://github.com/KevinH45/VisualizingAttendance.git
streamlit run PATH/TO/MAIN
```

You will need to update the credentials for Firebase.


## Deploying on Streamlit Cloud

Follow these directions:
- Sign up for Streamlit Cloud
- Fork this repository
- Format your Firebase credentials into TOML format
- Create a new app and fill out necessary information
- Go to advanced settings and enter the formatted credentials into the secrets TOML file
- Deploy!

