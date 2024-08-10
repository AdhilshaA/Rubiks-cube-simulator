from vpython import *
# scene2 = canvas(title='Examples of Tetrahedrons',
#      width=600, height=200,
#      center=vector(0,0,0), background=color.cyan)

# def cube_part(part,colors):
#     if part == "c":
#         if len(colors) != 3:
#             return "Wrong colors or part!"
#         L = [box(size=vector(1,1,0.1),pos=vector(0,0,0),color=color.red),
#              box(size=vector(1,1,0.1),pos = vector(0,0,0.7)),
#              box(size=vector(1,0.1,1),pos = vector(0,0,0),color=color.blue),
#              box(size=vector(1,0.1,1),pos = vector(0,0.7,0)),
#              box(size=vector(0.1,1,1),pos = vector(0,0,0),color=color.green),
#              box(size=vector(0.1,1,1),pos = vector(0.7,0,0))]
#         return compound(L)
    
# q1 = cube_part("c",["red","green","blue"])
# # q1 = box(size=(1,1,0.1),pos=(0,0,0),color=color.red)
# # mybox = box(canvas=scene2,pos=(0,0,0),axis=(1,1,1), length=1,
#     # height=1, width=1)
# # q1.pos = (0,0,0)
# q1.canvas = scene2

    
# # b1 = box(canvas = scene2)
# # scene2.range = 20
# # ball = sphere(canvas = scene2,color=color.red)
# # v = vec(0,0,0)
# # dv = 0.2
# # dt = 0.01
# while True:
#     # key = scene2.kb.getkey()
    
#     rate(30)
#     # k = keysdown() # a list of keys that are down
#     # if 'left' in k: v.x -= dv
#     # if 'right' in k: v.x += dv
#     # if 'down' in k: v.y -= dv
#     # if 'up' in k: v.y += dv
#     # ball.pos += v*dt


# scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
# To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
#     On a two-button mouse, middle is left + right.
# Shift-drag to pan left/right and up/down.
# Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""

# side = 4.0
# thk = 0.3
# s2 = 2*side - thk
# s3 = 2*side + thk

# wallR = box (pos=vector( side, 0, 0), size=vector(thk, s2, s3),  color = color.red)
# wallL = box (pos=vector(-side, 0, 0), size=vector(thk, s2, s3),  color = color.red)
# wallB = box (pos=vector(0, -side, 0), size=vector(s3, thk, s3),  color = color.blue)
# wallT = box (pos=vector(0,  side, 0), size=vector(s3, thk, s3),  color = color.blue)
# wallBK = box(pos=vector(0, 0, -side), size=vector(s2, s2, thk), color = color.gray(0.7))

# ball = sphere (color = color.green, radius = 0.4, make_trail=True, retain=200)
# ball.mass = 1.0
# ball.p = vector (-0.15, -0.23, +0.27)

# side = side - thk*0.5 - ball.radius

# dt = 0.3
# def move():
#     while True:
#             rate(200)
#             ball.pos = ball.pos + (ball.p/ball.mass)*dt
#             if not (side > ball.pos.x > -side):
#                 ball.p.x = -ball.p.x
#             if not (side > ball.pos.y > -side):
#                 ball.p.y = -ball.p.y
#             if not (side > ball.pos.z > -side):
#                 ball.p.z = -ball.p.z

# move()

def make_cube():
    side = 4.0
    thk = 0.3
    s2 = 2*side - thk
    s3 = 2*side + thk

    wallR = box (pos=vector( side, 0, 0), size=vector(thk, s2, s3))
    wallL = box (pos=vector(-side, 0, 0), size=vector(thk, s2, s3),  color = color.red)
    wallB = box (pos=vector(0, -side, 0), size=vector(s3, thk, s3),  color = color.blue)
    wallT = box (pos=vector(0,  side, 0), size=vector(s3, thk, s3))
    wallBK = box(pos=vector(0, 0, -side), size=vector(s2, s2, thk), color = color.green)
    wallFT = box(pos=vector(0, 0, side), size=vector(s2, s2, thk))
    q1 = compound([wallB,wallBK,wallFT,wallL,wallR,wallT])
    q1.pos=vector((1,1,1))
    
    twowallR = box (pos=vector( side, 0, 0), size=vector(thk, s2, s3))
    twowallL = box (pos=vector(-side, 0, 0), size=vector(thk, s2, s3),  color = color.red)
    twowallB = box (pos=vector(0, -side, 0), size=vector(s3, thk, s3),  color = color.blue)
    twowallT = box (pos=vector(0,  side, 0), size=vector(s3, thk, s3))
    twowallBK = box(pos=vector(0, 0, -side), size=vector(s2, s2, thk), color = color.green)
    twowallFT = box(pos=vector(0, 0, side), size=vector(s2, s2, thk))
    q2 = compound([twowallB,twowallBK,twowallFT,twowallL,twowallR,twowallT])
    q2.pos=vector((1+side+thk,1,1))
    
make_cube()

while True:
    rate(30)
