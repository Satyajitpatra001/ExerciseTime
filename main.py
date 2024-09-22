import os
import time
import threading
import pygame
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

class TimerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.timer_label = Label(text="Start", font_size='48sp')
        self.layout.add_widget(self.timer_label)

        # Reset Button
        self.reset_button = Button(text='Reset', size_hint=(None, None), size=(70, 70))
        self.reset_button.bind(on_press=self.reset_timer)
        self.layout.add_widget(self.reset_button)

        # Start Button
        self.start_button = Button(text='Start', size_hint=(None, None), size=(100, 100))
        self.start_button.bind(on_press=self.toggle_start_pause)
        self.layout.add_widget(self.start_button)

        # Timer variables
        self.seconds = 0
        self.is_paused = True
        self.is_running = False
        self.is_resting = False
        self.thread = None  # Keep track of the running thread

        # Initialize pygame mixer for playing sounds
        pygame.mixer.init()

        return self.layout

    def start_timer(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.run_timer, daemon=True)
        self.thread.start()

    def run_timer(self):
        while self.is_running:
            if not self.is_paused:
                if not self.is_resting:
                    if self.seconds == 0:
                        self.play_sound('start.mp3')
                        self.timer_label.text = "Start"
                    elif 1 <= self.seconds <= 10:
                        self.timer_label.text = str(self.seconds)
                        self.play_number_sound(self.seconds)
                    elif self.seconds == 11:
                        self.play_sound('ting.mp3')
                        self.timer_label.text = "Relax"
                        self.is_resting = True
                        self.seconds = 0  # Reset seconds for resting period
                    self.seconds += 1
                else:
                    self.timer_label.text = f"Rest: {self.seconds}"
                    if self.seconds == 15:
                        self.is_resting = False
                        self.seconds = 0  # Reset the count and go back to start
                    else:
                        self.seconds += 1  # Increment only once in rest mode
            time.sleep(1)  # Wait for 1 second

    def play_number_sound(self, number):
        file_path = f'{number}.mp3'
        self.play_sound(file_path)

    def play_sound(self, sound_file):
        sound_path = os.path.join('assets/sounds', sound_file)
        if os.path.exists(sound_path):
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        else:
            print(f"Sound file {sound_path} not found.")

    def toggle_start_pause(self, instance):
        if self.is_paused:
            self.is_paused = False
            self.start_button.text = "Pause"
            if self.thread is None or not self.thread.is_alive():
                self.start_timer()  # Start the timer if it's not already running
        else:
            self.is_paused = True
            self.start_button.text = "Start"

    def reset_timer(self, instance):
        # Stop the current thread and reset everything
        self.is_running = False
        self.is_paused = True
        self.seconds = 0
        self.is_resting = False
        self.timer_label.text = "Start"
        self.start_button.text = "Start"

        # Wait for any existing thread to stop
        if self.thread is not None and self.thread.is_alive():
            self.thread.join()

        # Now set the timer to a paused state and start fresh
        self.is_running = False
        self.thread = None

if __name__ == '__main__':
    TimerApp().run()
