#region Imports
import customtkinter as ctk
import darkdetect
from settings import *
from pathlib import Path

try:
	from ctypes import windll, byref, sizeof, c_int
except:
	pass
#endregion

#region Calculator
class App(ctk.CTk):
    def __init__(self):
        # setup
        self.isDark: bool = darkdetect.isDark()
        super().__init__(fg_color = ("#1B59F0", "#041339"))
        ctk.set_appearance_mode(f"{'dark' if self.isDark else 'light'}")

        # customisation
        self.attributes("-topmost", True)
        self.geometry(f"300x600")
        self.minsize(400, 400)
        self.resizable(False, False)
        self.title(" Calculator")
        self.ChangeTitleBar()

        icoPath = Path(__file__).with_name("Cookie.ico")   # same folder as Calculator.py
        self.iconbitmap(default=str(icoPath))
    
        # data
        self.resultString = ctk.StringVar(value = "0")
        self.formulaString = ctk.StringVar(value = " ")
        self.numberDisplay = ["0"]
        self.operatorDisplay = []
        self.answerPresent = True

        # grid layout
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1, uniform = "a") # -> 7 rows
        self.columnconfigure((0, 1, 2, 3), weight = 1, uniform = "a") # -> 4 columns

        # widgets
        self.CreateWidgets()
        self.Binds()
        
        self.mainloop()
    
    def ChangeTitleBar(self) -> None:
        '''Changes title bar colour. NOTE: Only works on windows'''
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = 0x00391304 if self.isDark else 0x00F0591B
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            KeyError("Function not excuted properly")
            pass

    def CreateWidgets(self) -> None:
        '''Settings up app objects ''' 

        # text labels
        equationFont = ctk.CTkFont('Helvetica', 25)
        primaryFont = ctk.CTkFont('Helvetica', 32)
        resultFont = ctk.CTkFont('Helvetica', 70)
        self.Output = Output(self, (0, 0, "se"), equationFont, self.formulaString, "#999999")
        self.OutputSave = Output(self, (0, 1, "e"), resultFont, self.resultString, "#f1f1f1")

        # misc
        self.clearButton = Button(self, (0, 2), self.ClearPressed, primaryFont, "C", "#0FADE0")
        self.backSpaceButton = Button(self, (2, 2), self.DeletePressed, primaryFont, "Del", "#0FADE0")
        self.expNotationButton = Button(self, (2, 6), self.ClearPressed, primaryFont, "x10", "#0E34A4")

        # operations
        self.squareButton = OperatorButton(self, (1, 2), "**2", self.OperatorPressed, primaryFont, "^2", "#0FADE0")
        self.divideButton = OperatorButton(self, (3, 2), "/", self.OperatorPressed, primaryFont, "÷", "#0ECA92")
        self.multiplyButton = OperatorButton(self, (3, 3), "*", self.OperatorPressed, primaryFont, "x", "#0ECA92")
        self.subtractButton = OperatorButton(self, (3, 4), "-", self.OperatorPressed, primaryFont, "-", "#0ECA92")
        self.addButton = OperatorButton(self, (3, 5), "+", self.OperatorPressed, primaryFont, "+", "#0ECA92")
        self.equalsButton = OperatorButton(self, (3, 6), "=", self.OperatorPressed, primaryFont, "=", "#0ECA92")

        # numbers
        self.oneButton = NumberButton(self, (0, 3), self.NumberPressed, primaryFont, "1", "#0E34A4")
        self.twoButton = NumberButton(self, (1, 3), self.NumberPressed, primaryFont, "2", "#0E34A4")
        self.threeButton = NumberButton(self, (2, 3), self.NumberPressed, primaryFont, "3", "#0E34A4")
        self.fourButton = NumberButton(self, (0, 4), self.NumberPressed, primaryFont, "4", "#0E34A4")
        self.fiveButton = NumberButton(self, (1, 4), self.NumberPressed, primaryFont, "5", "#0E34A4")
        self.sixButton = NumberButton(self, (2, 4), self.NumberPressed, primaryFont, "6", "#0E34A4")
        self.sevenButton = NumberButton(self, (0, 5), self.NumberPressed, primaryFont, "7", "#0E34A4")
        self.eightButton = NumberButton(self, (1, 5), self.NumberPressed, primaryFont, "8", "#0E34A4")
        self.nineButton = NumberButton(self, (2, 5), self.NumberPressed, primaryFont, "9", "#0E34A4")
        self.zeroButton = NumberButton(self, (0, 6), self.NumberPressed, primaryFont, "0", "#0E34A4")
        self.dotButton = NumberButton(self, (1, 6), self.NumberPressed, primaryFont, ".", "#0E34A4")        

    def Binds(self) -> None:
        '''All the key binds to make the calculator easier to use'''
        self.bind("<Escape>", lambda event: self.destroy())
        self.bind("<BackSpace>", lambda event: self.DeletePressed())
        self.bind("c", lambda event: self.ClearPressed())
        self.bind("1", lambda event: self.NumberPressed("1"))
        self.bind("2", lambda event: self.NumberPressed("2"))
        self.bind("3", lambda event: self.NumberPressed("3"))
        self.bind("4", lambda event: self.NumberPressed("4"))
        self.bind("5", lambda event: self.NumberPressed("5"))
        self.bind("6", lambda event: self.NumberPressed("6"))
        self.bind("7", lambda event: self.NumberPressed("7"))
        self.bind("8", lambda event: self.NumberPressed("8"))
        self.bind("9", lambda event: self.NumberPressed("9"))
        self.bind("0", lambda event: self.NumberPressed("0"))
        self.bind(".", lambda event: self.NumberPressed("."))
        self.bind("+", lambda event: self.OperatorPressed("+"))
        self.bind("-", lambda event: self.OperatorPressed("-"))
        self.bind("/", lambda event: self.OperatorPressed("/"))
        self.bind("*", lambda event: self.OperatorPressed("*"))
        self.bind("=", lambda event: self.OperatorPressed("="))
        self.bind("<Return>", lambda event: self.OperatorPressed("="))        

    def OperatorPressed(self, value) -> None:
        '''Operator pressed running calculation'''

        # allows the usage of previous answer in next equation
        if self.answerPresent:
            currentNumber = self.resultString.get()
            self.answerPresent = False
        else:
            currentNumber = "".join(self.numberDisplay)

        if currentNumber:        
            self.operatorDisplay.append(currentNumber)

            if value == "=":
                # evaluates equation
                fullEquation = " ".join(self.operatorDisplay)
                answer = eval(fullEquation)
                self.resultString.set(f"{round(answer, 2)}")
                self.answerPresent = True

                self.UpdateOperatorDisplay(value)
                self.operatorDisplay.clear()
                self.ResetNumberDisplay()
            else:
                # adds operator to equation
                self.ResetNumberDisplay()
                self.UpdateOperatorDisplay(value)
    
    def UpdateOperatorDisplay(self, value = None) -> None:
        '''Updates the operator display'''
        if value:
            self.operatorDisplay.append(value)

        fullEquation = " ".join(self.operatorDisplay)
        self.formulaString.set(fullEquation)

    def UpdateNumberDisplay(self, value = None) -> None:
        '''Updates the number display'''
        if value:
            self.numberDisplay.append(str(value))

        fullNumber = "".join(self.numberDisplay)
        self.resultString.set(fullNumber)
        self.answerPresent = False

    def ResetNumberDisplay(self) -> None:
        '''Sets the number display back to placeholder'''
        self.numberDisplay.clear()
        # self.numberDisplay.append("0")

    def NumberPressed(self, value) -> None:
        '''What should happen when a number is pressed'''
        # clears placeholder zero
        if len(self.numberDisplay) == 1 and self.numberDisplay[0] == "0" and value != ".":
            self.numberDisplay.clear()
        
        # breaks when decimal point already exists
        if "." in self.numberDisplay and value == "." : return

        self.UpdateNumberDisplay(value)

    def DeletePressed(self) -> None:
        '''Deletes the last thing pressed'''
        if self.answerPresent:
            self.operatorDisplay.clear()
            self.UpdateOperatorDisplay()
        else:
            if len(self.numberDisplay) > 0:
                self.numberDisplay.pop(-1)
            self.UpdateNumberDisplay()
    
    def ClearPressed(self) -> None:
        '''Clears the calculator'''
        self.operatorDisplay.clear()
        self.ResetNumberDisplay()
        self.UpdateOperatorDisplay()
        self.UpdateNumberDisplay()

