import pygame
from scripts import spritefont
from scripts.ui import (
    UiManager,
    UiPage,
    Element,
    Container,
    ElementRenderer,
    Label
)

def init_ui(
        manager: UiManager,
        path_font_file: str
    ):
    """Initializes all required ui pages for Flappy Friends.

    Args:
        manager (UiManager): The UI Manager instance.
    """

    font_main = spritefont.SpriteFont(
        surface=pygame.image.load(path_font_file).convert(),
        colour=(255, 255, 255))

    font_secondary = spritefont.SpriteFont(
        surface=pygame.image.load(path_font_file).convert(),
        colour=(140, 140, 140))
    


    _page = UiPage("connecting")
    _page.add_element(Label(
        identifier="label_1",
        position=(150, 5),
        text="Connecting to Flappy Friends server...",
        text_alignment=(0,-1),
        font=font_secondary
    ))

    manager.add_page(_page)
    




    # Main menu page

    def main_menu_join_clicked():
        manager.set_page("game_join")

    def main_menu_create_clicked():
        manager.set_page("game_create")

    _page = UiPage("main")
    _page.add_element(Label(
        identifier="label_1",
        position=(150, 5),
        text="Flappy Friends",
        text_alignment=(0,-1),
        font=font_main
    ))
    _page.add_element(Label(
        identifier="label_2",
        position=(150, 15),
        text="Main Menu",
        text_alignment=(0,-1),
        font=font_secondary
    ))

    _button_panel = Container(
        identifier="button_container",
        rect=pygame.Rect(20, 75, 0, 0)
    )

    _button = Container(
        identifier="button_join_game",
        rect=pygame.Rect(0, 0, 100, 20))
    _button_left = _button.add_child(Element(
        "button_1_left",
        rect=pygame.Rect(0, 5, 2, 10),
        renderer=ElementRenderer()
    ))
    _button_left.renderer.color = (230, 230, 230)
    _button.add_child(Label(
        identifier="button_1_text",
        position=( 6, 8 ),
        text="Join A Game",
        text_alignment=(-1, -1),
        font=font_main
    ))
    _button.can_click = True
    _button.on_click = main_menu_join_clicked
    _button_panel.add_child(_button)

    _button = Container(
        identifier="button_create_game",
        rect=pygame.Rect(0, 30, 100, 20))
    _button_left = _button.add_child(Element(
        "button_2_left",
        rect=pygame.Rect(0, 5, 2, 10),
        renderer=ElementRenderer()
    ))
    _button_left.renderer.color = (230, 230, 230)
    _button.add_child(Label(
        identifier="button_2_text",
        position=( 6, 8 ),
        text="Create New Game",
        text_alignment=(-1, -1),
        font=font_main
    ))
    _button.can_click = True
    _button.on_click = main_menu_create_clicked
    _button_panel.add_child(_button)

    _page.add_element(_button_panel)

    manager.add_page(_page)