from guizero import App, PushButton
from gpiozero import LED
import sys



def exitApp():
    sys.exit()   

app = App('First Gui', height = 600, width = 800)

ledButton = PushButton(app, toggleLED, text="LED ON", align="top",width = 15, height = 3)
ledButton.text_size = 36

exitButton = PushButton(app, exitApp, text="Exit", align="bottom" , width = 15, height = 3)
exitButton.text_size = 36

app.display()




