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

# write the game loop

class Font:
    def __init__(self, font_color = (255, 255, 255), font_size = 1, background_color = (0, 0, 0), alphabet_vertex: dict = None, font_stroke = None) -> None:
        self.font_color = [x/255 for x in font_color]
        self.font_size = font_size
        self.background_color = [x/255 for x in background_color]
        if font_stroke is None:
            self.font_stroke = font_size * 5
        else:
            self.font_stroke = font_stroke
        
        # alphabets in 2D as lines in a square bound by (0,0) and (1,1)
        if alphabet_vertex is None:
            self.alphabet_vertex = {
                'A': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.85, 0.9], [0.85, 0.9], [0.85, 0.1], [0.15, 0.5], [0.85, 0.5]],
                'B': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.8, 0.9], [0.8, 0.9], [0.85, 0.8], [0.85, 0.8], [0.85, 0.2], [0.85, 0.2], [0.8, 0.1], [0.15, 0.5], [0.85, 0.5], [0.8, 0.1], [0.15, 0.1]],
                'C': [[0.85, 0.1], [0.15, 0.1], [0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.85, 0.9]],
                'D': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.8, 0.9], [0.8, 0.9], [0.85, 0.8], [0.85, 0.8], [0.85, 0.2], [0.85, 0.2], [0.8, 0.1], [0.8, 0.1], [0.15, 0.1]],
                'E': [[0.85, 0.1], [0.15, 0.1], [0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.85, 0.9], [0.85, 0.5], [0.15, 0.5]],
                'F': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.85, 0.9], [0.85, 0.5], [0.15, 0.5]],
                'G': [[0.85, 0.1], [0.15, 0.1], [0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.85, 0.9], [0.85, 0.5], [0.5, 0.5], [0.85, 0.5], [0.85, 0.1]],
                'H': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.5], [0.85, 0.5], [0.85, 0.1], [0.85, 0.9]],
                'I': [[0.5, 0.1], [0.5, 0.9], [0.15, 0.1], [0.85, 0.1], [0.15, 0.9], [0.85, 0.9]],
                'J': [[0.5, 0.1], [0.5, 0.9], [0.15, 0.1], [0.5, 0.1], [0.15, 0.9], [0.85, 0.9], [0.15, 0.5], [0.15, 0.1]],
                'K': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.5], [0.85, 0.9], [0.15, 0.5], [0.85, 0.1]],
                'L': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.1], [0.85, 0.1]],
                'M': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.5, 0.5], [0.5, 0.5], [0.85, 0.9], [0.85, 0.9], [0.85, 0.1]],
                'N': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.85, 0.1], [0.85, 0.1], [0.85, 0.9]],
                'O': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.85, 0.9], [0.85, 0.9], [0.85, 0.1], [0.85, 0.1], [0.15, 0.1]],
                'P': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.85, 0.9], [0.85, 0.9], [0.85, 0.5], [0.85, 0.5], [0.15, 0.5]],
                'Q': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.85, 0.9], [0.85, 0.9], [0.85, 0.1], [0.85, 0.1], [0.15, 0.1], [0.5, 0.5], [0.85, 0.1]],
                'R': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.85, 0.9], [0.85, 0.9], [0.85, 0.5], [0.85, 0.5], [0.15, 0.5], [0.15, 0.5], [0.85, 0.1]],
                'S': [[0.85, 0.1], [0.15, 0.1], [0.85, 0.1], [0.85, 0.5], [0.15, 0.5], [0.85, 0.5], [0.15, 0.5], [0.15, 0.9], [0.85, 0.9], [0.15, 0.9]],
                'T': [[0.15, 0.9], [0.85, 0.9], [0.5, 0.1], [0.5, 0.9]],
                'U': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.1], [0.85, 0.1], [0.85, 0.9], [0.85, 0.1]],
                'V': [[0.15, 0.9], [0.5, 0.1], [0.5, 0.1], [0.85, 0.9]],
                'W': [[0.15, 0.9], [0.15, 0.1], [0.15, 0.1], [0.5, 0.5], [0.5, 0.5], [0.85, 0.1], [0.85, 0.1], [0.85, 0.9]],
                'X': [[0.15, 0.1], [0.85, 0.9], [0.15, 0.9], [0.85, 0.1]],
                'Y': [[0.15, 0.1], [0.15, 0.25], [0.15,0.5], [0.15, 0.9], [0.15, 0.1], [0.85, 0.1], [0.85, 0.9], [0.85, 0.1], [0.15, 0.5], [0.85, 0.5]],
                'Z': [[0.15, 0.9], [0.85, 0.9], [0.15, 0.1], [0.85, 0.1], [0.15, 0.1], [0.85, 0.9]],
                '0': [[0.15, 0.25], [0.15, 0.75], [0.25, 0.9], [0.75, 0.9], [0.85, 0.75], [0.85, 0.25], [0.75, 0.1], [0.25, 0.1], [0.15, 0.4], [0.85, 0.6], [0.25, 0.1], [0.15, 0.25], [0.15, 0.75], [0.25, 0.9], [0.75, 0.9], [0.85, 0.75], [0.85, 0.25], [0.75, 0.1]],
                '1': [[0.25, 0.9], [0.55 , 0.9], [0.55, 0.9], [0.55, 0.1], [0.85, 0.1], [0.15, 0.1], [0.15, 0.75], [0.25, 0.9]],
                '2': [[0.15, 0.1], [0.15, 0.5], [0.25, 0.9], [0.85, 0.9], [0.85, 0.5], [0.85, 0.9], [0.75, 0.1], [0.15, 0.1], [0.15, 0.5], [0.85, 0.5], [0.15, 0.75], [0.25, 0.9], [0.85, 0.25], [0.75, 0.1]],
                '3': [[0.25, 0.9], [0.85, 0.9], [0.85, 0.9], [0.85, 0.1], [0.85, 0.1], [0.25, 0.1], [0.18, 0.5], [0.85, 0.5], [0.25, 0.1], [0.15, 0.25], [0.15, 0.75], [0.25, 0.9]],
                '4': [[0.15, 0.9], [0.15, 0.5], [0.15, 0.5], [0.85, 0.5], [0.85, 0.1], [0.85, 0.9]],
                '5': [[0.15, 0.5], [0.15, 0.9], [0.15, 0.9], [0.75, 0.9], [0.85, 0.5], [0.85, 0.1], [0.85, 0.1], [0.25, 0.1], [0.15, 0.5], [0.85, 0.5], [0.25, 0.1], [0.15, 0.25], [0.75, 0.9], [0.85, 0.75]],
                '6': [[0.85, 0.1], [0.15, 0.1], [0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.75, 0.9], [0.85, 0.5], [0.15, 0.5], [0.85, 0.5], [0.85, 0.1], [0.75, 0.9], [0.85, 0.75]],
                '7': [[0.25, 0.9], [0.85, 0.9], [0.85, 0.9], [0.85, 0.1], [0.15, 0.75], [0.25, 0.9]],
                '8': [[0.15, 0.1], [0.15, 0.9], [0.15, 0.9], [0.85, 0.9], [0.85, 0.9], [0.85, 0.1], [0.85, 0.1], [0.15, 0.1], [0.15, 0.5], [0.85, 0.5]],
                '9': [[0.15, 0.5], [0.15, 0.9], [0.15, 0.9], [0.85, 0.9], [0.85, 0.9], [0.85, 0.1], [0.85, 0.1], [0.25, 0.1], [0.15, 0.5], [0.85, 0.5], [0.25, 0.1], [0.15, 0.25]],
                '-': [[0.15, 0.5], [0.85, 0.5]],
                ':': [[0.5, 0.85], [0.5, 0.7], [0.5, 0.3], [0.5, 0.15]],
                '=': [[0.15, 0.4], [0.85, 0.4], [0.15, 0.6], [0.85, 0.6]],
                '+': [[0.15, 0.5], [0.85, 0.5], [0.5, 0.15], [0.5, 0.85]],
                '*': [[0.25, 0.25], [0.75, 0.75], [0.25, 0.75], [0.75, 0.25]],
                '/': [[0.25, 0.1], [0.75, 0.9]],
                '.': [[0.45, 0.1], [0.55, 0.1]],
                ',': [[0.5, 0.4], [0.5, 0.25], [0.5, 0.25], [0.4, 0.1]],
                '?': [[0.25, 0.9], [0.85, 0.9], [0.85, 0.85], [0.85, 0.5], [0.5, 0.5], [0.85, 0.5], [0.15, 0.75], [0.25, 0.9], [0.75, 0.9], [0.85, 0.75], [0.5, 0.5], [0.5, 0.25], [0.45, 0.1], [0.55, 0.1]],
            }
        else:
            self.alphabet_vertex = alphabet_vertex
        
        self.alphabet_vertex = {key: np.array(value) for key, value in self.alphabet_vertex.items()}
        
    def __call__(self):
        return self.font_color, self.font_size, self.background_color, self.font_stroke, self.alphabet_vertex

