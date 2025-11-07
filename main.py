from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from pydualsense import pydualsense, TriggerModes
import pyautogui
import sys

#['ctrl']['shift']['alt']['macro']['KEY']


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


def test_pyautogui():
   print("asdf")
   #pyautogui.typewrite('Hello world!\n', interval=0.5)
   print(pyautogui.KEYBOARD_KEYS)
   print(len(pyautogui.KEYBOARD_KEYS))
   pyautogui.hotkey('ctrl', 'shift', 'alt', 'win', 'l')
   print(input())
   #pyautogui.keyDown(pyautogui.KEYBOARD_KEYS)
   
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
    #print(input())
    #ds.close() # closing the controller

def run_test():
    #test_pyautogui()
    #test_pydualsense()
    return

if __name__ == "__main__":
    run_test()
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())