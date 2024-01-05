import streamlit as st
import pickle
import pandas as pd
import numpy as np
import sklearn
import plotly.express as px
import xgboost
import joblib
import math
import datetime

# layout
st.set_page_config(page_title="Predict Air Flight Tickets Price", layout="wide")
df = pd.read_csv("clean_data.csv")
df_min_max_duration = pd.read_csv("min_max_duration.csv")

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2.3, 0.1, 1.3, 0.1)
)

with row0_1:
    st.title("Prediction ticket Price")
    st.markdown(
        """ <h6>
                    You will be book flight ticket from city to city in india , predict your ticket price. </center> </h6> """,
        unsafe_allow_html=True,
    )
with row0_2:
    st.text("")
    st.subheader(
        "Linkedin : App by [Ahmed Ramadan](https://www.linkedin.com/in/ahmed-ramadan-18b873230/) "
    )
    st.subheader(
        "Github : App by [Ahmed Ramadan](https://github.com/AhmedRamadan74/Air-Flight-Tickets)"
    )

model = joblib.load("model.pkl")  # load model
inputs = joblib.load("input.pkl")  # load input


def Make_Prediction(
    Airline,
    Source,
    Destination,
    Total_Stops,
    Additional_Info,
    month_of_Journey,
    day_of_Journey,
    Duration_minute,
):
    data = pd.DataFrame(columns=inputs)
    data.at[0, "Airline"] = Airline
    data.at[0, "Source"] = Source
    data.at[0, "Destination"] = Destination
    data.at[0, "Total_Stops"] = Total_Stops
    data.at[0, "Additional_Info"] = Additional_Info
    data.at[0, "month_of_Journey"] = month_of_Journey
    data.at[0, "day_of_Journey"] = day_of_Journey
    data.at[0, "Duration_minute"] = Duration_minute

    # prediction output
    result = model.predict(data)
    return round(result[0], 2)


st.write("Frist , Entry details  your Air Flight ")

Airline = st.selectbox(
    " An airline that booked a ticket :", df.Airline.unique().tolist()
)
Source = st.selectbox(
    "The place of take-off :", df_min_max_duration.Source.unique().tolist()
)
Destination = st.selectbox(
    "The landing place :",
    df_min_max_duration[df_min_max_duration["Source"] == Source]["Destination"]
    .unique()
    .tolist(),
)

Date_of_Journey = st.date_input("The date of journey")
Dep_Time = st.time_input("Time of take-off ")

st.write(f"represent if flight fly from Source to Destination with rest or not :")
value_total_stop = (
    df_min_max_duration[
        (df_min_max_duration["Source"] == Source)
        & (df_min_max_duration["Destination"] == Destination)
    ]["Total_Stops"]
    .unique()
    .tolist()
)
Total_Stops = st.selectbox("0 represented to no rest : ", value_total_stop)
Total_Stops = int(Total_Stops)
Additional_Info = st.selectbox(
    "some additional info required :", df.Additional_Info.unique().tolist()
)

Min_Duration_minute = df_min_max_duration[
    (df_min_max_duration["Source"] == Source)
    & (df_min_max_duration["Destination"] == Destination)
    & (df_min_max_duration["Total_Stops"] == Total_Stops)
]["Min_Duration_minute"].values[0]
Min_Duration_minute = math.floor(Min_Duration_minute / 60)
Max_Duration_minute = df_min_max_duration[
    (df_min_max_duration["Source"] == Source)
    & (df_min_max_duration["Destination"] == Destination)
    & (df_min_max_duration["Total_Stops"] == Total_Stops)
]["Max_Duration_minute"].values[0]
Max_Duration_minute = math.floor(Max_Duration_minute / 60)

st.write(
    f"Range time of arrival is between {Min_Duration_minute} hours  and {Max_Duration_minute} hours"
)
decimal_hours = st.number_input(
    label="Time of arrival - format (hour.minute)",
    min_value=float(Min_Duration_minute),
    max_value=float(Max_Duration_minute),
)
hours, minutes = divmod(
    int(decimal_hours * 60), 60
)  # to convert decimal number to hour and minutes
st.write(f"Time of arrival is {hours} hours and {minutes} minutes")

Duration_minute = int(decimal_hours * 60)

result = Make_Prediction(
    Airline,
    Source,
    Destination,
    Total_Stops,
    Additional_Info,
    Date_of_Journey.month,
    Date_of_Journey.day,
    Duration_minute,
)
btn = st.button("Predict")
if btn:
    st.write(f"Price of ticket = ", result)
