import tkinter as tk
from tkinter import ttk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json


class App(tk.Tk):

    def __init__(self, sp):
        super().__init__()

        # The spotify auth object to use for controlling Spotify
        self.spot = sp

        # Window setup
        self.title('Smart Shuffle')
        self.geometry("400x300+50+50")
        self.eval('tk::PlaceWindow . center')
        self.geometry("400x300+50+50")
        self.eval('tk::PlaceWindow . center')
        self.resizable(False, False)
        img = tk.PhotoImage(file='assets/icon.gif')
        self.iconphoto(True, img)

        # Window style
        style = ttk.Style(self)
        style.configure('.', font=('Helvetica', 20))

        #Welcome message
        var = tk.StringVar()
        label = tk.Label(self, textvariable=var)
        var.set(f"Welcome, {sp.current_user()['display_name']}")
        label.pack()

        # Buttons
        self.play = tk.Button(self, text="Play", command=self.playPauseMusic)
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



if __name__ == "__main__":

    scope = "user-library-read, user-modify-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    app = App(sp)
    app.mainloop()
