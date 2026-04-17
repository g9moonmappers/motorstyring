from dynamixel_sdk import *

#test

#portHandler = PortHandler("/dev/ttyUSB0") linux
#portHandler = PortHandler("COM5") Windows
packetHandler = PacketHandler(2.0)

mode_adresse = 11
torque_on_address = 64
goal_velocity_adresse = 104
present_velocity_adresse = 128

dxl_id1 = 1
dxl_id2 = 2

T_ON = 1
T_OFF = 0

velocity_mode = 1

groupBulkWrite = GroupBulkWrite(portHandler, packetHandler)
groupBulkRead = GroupBulkRead(portHandler, packetHandler)

if portHandler.openPort():
  print("Succeeded to open the port!")
else:
  print("Failed to open the port!")
  exit()

if portHandler.setBaudRate(57600):
  print("Succeeded to change the baudrate!")
else:
  print("Failed to change the baudrate!")
  exit()

packetHandler.write1ByteTxRx(portHandler, dxl_id1, mode_adresse, velocity_mode)
packetHandler.write1ByteTxRx(portHandler, dxl_id2, mode_adresse, velocity_mode)

packetHandler.write1ByteTxRx(portHandler, dxl_id1, torque_on_address, T_ON)
packetHandler.write1ByteTxRx(portHandler, dxl_id2, torque_on_address, T_ON)

dxl_addparam_result = groupBulkRead.addParam(dxl_id1, present_velocity_adresse, 4)
dxl_addparam_result = groupBulkRead.addParam(dxl_id2, present_velocity_adresse, 4)

while True:
    try:
        target_velocity = int(input("Enter target velocity (-460 ~ 460, 0 to exit): "))
    except ValueError:
        print("Please enter an integer.")
        continue

    if target_velocity == 0:
        break
        
    elif target_velocity < -460 or target_velocity > 460:
        print("Value must be between 0 and 460.")
        continue
    
    
    param_goal_velocity_H = [
        DXL_LOBYTE(DXL_LOWORD(target_velocity)),
        DXL_HIBYTE(DXL_LOWORD(target_velocity)),
        DXL_LOBYTE(DXL_HIWORD(target_velocity)),
        DXL_HIBYTE(DXL_HIWORD(target_velocity))
    ]
    
    
    
    
    param_goal_velocity_V = [
        DXL_LOBYTE(DXL_LOWORD(target_velocity)),
        DXL_HIBYTE(DXL_LOWORD(target_velocity)),
        DXL_LOBYTE(DXL_HIWORD(target_velocity)),
        DXL_HIBYTE(DXL_HIWORD(target_velocity))
    ]


    dxl_addparam_result = groupBulkWrite.addParam(dxl_id1, goal_velocity_adresse, 4, param_goal_velocity_H)
    if not dxl_addparam_result:
        print("[ID:%03d] groupBulkWrite addparam failed" % dxl_id1)
        exit()

    dxl_addparam_result = groupBulkWrite.addParam(dxl_id2, goal_velocity_adresse, 4, param_goal_velocity_V)
    if not dxl_addparam_result:
        print("[ID:%03d] groupBulkWrite addparam failed" % dxl_id2)
        exit()

    groupBulkWrite.txPacket()
    groupBulkWrite.clearParam()

    while True:
        groupBulkRead.txRxPacket()
        dxl1_present_velocity = groupBulkRead.getData(dxl_id1, present_velocity_adresse, 4)
        dxl2_present_velocity = groupBulkRead.getData(dxl_id2, present_velocity_adresse, 4)
        print("[ID:%03d] velocity motor 1 : %d \t [ID:%03d] velocity motor 2: %d" % (dxl_id1, dxl1_present_velocity, dxl_id2, dxl2_present_velocity))
        if (abs(target_velocity - dxl1_present_velocity) == 0) and (abs(target_velocity - dxl2_present_velocity) == 0):
            break
        
packetHandler.write1ByteTxRx(portHandler, dxl_id1, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id2, torque_on_address, T_OFF)
portHandler.closePort()

#%%

from dynamixel_sdk import *
import time

portHandler = PortHandler("COM12")
packetHandler = PacketHandler(2.0)

mode_adresse = 11
torque_on_address = 64
goal_velocity_adresse = 104
present_velocity_adresse = 128

