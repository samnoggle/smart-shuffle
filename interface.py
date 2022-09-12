import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Smart Shuffle')
        self.geometry("400x300+50+50")
        self.eval('tk::PlaceWindow . center')
        self.geometry("400x300+50+50")
        self.eval('tk::PlaceWindow . center')
        self.resizable(False, False)
        img = tk.PhotoImage(file='assets/icon.gif')
        self.iconphoto(True, img)

        # Style
        style = ttk.Style(self)
        style.configure('.', font=('Helvetica', 20))

        # Adding widjets
        play = tk.Button(self, text="Play/Pause")
        play.place(relx=0.5, rely=0.5, anchor='center')

        skip = tk.Button(self, text ="Skip")
        skip.place(relx=0.8, rely=0.5, anchor='e')

    def playMusic(self):
        # First change the button to pause?
        pass

    def pauseMusic(self):
        # First change button to play?
        pass

    def skipMusic(self):
        # Do the skipping !!
        pass



                


if __name__ == "__main__":
    app = App()
    app.mainloop()
