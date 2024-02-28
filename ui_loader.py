import pygame
from scripts import spritefont
from scripts.ui import (
    UiManager,
    UiPage,
    Element,
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

    manager.add_page(_page)