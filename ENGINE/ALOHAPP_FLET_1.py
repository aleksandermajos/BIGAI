import flet as ft

def main(page: ft.Page):
    # Function to play a sound
    def play_sound(word):
        page.snack_bar = ft.SnackBar(ft.Text(f"Playing sound for '{word}'"))
        page.snack_bar.open()

    # Function to toggle the visibility of the context menu
    def toggle_context_menu(e, menu_container):
        if e.data == "true":  # Mouse is over the word
            menu_container.visible = True
        else:  # Mouse has left the word
            menu_container.visible = False
        page.update()

    # List of words with their properties
    words = [
        {"word": "Hello", "color": "red"},
        {"word": "world", "color": "blue"}
    ]

    # Creating word and menu components
    content = []
    for item in words:
        # Menu container
        menu_container = ft.Container(
            content=ft.TextButton("Play Sound", on_click=lambda _: play_sound(item["word"])),
            bgcolor="white",
            border=ft.border.all(1, "black"),
            padding=ft.padding.all(10),
            opacity=0.8,  # Semi-transparent menu
            visible=False,  # Menu hidden by default
        )

        # Word container
        word_container = ft.Container(
            content=ft.Text(item["word"], size=18, weight="bold", color=item["color"]),
            padding=ft.padding.all(10),
            on_hover=lambda e, menu=menu_container: toggle_context_menu(e, menu)
        )

        # Adding the word and menu to the layout
        content.append(ft.Column([word_container, menu_container], spacing=5))

    # Adding content to the page
    page.add(ft.Column(content, alignment="center"))

# Run the application
ft.app(target=main)