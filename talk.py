import kivy
import pyttsx3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
import speech_recognition as sr
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard

class OnboardingPage(App): # ONBOARDING
    def build(self):
        self.title = 'SpeakCast'
        Window.clearcolor = get_color_from_hex('#2274F0')
        Window.size = (300, 550)
        self.window = GridLayout()
        self.window.cols = 1

        # First Onboard
        self.window.add_widget(Label())
        image = Image(source="images/whiteCastSpeakLogo.png")
        self.window.add_widget(image)
        self.window.add_widget(Label())

        self.landingGreeting = Label(
            text="Speak and Read with Confidence",
            color='#FFFFFF',    
            font_size='30',
            italic=True
        )
        self.window.add_widget(self.landingGreeting)

        # PROCEED BUTTON
        proceed_in_onboarding = Button(
            text="Proceed",
            color='#FFFFFF',
            background_color="#2274F0",
            bold=True,
            font_size='25'
        )
        proceed_in_onboarding.bind(on_press=self.proceed_onboarding)
        self.window.add_widget(proceed_in_onboarding)

        return self.window

    def proceed_onboarding(self, instance):
        self.stop()
        SpeechApp().run()

class SpeechApp(App): # Home page
    def build(self):
        self.title = 'SpeakCast'
        Window.clearcolor = get_color_from_hex('#FFFFFF')
        Window.size = (300, 550)
        self.window = GridLayout(cols=1)

        # Image
        self.window.add_widget(Label())  # BLANK
        self.window.add_widget(Image(source="images/CastSpeakLogo.png"))
        self.window.add_widget(Label())  # BLANK

        # Greeting Text
        self.window.add_widget(Label())  # BLANK
        self.homeGreeting = Label(
            text="Welcome to SpeakCast",
            color='#000000',
            font_size='50',
            bold=True
        )
        self.window.add_widget(self.homeGreeting)
        self.window.add_widget(Label())  # BLANK

        # Supporting Text
        self.window.add_widget(Label())  # BLANK
        self.homeDescription = Label(
            text="Use speech-to-text and text-to-speech \n technologies to communicate confidently",
            color='#B6B0B0',
            halign='center',
            valign='middle',
            font_size='28'
        )
        self.window.add_widget(self.homeDescription)
        self.window.add_widget(Label())  # BLANK

        # Swap Button
        self.swap_button = Button(
            text='Swap to Text to Speech',
            color="#FFFFFF",
            halign='center',
            valign='middle',
            background_color='#68A3FB',
            font_size="20",
            bold=True
        )
        self.swap_button.bind(on_press=self.swap_functionality)
        self.window.add_widget(self.swap_button)

        # Main Button
        self.main_button = Button(
            text='Speech\nto\nText',
            color="#FFFFFF",
            halign='center',
            valign='middle',
            background_color='#68A3FB',
            font_size="20",
            bold=True
        )
        self.main_button.bind(on_press=self.open_speech_to_text)
        self.window.add_widget(self.main_button)

        return self.window
    
    def open_speech_to_text(self, instance):
        self.stop()
        SpeechToTextApp().run()

    def open_text_to_speech(self, instance):
        self.stop()
        TextToSpeechApp().run()

    def swap_functionality(self, instance):
        if self.main_button.text == 'Speech\nto\nText':
            self.main_button.text = 'Text\nto\nSpeech'
            self.main_button.unbind(on_press=self.open_speech_to_text)
            self.main_button.bind(on_press=self.open_text_to_speech)
            self.swap_button.text = 'Swap to Speech to Text'
        else:
            self.main_button.text = 'Speech\nto\nText'
            self.main_button.unbind(on_press=self.open_text_to_speech)
            self.main_button.bind(on_press=self.open_speech_to_text)
            self.swap_button.text = 'Swap to Text to Speech'

