"""

This file is responsible for handling pygame UI.

The technical requirements are:

    Store page index / name

    Show text, buttons, or images for pages

    Allow clicking buttons

"""

import pygame
from typing import List, Dict, Union, Tuple
from . import spritefont


class UiManager(object):
    pages: Dict[str, "UiPage"]
    current_page_identifier: str
    current_page: "UiPage"

    def __init__(self) -> None:
        self.pages = {}
    
    def set_page(self, identifier:str):
        self.current_page_identifier = identifier
        self.current_page = self.get_page(identifier)
    
    def add_page(self, page:"UiPage"):
        self.pages[page.identifier] = page
    
    def get_page(self, identifier:str):
        return self.pages.get(identifier)
    
    def render(self, surface:pygame.Surface):
        if self.current_page is not None:
            self.current_page.render(surface)

    def update(self, events:List[pygame.event.Event]):
        pass


class UiPage(object):
    identifier: str
    root: "Element"

    def __init__(self, identifier:str) -> None:
        self.identifier = identifier
        self.root = Element(
            identifier="root",
            renderer=ElementRenderer.empty_renderer())
    
    def add_element(self, element:"Element") -> None:
        self.root.add_child(element)
    
    def get_element(self, path:str) -> Union["Element", None]:
        """Gets an element given a path.
        See Element.get_child docstring for
        more information.

        Args:
            identifier (str): The element identifier to look for.

        Returns:
            Element | None : The element, or None.
        """
        return self.root.get_child(path)
    
    def render(self, surface:pygame.Surface):
        """Renders this page onto the provided pygame Surface.

        Args:
            surface (pygame.Surface): The surface to render to.
        """
        self.root.render(surface)


class ElementRenderer(object):
    @staticmethod
    def empty_renderer():
        r = ElementRenderer()
        r.show_rect = False
        return r
    
    def __init__(self):
        self.show_rect = True
        self.rect_width = 0
        self.color = (255, 255, 255)
        self.rect_border_radius = -1
        self.rect_border_top_left_radius = -1
        self.rect_border_top_right_radius = -1
        self.rect_border_bottom_left_radius = -1
        self.rect_border_bottom_right_radius = -1
    
    def render(self, element:"Element", surface:pygame.Surface):
        if self.show_rect:
            pygame.draw.rect(
                surface=surface,
                color=self.color,
                rect=element.rect,
                width=self.rect_width,
                border_radius=self.rect_border_radius,
                border_top_left_radius=self.rect_border_top_left_radius,
                border_top_right_radius=self.rect_border_top_right_radius,
                border_bottom_left_radius=self.rect_border_bottom_left_radius,
                border_bottom_right_radius=self.rect_border_bottom_right_radius
            )


class Element(object):
    identifier: str
    children: List["Element"]
    rect: pygame.Rect
    renderer: ElementRenderer
    parent: "Element"

    def __init__(self,
                 identifier:str,
                 rect:Union[pygame.Rect, tuple, None]=None,
                 renderer:Union[ElementRenderer, None]=None) -> None:
        self.parent = None
        self.children = []
        self.identifier = identifier
        self.local_rect = pygame.Rect(0,0,0,0) if rect is None else rect
        self.refresh_global_rect()
        self.renderer = renderer or ElementRenderer()
    
    def refresh_global_rect(self):
        print(f"Refresh global rect {self.identifier}")
        if self.parent is None:
            self.rect = self.local_rect
        else:
            self.rect = self.local_rect.copy()
            self.rect.x += self.parent.rect.x
            self.rect.y += self.parent.rect.y
            print(f"Offset by {self.parent.rect.x}, {self.parent.rect.y}")

    def set_parent(self, parent:"Element"):
        self.parent = parent
    
    def add_child(self, child:"Element") -> "Element":
        child.set_parent(self)
        self.children.append(child)
        child.refresh_global_rect()
        return child
    
    def get_child_by_identifier(self, identifier:str) -> Union["Element", None]:
        """Gets this element's child based on identifier.
        If no direct child matching the identifier could be
        found then the function returns None.

        Args:
            identifier (str): The element identifier to look for.

        Returns:
            Element | None : The element, or None.
        """
        for child in self.children:
            if child.identifier == identifier:
                return child
        raise Exception(f"Could not find ui element with identifier \"{identifier}\".")

    def get_child(self, path:str) -> Union["Element", None]:
        """Gets this element's child given a path.
        A path is a string of identifiers, separated by "/".
        If no element was found, then the function returns None.

        Args:
            path (str): The relative path to the element.

        Returns:
            Element | None : The element, or None.
        """
        root = self
        identifiers = path.split("/")
        for identifier in identifiers:
            root = root.get_child_by_identifier(identifier)
            if root is None:
                raise Exception(f"While processing get_child with path \"{path}\", could not find element.")
        return root
    
    def render(
            self,
            surface:pygame.Surface):
        # Draw this element and all children elements
        if self.rect is not None:
            self.renderer.render(self, surface)
        for child in self.children:
            child.render(surface)

class Container(Element):
    def __init__(self,
                 identifier: str,
                 rect: Union[pygame.Rect, Tuple, None] = None) -> None:
        super().__init__(identifier=identifier,
                         rect=rect,
                         renderer=ElementRenderer.empty_renderer())

class Label(Element):
    text: str
    font: spritefont.SpriteFont

    def __init__(self,
                 identifier:str,
                 position:Tuple[int, int]=(0,0),
                 text:str="Text",
                 text_alignment:tuple=(-1, -1),
                 font:spritefont.SpriteFont=None):
        super().__init__(identifier=identifier,
                         rect=pygame.Rect(position[0],
                                          position[1],
                                          0,
                                          0),
                         renderer=ElementRenderer.empty_renderer())
        self.text = text
        self.text_alignment = text_alignment
        self.font = font
        self.refresh_font_surface()
    
    def refresh_font_surface(self):
        self.font_surface, self.font_surface_position = self.font.render(self.text, self.text_alignment)
        self.font_surface_position.x += self.rect.left
        self.font_surface_position.y += self.rect.top
    
    def render(self, surface:pygame.Surface):
        super().render(surface)
        surface.blit(
            self.font_surface,
            self.font_surface_position)
