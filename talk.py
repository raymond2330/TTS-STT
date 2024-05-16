import kivy
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
from gtts import gTTS
import os

class BaseApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_page = None

    def change_page(self, page):
        if self.current_page:
            self.current_page.clear_widgets()
        self.current_page = page
        self.root_window.remove_widget(self.root)
        self.root_window.add_widget(self.current_page)

class OnboardingPage(GridLayout): #ONBOARDING
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = get_color_from_hex('#2274F0')
        self.cols = 1

        self.add_widget(Label())  # BLANK
        image = Image(source="images/whiteCastSpeakLogo.png")
        self.add_widget(image)
        self.add_widget(Label())  # BLANK

        landing_greeting = Label(
            text="Speak and Read with Confidence",
            color='#FFFFFF',    
            font_size='30',
            italic=True
        )
        self.add_widget(landing_greeting)

        proceed_in_onboarding = Button(
            text="Proceed",
            color='#FFFFFF',
            background_color="#2274F0",
            bold=True,
            font_size='25'
        )
        proceed_in_onboarding.bind(on_press=self.proceed_onboarding)
        self.add_widget(proceed_in_onboarding)

    def proceed_onboarding(self, instance):
        app = App.get_running_app()
        app.change_page(SpeechApp())

class SpeechApp(GridLayout):  # Home page
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = get_color_from_hex('#FFFFFF')
        self.cols = 1

        self.add_widget(Label())  # BLANK
        home_greeting = Label(
            text="Welcome to SpeakCast",
            color='#000000',
            font_size='50',
            bold=True
        )
        self.add_widget(home_greeting)

        home_description = Label(
            text="Use speech-to-text and text-to-speech \n technologies to communicate confidently",
            color='#B6B0B0',
            halign='center',
            valign='middle',
            font_size='28'
        )
        self.add_widget(home_description)

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
        self.add_widget(self.swap_button)

        self.main_button = Button(
            text='Speech\nto\nText',
            color="#FFFFFF",
            halign='center',
            valign='middle',
            background_color='#68A3FB',
            font_size="30",
            bold=True
        )
        self.main_button.bind(on_press=self.open_speech_to_text)
        self.add_widget(self.main_button)

    def open_speech_to_text(self, instance):
        app = App.get_running_app()
        app.change_page(SpeechToTextApp())

    def open_text_to_speech(self, instance):
        app = App.get_running_app()
        app.change_page(TextToSpeechApp())

    def swap_functionality(self, instance):
        main_button = self.main_button
        swap_button = self.swap_button

        if main_button.text == 'Speech\nto\nText':
            main_button.text = 'Text\nto\nSpeech'
            main_button.unbind(on_press=self.open_speech_to_text)
            main_button.bind(on_press=self.open_text_to_speech)
            swap_button.text = 'Swap to Speech to Text'
        else:
            main_button.text = 'Speech\nto\nText'
            main_button.unbind(on_press=self.open_text_to_speech)
            main_button.bind(on_press=self.open_speech_to_text)
            swap_button.text = 'Swap to Text to Speech'


class SpeechToTextApp(BoxLayout): #STT
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = get_color_from_hex('#FFFFFF')
        self.orientation = 'vertical'

        self.output_label = Label(
            text='Output will appear here',
            size_hint=(1, 0.5),
            color="#000000"
        )
        self.add_widget(self.output_label)

        self.start_button = Button(text='Start Recording', size_hint=(1, 0.1))
        self.start_button.bind(on_press=self.start_recording)
        self.add_widget(self.start_button)

        self.stop_button = Button(text='Stop Recording', size_hint=(1, 0.1))
        self.stop_button.bind(on_press=self.stop_recording)
        self.stop_button.disabled = True
        self.add_widget(self.stop_button)

        back_button = Button(text='Back to Home', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back_to_home)
        self.add_widget(back_button)

    def start_recording(self, instance):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.recognizer = recognizer
        self.audio = audio

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

    def go_back_to_home(self, instance):
        app = App.get_running_app()
        app.change_page(SpeechApp())

class TextToSpeechApp(BoxLayout): #TTS
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = get_color_from_hex('#FFFFFF')
        self.orientation = 'vertical'

        self.text_input = TextInput(hint_text='Enter text here', multiline=False, size_hint=(1, 0.1))
        self.add_widget(self.text_input)

        text_to_speech_button = Button(text='Convert to Speech', size_hint=(1, 0.1))
        text_to_speech_button.bind(on_press=self.text_to_speech)
        self.add_widget(text_to_speech_button)

        back_button = Button(text='Back to Home', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back_to_home)
        self.add_widget(back_button)

    def text_to_speech(self, instance):
        text = self.text_input.text
        if text:
            tts = gTTS(text=text, lang='en')
            tts.save("output.mp3")
            os.system("start output.mp3")
        else:
            self.output_label.text = "Please enter some text first."

    def go_back_to_home(self, instance):
        app = App.get_running_app()
        app.change_page(SpeechApp())

class SpeakCastApp(BaseApp):
    def build(self):
        return OnboardingPage()

if __name__ == "__main__":
    SpeakCastApp().run()
