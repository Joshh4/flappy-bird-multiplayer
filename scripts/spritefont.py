import pygame as pg

COLORKEY = (9, 0, 17)

class SpriteFont(object):
    STANDARD_CHARS = (
        r"""abcdefghijklmnopqrstuvwxyz"""
        r"""ABCDEFGHIJKLMNOPQRSTUVWXYZ"""
        r"""0123456789.,?!&@/|\<>()[]{}#'"^+-=_"""
    )
    def __init__(
            self,
            surface:pg.Surface,
            colour:tuple[int,int,int]=(255,255,255),
            char_order:str=STANDARD_CHARS):
        self.colour = colour
        self.char_order = char_order
        self.char_spacing = 1
        self.chars = {}
        # modify the font colour
        px = pg.PixelArray(surface)
        px.replace((255, 255, 255), colour)
        surface = px.make_surface()
        px.close()
        # load chars
        char_index = 0
        # pg.image.save(surface, "font.png")
        w,h = surface.get_size()
        last_clear = True
        char_w = 0
        for x in range(w):
            rgb = surface.get_at((x,0))[:3]
            if rgb == COLORKEY:
                if not last_clear:
                    # save this char
                    char = char_order[char_index]
                    char_surf = pg.Surface((char_w, h-2))
                    char_surf.set_colorkey(COLORKEY)
                    char_surf.blit(surface, (-(x-char_w), -2))
                    self.chars[char] = (char_surf, char_w)
                last_clear = True
                char_w = 0
                char_index += 1
            else:
                last_clear = False
                char_w += 1
        self.chars[" "] = (None, 3)
        self.chars["\n"] = (None, 0)
        self.char_h = h-2
    
    def render_to(
            self,
            text:str,
            surface:pg.Surface,
            position:pg.Vector2,
            alignment:tuple[int,int]=(-1,-1)):
        text_surface, offset = self.render(
            text=text,
            alignment=alignment)
        surface.blit(text_surface, position+offset)
    
    def render(
            self,
            text:str,
            alignment:tuple[int,int]=(-1,-1)):
        # remove any chars we can't draw
        text = "".join([char for char in text if char in self.chars])
        # calculate the total text width so we can align
        lines = text.split("\n")
        line_widths = [
            sum([self.chars[char][1] for char in line])+len(line)*self.char_spacing\
            for line in lines]
        total_w = max(line_widths)
        total_h = (text.count("\n")+1)*(self.char_h+1)-1
        
        surface = pg.Surface((total_w, total_h))
        surface.set_colorkey(COLORKEY)
        surface.fill(COLORKEY)

        position = pg.Vector2()

        # adjust position for alignment
        if alignment[0] == 0:
            position.x -= int(total_w/2)
        elif alignment[0] == 1:
            position.x -= total_w
        if alignment[1] == 0:
            position.y -= int(total_h/2)
        elif alignment[1] == 1:
            position.y -= total_h
        # render each char individually
        x = 0
        y = 0
        for char in text:
            char_surf, char_w = self.chars[char]
            if char_surf:
                surface.blit(char_surf, (x, y))
            x += char_w+self.char_spacing
            if char == "\n":
                x = 0
                y += self.char_h+1
        return surface, position
    
    def render_font_surface(self):
        # remove any chars we can't draw
        text = "".join(self.chars.keys())+" "
        # calculate the total text width so we can align
        total_w = sum([self.chars[char][1] for char in text])+len(text)*self.char_spacing-1
        total_h = self.char_h+2
        # create the new surface
        surface = pg.Surface((total_w, total_h))
        surface.set_colorkey(COLORKEY)
        surface.fill(COLORKEY)
        # render each char individually
        x = 0
        y = 2
        for char in text:
            char_surf, char_w = self.chars[char]
            if char_surf:
                for sx in range(char_w+(self.char_spacing-1)):
                    surface.set_at((x+sx, 0), (0,0,0))
                surface.blit(char_surf, (x, y))
            x += char_w+self.char_spacing
        return surface