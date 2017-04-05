try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
    OPENGLENABLED = True
except ImportError as e:
    OPENGLENABLED = False
    print("Unable to open OpenGL, OpenGLPrinter won't be available:", e)

import time
import math
import threading


class bcolors:
    BLUE = '\033[44m'
    GREEN = '\033[102m'
    YELLOW = '\033[103m'
    RED = '\033[101m'
    WHITE = '\033[107m'
    ORANGE = '\033[48;5;214m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Printer(object):
    def __init__(self, cube):
        self._cube = cube

    @property
    def cube(self):
        '''
        Initial implementation worked with NaiveCube, this hack the whole class accesses to self.cube
        to work the same way as before
        '''
        return self._cube.to_naive_cube()

    def pprint(self):
        pass


class TtyPrinter(Printer):
    def __init__(self, cube, colours=False):
        self.colours = colours
        super(TtyPrinter, self).__init__(cube)

    def pprint(self):
        self.print_upper()
        self.print_center()
        self.print_down()

    def print_upper(self):
        for i in xrange(self.cube.size * 2 + 1):
            print(' ' * (self.cube.size * 6), end = '')
            if (i % 2) == 0:
                for j in xrange(self.cube.size * 2):
                    if (j % 2) == 0:
                        print('|', end = '')
                    else:
                        print('---', end = '')
                print('|')
            else:
                for j in xrange(self.cube.size * 2):
                    if (j % 2) == 0:
                        print('|', end = '')
                    else:
                        self.print_square(
                            int(i / 2), int(j / 2), self.cube.faces['U'].get_colour(int(i / 2), int(j / 2)))
                print('|')

    def print_center(self):
        for i in xrange(self.cube.size * 2 + 1):
            for face in ['L', 'F', 'R', 'B']:
                if (i % 2) == 0:
                    for j in xrange(self.cube.size * 2):
                        if (j % 2) == 0:
                            print('|', end = '')
                        else:
                            print('---', end = '')
                else:
                    for j in xrange(self.cube.size * 2):
                        if (j % 2) == 0:
                            print('|', end = '')
                        else:
                            self.print_square(
                                int(i / 2), int(j / 2), self.cube.faces[face].get_colour(int(i / 2), int(j / 2)))
                print('|', end = '')
            print()

    def print_down(self):
        for i in xrange(self.cube.size * 2 + 1):
            print(' ' * (self.cube.size * 6), end = '')
            if (i % 2) == 0:
                for j in xrange(self.cube.size * 2):
                    if (j % 2) == 0:
                        print('|', end = '')
                    else:
                        print('---', end = '')
                print('|')
            else:
                for j in xrange(self.cube.size * 2):
                    if (j % 2) == 0:
                        print('|', end = '')
                    else:
                        self.print_square(
                            int(i / 2), int(j / 2), self.cube.faces['D'].get_colour(int(i / 2), int(j / 2)))
                print('|')

    def print_square(self, x, y, c):
        if self.colours:
            if c == 'w':
                print(bcolors.WHITE, end = '')
            elif c == 'b':
                print(bcolors.BLUE, end = '')
            elif c == 'g':
                print(bcolors.GREEN, end = '')
            elif c == 'r':
                print(bcolors.RED,)
            elif c == 'y':
                print(bcolors.YELLOW, end = '')
            elif c == 'o':
                print(bcolors.ORANGE, end = '')
            print(' ', bcolors.ENDC, end = '')
        else:
            print(c.upper(), end = '')


