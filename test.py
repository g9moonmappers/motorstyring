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
        target_velocityH = - int(input("Enter target velocity (-460 ~ 460, 0 to exit): "))
    except ValueError:
        print("Please enter an integer.")
        continue

    if target_velocityH == 0:
        break
        
    elif target_velocityH < -460 or target_velocityH > 460:
        print("Value must be between -460 and 460.")
        continue
    
    
    param_goal_velocity_H = [
        DXL_LOBYTE(DXL_LOWORD(target_velocityH)),
        DXL_HIBYTE(DXL_LOWORD(target_velocityH)),
        DXL_LOBYTE(DXL_HIWORD(target_velocityH)),
        DXL_HIBYTE(DXL_HIWORD(target_velocityH))
    ]
    
    try:
        target_velocityV = int(input("Enter target velocity (-460 ~ 460, 0 to exit): "))
    except ValueError:
        print("Please enter an integer.")
        continue

    if target_velocityV == 0:
        break
    
    elif target_velocityV < -460 or target_velocityV > 460:
        print("Value must be between -460 and 460.")
        continue
    
    
    param_goal_velocity_V = [
        DXL_LOBYTE(DXL_LOWORD(target_velocityV)),
        DXL_HIBYTE(DXL_LOWORD(target_velocityV)),
        DXL_LOBYTE(DXL_HIWORD(target_velocityV)),
        DXL_HIBYTE(DXL_HIWORD(target_velocityV))
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
        
        
        if (target_velocityH < 0) and (target_velocityV < 0):
            print("[ID:%03d] velocity motor 1 : %d \t [ID:%03d] velocity motor 2: %d" % (dxl_id1, dxl1_present_velocity - 4294967295, dxl_id2, dxl2_present_velocity - 4294967295))
            if (abs(target_velocityH - dxl1_present_velocity) - 4294967295 == 0) and (abs(target_velocityV - dxl2_present_velocity) - 4294967295 == 0):
                break
        elif (target_velocityH < 0) and (target_velocityV > 0):
            print("[ID:%03d] velocity motor 1 : %d \t [ID:%03d] velocity motor 2: %d" % (dxl_id1, dxl1_present_velocity, dxl_id2,  abs(dxl2_present_velocity - 4294967295)))
            if (abs(target_velocityH + dxl1_present_velocity) == 0) and (abs(target_velocityV - 4294967295 + dxl2_present_velocity) == 0):
                break
        elif (target_velocityH > 0) and (target_velocityV < 0):
            print("[ID:%03d] velocity motor 1 : %d \t [ID:%03d] velocity motor 2: %d" % (dxl_id1, dxl1_present_velocity - 4294967295, dxl_id2, dxl2_present_velocity))
            if (abs(target_velocityH - 4294967295 + dxl1_present_velocity) == 0) and (abs(target_velocityV + dxl2_present_velocity) == 0):
                break
        else:
            print("[ID:%03d] velocity motor 1 : %d \t [ID:%03d] velocity motor 2: %d" % (dxl_id1, dxl1_present_velocity, dxl_id2, dxl2_present_velocity))
            if (abs(target_velocityH - dxl1_present_velocity) == 0) and (abs(target_velocityV - dxl2_present_velocity) == 0):
                break
        
packetHandler.write1ByteTxRx(portHandler, dxl_id1, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id2, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id3, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id4, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id5, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id6, torque_on_address, T_OFF)
portHandler.closePort()

#%%

import keyboard
from dynamixel_sdk import *

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

turn_factor = 2

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
        velocity = int(input("Enter target velocity (0 ~ 460, esc to exit): "))
    
    except ValueError:
        print("Please enter an integer.")
        continue
        
    if velocity < 0 or velocity > 460:
        print("Value must be between -460 and 460.")
        continue
    
    
    while True:
        w = keyboard.is_pressed('w')
        a = keyboard.is_pressed('a')
        d = keyboard.is_pressed('d')
        s = keyboard.is_pressed('s')
        e = keyboard.is_pressed('e')
        o = keyboard.is_pressed('o')
        backspace = keyboard.is_pressed('backspace')
        
        if backspace:
            target_velocityV = target_velocityH = 0
            break
        
        elif w and a:
            target_velocityH = -turn_factor*velocity
            target_velocityV = velocity
            print("w + a")
            
        elif w and d:
            target_velocityH = -velocity
            target_velocityV = turn_factor*velocity
            print("w + d")
            
        elif s and a:
            target_velocityH = turn_factor*velocity
            target_velocityV = -velocity
            print("s + a")
            
        elif s and d:
            target_velocityH = velocity
            target_velocityV = -turn_factor*velocity
            print("s + d")
            
        elif w:
            target_velocityH = -velocity
            target_velocityV = velocity
            print("w")
            
        elif s:
            target_velocityH = velocity
            target_velocityV = -velocity
            print("s")
            
        elif a:
            target_velocityH = -velocity
            target_velocityV = -velocity
            print("a")
            
        elif d:
            target_velocityH = velocity
            target_velocityV = velocity
            print("d")
            
        else:
            target_velocityH = target_velocityV = 0
            
        
        param_goal_velocity_H = [
            DXL_LOBYTE(DXL_LOWORD(target_velocityH)),
            DXL_HIBYTE(DXL_LOWORD(target_velocityH)),
            DXL_LOBYTE(DXL_HIWORD(target_velocityH)),
            DXL_HIBYTE(DXL_HIWORD(target_velocityH))
        ]    
        
        param_goal_velocity_V = [
            DXL_LOBYTE(DXL_LOWORD(target_velocityV)),
            DXL_HIBYTE(DXL_LOWORD(target_velocityV)),
            DXL_LOBYTE(DXL_HIWORD(target_velocityV)),
            DXL_HIBYTE(DXL_HIWORD(target_velocityV))
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
        
packetHandler.write1ByteTxRx(portHandler, dxl_id1, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id2, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id3, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id4, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id5, torque_on_address, T_OFF)
packetHandler.write1ByteTxRx(portHandler, dxl_id6, torque_on_address, T_OFF)
portHandler.closePort()

#%%
