create database MallParkingDB;
use MallParkingDB;

create table ParkingSlots(
    SlotID int identity(1,1) primary key,
    SlotNumber varchar(10),
    SlotStatus varchar(20)
);
create table ParkingRecords
(
    ParkingID int identity(1,1) primary key,
    VehicleNumber varchar(20),
    VehicleType varchar(20),
    SlotNumber varchar(10),
    EntryTime datetime,
    ExitTime datetime,
    ParkingFee decimal(10,2),
    Status varchar(20)
);

DECLARE @i INT = 01

WHILE @i <= 200
BEGIN

    INSERT INTO ParkingSlots
    VALUES (
        'P' + CAST(@i AS VARCHAR),
        'Available'
    )

    SET @i = @i + 1

END
select * from ParkingSlots;
-- update ParkingSlots
-- set SlotStatus = 'Available';
-- delete from ParkingSlots;

select * from ParkingRecords;
-- delete from ParkingRecords;
-- drop table ParkingRecords;
-- drop table ParkingSlots;
select count(*) from ParkingSlots;