class Text:
    def __init__(self) -> None:
        pass
    
    def draw_alphabet(self, alphabet, x, y, font_instance = Font()): 
        
               
        if alphabet not in font_instance.alphabet_vertex.keys():
            return
        
        glBegin(GL_LINES)
        vertices = (np.copy(font_instance.alphabet_vertex[alphabet]) * font_instance.font_size) + np.array([x, y])
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()
            
    def draw_text_background(self, text, x, y, padding = (0, 0, 0, 0), font_instance = Font()):
        # padding is of the form (left, right, top, bottom)
        
        # draw the background
        glColor3fv(font_instance.background_color)
        text_length = len(text) * font_instance.font_size
        text_height = font_instance.font_size
        z = - 1e-2
        y_adjust = - y * 5e-2
        y_adjust = 0
        corners = np.array([[x - padding[0], y + y_adjust + text_height + padding[2], z], [x + text_length + padding[1], y + y_adjust + text_height + padding[2], z], [x + text_length + padding[1], y + y_adjust - padding[3], z], [x - padding[0], y + y_adjust - padding[3], z]])

        glBegin(GL_QUADS)
        for corner in corners:
            glVertex3fv(corner)
        glEnd()
        
    def draw_text(self, text, x, y, font_instance = Font()):
        
        glLineWidth(font_instance.font_stroke)
        glColor3fv(font_instance.font_color)
        for alphabet in text:
            self.draw_alphabet(alphabet, x, y, font_instance=font_instance)
            x += (1 * font_instance.font_size)

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
                # print("up")
                self.cube_structure[layer, :, :] = np.rot90(curr_layer, axes=(1, 0))
            else:
                # print("down")
                self.cube_structure[layer, :, :] = np.rot90(curr_layer, axes=(0, 1))
                
        elif axis == 1:
            curr_layer = np.copy(self.cube_structure[:, layer, :])
            if direction == 1:
                # print("right",curr_layer.shape)
                self.cube_structure[:, layer, :] = np.rot90(curr_layer, axes=(0, 1))
            else:
                # print("left", curr_layer.shape)
                self.cube_structure[:, layer, :] = np.rot90(curr_layer, axes=(1, 0))
        
        elif axis == 2:
            curr_layer = np.copy(self.cube_structure[:, :, layer])
            if direction == 1:
                # print("clockwise")
                self.cube_structure[:, :, layer] = np.rot90(curr_layer, axes=(1, 0))
            else:
                # print("anti-clockwise")
                self.cube_structure[:, :, layer] = np.rot90(curr_layer, axes=(0, 1))
                
    
    # def opposite_face(self, face):
    #     if face == 'front':
    #         return 'back'
    #     elif face == 'back':
    #         return 'front'
    #     elif face == 'left':
    #         return 'right'
    #     elif face == 'right':
    #         return 'left'
    #     elif face == 'top':
    #         return 'bottom'
    #     else:
    #         return 'top'
        
    # def get_current_axes(self):
    #     axes = [0, 1, 2]
    #     axes_inversion = [False, False, False]
    #     def get_axis_from_face(face):
    #         if face == 'front':
    #             return 2, False
    #         elif face == 'back':
    #             return 2, True
    #         elif face == 'right':
    #             return 0, False
    #         elif face == 'left':
    #             return 0, True
    #         elif face == 'top':
    #             return 1, False
    #         else:
    #             return 1, True
        
    #     axes[0], axes_inversion[0] = get_axis_from_face(self.right_face)
    #     axes[1], axes_inversion[1] = get_axis_from_face(self.top_face)
    #     axes[2], axes_inversion[2] = get_axis_from_face(self.curr_face)
        
    #     return axes, axes_inversion
            
    
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
                        
    def check_cube(self):
        # final_check = False
        # for i in range(4):
        #     self.rotate_layer(90, 0, 0, 0)
        #     self.rotate_layer(90, 0, 0, 1)
        #     self.rotate_layer(90, 0, 0, 2)
        #     final_check = self.__check_cube()
        #     if final_check:
        #         break
        return self.__check_cube()
        
    def __check_cube(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if self.cube_structure[i, j, k][0] != i or self.cube_structure[i, j, k][1] != j or self.cube_structure[i, j, k][2] != k:
                        return False
        return True

# def draw_text(text, x, y):
    

def game_loop():
    
    
    cube = Cube()
    title_font = Font(font_color = (255, 255, 255), font_size = 0.6, background_color = (102, 0, 51))
    button_font = Font(font_color = (0, 0, 0), font_size = 0.3, background_color = (255, 255, 0))
    sub_button_font = Font(font_color = (0, 0, 0), font_size = 0.2, background_color = (255, 255, 255), font_stroke=2)
    
    sub_header_font = Font(font_color = (0, 0, 0), font_size = 0.15, background_color = (0, 255, 0), font_stroke=2)
    sub_content_font = Font(font_color = (0, 0, 0), font_size = 0.125, background_color = (255, 255, 255), font_stroke=1.5)
    
    sub_header_font2 = Font(font_color = (0, 0, 0), font_size = 0.15, background_color = (255, 255, 0), font_stroke=2)
    sub_content_font2 = Font(font_color = (0, 0, 0), font_size = 0.125, background_color = (255, 255, 255), font_stroke=1.5)
    
    text_type = Text()
    
    
    pygame.init()
    clock = pygame.time.Clock()


    # # setting up the background with image
    background = pygame.image.load(curr_path + fig_path + r"\bg.png")
    background = pygame.transform.scale(background, (width_display, height_display))

    window = pygame.display.set_mode((width_display, height_display), DOUBLEBUF|OPENGL)
        
    pygame.display.set_caption(window_title)
    
    rotate = False
    rotate_direction = ''
    rotate_angle = 0
    
    
    moving = False
    moving_direction = ''
    moving_angle = 0
    
    started = False
    shuffling = False
    shuffle_moves = 100
    
    cube_check = False
    
    shuffling_patience = 180
    
    time_passed = 0
    
    window.blit(background, (0, 0))
    
    angle_change = 9 #6, 9, 10, 15
    
    # curr_axes, axes_inversion = cube.get_current_axes()
    
    # set up OpenGL
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, (width_display/height_display), 0.2, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0,-1, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                
                if rotate or moving or shuffling:
                    pass
                elif not started or cube_check:
                    if event.key == pygame.K_SPACE:
                        started = True
                        shuffling = True
                        cube_check = False
                elif event.key == pygame.K_LEFT: # press 'left' to rotate the cube to the left
                    rotate = True
                    rotate_direction = 'left'
                elif event.key == pygame.K_RIGHT: # press 'right' to rotate the cube to the right
                    rotate = True
                    rotate_direction = 'right'
                elif event.key == pygame.K_UP:  # press 'up' to rotate the cube to the top
                    rotate = True
                    rotate_direction = 'up'
                elif event.key == pygame.K_DOWN: # press 'down' to rotate the cube to the bottom
                    rotate = True
                    rotate_direction = 'down'
        
                elif event.key == pygame.K_a: # press 'a' to move the current y_highlighted layer to the left
                    # curr_axes, axes_inversion = cube.get_current_axes()
                    moving = True
                    moving_direction = 'left'
                elif event.key == pygame.K_d: # press 'd' to move the current y_highlighted layer to the right
                    # curr_axes, axes_inversion = cube.get_current_axes()
                    moving = True
                    moving_direction = 'right'
                elif event.key == pygame.K_w: # press 'w' to move the current x_highlighted layer to the top
                    # curr_axes, axes_inversion = cube.get_current_axes()
                    moving = True
                    moving_direction = 'up'
                elif event.key == pygame.K_s: # press 's' to move the current y_highlighted layer to the bottom
                    # curr_axes, axes_inversion = cube.get_current_axes()
                    moving = True
                    moving_direction = 'down'
                elif event.key == pygame.K_e: # press 'q' to change the current face to the left face
                    # curr_axes, axes_inversion = cube.get_current_axes()
                    moving = True
                    moving_direction = 'face_right'
                elif event.key == pygame.K_q: # press 'e' to change the current face to the right face
                    # curr_axes, axes_inversion = cube.get_current_axes()
                    moving = True
                    moving_direction = 'face_left'
                elif event.key == pygame.K_BACKSPACE:
                    shuffling = True
                elif event.key == pygame.K_END:
                    cube_check = cube.check_cube()
                
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
        
        if shuffling:
            
            if shuffling_patience != 0:
                shuffling_patience -= 1
            
            elif rotate or moving:
                pass
            else:
                if shuffle_moves == 0:
                    shuffling = False
                    shuffle_moves = 100
                    shuffling_patience = 180
                    time_passed = 0
                else:
                    shuffle_moves -= 1
                    move = np.random.choice(['rotate', 'move'])
                    if move == 'rotate':
                        shuffle_direction = np.random.choice(['left', 'right', 'up', 'down'])
                        
                        rotate = True
                        rotate_direction = shuffle_direction
                    else:
                        axis = np.random.choice([0, 1, 2])
                        axis_change = np.random.choice([1, -1, 0])
                        x_highlight = np.random.choice([0, 1, 2])
                        y_highlight = np.random.choice([0, 1, 2])
                        
                        cube.curr_x_highlight = x_highlight
                        cube.curr_y_highlight = y_highlight
                        if axis == 0:
                            if axis_change == 1:
                                moving = True
                                moving_direction = 'right'
                            elif axis_change == -1:
                                moving = True
                                moving_direction = 'left'
                        elif axis == 1:
                            if axis_change == 1:
                                moving = True
                                moving_direction = 'up'
                            elif axis_change == -1:
                                moving = True
                                moving_direction = 'down'
                        else:
                            if axis_change == 1:
                                moving = True
                                moving_direction = 'face_left'
                            elif axis_change == -1:
                                moving = True
                                moving_direction = 'face_right'
        
        if cube_check:
            started = True
            text = "SOLVED"
            text_position_x = - len(text) * sub_header_font.font_size / 2
            text_position_y = 3.5
            
            text_type.draw_text_background(text, text_position_x, text_position_y, padding = (2, 2, 0.1, 0.1), font_instance = sub_header_font)
            text_type.draw_text(text, text_position_x, text_position_y, font_instance = sub_header_font)
            
            sub_text = "Time taken: " + f"{time_passed//3600:2.0f} MIN {time_passed//60:2.0f} SEC"
            text_position_x = - len(sub_text) * sub_content_font.font_size / 2
            text_position_y = 3
            
            text_type.draw_text_background(sub_text, text_position_x, text_position_y, padding = (1, 1, 0.1, 0.1), font_instance = sub_content_font)
            text_type.draw_text(sub_text, text_position_x, text_position_y, font_instance = sub_content_font)  
            
            text = "PRESS SPACE TO RESTART"
            text_position_x = - len(text) * sub_header_font2.font_size / 2
            text_position_y = 2
            
            text_type.draw_text_background(text, text_position_x, text_position_y, padding = (1, 1, 0.1, 0.1), font_instance = sub_header_font2)
            text_type.draw_text(text, text_position_x, text_position_y, font_instance = sub_header_font2)     
        
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
            cube.rotate_layer(direction*angle_change, space_axis, space_axis, 0)
            cube.rotate_layer(direction*angle_change, space_axis, space_axis, 1)
            cube.rotate_layer(direction*angle_change, space_axis, space_axis, 2)
            rotate_angle += angle_change
                
            if rotate_angle == 90:
                rotate_angle = 0
                rotate = False
                # if rotate_direction == 'left':
                #     cube.curr_face, cube.right_face = cube.right_face, cube.opposite_face(cube.curr_face)
                # elif rotate_direction == 'right':
                #     cube.curr_face, cube.right_face = cube.opposite_face(cube.right_face), cube.curr_face
                # elif rotate_direction == 'up':
                #     cube.curr_face, cube.top_face = cube.opposite_face(cube.top_face), cube.curr_face
                # elif rotate_direction == 'down':
                #     cube.curr_face, cube.top_face = cube.top_face, cube.opposite_face(cube.curr_face)
                # curr_axes,axes_inversion = cube.get_current_axes()
                
                cube.cube_structure_rotate(space_axis, 0, direction)
                cube.cube_structure_rotate(space_axis, 1, direction)
                cube.cube_structure_rotate(space_axis, 2, direction)
                
                # print('Current face:', cube.curr_face)
                # print('Top face:', cube.top_face)
                # print('Right face:', cube.right_face)
                # print('Current axes:', curr_axes)
                # print('Axes inversion:', axes_inversion)
                
                
        elif moving:       
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
            elif moving_direction == 'face_right': # move the current face to the left
                space_axis = 2
                layer_to_rotate = 2
                direction = 1
            elif moving_direction == 'face_left': # move the current face to the right
                space_axis = 2
                layer_to_rotate = 2
                direction = -1
            cube.rotate_layer(direction*angle_change, space_axis, space_axis, layer_to_rotate)
            moving_angle += angle_change

            if moving_angle == 90:
                moving_angle = 0
                moving = False
                cube.cube_structure_rotate(space_axis, layer_to_rotate, direction)
                # print('Current face:', cube.curr_face)
                # print('Top face:', cube.top_face)
                # print('Right face:', cube.right_face)
                # print('Current axes:', curr_axes)
                # print('Axes inversion:', axes_inversion)
        
        # printing the current faces of the cube and the current axes
        
        text = "THE CUBE"
        text_position_x = - len(text) * title_font.font_size / 2
        text_position_y = 5
        
        text_type.draw_text_background(text, text_position_x, text_position_y, padding = (5, 5, 0.1, 0.1), font_instance = title_font)
        text_type.draw_text(text, text_position_x, text_position_y, font_instance = title_font)
        
        if not started and not cube_check:
            button_text = "START ?"
            
            text_position_x = - len(button_text) * button_font.font_size / 2
            text_position_y = 3.5
            
            text_type.draw_text_background(button_text, text_position_x, text_position_y, padding = (1, 1, 0.1, 0.1), font_instance = button_font)
            text_type.draw_text(button_text, text_position_x, text_position_y, font_instance = button_font)
            
            sub_button_text = "PRESS SPACE"
            
            text_position_x = - len(sub_button_text) * sub_button_font.font_size / 2
            text_position_y = 3
            
            text_type.draw_text_background(sub_button_text, text_position_x, text_position_y, padding = (1, 1, 0.1, 0.1), font_instance = sub_button_font)
            text_type.draw_text(sub_button_text, text_position_x, text_position_y, font_instance = sub_button_font)
            
        elif shuffling_patience != 0 and shuffling:
            
            button_text = "SHUFFLING IN"
            
            text_position_x = - len(button_text) * button_font.font_size / 2
            text_position_y = 3.5
            
            text_type.draw_text_background(button_text, text_position_x, text_position_y, padding = (1, 1, 0.1, 0.1), font_instance = button_font)
            text_type.draw_text(button_text, text_position_x, text_position_y, font_instance = button_font)
            
            sub_button_text = str(f"{shuffling_patience/60:.1f} SEC")
            
            text_position_x = - len(sub_button_text) * sub_button_font.font_size / 2
            text_position_y = 3
            
            text_type.draw_text_background(sub_button_text, text_position_x, text_position_y, padding = (2, 2, 0.1, 0.1), font_instance = sub_button_font)
            text_type.draw_text(sub_button_text, text_position_x, text_position_y, font_instance = sub_button_font)
        
        elif shuffling_patience == 0 and shuffling:
            
            button_text = "SHUFFLING IN PROGRESS"
            
            text_position_x = - len(button_text) * button_font.font_size / 2
            text_position_y = 3.5
            
            text_type.draw_text_background(button_text, text_position_x, text_position_y, padding = (1, 1, 0.1, 0.1), font_instance = button_font)
            text_type.draw_text(button_text, text_position_x, text_position_y, font_instance = button_font)
        
        elif cube_check:
            pass
        
        else:
            
            button_text = "ROTATE"
            
            text_position_x = - len(button_text) * sub_header_font.font_size / 2 -2
            text_position_y = 4.5
            
            text_type.draw_text_background(button_text, text_position_x, text_position_y, padding = (1.2, 1.2, 0.1, 0.1), font_instance = sub_header_font)
            text_type.draw_text(button_text, text_position_x, text_position_y, font_instance = sub_header_font)
            
            sub_button_text = "PRESS LEFT/RIGHT/UP/DOWN"
            
            text_position_x = - len(sub_button_text) * sub_content_font.font_size / 2 - 2
            text_position_y = 4.1
            
            text_type.draw_text_background(sub_button_text, text_position_x, text_position_y, padding = (0.1, 0.1, 0.1, 0.1), font_instance = sub_content_font)
            text_type.draw_text(sub_button_text, text_position_x, text_position_y, font_instance = sub_content_font)
            
            button_text = "PRESS BACKSPACE TO RESET"
            
            text_position_x = - len(button_text) * sub_content_font.font_size / 2 + 2
            text_position_y = 4.5
            
            text_type.draw_text_background(button_text, text_position_x, text_position_y, padding = (0.2, 0.2, 0.1, 0.1), font_instance = sub_content_font)
            text_type.draw_text(button_text, text_position_x, text_position_y, font_instance = sub_content_font)
            
            sub_button_text = "PRESS END TO CHECK"
            
            text_position_x = - len(sub_button_text) * sub_content_font.font_size / 2 + 2
            text_position_y = 4.1
            
            text_type.draw_text_background(sub_button_text, text_position_x, text_position_y, padding = (0.4, 0.4, 0.1, 0.1), font_instance = sub_content_font)
            text_type.draw_text(sub_button_text, text_position_x, text_position_y, font_instance = sub_content_font)
            
            button_text = "MOVE"
            
            button_text = "MOVE"
            
            
            text_position_x = - len(button_text) * sub_header_font.font_size / 2 - 2
            text_position_y = 3.6
            
            text_type.draw_text_background(button_text, text_position_x, text_position_y, padding = (1.25, 1.25, 0.1, 0.1), font_instance = sub_header_font)
            text_type.draw_text(button_text, text_position_x, text_position_y, font_instance = sub_header_font)
            
            sub_button_text = "PRESS A/D/W/S/Q/E"
            
            text_position_x = - len(sub_button_text) * sub_content_font.font_size / 2 - 2
            text_position_y = 3.2
            
            text_type.draw_text_background(sub_button_text, text_position_x, text_position_y, padding = (0.5, 0.5, 0.1, 0.1), font_instance = sub_content_font)
            text_type.draw_text(sub_button_text, text_position_x, text_position_y, font_instance = sub_content_font)
            
            button_text = "CHANGE HIGHLIGHTS"
            
            text_position_x = - len(button_text) * sub_header_font.font_size / 2 + 2
            text_position_y = 3.6
            
            text_type.draw_text_background(button_text, text_position_x, text_position_y, padding = (0.3, 0.3, 0.1, 0.1), font_instance = sub_header_font)
            text_type.draw_text(button_text, text_position_x, text_position_y, font_instance = sub_header_font)
            
            sub_button_text = "PRESS I/K/J/L"
            
            text_position_x = - len(sub_button_text) * sub_content_font.font_size / 2 + 2
            text_position_y = 3.2
            
            text_type.draw_text_background(sub_button_text, text_position_x, text_position_y, padding = (0.75, 0.75, 0.1, 0.1), font_instance = sub_content_font)
            text_type.draw_text(sub_button_text, text_position_x, text_position_y, font_instance = sub_content_font)
            
            sub_header_text2 = "TIME PASSED"
            
            text_position_x = - len(sub_header_text2) * sub_header_font2.font_size / 2
            text_position_y = 2.5
            
            text_type.draw_text_background(sub_header_text2, text_position_x, text_position_y, padding = (0.7, 0.7, 0.1, 0.1), font_instance = sub_header_font2)
            text_type.draw_text(sub_header_text2, text_position_x, text_position_y, font_instance = sub_header_font2)
            
            sub_content_text2 = f"{time_passed//3600:2.0f} MIN {(time_passed//60)%60:2.0f} SEC"
            
            text_position_x = - len(sub_content_text2) * sub_content_font2.font_size / 2
            text_position_y = 2.1
            
            text_type.draw_text_background(sub_content_text2, text_position_x, text_position_y, padding = (0.75, 0.75, 0.1, 0.1), font_instance = sub_content_font2)
            text_type.draw_text(sub_content_text2, text_position_x, text_position_y, font_instance = sub_content_font2)
            
            time_passed += 1
            
            
            
            
        
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