class SpeechToTextApp(App): # STT
    def build(self):
        self.title = 'Speech to Text'
        layout = BoxLayout(orientation='vertical', padding=10)

        self.output_label = Label(
            text='Output will appear here',
            size_hint=(1, 0.1),
            color="#000000"
        )
        layout.add_widget(self.output_label)

        self.start_button = Button(
            text='Start\nRecording',
            color="#FFFFFF",
            halign='center',
            valign='middle',
            background_color='#68A3FB',
            font_size="20",
            size_hint=(1, 0.1),
            bold=True
        )
        self.start_button.bind(on_press=self.start_recording)
        layout.add_widget(self.start_button)

        self.stop_button = Button(
            text='Stop\nRecording',
            color="#FFFFFF",
            halign='center',
            valign='middle',
            background_color='#68A3FB',
            font_size="20",
            size_hint=(1, 0.1),
            bold=True
        )
        self.stop_button.bind(on_press=self.stop_recording)
        self.stop_button.disabled = True
        layout.add_widget(self.stop_button)

        self.copy_button = Button(
            text='Copy\nText',
            color="#FFFFFF",
            halign='center',
            valign='middle',
            background_color='#68A3FB',
            font_size="20",
            size_hint=(1, 0.1),
            bold=True
        )
        self.copy_button.bind(on_press=self.copy_text)
        layout.add_widget(self.copy_button)

        # Back Button
        back_button = Button(
            text='Back\nto\nHome',
            color="#FFFFFF",
            halign='center',
            valign='middle',
            background_color='#68A3FB',
            font_size="20",
            size_hint=(1, 0.1),
            bold=True
        )
        back_button.bind(on_press=self.go_back_to_home)
        layout.add_widget(back_button)

        return layout

    def copy_text(self, instance):
        Clipboard.copy(self.output_label.text)

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
            self.show_popup("Error", "Sorry, could not understand audio.")
        except sr.RequestError as e:
            self.show_popup("Error", f"Could not request results; {e}")

        self.start_button.disabled = False
        self.stop_button.disabled = True

    def show_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=10)
        label = Label(text=message, size_hint=(1, 0.8))
        layout.add_widget(label)

        popup = Popup(title=title, content=layout, size_hint=(0.8, 0.3))
        popup.open()

        # Automatically dismiss the popup after 3 seconds
        Clock.schedule_once(popup.dismiss, 3)

    def go_back_to_home(self, instance):
        self.stop()
        SpeechApp().run()

class TextToSpeechApp(App): # TTS
    def build(self):
        self.title = 'Text to Speech'
        layout = BoxLayout(orientation='vertical', padding=10)

        self.engine = pyttsx3.init()  # Initialize the engine once
        self.text_input = TextInput(hint_text='Enter text here', multiline=False, size_hint=(1, 0.1))
        layout.add_widget(self.text_input)

        text_to_speech_button = Button(
            text='Convert\nto\nSpeech',
            color="#FFFFFF",
            halign='center',
            valign='middle',
            background_color='#68A3FB',
            font_size="20",
            size_hint=(1, 0.1),
            bold=True
        )
        text_to_speech_button.bind(on_press=self.text_to_speech)
        layout.add_widget(text_to_speech_button)

        # Back Button
        back_button = Button(
            text='Back\nto\nHome',
            color="#FFFFFF",
            halign='center',
            valign='middle',
            background_color='#68A3FB',
            font_size="20",
            size_hint=(1, 0.1),
            bold=True
        )
        back_button.bind(on_press=self.go_back_to_home)
        layout.add_widget(back_button)

        return layout

    def text_to_speech(self, instance):
        text = self.text_input.text
        if text:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            self.show_popup("Please enter some text first.")

    def show_popup(self, message):
        popup_content = BoxLayout(orientation='vertical', padding=10)
        popup_label = Label(text=message)
        popup_content.add_widget(popup_label)

        popup = Popup(title="Error", content=popup_content, size_hint=(0.8, 0.3))
        popup.open()

    def go_back_to_home(self, instance):
        self.stop()
        SpeechApp().run()

    def on_stop(self):
        # Terminate the engine when the app stops
        self.engine.stop()
        super().on_stop()

if __name__ == "__main__":
    OnboardingPage().run()