class OpenGLPrinter(Printer):
    COLORS = {
        'w': (1.0, 1.0, 1.0),
        'r': (1.0, 0.0, 0.0),
        'g': (0.0, 1.0, 0.0),
        'b': (0.0, 0.0, 1.0),
        'y': (1.0, 1.0, 0.0),
        'o': (1.0, 0.5, 0.0),
        '.': (0.5, 0.5, 0.5),
    }

    def __init__(self, cube):
        self.fov = 45
        self.zNear = 0.1
        self.zFar = 50.0
        if OPENGLENABLED:
            super(OpenGLPrinter, self).__init__(cube)
        self.display = (800, 600)
        self.alfa = 45.0
        self.beta = 45.0
        self.radius = 6.0
        self.thread = None

    def stop(self):
        if self.thread:
            glutLeaveMainLoop()

    def pprint(self):
        if OPENGLENABLED:
            self.thread = threading.Thread(target=self._pprint)
            self.thread.start()

    def _pprint(self):
        glutInit()
        glutInitWindowSize(640, 480)
        glutCreateWindow("Rubik Printer")

        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)
        glutDisplayFunc(self.displayFun)
        glutIdleFunc(self.idleFun)
        glutKeyboardFunc(self.inputKeyboard)
        glutSpecialFunc(self.specialInputKeyboard)
        glutMainLoop()

    def idleFun(self):
        time.sleep(0.5)
        glutPostRedisplay()

    def specialInputKeyboard(self, key, x, y):
        if key == 100:  # Left arrow
            self.alfa -= 5.0
        elif key == 102:  # Right arrow
            self.alfa += 5.0
        elif key == 101:  # Up arrow
            self.beta += 5.0
        elif key == 103:  # Down arrow
            self.beta -= 5.0
        elif key == 104:  # Page down
            self.radius -= 0.5
        elif key == 105:  # Page up
            self.radius += 0.5

        self.alfa %= 360.0
        self.beta %= 360.0

        glutPostRedisplay()

    def inputKeyboard(self, key, x, y):
        if key in 'fbrlud':
            self.cube.move(key.upper())

        glutPostRedisplay()

    def lookAt(self):
        alfaRad = math.radians(self.alfa)
        betaRad = math.radians(self.beta - 180.0)
        viewX = math.sin(alfaRad) * self.radius
        viewY = math.sin(betaRad) * math.sin(alfaRad) * self.radius
        viewZ = math.cos(alfaRad) * self.radius

        gluLookAt(viewX, viewY, viewZ, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    def displayFun(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # gluLookAt(-75.0, -75.0, -75.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        self.lookAt()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.threeAxis(4)

        glPushMatrix()
        # Translate cube to coordinates origin
        glTranslatef(-self.cube.size / 2.0, -self.cube.size /
                     2.0, -self.cube.size / 2.0)
        self.drawCube()
        glPopMatrix()
        glFlush()

    def drawCube(self):
        """Draw a multicolored cube"""
        glBegin(GL_QUADS)
        for i in range(self.cube.size):
            for j in range(self.cube.size):
                glColor3f(*self.COLORS[self.cube.faces['F'].get_colour(i, j)])
                glVertex3f(self.cube.size - 1 + 0.0 - j,
                           self.cube.size - 1 + 0.0 - i, 0.0)
                glVertex3f(self.cube.size - 1 + 1.0 - j,
                           self.cube.size - 1 + 0.0 - i, 0.0)
                glVertex3f(self.cube.size - 1 + 1.0 - j,
                           self.cube.size - 1 + 1.0 - i, 0.0)
                glVertex3f(self.cube.size - 1 + 0.0 - j,
                           self.cube.size - 1 + 1.0 - i, 0.0)

        for i in range(self.cube.size):
            for j in range(self.cube.size):
                glColor3f(
                    *self.COLORS[self.cube.faces['B'].get_colour(i, self.cube.size - 1 - j)])
                # glColor3f(*self.cube.faces['B'].get_colour(i, j))
                glVertex3f(self.cube.size - 1 + 0.0 - j,
                           self.cube.size - 1 + 0.0 - i, self.cube.size)
                glVertex3f(self.cube.size - 1 + 1.0 - j,
                           self.cube.size - 1 + 0.0 - i, self.cube.size)
                glVertex3f(self.cube.size - 1 + 1.0 - j,
                           self.cube.size - 1 + 1.0 - i, self.cube.size)
                glVertex3f(self.cube.size - 1 + 0.0 - j,
                           self.cube.size - 1 + 1.0 - i, self.cube.size)

        for i in range(self.cube.size):
            for j in range(self.cube.size):
                # glColor3f(*self.cube.faces['D'].get_colour(i, j))
                glColor3f(
                    *self.COLORS[self.cube.faces['D'].get_colour(self.cube.size - 1 - i, j)])
                glVertex3f(self.cube.size - 1 + 0.0 - j,
                           0.0, self.cube.size - 1 + 1.0 - i)
                glVertex3f(self.cube.size - 1 + 1.0 - j,
                           0.0, self.cube.size - 1 + 1.0 - i)
                glVertex3f(self.cube.size - 1 + 1.0 - j,
                           0.0, self.cube.size - 1 + 0.0 - i)
                glVertex3f(self.cube.size - 1 + 0.0 - j,
                           0.0, self.cube.size - 1 + 0.0 - i)

        for i in range(self.cube.size):
            for j in range(self.cube.size):
                # glColor3f(*self.cube.faces['U'].get_colour(i, j))
                glColor3f(*self.COLORS[self.cube.faces['U'].get_colour(i, j)])
                glVertex3f(self.cube.size - 1 + 0.0 - j,
                           self.cube.size, self.cube.size - 1 + 1.0 - i)
                glVertex3f(self.cube.size - 1 + 0.0 - j,
                           self.cube.size, self.cube.size - 1 + 0.0 - i)
                glVertex3f(self.cube.size - 1 + 1.0 - j,
                           self.cube.size, self.cube.size - 1 + 0.0 - i)
                glVertex3f(self.cube.size - 1 + 1.0 - j,
                           self.cube.size, self.cube.size - 1 + 1.0 - i)

        for i in range(self.cube.size):
            for j in range(self.cube.size):
                # glColor3f(*self.cube.faces['R'].get_colour(i, j))
                glColor3f(
                    *self.COLORS[self.cube.faces['R'].get_colour(i, self.cube.size - 1 - j)])
                glVertex3f(0.0, self.cube.size - 1 + 1.0 -
                           i, self.cube.size - 1 + 0.0 - j)
                glVertex3f(0.0, self.cube.size - 1 + 0.0 -
                           i, self.cube.size - 1 + 0.0 - j)
                glVertex3f(0.0, self.cube.size - 1 + 0.0 -
                           i, self.cube.size - 1 + 1.0 - j)
                glVertex3f(0.0, self.cube.size - 1 + 1.0 -
                           i, self.cube.size - 1 + 1.0 - j)

        for i in range(self.cube.size):
            for j in range(self.cube.size):
                # glColor3f(*self.cube.faces['L'].get_colour(i, j))
                glColor3f(*self.COLORS[self.cube.faces['L'].get_colour(i,  j)])
                glVertex3f(self.cube.size, self.cube.size - 1 +
                           1.0 - i, self.cube.size - 1 + 0.0 - j)
                glVertex3f(self.cube.size, self.cube.size - 1 +
                           0.0 - i, self.cube.size - 1 + 0.0 - j)
                glVertex3f(self.cube.size, self.cube.size - 1 +
                           0.0 - i, self.cube.size - 1 + 1.0 - j)
                glVertex3f(self.cube.size, self.cube.size - 1 +
                           1.0 - i, self.cube.size - 1 + 1.0 - j)
        glEnd()

    def axis(self, length):
        """ Draws an axis (basicly a line with a cone on top) """
        glPushMatrix()
        glBegin(GL_LINES)
        glVertex3d(0, 0, 0)
        glVertex3d(0, 0, length)
        glEnd()
        glTranslated(0, 0, length)
        glutWireCone(0.04, 0.2, 12, 9)
        glPopMatrix()

    def threeAxis(self, length):
        """ Draws an X, Y and Z-axis """

        glPushMatrix()
        # Z-axis
        glColor3f(1.0, 0.0, 0.0)
        self.axis(length)
        # X-axis
        glRotated(90, 0, 1.0, 0)
        glColor3f(0.0, 1.0, 0.0)
        self.axis(length)
        # Y-axis
        glRotated(-90, 1.0, 0, 0)
        glColor3f(0.0, 0.0, 1.0)
        self.axis(length)
        glPopMatrix()