dxl_id1 = 1
dxl_id2 = 2
dxl_id3 = 3
dxl_id4 = 4
dxl_id5 = 5
dxl_id6 = 6

T_ON = 1
T_OFF = 0

velocity_mode = 1

groupBulkWrite = GroupBulkWrite(portHandler, packetHandler)
groupBulkRead = GroupBulkRead(portHandler, packetHandler)

if portHandler.openPort():
  print("Succeeded to open the port!")
else:
  print("Failed to open the port!")
  exit()

if portHandler.setBaudRate(57600):
  print("Succeeded to change the baudrate!")
else:
  print("Failed to change the baudrate!")
  exit()

packetHandler.write1ByteTxRx(portHandler, dxl_id1, mode_adresse, velocity_mode)
packetHandler.write1ByteTxRx(portHandler, dxl_id2, mode_adresse, velocity_mode)
packetHandler.write1ByteTxRx(portHandler, dxl_id3, mode_adresse, velocity_mode)
packetHandler.write1ByteTxRx(portHandler, dxl_id4, mode_adresse, velocity_mode)
packetHandler.write1ByteTxRx(portHandler, dxl_id5, mode_adresse, velocity_mode)
packetHandler.write1ByteTxRx(portHandler, dxl_id6, mode_adresse, velocity_mode)


packetHandler.write1ByteTxRx(portHandler, dxl_id1, torque_on_address, T_ON)
packetHandler.write1ByteTxRx(portHandler, dxl_id2, torque_on_address, T_ON)
packetHandler.write1ByteTxRx(portHandler, dxl_id3, torque_on_address, T_ON)
packetHandler.write1ByteTxRx(portHandler, dxl_id4, torque_on_address, T_ON)
packetHandler.write1ByteTxRx(portHandler, dxl_id5, torque_on_address, T_ON)
packetHandler.write1ByteTxRx(portHandler, dxl_id6, torque_on_address, T_ON)


dxl_addparam_result = groupBulkRead.addParam(dxl_id1, present_velocity_adresse, 4)
dxl_addparam_result = groupBulkRead.addParam(dxl_id2, present_velocity_adresse, 4)
dxl_addparam_result = groupBulkRead.addParam(dxl_id3, present_velocity_adresse, 4)
dxl_addparam_result = groupBulkRead.addParam(dxl_id4, present_velocity_adresse, 4)
dxl_addparam_result = groupBulkRead.addParam(dxl_id5, present_velocity_adresse, 4)
dxl_addparam_result = groupBulkRead.addParam(dxl_id6, present_velocity_adresse, 4)


