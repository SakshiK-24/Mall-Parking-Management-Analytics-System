import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_all_records


def show_dashboard():

    st.title("📊 Parking Analytics Dashboard")

    df = get_all_records()

    if len(df) == 0:
        st.warning("No Data Available")
        return

    # Convert datetime columns
    df["EntryTime"] = pd.to_datetime(df["EntryTime"])

    if "ExitTime" in df.columns:
        df["ExitTime"] = pd.to_datetime(df["ExitTime"])

    # Analytics columns
    df["Hour"] = df["EntryTime"].dt.hour
    df["Day"] = df["EntryTime"].dt.day_name()

    # Replace NULL fees with 0
    df["ParkingFee"] = df["ParkingFee"].fillna(0)

    # KPI CARDS
    total_vehicles = len(df)

    total_revenue = df["ParkingFee"].sum()

    avg_fee = df["ParkingFee"].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🚗 Total Vehicles",
            total_vehicles
        )

    with col2:
        st.metric(
            "💰 Revenue",
            f"₹{total_revenue:.2f}"
        )

    with col3:
        st.metric(
            "📈 Average Fee",
            f"₹{avg_fee:.2f}"
        )

    st.divider()


    # VEHICLE TYPE DISTRIBUTION
    st.subheader("🚗 Vehicle Type Distribution")

    vehicle_chart = (
        df["VehicleType"]
        .value_counts()
        .reset_index()
    )

    vehicle_chart.columns = [
        "VehicleType",
        "Count"
    ]

    fig = px.pie(
        vehicle_chart,
        names="VehicleType",
        values="Count",
        title="Vehicle Type Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # REVENUE BY VEHICLE TYPE
    st.subheader("💰 Revenue by Vehicle Type")

    revenue_chart = (
        df.groupby("VehicleType")["ParkingFee"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        revenue_chart,
        x="VehicleType",
        y="ParkingFee",
        title="Revenue by Vehicle Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # PEAK HOURS
    st.subheader("⏰ Peak Parking Hours")

    hour_chart = (
        df.groupby("Hour")
        .size()
        .reset_index(name="Vehicles")
    )

    fig = px.bar(
        hour_chart,
        x="Hour",
        y="Vehicles",
        title="Peak Parking Hours"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # REVENUE BY DAY
    st.subheader("📅 Revenue by Day")

    day_chart = (
        df.groupby("Day")["ParkingFee"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        day_chart,
        x="Day",
        y="ParkingFee",
        title="Revenue by Day"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # RECENT RECORDS
    st.subheader("📋 Recent Parking Records")

    st.dataframe(
        df.sort_values(
            by="ParkingID",
            ascending=False
        ).head(10),
        use_container_width=True
    )

    # BUSINESS INSIGHTS
    st.subheader("📌 Business Insights")

    peak_hour = (
        df["Hour"]
        .value_counts()
        .idxmax()
    )

    highest_day = (
        day_chart.loc[
            day_chart["ParkingFee"].idxmax(),
            "Day"
        ]
    )

    st.info(
        f"Peak Parking Hour: {peak_hour}:00"
    )

    st.success(
        f"Highest Revenue Day: {highest_day}"
    )