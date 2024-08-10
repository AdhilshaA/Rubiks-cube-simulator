import numpy as np
import pygame

from pygame.locals import *
import os
import time
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize the pygame

width_display = 800
height_display = 800
window_title = "Rubik's Cube Simulator"
fig_path = r"\figures"
curr_path = os.path.dirname(__file__)

pygame.init()

clock = pygame.time.Clock()

# window = pygame.display.set_mode((width_display, height_display), DOUBLEBUF|OPENGL)
# pygame.display.set_caption(window_title)

# # setting up the background with image
background = pygame.image.load(curr_path + fig_path + r"\bg.png")
background = pygame.transform.scale(background, (width_display, height_display))

# gluPerspective(90, (width_display/height_display), 0.2, 100.0)
# glTranslatef(0.0,0.0, -5)

# write the game loop

class Cube:
    def __init__(self) -> None:
        
        self.center = [0, 0, 0]
        self.side = 3
        self.small_side = self.side // 3
        self.curr_face = 'front' # front, back, left, right, top, bottom
        self.top_face = 'top'
        self.right_face = 'right'
        self.curr_x_highlight = 0
        self.curr_y_highlight = 2
        
        cube_centers = np.zeros((3, 3, 3, 3), dtype=float)
        self.cube_corners = np.zeros((3, 3, 3, 8, 3), dtype=float)
        
        # setting up the cube center
        cube_centers[1, 1, 1] = np.copy(self.center)
        
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if i == 1 and j == 1 and k == 1:
                        continue
                    cube_centers[i, j, k] = np.array([self.center[0] + (i - 1) * self.small_side, 
                                                   self.center[1] + (j - 1) * self.small_side, 
                                                   self.center[2] + (k - 1) * self.small_side])
        
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.cube_corners[i, j, k, 0] = np.copy(cube_centers[i, j, k] + np.array([- self.small_side/2, - self.small_side/2, - self.small_side/2])) # back bottom left
                    self.cube_corners[i, j, k, 1] = np.copy(cube_centers[i, j, k] + np.array([self.small_side/2, - self.small_side/2, - self.small_side/2])) # back bottom right
                    self.cube_corners[i, j, k, 2] = np.copy(cube_centers[i, j, k] + np.array([self.small_side/2, self.small_side/2, - self.small_side/2])) # back top right
                    self.cube_corners[i, j, k, 3] = np.copy(cube_centers[i, j, k] + np.array([- self.small_side/2, self.small_side/2, - self.small_side/2])) # back top left
                    self.cube_corners[i, j, k, 4] = np.copy(cube_centers[i, j, k] + np.array([- self.small_side/2, - self.small_side/2, self.small_side/2])) # front bottom left
                    self.cube_corners[i, j, k, 5] = np.copy(cube_centers[i, j, k] + np.array([self.small_side/2, - self.small_side/2, self.small_side/2])) # front bottom right
                    self.cube_corners[i, j, k, 6] = np.copy(cube_centers[i, j, k] + np.array([self.small_side/2, self.small_side/2, self.small_side/2])) # front top right
                    self.cube_corners[i, j, k, 7] = np.copy(cube_centers[i, j, k] + np.array([- self.small_side/2, self.small_side/2, self.small_side/2])) # front top left
        
        del cube_centers
        
        self.cube_structure = np.zeros((3,3,3,3))
        
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.cube_structure[i, j, k] = np.array([i, j, k])
                
        self.cube_structure = self.cube_structure.astype(int)
        
        self.colors = {
            0: [0, 0, 0], # black - neutral color
            1: [255, 255, 255], # white
            2: [255, 0, 0], # red
            3: [0, 255, 0], # green
            4: [0, 0, 255], # blue
            5: [255, 255, 0], # yellow
            6: [150,0,150], # purple
            7: [150, 150, 150], # gray
            8: [150, 0, 0], # dark red
            9: [0, 150, 0], # dark green
            10: [0, 0, 150], # dark blue
            11: [150, 150, 0], # dark yellow
            12: [70, 0, 70], # dark purple
        }                
        
        for key,values in self.colors.items():
            self.colors[key] = [x/255 for x in values]
                
        self.cube_color_ids = np.zeros((3, 3, 3, 6), dtype=int)
        
        self.cube_color_ids[:, :, 0, 0] = 1 # back face (connect (corner 0, corner 1, corner 2, corner 3)) = white
        self.cube_color_ids[:, :, 2, 1] = 2 # front face (connect (corner 4, corner 5, corner 6, corner 7)) = red
        self.cube_color_ids[0, :, :, 2] = 3 # left face (connect (corner 0, corner 3, corner 7, corner 4)) = green
        self.cube_color_ids[2, :, :, 3] = 4 # right face (connect (corner 1, corner 2, corner 6, corner 5)) = blue
        self.cube_color_ids[:, 0, :, 4] = 5 # bottom face (connect (corner 0, corner 1, corner 5, corner 4)) = yellow
        self.cube_color_ids[:, 2, :, 5] = 6 # top face (connect (corner 3, corner 2, corner 6, corner 7)) = purple
    
    
    def cube_structure_rotate(self, axis, layer, direction):        
        if axis == 0:
            curr_layer = np.copy(self.cube_structure[layer, :, :])
            if direction == 1:
                print("up")
                self.cube_structure[layer, :, :] = np.rot90(curr_layer, axes=(1, 0))
                # for i in range(3):
                #     self.cube_structure[layer, 2 - i, :] = np.copy(curr_layer[:, i])
            else:
                print("down")
                self.cube_structure[layer, :, :] = np.rot90(curr_layer, axes=(0, 1))
                # for i in range(3):
                #     self.cube_structure[layer, i, :] = np.copy(curr_layer[:, i])
        elif axis == 1:
            curr_layer = np.copy(self.cube_structure[:, layer, :])
            if direction == 1:
                print("right",curr_layer.shape)
                self.cube_structure[:, layer, :] = np.rot90(curr_layer, axes=(0, 1))
                # for i in range(3):
                #     self.cube_structure[2-i, layer, :] = np.copy(curr_layer[:, i])
            else:
                print("left", curr_layer.shape)
                self.cube_structure[:, layer, :] = np.rot90(curr_layer, axes=(1, 0))
                # for i in range(3):
                #     self.cube_structure[i, layer, :] = np.copy(curr_layer[:, i])
                        
    
    
    def opposite_face(self, face):
        if face == 'front':
            return 'back'
        elif face == 'back':
            return 'front'
        elif face == 'left':
            return 'right'
        elif face == 'right':
            return 'left'
        elif face == 'top':
            return 'bottom'
        else:
            return 'top'
        
    def get_current_axes(self):
        axes = [0, 1, 2]
        axes_inversion = [False, False, False]
        def get_axis_from_face(face):
            if face == 'front':
                return 2, False
            elif face == 'back':
                return 2, True
            elif face == 'right':
                return 0, False
            elif face == 'left':
                return 0, True
            elif face == 'top':
                return 1, False
            else:
                return 1, True
        
        axes[0], axes_inversion[0] = get_axis_from_face(self.right_face)
        axes[1], axes_inversion[1] = get_axis_from_face(self.top_face)
        axes[2], axes_inversion[2] = get_axis_from_face(self.curr_face)
        
        return axes, axes_inversion
            
    
    def draw_one_small_face(self, i, j, k, l):
        if l == 0:
            glBegin(GL_QUADS)
            glVertex3fv(self.cube_corners[i, j, k, 0])
            glVertex3fv(self.cube_corners[i, j, k, 1])
            glVertex3fv(self.cube_corners[i, j, k, 2])
            glVertex3fv(self.cube_corners[i, j, k, 3])
            glEnd()

        elif l == 1:
            glBegin(GL_QUADS)
            glVertex3fv(self.cube_corners[i, j, k, 4])
            glVertex3fv(self.cube_corners[i, j, k, 5])
            glVertex3fv(self.cube_corners[i, j, k, 6])
            glVertex3fv(self.cube_corners[i, j, k, 7])
            glEnd()

        elif l == 2:
            glBegin(GL_QUADS)
            glVertex3fv(self.cube_corners[i, j, k, 0])
            glVertex3fv(self.cube_corners[i, j, k, 3])
            glVertex3fv(self.cube_corners[i, j, k, 7])
            glVertex3fv(self.cube_corners[i, j, k, 4])
            glEnd()

        elif l == 3:
            glBegin(GL_QUADS)
            glVertex3fv(self.cube_corners[i, j, k, 1])
            glVertex3fv(self.cube_corners[i, j, k, 2])
            glVertex3fv(self.cube_corners[i, j, k, 6])
            glVertex3fv(self.cube_corners[i, j, k, 5])
            glEnd()

        elif l == 4:
            glBegin(GL_QUADS)
            glVertex3fv(self.cube_corners[i, j, k, 0])
            glVertex3fv(self.cube_corners[i, j, k, 1])
            glVertex3fv(self.cube_corners[i, j, k, 5])
            glVertex3fv(self.cube_corners[i, j, k, 4])
            glEnd()

        else:
            glBegin(GL_QUADS)
            glVertex3fv(self.cube_corners[i, j, k, 3])
            glVertex3fv(self.cube_corners[i, j, k, 2])
            glVertex3fv(self.cube_corners[i, j, k, 6])
            glVertex3fv(self.cube_corners[i, j, k, 7])
            glEnd()
    
    def draw_all_faces(self):
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    i,j,k  = self.cube_structure[x, y, z]
                    for l in range(6):
                        
                        # drawing faces
                        color_idx = self.cube_color_ids[i, j, k, l]
                        if self.curr_x_highlight == x:
                            # print('Highlighting x:', i)
                            color_idx += 6
                        elif self.curr_y_highlight == y:
                            # print('Highlighting y:', j)
                            color_idx += 6
                        
                        color = self.colors[color_idx]
                        
                        glColor3fv(color)
                        
                        
                        self.draw_one_small_face(i, j, k, l)
                        
                    # drawing outlines
                    glLineWidth(5.0)  # Increase the linewidth
                    glColor3fv((0, 0, 0))
                    
                    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                    for l in range(6):
                        self.draw_one_small_face(i, j, k, l)
                    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

                     
    def rotate_layer(self, angle_deg, axis, cube_axis ,layer):
        # layer = 0, 1, 2 (0 - closest to the 0 of the axis, 2 - farthest from the 0 of the axis)
        # axis = 0, 1, 2 (0 - x, 1 - y, 2 - z)
        angle = np.radians(angle_deg)
        
        if axis == 0: # rotate along x-axis
            rotation_matrix = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
            
        elif axis == 1: # rotate along y-axis
            rotation_matrix = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])
            
        else: # rotate along z-axis
            rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
        
        points = []
        if cube_axis == 0:
            points.extend(self.cube_structure[layer, :, :].reshape(-1,3))
        elif cube_axis == 1:
            points.extend(self.cube_structure[:, layer, :].reshape(-1,3))
        else:
            points.extend(self.cube_structure[:, :, layer].reshape(-1,3))
        
        # print(np.array(points).shape)
        
        for point in points:
            self.cube_corners[point[0],point[1],point[2]] = self.cube_corners[point[0],point[1],point[2]] @ rotation_matrix

        # if cube_axis == 0:
        #     self.cube_corners[layer, :, :] = self.cube_corners[layer, :, :] @ rotation_matrix
        # elif cube_axis == 1:
        #     self.cube_corners[:, layer, :] = self.cube_corners[:, layer, :] @ rotation_matrix
        # else:
        #     self.cube_corners[:, :, layer] = self.cube_corners[:, :, layer] @ rotation_matrix
                        
