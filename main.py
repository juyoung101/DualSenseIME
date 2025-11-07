from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QWidget
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

def test_pydualsense():
    def cross_pressed(state):
        print("Cross button state: ")
        print(state)

    ds = pydualsense() # open controller
    ds.init() # initialize controller

    ds.cross_pressed += cross_pressed
    ds.light.setColorI(0,255,0) # set touchpad color to green
    ds.triggerL.setMode(TriggerModes.Rigid)
    ds.triggerL.setForce(1, 255)
    print(input()) #hang for testing
    ds.close() # closing the controller

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        v_width = 200
        v_height = 100
        #main window
        self.resize(v_width, v_height)
        #remove frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        #make the main window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)

        #round widget
        self.round_widget = QWidget(self)
        self.round_widget.resize(v_width, v_height)

        self.round_widget.setStyleSheet(
            """
            background:rgba(50, 50, 50, 150);
            border-radius: 50px;
            """
        )

        self.show()

if __name__ == "__main__":
    run_test()