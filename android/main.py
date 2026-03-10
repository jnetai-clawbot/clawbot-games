#!/usr/bin/env python3
"""
ClawBot Android - Kivy App Template
A simple Android app template using Kivy
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty

# Set window size for testing (will be fullscreen on Android)
Window.size = (360, 640)

class HomeScreen(Screen):
    pass

class CalcScreen(Screen):
    display = StringProperty("0")
    
    def num_press(self, num):
        if self.display == "0":
            self.display = str(num)
        else:
            self.display += str(num)
    
    def op_press(self, op):
        self.display += op
    
    def clear(self):
        self.display = "0"
    
    def calculate(self):
        try:
            result = eval(self.display)
            self.display = str(result)
        except:
            self.display = "Error"

class QuizScreen(Screen):
    score = StringProperty("0")
    question = StringProperty("What is 2 + 2?")
    answer = StringProperty("")
    
    questions = [
        ("What is 2 + 2?", "4"),
        ("What is 5 + 3?", "8"),
        ("What is 10 - 4?", "6"),
        ("What is 3 × 3?", "9"),
        ("What is 12 ÷ 4?", "3"),
    ]
    current = 0
    
    def check_answer(self):
        if self.answer == self.questions[self.current][1]:
            self.score = str(int(self.score) + 1)
        self.next_question()
    
    def next_question(self):
        self.current = (self.current + 1) % len(self.questions)
        self.question = self.questions[self.current][0]
        self.answer = ""

class ClawBotAndroidApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CalcScreen(name='calc'))
        sm.add_widget(QuizScreen(name='quiz'))
        return sm

if __name__ == '__main__':
    ClawBotAndroidApp().run()
