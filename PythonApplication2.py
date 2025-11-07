from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
import pyautogui
from pydualsense import pydualsense, TriggerModes
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        w = 200
        h = 100

        #main window
        self.resize(w, h)
        #remove frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        #make the main window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)

        #round widget
        self.round_widget = QWidget(self)
        self.round_widget.resize(w, h)

        self.round_widget.setStyleSheet(
            """
            background:rgba(50, 50, 50, 150);
            border-radius: 50px;
            """
        )

        #self.setStyleSheet("border-radius: 10px;".format(radius))
        self.show()



def test_pyautogui():
   print("asdf")
   #pyautogui.typewrite('Hello world!\n', interval=0.5)
   print(pyautogui.KEYBOARD_KEYS)
   print(len(pyautogui.KEYBOARD_KEYS))
   pyautogui.hotkey('ctrl', 'v')
   print(input())
   #pyautogui.keyDown(pyautogui.KEYBOARD_KEYS)
   
def test_pydualsense():
    def cross_pressed(state):
        print("Cross button state: ")
        print(state)

    ds = pydualsense() # open controller
    ds.init() # initialize controller

    ds.cross_pressed += cross_pressed
    ds.light.setColorI(0,255,0) # set touchpad color to red
    ds.triggerL.setMode(TriggerModes.Rigid)
    ds.triggerL.setForce(1, 255)
    #print(input())
    #ds.close() # closing the controller


def run():
    test_pyautogui()
    test_pydualsense()

if __name__ == "__main__":
    run()
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())