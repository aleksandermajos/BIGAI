import whisper
import flet as ft


def main(page: ft.Page):
    page.title = "Speech Recognizer"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Create a text input field for displaying recognized text
    text_input = ft.TextField(width=500, height=200)

    # Create a button to start speech recognition
    def start_recognition(e):
        # Initialize Whisper speech recognizer
        model = whisper.load_model("tiny.en")

        # Start recognizing speech and update the text input field
        result = model.transcribe("recording.wav")
        text_input.value = result.text

    recognize_button = ft.ElevatedButton("Start Recognizing", on_click=start_recognition)

    # Add controls to the page
    page.add(
        ft.Row(
            [
                text_input,
                recognize_button,
            ]
        )
    )

ft.app(main)
