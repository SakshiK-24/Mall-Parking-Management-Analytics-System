import pyodbc

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-86GM60Q\\SQLEXPRESS;"
    "DATABASE=MallParkingDB;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

from datetime import datetime

def add_vehicle(vehicle_no, vehicle_type):

    slot_no = get_available_slot()

    if slot_no is None:
        return "No Slots Available"

    entry_time = datetime.now()

    cursor.execute("""
    INSERT INTO ParkingRecords
    (
    VehicleNumber,
    VehicleType,
    SlotNumber,
    EntryTime,
    Status
    )
    VALUES
    (?, ?, ?, ?, ?)
    """,

    vehicle_no,
    vehicle_type,
    slot_no,
    entry_time,
    "Parked")

    conn.commit()

    occupy_slot(slot_no)

    return slot_no

def get_available_slot():

    cursor.execute("""
    SELECT TOP 1 SlotNumber
    FROM ParkingSlots
    WHERE SlotStatus='Available'
    """)

    slot = cursor.fetchone()

    if slot:
        return slot[0]

    return None

def occupy_slot(slot_number):

    cursor.execute("""
    UPDATE ParkingSlots
    SET SlotStatus='Occupied'
    WHERE SlotNumber=?
    """,
    slot_number)

    conn.commit()

import pandas as pd

def get_all_records():

    new_conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-86GM60Q\\SQLEXPRESS;"
        "DATABASE=MallParkingDB;"
        "Trusted_Connection=yes;"
    )

    query = """
    SELECT *
    FROM ParkingRecords
    """

    df = pd.read_sql(query, new_conn)

    new_conn.close()

    return df

def vehicle_exit(vehicle_no):

    cursor.execute("""
    SELECT ParkingID,
           SlotNumber,
           EntryTime
    FROM ParkingRecords
    WHERE VehicleNumber=?
    AND Status='Parked'
    """,
    vehicle_no)

    record = cursor.fetchone()

    if record is None:
        return "Vehicle Not Found"

    parking_id = record[0]
    slot_number = record[1]
    entry_time = record[2]

    from datetime import datetime

    exit_time = datetime.now()

    duration = exit_time - entry_time

    hours = duration.total_seconds() / 3600

    fee = round(hours * 20, 2)

    cursor.execute("""
    UPDATE ParkingRecords
    SET ExitTime=?,
        ParkingFee=?,
        Status='Exited'
    WHERE ParkingID=?
    """,
    exit_time,
    fee,
    parking_id)

    conn.commit()

    cursor.execute("""
    UPDATE ParkingSlots
    SET SlotStatus='Available'
    WHERE SlotNumber=?
    """,
    slot_number)

    conn.commit()

    return fee

def total_slots():

    cursor.execute("""
    SELECT COUNT(*)
    FROM ParkingSlots
    """)

    return cursor.fetchone()[0]

def occupied_slots():

    cursor.execute("""
    SELECT COUNT(*)
    FROM ParkingSlots
    WHERE SlotStatus='Occupied'
    """)

    return cursor.fetchone()[0]

def available_slots():

    cursor.execute("""
    SELECT COUNT(*)
    FROM ParkingSlots
    WHERE SlotStatus='Available'
    """)

    return cursor.fetchone()[0]

def total_revenue():

    cursor.execute("""
    SELECT ISNULL(
        SUM(ParkingFee),
        0
    )
    FROM ParkingRecords
    """)

    return cursor.fetchone()[0]
