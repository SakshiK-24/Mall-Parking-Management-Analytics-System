import streamlit as st
from PIL import Image

from database import (
    add_vehicle,
    vehicle_exit,
    get_all_records,
    total_slots,
    occupied_slots,
    available_slots,
    total_revenue
)
from dashboard import show_dashboard


# PAGE CONFIG
st.set_page_config(
    page_title="Mall Parking Management",
    layout="wide"
)


# SESSION STATE
if "page" not in st.session_state:
    st.session_state.page = "home"


# HOME PAGE


if st.session_state.page == "home":

    st.title("🚗 Mall Parking Management System")

    image = Image.open("images/Car_Image.jpg")

    st.image(
        image,
        use_container_width=True
    )

    st.subheader("Parking Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Slots",
            total_slots()
        )

    with col2:
        st.metric(
            "Occupied Slots",
            occupied_slots()
        )

    with col3:
        st.metric(
            "Available Slots",
            available_slots()
        )

    with col4:
        st.metric(
            "Revenue",
            f"₹{total_revenue()}"
        )

    st.subheader("Operations")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🚗 Vehicle Entry"):
            st.session_state.page = "entry"
            st.rerun()

    with col2:
        if st.button("🚙 Vehicle Exit"):
            st.session_state.page = "exit"
            st.rerun()

    with col3:
        if st.button("📊 View Dataset"):
            st.session_state.page = "dataset"
            st.rerun()

    with col4:
        if st.button("📈 Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

# VEHICLE ENTRY PAGE
elif st.session_state.page == "entry":

    st.title("🚗 Vehicle Entry")

    if st.button("🏠 Home"):
        st.session_state.page = "home"
        st.rerun()

    vehicle_no = st.text_input(
        "Vehicle Number"
    )

    vehicle_type = st.selectbox(
        "Vehicle Type",
        [
            "Two Wheeler",
            "Four Wheeler"
        ]
    )

    if st.button("Add Vehicle"):

        if vehicle_no == "":
            st.error(
                "Enter Vehicle Number"
            )

        else:

            slot = add_vehicle(
                vehicle_no,
                vehicle_type
            )

            if slot == "No Slots Available":

                st.error(
                    "No Parking Slots Available"
                )

            else:

                st.success(
                    f"Vehicle parked in Slot {slot}"
                )


# VEHICLE EXIT PAGE
elif st.session_state.page == "exit":

    st.title("🚙 Vehicle Exit")

    if st.button("🏠 Home"):
        st.session_state.page = "home"
        st.rerun()

    vehicle_no = st.text_input(
        "Enter Vehicle Number"
    )

    if st.button("Exit Vehicle"):

        result = vehicle_exit(
            vehicle_no
        )

        if result == "Vehicle Not Found":

            st.error(
                result
            )

        else:

            st.success(
                f"Parking Fee = ₹{result}"
            )


# DATASET PAGE
elif st.session_state.page == "dataset":

    st.title("📊 Parking Records")

    if st.button("🏠 Home"):
        st.session_state.page = "home"
        st.rerun()

    df = get_all_records()

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="parking_records.csv",
        mime="text/csv"
    )


# DASHBOARD PAGE
elif st.session_state.page == "dashboard":

    if st.button("🏠 Home"):
        st.session_state.page = "home"
        st.rerun()

    show_dashboard()