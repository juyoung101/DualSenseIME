from multiprocessing import Value
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout
from PySide6.QtCore import Qt
from pydualsense import pydualsense, TriggerModes
from functools import partial
from enum import Enum
import pyautogui
import sys

#IME
#  Layer       #Chorded layout number
#  KeySets     #Chorded layouts
#  ButtonMap   #Held Buttons
#~pyautogui    #Keyboard emulator for forwarding inputs
#*pydualsense  #Gamepad Event/State Connector
#    #ps: quit;
#    #mic: send input;
#    #faces: mark ButtonMap; send input;
#    #arrows: mark ButtonMap; (update KeySets); send input;
#    #shoulders: mark ButtonMap; (update KeySets);
#qt #GUI App
#    #label.text = KeySets[Layer];
#    #label.style = StyleSet[ButtonMap[Button]];
#
#
#  layer - combo        dpad    face
#     1  - none         wads    mods
#     2  - L1           eqrf    ijlk
#     3  - R1           htg,    uyo.
#     4  - L2           xzvc    pbmn
#     5  - R2           mods    mods
#     6  - L1R1         macro   num1/num2/num3/sym5
#     7  - L2R2         macro   mods/sym6/dpad/sym7
#     8  - L1R2         sym1    sym2
#     9  - L2R1         sym3    sym4

def test_pyautogui():
    print("Sendable keys:", pyautogui.KEYBOARD_KEYS)
    print("Total:", len(pyautogui.KEYBOARD_KEYS))
    print("Typing string... ")
    pyautogui.typewrite('Hello world!\n', interval=0.1)
    print("Echo:", input())
    print("Pressing Enter to continue...")
    pyautogui.press('enter')
    input()
    print("Sending LinkedIn hotkey...")
    pyautogui.hotkey('ctrl', 'shift', 'alt', 'win', 'l')

def test_pydualsense():
    def cross_pressed(state): #event function
        print("CROSS: ", state)
    ds = pydualsense() # open controller
    ds.init() # initialize controller
    ds.cross_pressed += cross_pressed #attach event function
    ds.light.setColorI(0,255,0) # set touchpad color to green
    ds.triggerL.setMode(TriggerModes.Rigid)
    ds.triggerL.setForce(1, 255)
    ds.triggerR.setMode(TriggerModes.Pulse)
    ds.triggerR.setForce(1, 255)
    print("Press Enter to close app...")
    print("Echo: ", input()) #hang for testing
    ds.close()#closing the controller
    pass

def test_KeySets():
    keySets = KeySets()
    keySets.print()

def test_ButtonMap():
    buttonmap = ButtonMap()
    buttonmap.print()

def test_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

def run_tests(value):
    if(value == "A"):
        test_KeySets()
        test_ButtonMap()
        test_pyautogui()
    elif(value == "B"):
        test_pydualsense()
    elif(value == "C"):
        test_window()

class Labels(Enum):
    UP = 1
    LF = 2
    RT = 3
    DN = 4
    TR = 5
    SQ = 6
    CI = 7
    CR = 8
    L1 = 9
    R1 = 10
    L2 = 11
    R2 = 12

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

    def update(self, btn, value): #Updates to reflect button state
        if btn in ["L1","R1","L2","R2"]:
            self._bumpers[btn] = value
        elif btn in ["UA","DA","LA","RA"]:
            self._arrows[btn] = value
        elif btn in ["UF","LF","RF","DF"]:
            self._faces[btn] = value

    def process(self, btn, value):
        print("Processing", btn, value)
        pass #

    def getLayer(self): #codesmell
        if self._bumpers["L1"] == False and self._bumpers["R1"] == False and self._bumpers["L2"] == False and self._bumpers["R2"] == False: #none
            return 1
        if self._bumpers["L1"] == True and self._bumpers["R1"] == False and self._bumpers["L2"] == False and self._bumpers["R2"] == False: #L1
            return 2
        if self._bumpers["L1"] == False and self._bumpers["R1"] == True and self._bumpers["L2"] == False and self._bumpers["R2"] == False: #R1
            return 3
        if self._bumpers["L1"] == False and self._bumpers["R1"] == False and self._bumpers["L2"] == True and self._bumpers["R2"] == False: #L2
            return 4
        if self._bumpers["L1"] == False and self._bumpers["R1"] == False and self._bumpers["L2"] == False and self._bumpers["R2"] == True: #R2
            return 5
        if self._bumpers["L1"] == True and self._bumpers["R1"] == True and self._bumpers["L2"] == False and self._bumpers["R2"] == False: #L1R1
            return 6
        if self._bumpers["L1"] == False and self._bumpers["R1"] == False and self._bumpers["L2"] == True and self._bumpers["R2"] == True: #L2R2
            return 7
        if self._bumpers["L1"] == True and self._bumpers["R1"] == False and self._bumpers["L2"] == False and self._bumpers["R2"] == True: #L1R2
            return 8
        if self._bumpers["L1"] == False and self._bumpers["R1"] == True and self._bumpers["L2"] == True and self._bumpers["R2"] == False: #L2R1
            return 9
        return 1
    
    def get_button_number(self, button):
        match(button):
            case "UA": return 0
            case "LA": return 1
            case "RA": return 2
            case "DA": return 3
            case "UF": return 4
            case "LF": return 5
            case "RF": return 6
            case "DF": return 7
        return 0

    def print(self):
        print("Bumpers:", self._bumpers)
        print("Arrows:", self._arrows)
        print("Faces:", self._faces)