class Output(ctk.CTkLabel):
    def __init__(self, parent, position: tuple[int, int, str], font: tuple[str, int], textVariable: str, colour: str):
        # var "position" -> x, y, anchor
        super().__init__(parent, font = font, textvariable = textVariable, text_color = colour, anchor = "e")
        self.grid(column = position[0], columnspan = 4, row = position[1], sticky = position[2], padx = 10)
#endregion

#region Buttons
class Button(ctk.CTkButton):
    def __init__(self, parent, position: tuple[int ,int], function: any, font: tuple[str, int], text: str, colour: str):
        # button customisation and positioning
        super().__init__(parent, text = text, command = function, corner_radius = 50, font = font, fg_color = colour) #fg_color(light,dark) hover_color text_color
        self.grid(column = position[0], row = position[1], sticky = "nsew", padx = 2, pady = 2)

class NumberButton(Button):
    def __init__(self, parent, position: tuple[int ,int], function: any, font: tuple[str, int], text: str, colour: str):
        super().__init__(parent, position, function = lambda: function(text), font = font, text = text, colour = colour)

class OperatorButton(Button):
    def __init__(self, parent, position: tuple[int ,int], operator: str, function: any, font: tuple[str, int], text: str, colour: str):
        super().__init__(parent, position, function = lambda: function(operator), font = font, text = text, colour = colour)
#endregion

#region Run
if __name__ == "__main__":  
    App()
#endregion
