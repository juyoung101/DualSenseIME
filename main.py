from cProfile import label
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout
from PySide6.QtCore import Qt
from pydualsense import pydualsense, TriggerModes
import pyautogui
import json
import sys

class ButtonMap():
    _bumpers = {"L1": False, "R1": False, "L2": False, "R2": False}
    _arrows = {"UA": False, "DA": False, "LA": False, "RA": False}
    _faces = {"UF": False, "DF": False, "LF": False, "RF": False}
   
    def __init__(self):
        return

    def read_state_bumpers(self):
        return self._bumpers

    def read_state_arrows(self):
        return self._arrows
    
    def read_state_faces(self):
        return self._faces

    def get_bumpers(self, value):
        return self._bumpers[value]

    def get_arrows(self, value):
        return self._arrows[value]

    def get_face(self, value):
        return self._faces[value]

    def press_bumper(self, value):
        self._bumpers[value] = True
    
    def press_arrow(self, value):
        self._arrows[value] = True

    def press_face(self, value):
        self._faces[value] = True

    def depress_bumper(self, value):
        self._bumpers[value] = False

    def depress_arrow(self, value):
        self._arrows[value] = False

    def depress_face(self, value):
        self._faces[value] = False

    def print(self):
        print(self._bumpers)
        print(self._arrows)
        print(self._faces)

class KeyMap():
    _modifiers = {"ctrl": False, "shift": False, "alt": False, "meta": False, "macro": False}
    _keys = {"a" : False, "b" : False, "c" : False, "d" : False, "e" : False, "f" : False, "g" : False, "h" : False, "i" : False, "j" : False,
                "k" : False, "l" : False, "m" : False, "n" : False, "o" : False, "p" : False, "q" : False, "r" : False, "s" : False, "t" : False,
                "u" : False, "v" : False, "w" : False, "x" : False, "y" : False, "z" : False,
                "0" : False, "1" : False, "2" : False, "3" : False, "4" : False, "5" : False, "6" : False, "7" : False, "8" : False, "9" : False,
                "space": False, "enter" : False, "backspace" : False }
    
    def __init__(self):
        return

    def read_state_modifiers(self):
        return self._modifiers

    def read_state_keys(self):
        return self._keys

    def press_modifier(self, value):
        self._modifiers[value] = True

    def press_key(self, value):
        self._keys[value] = True

    def depress_modifier(self, value):
        self._modifiers[value] = False

    def depress_key(self, value):
        self._keys[value] = False

    def get_modifier(self, value):
        return self._modifiers[value]

    def get_key(self, value):
        return self._keys[value]

    def print(self):
        print(self._modifiers)
        print(self._keys)

def test_pyautogui():
   pyautogui.typewrite('Hello world!\n', interval=0.1)
   pyautogui.hotkey('ctrl', 'shift', 'alt', 'win', 'l')
   print(pyautogui.KEYBOARD_KEYS)
   print(len(pyautogui.KEYBOARD_KEYS))

def test_pydualsense(window):
    def cross_pressed(state):
        print("Cross button state: ")
        print(state)
        window.label.setStyleSheet('background-clip: content-box; background-color: green;')

    ds = pydualsense() # open controller
    ds.init() # initialize controller

    ds.cross_pressed += cross_pressed
    ds.light.setColorI(0,255,0) # set touchpad color to green
    ds.triggerL.setMode(TriggerModes.Rigid)
    ds.triggerL.setForce(1, 255)
    print(input()) #hang for testing
   # ds.close() # closing the controller

def test_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

def test_KeyMap():
    keymap = KeyMap()
    mods = keymap.read_state_modifiers()
    keys = keymap.read_state_keys()
    keymap.print()

def test_ButtonMap():
    buttonmap = ButtonMap()
    bumpers = buttonmap.read_state_bumpers()
    arrows = buttonmap.read_state_arrows()
    faces = buttonmap.read_state_faces()
    buttonmap.print()

def run_test():
    test_KeyMap()
    test_ButtonMap()
    #test_pyautogui()
    #test_pydualsense()
    test_window()
    return

class Controller():
    def __init__(self):
        ds = pydualsense() # open controller
        self.setup(ds)
        
    def setup(self, ds):
        ds.init() # initialize controller
        ds.light.setColorI(0,255,0) # set touchpad color to green
        ds.triggerL.setMode(TriggerModes.Rigid)
        ds.triggerL.setForce(1, 255)

        
        def dpad_up_pressed(state):
            print("UP:", state)
        ds.dpad_up += dpad_up_pressed

        def dpad_left_pressed(state):
            print("LF:", state)
        ds.dpad_left += dpad_left_pressed
                
        def dpad_right_pressed(state):
            print("RT:", state)
        ds.dpad_right += dpad_right_pressed
        
        def dpad_down_pressed(state):
            print("DN:", state)
        ds.dpad_down += dpad_down_pressed

        def cross_pressed(state):
            print("Cross:", state)
        ds.cross_pressed += cross_pressed

        def square_pressed(state):
            print("Square:", state)
        ds.square_pressed += square_pressed

        def circle_pressed(state):
            print("Circle:", state)
        ds.circle_pressed += circle_pressed
        
        def triangle_pressed(state):
            print("Triangle:", state)
        ds.triangle_pressed += triangle_pressed
        
        def l1_changed(state):
            print("L1:", state)
        ds.l1_changed  += l1_changed

        def r1_changed(state):
            print("R1:", state)
        ds.r1_changed  += r1_changed

        def l2_changed(state):
            print("L2:", state)
        ds.l2_changed  += l2_changed

        def r2_changed(state):
            print("R2:", state)
        ds.r2_changed  += r2_changed

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        v_width = 400
        v_height = 200
        #main window
        self.resize(v_width, v_height)
        #remove frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        #make the main window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.round_widget = QWidget(self)
        self.round_widget.resize(v_width, v_height)
        self.round_widget.setStyleSheet(
            """
            background:rgba(50, 50, 50, 250);
            border-radius: 100px;
            font-size: 60px;
            font-style: bold;
            """
        )
        
        lay = QGridLayout(self.round_widget)

        self.label = QLabel('↑')
        self.label.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.label, 0, 1)
        
        self.label2 = QLabel('←')
        self.label2.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.label2, 1, 0)

        self.label3 = QLabel('→')
        self.label3.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.label3, 1, 2)
        
        self.label4 = QLabel('↓')
        self.label4.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.label4, 2, 1)

        #

        self.label5 = QLabel('△')
        self.label5.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.label5, 0, 5)
        
        self.label6 = QLabel('⃞')
        self.label6.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.label6, 1, 4)

        self.label7 = QLabel('○')
        self.label7.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.label7, 1, 6)
        
        self.label8 = QLabel('🞩')
        self.label8.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.label8, 2, 5)


        self.show()

if __name__ == "__main__":
    #run_test()
    controller = Controller()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
    