class KeySets():
    _modifiers = {"ctrl": False, "shift": False, "alt": False, "meta": False, "macro": False}
    _keys = {"a" : False, "b" : False, "c" : False, "d" : False, "e" : False, "f" : False, "g" : False, "h" : False, "i" : False, "j" : False,
            "k" : False, "l" : False, "m" : False, "n" : False, "o" : False, "p" : False, "q" : False, "r" : False, "s" : False, "t" : False,
            "u" : False, "v" : False, "w" : False, "x" : False, "y" : False, "z" : False,
            "0" : False, "1" : False, "2" : False, "3" : False, "4" : False, "5" : False, "6" : False, "7" : False, "8" : False, "9" : False,
            "space": False, "enter" : False, "backspace" : False }
    _layers = {'1': ['w','a','d','s',
                     'backspace','tav','enter','space'],# none
               '2': ['e','q','r','f',
                     'i','j','l','k'],# L1
               '3': ['h','t','g',',',
                     'u','y','o','.'],# R1
               '4': ['x','z','v','c',
                     'p','b','m','n'],# L2
               '5': ['ctrl','shift','alt','win',
                     'escape','home','end','delete'],# R2
               '6': [['1','2','3','4'],
                     ['5','6','7','8'],
                     ['9','0','=','_'],
                     ['*','/','+','-']],# L1 R1 MACRO
               '7': [['pageup','print','pause','pagedown'],
                     ['}','{','>','<'],
                     ['up','left','right','down'],
                     [']','[',')','(']],# L2 R2 MACRO
               '8': ['!','@','$','#',
                     '^','%','*','&'],# L1 R2
               '9': ['`', '\\','~','?',
                     '"',"'",':',';']}# L2 R1

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

    def get_layer(self, value):
        return self._layers.get(str(value))

    def print(self):
        print("Modifiers:", self._modifiers)
        print("Keys:", self._keys)
        print("Layers:", self._layers)

