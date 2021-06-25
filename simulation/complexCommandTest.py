# This example illustrates how to execute complex commands from
# a remote API client. You can also use a similar construct for
# commands that are not directly supported by the remote API.
#
# Load the demo scene 'remoteApiCommandServerExample.ttt' in CoppeliaSim, then 
# start the simulation and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
    import simulation.sim as sim
    import simulation.simConst as vrep
    import numpy as np
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import sys
import ctypes
color_space = np.asarray([[78.0, 121.0, 167.0],  # blue
                                           [89.0, 161.0, 79.0],  # green
                                           [156, 117, 95],  # brown
                                           [242, 142, 43],  # orange
                                           [237.0, 201.0, 72.0],  # yellow
                                           [186, 176, 172],  # gray
                                           [255.0, 87.0, 89.0],  # red
                                           [176, 122, 161],  # purple
                                           [118, 183, 178],  # cyan
                                           [255, 157, 167]]) / 255.0  #pink
print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:
    print ('Connected to remote API server')

    # 1. First send a command to display a specific message in a dialog box:
    emptyBuff = bytearray()
    res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_childscript,'displayText_function',[],[],['Hello world!'],emptyBuff,vrep.simx_opmode_blocking)
    if res==vrep.simx_return_ok:
        print ('Return string: ',retStrings[0]) # display the reply from CoppeliaSim (in this case, just a string)
    else:
        print ('Remote function call failed')

    # #2. Now create a dummy object at coordinate 0.1,0.2,0.3 with name 'MyDummyName':
    # res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_childscript,'createDummy_function',[],[0.1,0.2,0.3],['MyDummyName'],emptyBuff,vrep.simx_opmode_blocking)
    # if res==vrep.simx_return_ok:
    #     print ('Dummy handle: ',retInts[0]) # display the reply from CoppeliaSim (in this case, the handle of the created dummy)
    # else:
    #     print ('Remote function call failed')

    # 3. Now send a code string to execute some random functions:
    # code="local octreeHandle=simCreateOctree(0.5,0,1)\n" \
    # "simInsertVoxelsIntoOctree(octreeHandle,0,{0.1,0.1,0.1},{255,0,255})\n" \
    # "return 'done'"
    # res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,"remoteApiCommandServer",vrep.sim_scripttype_childscript,'executeCode_function',[],[],[code],emptyBuff,vrep.simx_opmode_blocking)
    # if res==vrep.simx_return_ok:
    #     print ('Code execution returned: ',retStrings[0])
    # else:
    #     print ('Remote function call failed')
    #
    # # Now close the connection to CoppeliaSim:
    # sim.simxFinish(clientID)

    position = [0.1, 0.1, 1]
    sizes = [0.15, 0.3, 0.2]
    orientation = [0, 0, 0]
    color = color_space[1].tolist()
    res, resInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(clientID, "remoteApiCommandServer", vrep.sim_scripttype_childscript, 'createPureshape_function', [0],  position+sizes+orientation+color, ['obj1'], emptyBuff, vrep.simx_opmode_blocking)
    if res==vrep.simx_return_ok:
        print ('Code execution returned: ',retStrings[0])
    else:
        print ('Remote function call failed')

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
