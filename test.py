import flet as ft

def main(page: ft.Page):
    page.title = "App Flet"
    page.window.width = 300
    page.window.height = 90
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # page.window.resizable = False
    # page.window.maximizable = False
    page.window.center()
    page.bgcolor = ft.ThemeMode.DARK
    
    layout = ft.Text(
        "Hello World!", 
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD
    )
 
    page.add(layout)
ft.app(main)