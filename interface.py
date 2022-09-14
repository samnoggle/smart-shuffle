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
        self.play = tk.Button(self, text="Play/Pause", command=self.playPauseMusic)
        self.play.place(relx=0.5, rely=0.5, anchor='center')

        self.skip = tk.Button(self, text ="Skip", command=self.skipMusic)
        self.skip.place(relx=0.8, rely=0.5, anchor='e')

    def playPauseMusic(self):
        print("The music should play or pause now!")

        #Pause
        if self.play["text"] == "Pause":
            self.play["text"] = "Play"
            # pause method goes here
        else:
            self.play["text"] = "Pause"
            # play method goes here

    def skipMusic(self):
        # Do the skipping !!
        # will call a method to skip a song
        print("The music should skip now!")
        pass





if __name__ == "__main__":
    app = App()
    app.mainloop()