while True:
    try:
        target_velocity1 = int(input("Enter target velocity (-460 ~ 460, 0 to exit): "))
    except ValueError:
        print("Please enter an integer.")
        continue

    if target_velocity1 == 0:
        break
        
    elif target_velocity1 < -460 or target_velocity1 > 460:
        print("Value must be between -460 and 460.")
        continue
    
    
    param_goal_velocity_H = [
        DXL_LOBYTE(DXL_LOWORD(target_velocity1)),
        DXL_HIBYTE(DXL_LOWORD(target_velocity1)),
        DXL_LOBYTE(DXL_HIWORD(target_velocity1)),
        DXL_HIBYTE(DXL_HIWORD(target_velocity1))
    ]
    
    try:
        target_velocity2 = int(input("Enter target velocity (-460 ~ 460, 0 to exit): "))
    except ValueError:
        print("Please enter an integer.")
        continue

    if target_velocity2 == 0:
        break
    
    elif target_velocity2 < -460 or target_velocity2 > 460:
        print("Value must be between -460 and 460.")
        continue
    
    
    param_goal_velocity_V = [
        DXL_LOBYTE(DXL_LOWORD(target_velocity2)),
        DXL_HIBYTE(DXL_LOWORD(target_velocity2)),
        DXL_LOBYTE(DXL_HIWORD(target_velocity2)),
        DXL_HIBYTE(DXL_HIWORD(target_velocity2))
    ]


    dxl_addparam_result = groupBulkWrite.addParam(dxl_id1, goal_velocity_adresse, 4, param_goal_velocity_V)
    if not dxl_addparam_result:
        print("[ID:%03d] groupBulkWrite addparam failed" % dxl_id1)
        exit()
    dxl_addparam_result = groupBulkWrite.addParam(dxl_id3, goal_velocity_adresse, 4, param_goal_velocity_V)
    if not dxl_addparam_result:
        print("[ID:%03d] groupBulkWrite addparam failed" % dxl_id3)
        exit()
    dxl_addparam_result = groupBulkWrite.addParam(dxl_id5, goal_velocity_adresse, 4, param_goal_velocity_V)
    if not dxl_addparam_result:
        print("[ID:%03d] groupBulkWrite addparam failed" % dxl_id5)
        exit()

    dxl_addparam_result = groupBulkWrite.addParam(dxl_id2, goal_velocity_adresse, 4, param_goal_velocity_H)
    if not dxl_addparam_result:
        print("[ID:%03d] groupBulkWrite addparam failed" % dxl_id2)
        exit()
    dxl_addparam_result = groupBulkWrite.addParam(dxl_id4, goal_velocity_adresse, 4, param_goal_velocity_H)
    if not dxl_addparam_result:
        print("[ID:%03d] groupBulkWrite addparam failed" % dxl_id4)
        exit()
    dxl_addparam_result = groupBulkWrite.addParam(dxl_id6, goal_velocity_adresse, 4, param_goal_velocity_H)
    if not dxl_addparam_result:
        print("[ID:%03d] groupBulkWrite addparam failed" % dxl_id16)
        exit()

    groupBulkWrite.txPacket()
    groupBulkWrite.clearParam()

    while True:
        groupBulkRead.txRxPacket()
        dxl1_present_velocity = groupBulkRead.getData(dxl_id1, present_velocity_adresse, 4)
        dxl2_present_velocity = groupBulkRead.getData(dxl_id2, present_velocity_adresse, 4)
        dxl1_present_velocity = groupBulkRead.getData(dxl_id3, present_velocity_adresse, 4)
        dxl2_present_velocity = groupBulkRead.getData(dxl_id4, present_velocity_adresse, 4)
        dxl1_present_velocity = groupBulkRead.getData(dxl_id5, present_velocity_adresse, 4)
        dxl2_present_velocity = groupBulkRead.getData(dxl_id6, present_velocity_adresse, 4)
        
        
        if (target_velocity1 < 0) and (target_velocity2 < 0):
            print("[ID:%03d] velocity motor 1 : %d \t [ID:%03d] velocity motor 2: %d" % (dxl_id1, dxl1_present_velocity - 4294967295, dxl_id2, dxl2_present_velocity - 4294967295))
            if (abs(target_velocity1 - dxl1_present_velocity) - 4294967295 == 0) and (abs(target_velocity2 - dxl2_present_velocity) - 4294967295 == 0):
                break
        elif (target_velocity1 < 0) and (target_velocity2 > 0):
            print("[ID:%03d] velocity motor 1 : %d \t [ID:%03d] velocity motor 2: %d" % (dxl_id1, dxl1_present_velocity - 4294967295, dxl_id2, dxl2_present_velocity))
            if (abs(target_velocity1 - dxl1_present_velocity) - 4294967295 == 0) and (abs(target_velocity2 - dxl2_present_velocity) == 0):
                break
        elif (target_velocity1 > 0) and (target_velocity2 < 0):
            print("[ID:%03d] velocity motor 1 : %d \t [ID:%03d] velocity motor 2: %d" % (dxl_id1, dxl1_present_velocity, dxl_id2, dxl2_present_velocity - 4294967295))
            if (abs(target_velocity1 - dxl1_present_velocity) == 0) and (abs(target_velocity2 - dxl2_present_velocity) - 4294967295 == 0):
                break
        else:
            print("[ID:%03d] velocity motor 1 : %d \t [ID:%03d] velocity motor 2: %d" % (dxl_id1, dxl1_present_velocity, dxl_id2, dxl2_present_velocity))
            if (abs(target_velocity1 - dxl1_present_velocity) == 0) and (abs(target_velocity2 - dxl2_present_velocity) == 0):
                break
        
packetHandler.write1ByteTxRx(portHandler, dxl_id1, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id2, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id3, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id4, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id5, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id6, torque_on_address, T_OFF)
portHandler.closePort()