class Controller():
    _inputSystem = ""
    ds = pydualsense() # open controller
    def default_listeners(self):
        def dpad_up_pressed(state):
            print("UP:", state)
        self.ds.dpad_up += dpad_up_pressed

        def dpad_left_pressed(state):
            print("LF:", state)
        self.ds.dpad_left += dpad_left_pressed

        def dpad_right_pressed(state):
            print("RT:", state)
        self.ds.dpad_right += dpad_right_pressed

        def dpad_down_pressed(state):
            print("DN:", state)
        self.ds.dpad_down += dpad_down_pressed

        def triangle_pressed(state):
            print("UF:", state)
        self.ds.triangle_pressed += triangle_pressed

        def square_pressed(state):
            print("LF:", state)
        self.ds.square_pressed += square_pressed

        def circle_pressed(state):
            print("RF:", state)
        self.ds.circle_pressed += circle_pressed

        def cross_pressed(state):
            print("DF:", state)
        self.ds.cross_pressed += cross_pressed

        def l1_changed(state):
            print("L1:", state)
        self.ds.l1_changed  += l1_changed

        def r1_changed(state):
            print("R1:", state)
        self.ds.r1_changed  += r1_changed

        def l2_changed(state):
            print("L2:", state)
        self.ds.l2_changed  += l2_changed

        def r2_changed(state):
            print("R2:", state)
        self.ds.r2_changed  += r2_changed

    def special_listeners(self):
        def ps_pressed(state):
            print("PS:", state)
        self.ds.ps_pressed += ps_pressed

        def microphone_pressed(state):
            print("MIC:", state)
        self.ds.microphone_pressed += microphone_pressed

        def start_pressed(state):
            print("ST:", state)
        self.ds.share_pressed += start_pressed

        def select_pressed(state):
            print("SL:", state)
        self.ds.option_pressed += select_pressed

        def touch_pressed(state):
            print("TP:", state)
        self.ds.touch_pressed += touch_pressed

    def chord_listeners(self, listener): #excessive sugar but this is a really neat method for condensing and generalizing this specific code
        self.ds.l1_changed += partial(listener, button="L1")
        self.ds.r1_changed += partial(listener, button="R1")
        self.ds.l2_changed += partial(listener, button="L2")
        self.ds.r2_changed += partial(listener, button="R2")

        self.ds.dpad_up += partial(listener, button="UA")
        self.ds.dpad_left += partial(listener, button="LA")
        self.ds.dpad_right += partial(listener, button="RA")
        self.ds.dpad_down += partial(listener, button="DA")

        self.ds.triangle_pressed += partial(listener, button="UF")
        self.ds.square_pressed += partial(listener, button="LF")
        self.ds.circle_pressed += partial(listener, button="RF")
        self.ds.cross_pressed += partial(listener, button="DF")

    def __init__(self):
        self.setInputSystem("Event")
        self.setup()

    def setInputSystem(self, value):
        self._inputSystem = value

    def setup(self):
        try:
            self.ds.init() # initialize controller
            self.ds.light.setColorI(0,255,0) # set touchpad color to green
            self.ds.triggerL.setMode(TriggerModes.Rigid)
            self.ds.triggerR.setMode(TriggerModes.Rigid)
            self.ds.triggerL.setForce(1, 155)
            self.ds.triggerR.setForce(1, 155)
            if self._inputSystem == "Event":
                #self.default_listeners()
                self.special_listeners()
        except Exception as e:
            print("controller not available, please try again")
            print("exception message:", e)
            pass

    def readButton(self, value):
        return self.ds.state[value]

class MainWindow(QMainWindow):#main window
    window_style_sheet = """
        background:rgba(50, 50, 50, 250);
        border-radius: 100px;
        font-size: 60px;
        font-style: bold;
        padding:5px;
        color:#FFFFFF;
        font-size: 20px;
    """
    style_active_l = """
        background-color:green;
        """
    style_inactive_l = """
        background-color:none;
    """
    style_active_b = """
        background-color:none;
        """
    style_inactive_b = """
        background-color:none;
    """

    labels = {}

    def update_label(self, key, value):
        self.labels[key].text = value
        return

    def update_bumper_style(self, key, value):
        if value:
            self.labels[key].setStyleSheet(self.style_active_l)
        else:
            self.labels[key].setStyleSheet(self.style_inactive_l)

    def update_label_style(self, key, value):
        if value:
            self.labels[key].setStyleSheet(self.style_active_l)
        else:
            self.labels[key].setStyleSheet(self.style_inactive_l)

    def __init__(self):
        super().__init__()
        v_width = 400
        v_height = 200
        self.resize(v_width, v_height)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.round_widget = QWidget(self)
        self.round_widget.resize(v_width, v_height)
        self.round_widget.setStyleSheet(self.window_style_sheet)

        lay = QGridLayout(self.round_widget)

        self.label = QLabel('↑')
        lay.addWidget(self.label, 0, 1)
        self.labels[Labels.UP] = self.label

        self.label2 = QLabel('←')
        lay.addWidget(self.label2, 1, 0)
        self.labels[Labels.LF] = self.label2

        self.label3 = QLabel('→')
        lay.addWidget(self.label3, 1, 2)
        self.labels[Labels.RT] = self.label3

        self.label4 = QLabel('↓')
        lay.addWidget(self.label4, 2, 1)
        self.labels[Labels.DN] = self.label4

        #

        self.label5 = QLabel('△')
        lay.addWidget(self.label5, 0, 5)
        self.labels[Labels.TR] = self.label5
        
        self.label6 = QLabel('⃞')
        lay.addWidget(self.label6, 1, 4)
        self.labels[Labels.SQ] = self.label6

        self.label7 = QLabel('○')
        lay.addWidget(self.label7, 1, 6)
        self.labels[Labels.CI] = self.label7
        
        self.label8 = QLabel('🞩')
        lay.addWidget(self.label8, 2, 5)
        self.labels[Labels.CR] = self.label8

        #

        self.label9 = QLabel('L1')
        lay.addWidget(self.label9, 0, 0)
        self.labels[Labels.L1] = self.label9

        self.label10 = QLabel('R1')
        lay.addWidget(self.label10, 0, 6)
        self.labels[Labels.R1] = self.label10

        self.label11 = QLabel('L2')
        lay.addWidget(self.label11, 2, 0)
        self.labels[Labels.L2] = self.label11

        self.label12 = QLabel('R2')
        lay.addWidget(self.label12, 2, 6)
        self.labels[Labels.R2] = self.label12


        for i in Labels:
            if i.value >= Labels.L1.value:
                self.labels[i].setStyleSheet(self.style_active_b)
            else:
                self.labels[i].setStyleSheet(self.style_active_l)
            self.labels[i].setAlignment(Qt.AlignCenter)

        self.show()

