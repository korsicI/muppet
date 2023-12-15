import pygame
import bpy
import time


def refresh():
    bpy.context.view_layer.update()
    #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=0.1)
    

pygame.init()
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joysticks found.")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Initialized joystick:", joystick.get_name())


# set up variables
counter=0
x = 100
y = 100
joysticks = []
record = False
run =True
start_time = time.time()
current_time = time.time()
refresh_time = time.time()


# object selection

obj = bpy.context.scene.objects ["Suzanne"]


# main loop

while run:
    
# record keyframes
    
    if time.time() - current_time > 1/24:
        if record == True:
            obj.keyframe_insert(data_path="location",frame = bpy.context.scene.frame_current)
            counter = 0
            bpy.context.scene.frame_set(bpy.context.scene.frame_current+1)
        current_time = time.time()

# joystick stuff

    for joystick in joysticks:
        
        if joystick.get_button(0):
            print("STOP")
            run = False
            
        if joystick.get_button(1):
            print("Recording")
            
            if record == True:
                record = False
                
            else:
                record = True
            time.sleep(2)
            
        #Suzanne movement with joystick 
        
        horiz_move_x = joystick.get_axis(0)
        horiz_move_y = joystick.get_axis(1)
        vert_move = joystick.get_axis(3)
        
        
        if abs(vert_move) > 0.1:
            obj.location.z = vert_move * 4
            
            if time.time() - refresh_time > 1/24:
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=2)
                refresh_time=time.time()
            
        if abs(horiz_move_x) > 0.1:
            obj.location.x = horiz_move_x * 4
            
            if time.time() - refresh_time > 1/24:
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=2)
                refresh_time=time.time()
            
        if abs(horiz_move_y) > 0.1:
            obj.location.y = horiz_move_y * 4
            
            if time.time() - refresh_time > 1/24:
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=2)
                refresh_time= time.time()      
        
# pygame stuff
   
    for event in pygame.event.get():
        
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)

#quit program
        
        if event.type == pygame.QUIT:
            run = False

