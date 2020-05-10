import math

e = (25, 25)
s = (1, 1)
theta = (s[1] - e[1]) / (s[0] - e[0])
(d1, d2) = 2 ** (1/2), 2 ** (1/2)
(x1, y1) = (s[0] + d1*math.sin(math.atan(theta)),
            s[1] - d1*math.cos(math.atan(theta)))
(x2, y2) = (e[0] - d2*math.sin(math.atan(theta)),
            e[1] + d2*math.cos(math.atan(theta)))
print(x1, x2, y1, y2, theta)

equ = lambda x, y, xp, yp, m: (yp - y) - m*(xp - x)

x, y = (5, 5)
print(equ(x1, y1, x, y, theta) > 0,
      equ(x1, y1, x, y, -1/theta) < 0,
      equ(x2, y2, x, y, theta) < 0,
      equ(x2, y2, x, y, -1/theta) > 0)

if equ(x1, y1, x, y, math.tan(math.degrees(theta))) > 0 \
                        and equ(x1, y1, x, y, math.tan(math.degrees(-1/theta))) > 0 \
                        and equ(x2, y2, x, y, math.tan(math.degrees(theta))) < 0\
                        and equ(x2, y2, x, y, math.tan(math.degrees(-1/theta))) < 0:
    print('In')