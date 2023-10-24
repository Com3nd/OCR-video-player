import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk


class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player with Audio")

        self.video_path = "oop-video.mp4"  # Replace with your video file
        self.audio_path = "audio.mp3"     # Replace with your audio file

        self.cap = cv2.VideoCapture(self.video_path)
        self.frame = None

        self.create_widgets()

    def create_widgets(self):
        self.playing = False

        # Get the dimensions of the video
        video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.canvas = tk.Canvas(self.root, width=1280, height=800)
        self.canvas.pack()

        self.play_pause_button = ttk.Button(self.root, text="Play", command=self.toggle_play)
        self.play_pause_button.pack()

        self.skip_forward_button = ttk.Button(self.root, text="Skip Forward 5s", command=self.skip_forward)
        self.skip_forward_button.pack()

        self.skip_backward_button = ttk.Button(self.root, text="Skip Backward 5s", command=self.skip_backward)
        self.skip_backward_button.pack()

        self.update_frame()

    def toggle_play(self):
        if self.playing:
            self.playing = False
            self.play_pause_button["text"] = "Play"
        else:
            self.playing = True
            self.play_pause_button["text"] = "Pause"
            self.play_video()

    def play_video(self):
        while self.playing:
            ret, self.frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            self.update_frame()
            self.root.update_idletasks()
            self.root.update()

    def skip_forward(self):
        current_position = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        new_position = current_position + 5000  # 5000 milliseconds (5 seconds)
        self.cap.set(cv2.CAP_PROP_POS_MSEC, new_position)

    def skip_backward(self):
        current_position = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        new_position = max(0, current_position - 5000)  # 5000 milliseconds (5 seconds)
        self.cap.set(cv2.CAP_PROP_POS_MSEC, new_position)

    def update_frame(self):
        if self.frame is not None:
            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()