cube = Cube()

font = pygame.font.Font(None, 36)  # You can change the font and size here

# def draw_text(text, x, y):
    

def game_loop():
    
    # setting up the background with image
    # background = pygame.image.load(curr_path + fig_path + r"\background.png")
    # background = pygame.transform.scale(background, (width_display, height_display))

    window = pygame.display.set_mode((width_display, height_display), DOUBLEBUF|OPENGL)
        
    pygame.display.set_caption(window_title)
    
    rotate = False
    rotate_direction = ''
    rotate_angle = 0
    
    
    moving = False
    moving_direction = ''
    moving_angle = 0
    
    window.blit(background, (0, 0))
    
    curr_axes, axes_inversion = cube.get_current_axes()
    
    # set up OpenGL
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, (width_display/height_display), 0.2, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0,0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                
                if rotate:
                    pass
                elif moving:
                    pass
                elif event.key == pygame.K_LEFT:
                    rotate = True
                    rotate_direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    rotate = True
                    rotate_direction = 'right'
                elif event.key == pygame.K_UP:
                    rotate = True
                    rotate_direction = 'up'
                elif event.key == pygame.K_DOWN:
                    rotate = True
                    rotate_direction = 'down'
                # elif event.key == pygame.K_a: # press 'a' to move the top layer to the left
                #     curr_axes, axes_inversion = cube.get_current_axes()
                #     moving = True
                #     moving_direction = 'left'
                # elif event.key == pygame.K_d: # press 'd' to move the top layer to the right
                #     curr_axes, axes_inversion = cube.get_current_axes()
                #     moving = True
                #     moving_direction = 'right'
                # elif event.key == pygame.K_w: # press 'w' to move the left layer to the top
                #     curr_axes, axes_inversion = cube.get_current_axes()
                #     moving = True
                #     moving_direction = 'up'
                # elif event.key == pygame.K_s: # press 's' to move the left layer to the bottom
                #     curr_axes, axes_inversion = cube.get_current_axes()
                #     moving = True
                #     moving_direction = 'down'
                elif event.key == pygame.K_a: # press 'a' to move the current y_highlighted layer to the left
                    curr_axes, axes_inversion = cube.get_current_axes()
                    moving = True
                    moving_direction = 'left'
                elif event.key == pygame.K_d: # press 'd' to move the current y_highlighted layer to the right
                    curr_axes, axes_inversion = cube.get_current_axes()
                    moving = True
                    moving_direction = 'right'
                elif event.key == pygame.K_w: # press 'w' to move the current x_highlighted layer to the top
                    curr_axes, axes_inversion = cube.get_current_axes()
                    moving = True
                    moving_direction = 'up'
                elif event.key == pygame.K_s: # press 's' to move the current y_highlighted layer to the bottom
                    curr_axes, axes_inversion = cube.get_current_axes()
                    moving = True
                    moving_direction = 'down'
                
                # checking to change highlights
                if event.key == pygame.K_i:
                    cube.curr_y_highlight += 1
                    if cube.curr_y_highlight == 3:
                        cube.curr_y_highlight = 0
                elif event.key == pygame.K_k:
                    cube.curr_y_highlight -= 1
                    if cube.curr_y_highlight == -1:
                        cube.curr_y_highlight = 2
                elif event.key == pygame.K_j:
                    cube.curr_x_highlight -= 1
                    if cube.curr_x_highlight == -1:
                        cube.curr_x_highlight = 2
                elif event.key == pygame.K_l:
                    cube.curr_x_highlight += 1
                    if cube.curr_x_highlight == 3:
                        cube.curr_x_highlight = 0
                    

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        # if rotate:
        #     if rotate_direction == 'left':
        #         rotate_angle += 5
        #         glRotatef(5, 0, 1, 0)
        #     elif rotate_direction == 'right':
        #         rotate_angle += 5
        #         glRotatef(5, 0, -1, 0)
        #     elif rotate_direction == 'up':
        #         rotate_angle += 5
        #         glRotatef(5, 1, 0, 0)
        #     elif rotate_direction == 'down':
        #         rotate_angle += 5
        #         glRotatef(5, -1, 0, 0)
            
        #     if rotate_angle == 90:
        #         rotate_angle = 0
        #         rotate = False
        
        if rotate:
            
            if rotate_direction == 'left':
                space_axis = 1
                direction = 1  
            elif rotate_direction == 'right':
                space_axis = 1
                direction = -1
            elif rotate_direction == 'up':
                space_axis = 0
                direction = 1
            elif rotate_direction == 'down':
                space_axis = 0
                direction = -1
            cube.rotate_layer(direction*5, space_axis, space_axis, 0)
            cube.rotate_layer(direction*5, space_axis, space_axis, 1)
            cube.rotate_layer(direction*5, space_axis, space_axis, 2)
            rotate_angle += 5
        
            # if rotate_direction == 'left':
            #     rotate_angle += 5
            #     cube.rotate_layer(5, 1, 1, 0)
            #     cube.rotate_layer(5, 1, 1, 1)
            #     cube.rotate_layer(5, 1, 1, 2)
                
            # elif rotate_direction == 'right':
            #     rotate_angle += 5
            #     cube.rotate_layer(-5, 1, 1, 0)
            #     cube.rotate_layer(-5, 1, 1, 1)
            #     cube.rotate_layer(-5, 1, 1, 2)
                
            # elif rotate_direction == 'up':
            #     rotate_angle += 5
            #     cube.rotate_layer(5, 0, 0, 0)
            #     cube.rotate_layer(5, 0, 0, 1)
            #     cube.rotate_layer(5, 0, 0, 2)
                
            # elif rotate_direction == 'down':
            #     rotate_angle += 5
            #     cube.rotate_layer(-5, 0, 0, 0)
            #     cube.rotate_layer(-5, 0, 0, 1)
            #     cube.rotate_layer(-5, 0, 0, 2)
                
            if rotate_angle == 90:
                rotate_angle = 0
                rotate = False
                if rotate_direction == 'left':
                    cube.curr_face, cube.right_face = cube.right_face, cube.opposite_face(cube.curr_face)
                elif rotate_direction == 'right':
                    cube.curr_face, cube.right_face = cube.opposite_face(cube.right_face), cube.curr_face
                elif rotate_direction == 'up':
                    cube.curr_face, cube.top_face = cube.opposite_face(cube.top_face), cube.curr_face
                elif rotate_direction == 'down':
                    cube.curr_face, cube.top_face = cube.top_face, cube.opposite_face(cube.curr_face)
                curr_axes,axes_inversion = cube.get_current_axes()
                
                cube.cube_structure_rotate(space_axis, 0, direction)
                cube.cube_structure_rotate(space_axis, 1, direction)
                cube.cube_structure_rotate(space_axis, 2, direction)
                
                print('Current face:', cube.curr_face)
                print('Top face:', cube.top_face)
                print('Right face:', cube.right_face)
                print('Current axes:', curr_axes)
                print('Axes inversion:', axes_inversion)
                
                
        elif moving:       
            
            # if moving_direction == 'left': # move the top layer to the left
            #     space_axis = 1
            #     axis_to_rotate = curr_axes[1]
            #     if axes_inversion[1]:
            #         layer_to_rotate = 0
            #     else:
            #         layer_to_rotate = 2
            #     direction = 1

            # elif moving_direction == 'right': # move the top layer to the right
            #     space_axis = 1
            #     axis_to_rotate = curr_axes[1]
            #     if axes_inversion[1]:
            #         layer_to_rotate = 0
            #     else:
            #         layer_to_rotate = 2
            #     direction = -1

            # elif moving_direction == 'up': # move the left layer to the top
            #     space_axis = 0
            #     axis_to_rotate = curr_axes[0]
            #     if axes_inversion[0]:
            #         layer_to_rotate = 2
            #     else:
            #         layer_to_rotate = 0
            #     direction = 1

            # elif moving_direction == 'down': # move the left layer to the bottom
            #     space_axis = 0
            #     axis_to_rotate = curr_axes[0]
            #     if axes_inversion[0]:
            #         layer_to_rotate = 2
            #     else:
            #         layer_to_rotate = 0
            #     direction = -1
                
            if moving_direction == 'left': # move the current y_highlighted layer to the left
                space_axis = 1
                layer_to_rotate = cube.curr_y_highlight
                direction = 1
            elif moving_direction == 'right': # move the current y_highlighted layer to the right
                space_axis = 1
                layer_to_rotate = cube.curr_y_highlight
                direction = -1
            elif moving_direction == 'up': # move the current x_highlighted layer to the top
                space_axis = 0
                layer_to_rotate = cube.curr_x_highlight
                direction = 1
            elif moving_direction == 'down': # move the current x_highlighted layer to the bottom
                space_axis = 0
                layer_to_rotate = cube.curr_x_highlight
                direction = -1

            cube.rotate_layer(direction*5, space_axis, space_axis, layer_to_rotate)
            moving_angle += 5

            if moving_angle == 90:
                moving_angle = 0
                moving = False
                cube.cube_structure_rotate(space_axis, layer_to_rotate, direction)
                print('Current face:', cube.curr_face)
                print('Top face:', cube.top_face)
                print('Right face:', cube.right_face)
                print('Current axes:', curr_axes)
                print('Axes inversion:', axes_inversion)
                
        
        # printing the current faces of the cube and the current axes
        text = "Current face: " + cube.curr_face + "\nTop face: " + cube.top_face + "\n Right face: " + cube.right_face
        text2 = "\nCurrent axes: " + str(curr_axes) + "\nAxes inversion: " + str(axes_inversion)
        
        text_surface = font.render(text + text2, True, (255, 255, 255))  # Render the text
        text_rect = text_surface.get_rect()
        text_rect.center = (width_display // 4, height_display // 4)  # Set the position of the text
        window.blit(text_surface, text_rect)  # Blit the text onto the window surface
        
        # draw the cube
        # cube.draw()
        cube.draw_all_faces()
        
        pygame.display.flip()
        # pygame.display.update()
        # pygame.time.wait(1)
        
        
        clock.tick(800)
        # pygame.time.wait(1)

    
if __name__ == "__main__":
    game_loop()