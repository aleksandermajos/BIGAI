import flet as ft
import flet as ft
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)


def main(page: ft.Page):
    def open_file_dialog(e):
        # Open file dialog to choose a video file
        file_picker.pick_files(file_type=ft.FilePickerFileType.VIDEO)

    def file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            # Display the selected video file path
            selected_file_path.value = e.files[0].name
            video_file_path = e.files[0].path


            page.update()

    # Create a button to open the file picker
    open_file_button = ft.ElevatedButton("Choose Video File",icon=icons.UPLOAD_FILE, on_click=open_file_dialog)

    # Create a label to display the selected file path
    selected_file_path = ft.Text(value="No file selected")



    # Create a file picker
    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    # Add the UI elements to the page
    page.add(
        open_file_button,
        selected_file_path,
    )


# Run the Flet app
ft.app(target=main)



