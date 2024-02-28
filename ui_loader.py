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

    _button_1 = Container(
        identifier="button_1",
        rect=pygame.Rect(10, 30, 80, 10))
    _button_1_left = _button_1.add_child(Element(
        "button_1_left",
        rect=pygame.Rect(0,0,2,10),
        renderer=ElementRenderer()
    ))
    _button_1_left.renderer.color = (230, 230, 230)
    _button_1_text = _button_1.add_child(Label(
        identifier="button_1_text",
        position=( 5, 2 ),
        text="Join A Game",
        text_alignment=(-1, -1),
        font=font_main
    ))
    _page.add_element(_button_1)

    manager.add_page(_page)