class IME():
    layer = 1
    macro = 0
    keySets = KeySets()
    bMap = ButtonMap()

    def __init__(self):
        pass#
    
    def send(self, layer, button):
        print("Sending %d - %s " % (layer, button))
        
        available_buttons = self.keySets.get_layer(self.layer) #check KeySets for available layout
        if layer in [6,7]: #check macros if layer 67
            if self.macro > 1:
                print("Macro:", self.macro)
                print("Layout:", available_buttons[(self.macro%4)-1])
                if button in ["UF","LF","RF","DF"]:
                    print("pyautogui.press(available_buttons[buttonNum])")# send off only face presses
        else:
            available_buttons = self.keySets.get_layer(self.layer)
            print (available_buttons)
            buttonNum = self.bMap.get_button_number(button)
            pyautogui.press(available_buttons[buttonNum]) #TODO: holding not currently supported
                                                  #TODO: select key from layer, use enum?

    def updateLayer(self):
        self.layer = self.bMap.getLayer()
        if self.macro == 0: 
            if(self.layer not in [6,7]): 
                print("Current Layout: ", self.layer, self.keySets.get_layer(self.layer))#
            else:
                print("Current Layout: ", self.layer, self.keySets.get_layer(self.layer)[0])
        else: print("Current Macro Layout:", self.layer, self.keySets.get_layer(self.layer)[(self.macro%4)-1])#

    def action(self, button, value): #Processes macro and terminal buttons
        if button in ["L1","R1","L2","R3"]: #bumper buttons aren't handled here
            if value == False:
                pass#depress all keys
        if button in ["UA","LA","RA","DA"]: #arrow buttons
            if(self.layer in [6,7]):#calculate macro layer
                self.macro = 0
                if value: 
                    if (self.layer == 7):
                        self.macro += 4
                    if(button == "UA"): self.macro += 1
                    if(button == "LA"): self.macro += 2
                    if(button == "RA"): self.macro += 3
                    if(button == "DA"): self.macro += 4
                    self.updateLayer()
                else:
                    pass#depress all keys
            elif value: #non-macro presses only
                self.send(self.layer, button) #terminal buttons
        if button in ["UF","LF","RF","DF"]:#face buttons
            if value:#presses only
                self.send(self.layer, button)#terminal buttons

    def input(self, button, value):
        self.bMap.update(button, value)
        if button in ["L1","R1","L2","R2"]: #Chording buttons
            self.updateLayer()
        self.action(button, value) #Handle chorded button press, arrow button chording enables meta layouts for face buttons, terminal buttons check meta then send input 

    def print(self):
        self.keySets.print()
        self.bMap.print()

if __name__ == "__main__":
    mode = "Headless"
    isThreaded = True
    if(mode == "Test"): # Basic module functionality tests
        run_tests("A")
        #run_tests("B")
        #run_tests("C")
    if((mode == "Headless") & (isThreaded == True)): # Event-based input system
        controller = Controller()
        controller.setInputSystem("Event")
        ime = IME()
        def listener(state, button): #button supplied by partial function
            #print("event:", button, state)
            ime.input(button, value=state) #tell ime the tea
            #ime.print()
            pass#
        controller.chord_listeners(listener)
    if((mode == "Headless") & (isThreaded == False)): # State-based input system
        controller = Controller()
        controller.setInputSystem("State")
        ime = IME()
    if(mode == "GUI"): #Qt widget to display active layout, defaults to _-Based system
        controller = Controller()
        app = QApplication(sys.argv)
        window = MainWindow()
        ime = IME()
        sys.exit(app.exec())
