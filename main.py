import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import pytesseract
import pygame
import os

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\salmam\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Video Player")

        self.video_path = "oop-video.mp4"  # Replace with your video file

        self.cap = cv2.VideoCapture(self.video_path)
        self.frame = None

        # Initialize pygame for audio playback
        pygame.mixer.init()

        self.create_widgets()

        # Bind keyboard shortcuts to buttons
        root.bind('.', self.capture_code)  # Press '.' to capture code
        root.bind('<space>', self.toggle_play)  # Spacebar to play/pause

        root.bind('<Left>', self.skip_backward)  # Left arrow key to skip backward
        root.bind('<Right>', self.skip_forward)  # Right arrow key to skip forward

    def create_widgets(self):
        self.playing = False

        # Get the dimensions of the video
        video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.canvas = tk.Canvas(self.root, width=1280, height=800)
        self.canvas.pack()

        self.play_pause_button = ttk.Button(self.root, text="Play", command=self.toggle_play)
        self.play_pause_button.pack()

        self.capture_button = ttk.Button(self.root, text="Capture Code", command=self.capture_code)
        self.capture_button.pack()
        self.capture_button["state"] = "disabled"  # Disable the button initially

        self.skip_forward_button = ttk.Button(self.root, text="Skip Forward 5s", command=self.skip_forward)
        self.skip_forward_button.pack()

        self.skip_backward_button = ttk.Button(self.root, text="Skip Backward 5s", command=self.skip_backward)
        self.skip_backward_button.pack()

        self.update_frame()

    def toggle_play(self, event=None):
        if self.playing:
            self.playing = False
            self.play_pause_button["text"] = "Play"
            self.capture_button["state"] = "normal"  # Enable the capture button when paused
        else:
            self.playing = True
            self.play_pause_button["text"] = "Pause"
            self.capture_button["state"] = "disabled"  # Disable the capture button when playing
            self.play_video()

    def capture_code(self, event=None):
        if self.frame is not None:
            # Capture the current frame
            cv2.imwrite("captured_frame.png", self.frame)
            # Read the content of the captured frame using Tesseract OCR
            code = pytesseract.image_to_string("captured_frame.png")
            # Save the code to a text file
            with open("captured_code.txt", "w") as file:
                file.write(code)

    def play_video(self):
        while self.playing:
            ret, self.frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            self.update_frame()
            self.root.update_idletasks()
            self.root.update()

    def skip_forward(self, event=None):
        current_position = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        new_position = current_position + 5000  # 5000 milliseconds (5 seconds)
        self.cap.set(cv2.CAP_PROP_POS_MSEC, new_position)

    def skip_backward(self, event=None):
        current_position = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        new_position = max(0, current_position - 5000)  # 5000 milliseconds (5 seconds)
        self.cap.set(cv2.CAP_PROP_POS_MSEC, new_position)

    def update_frame(self):
        if self.frame is not None:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)

            # Resize the image to match the canvas dimensions
            image = image.resize((1280, 800))
            photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()
