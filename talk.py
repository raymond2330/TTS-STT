import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import speech_recognition as sr
from gtts import gTTS
import os

class SpeechApp(App): # Home page
    def build(self):
        self.title = 'Speech Recognition and Text-to-Speech'

        layout = BoxLayout(orientation='horizontal', padding=10)    

        speech_to_text_button = Button(text='Speech to Text', size_hint=(1, 0.5))
        speech_to_text_button.bind(on_press=self.open_speech_to_text)
        layout.add_widget(speech_to_text_button)

        text_to_speech_button = Button(text='Text to Speech', size_hint=(1, 0.5))
        text_to_speech_button.bind(on_press=self.open_text_to_speech)
        layout.add_widget(text_to_speech_button)

        return layout

    def open_speech_to_text(self, instance):
        self.stop()
        SpeechToTextApp().run()

    def open_text_to_speech(self, instance):
        self.stop()
        TextToSpeechApp().run()

class SpeechToTextApp(App): #STT
    def build(self):
        
        self.return_button = Button(text="Home", size=(.5, .5))
        
        self.title = 'Speech to Text'

        layout = BoxLayout(orientation='vertical', padding=10)

        self.output_label = Label(text='Output will appear here', size_hint=(1, 0.5))
        layout.add_widget(self.output_label)

        self.start_button = Button(text='Start Recording', size_hint=(1, 0.1))
        self.start_button.bind(on_press=self.start_recording)
        layout.add_widget(self.start_button)

        self.stop_button = Button(text='Stop Recording', size_hint=(1, 0.1))
        self.stop_button.bind(on_press=self.stop_recording)
        self.stop_button.disabled = True
        layout.add_widget(self.stop_button)

        return layout

    def start_recording(self, instance):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            self.audio = self.recognizer.listen(source)

        self.start_button.disabled = True
        self.stop_button.disabled = False

    def stop_recording(self, instance):
        try:
            print("Recognizing...")
            text = self.recognizer.recognize_google(self.audio)
            self.output_label.text = "You said: " + text
        except sr.UnknownValueError:
            self.output_label.text = "Sorry, could not understand audio."
        except sr.RequestError as e:
            self.output_label.text = "Could not request results; {0}".format(e)

        self.start_button.disabled = False
        self.stop_button.disabled = True

class TextToSpeechApp(App): #TTS
    def build(self):
        self.title = 'Text to Speech'

        layout = BoxLayout(orientation='vertical', padding=10)

        self.text_input = TextInput(hint_text='Enter text here', multiline=False, size_hint=(1, 0.1))
        layout.add_widget(self.text_input)

        text_to_speech_button = Button(text='Convert to Speech', size_hint=(1, 0.1))
        text_to_speech_button.bind(on_press=self.text_to_speech)
        layout.add_widget(text_to_speech_button)

        return layout

    def text_to_speech(self, instance):
        text = self.text_input.text
        if text:
            tts = gTTS(text=text, lang='en')
            tts.save("output.mp3")
            os.system("start output.mp3")
        else:
            self.output_label.text = "Please enter some text first."

if __name__ == "__main__":
    SpeechApp().run()