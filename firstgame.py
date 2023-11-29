import pygame


def arrows_movment_x(key_pressed, x, limit_x):
    """פונקציה מזיזה את האוביקט על ציר הX היא מקבלת האם נלחץ, את המיקום על ציר הX ומה הגבול של המסגרת"""
    if key_pressed[pygame.K_LEFT]:
        x -= 1
        if 0 >= x:
            x = 0
    elif key_pressed[pygame.K_RIGHT]:
        x += 1
        if x >= limit_x-30:
            x = limit_x-30
    return x


def arrows_movment_y(key_pressed, y, limit_y):
    """פונקציה מזיזה את האוביקט על ציר הY היא מקבלת האם נלחץ, את המיקום על ציר הY ומה הגבול של המסגרת"""
    if key_pressed[pygame.K_UP]:
        y -= 1
        if 0 >= y:
            y = 0
    elif key_pressed[pygame.K_DOWN]:
        y += 1
        if y >= limit_y-30:
            y = limit_y-30
    return y


class Block (pygame.sprite.Sprite):
    """מחלקה יוצרת של קוביות במשחק"""

    def __init__(self, x, y):
        super(self.__class__, self).__init__()
        self.image = pygame.image.load(r'C:\Users\netan\Downloads\black_clock_for_soccer_game.png').convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._vx = 0
        self._vy = 0

    def update_v(self, vx, vy):
        """מעדכן את משתנה המהירות, מקבל מהירות חדשה על ציר הX ואז על ציר הY"""
        self._vx = vx
        self._vy = vy

    def update_loc_x(self):
        """פונקציה שמזיזה את האובייקט על ידי השיננוי במהירות על ציר הX"""
        self.rect.x += self._vx

    def update_loc_y(self):
        """פונקציה שמזיזה את האובייקט על ידי השיננוי במהירות על ציר הY"""
        self.rect.y += self._vy

    def update_loc_x_v(self, x, y):
        """פונקציה שמעדכנת את ה X ואז את הY"""
        self.rect.y = y
        self.rect.x = x

    def get_pos(self):
        """הפונקציה מחזירה את המיקום של האובייקט, קודם על ציר הX ואז על ציר הY"""
        return self.rect.x, self.rect.y

    def get_v(self):
        """הפונקציה מחזירה את מהירות האובייקט, קודם על ציר הX ואז על ציר הY"""
        return self._vx, self._vy

    def touch_frame_block(self, WINDOW_WIDTH):
        """ בודק האם האובייקט של הבלוק נוגע בצד המסך ואם כן מביא לו מהירות הפוכה """
        if self.rect.x + 100 > WINDOW_WIDTH or self.rect.x < 0:
            self._vx *= -1


class Player (pygame.sprite.Sprite):
    """מחלקה יוצרת של השחקן"""

    def __init__(self, x, y):
        super(self.__class__, self).__init__()
        self.PLAYER_PIC_WIDTH = 25
        self.PLAYER_PIC_HEIGHT = 25
        self.player_pic1 = pygame.image.load(r'C:\Users\netan\Downloads\soccer-ball-png-31.png')
        self.image = pygame.transform.scale(self.player_pic1, (self.PLAYER_PIC_WIDTH, self.PLAYER_PIC_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._vx = 0
        self._vy = 0

    def update_v(self, vx, vy):
        """מעדכן את משתנה המהירות, מקבל מהירות חדשה על ציר הX ואז על ציר הY"""
        self._vx = vx
        self._vy = vy

    def update_place_by_x_y(self, x, y):
        """פונקציה שמזיזה את האובייקט על ידי השיננוי במהירות"""
        self.rect.x = x
        self.rect.y = y

    def update_loc(self):
        """פונקציה שמזיזה את האובייקט על ידי השיננוי במהירות"""
        self.rect.x += self._vx
        self.rect.y += self._vy

    def get_pos_x(self):
        """הפונקציה מחזירה את המיקום של האובייקט על ציר ה X"""
        return self.rect.x

    def get_pos_y(self):
        """הפונקציה מחזירה את המיקום של האובייקט  על ציר הY"""
        return self.rect.y

    def get_v(self):
        """הפונקציה מחזירה את מהירות האובייקט, קודם על ציר הX ואז על ציר הY"""
        return self._vx, self._vy

    def touch_frame_block(self, WINDOW_WIDTH, WINDOW_HEIGHT):
        """ בודק האם האובייקט של הבלוק נוגע בצד המסך ואם כן מביא לו מהירות הפוכה """
        if self.rect.x + 20 > WINDOW_WIDTH:
            self.rect.x = WINDOW_WIDTH
        elif self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.y + 20 > WINDOW_HEIGHT:
            self.rect.y = WINDOW_HEIGHT
        elif self.rect.y < 0:
            self.rect.y = 0


class Button:
    """מחלקה יוצרת של כפתורים"""
    def __init__(self, x, y, width, height, text, color, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.font_size = font_size

    def draw(self, screen):
        # יוצר את המרובע עליו יושב הטקסט
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # מיישר את הטקסט על המרובע
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, pos, get_pressed):
        # כאשר נלחץ בודק אם העכבר היה בתוך המרובע
        mouse_x, mouse_y = pos
        if get_pressed[0]:
            return (self.x - 25 <= mouse_x <= self.x + self.width + 25) and (self.y <= mouse_y <= self.y + self.height)
