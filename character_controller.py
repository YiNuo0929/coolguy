# character_controller.py
class CharacterController:
    def __init__(self, canvas_width, canvas_height, scale=0.3, speed=10, jump_height=60):
        self.scale = scale
        self.speed = speed
        self.jump_height = jump_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.char_width = 100
        self.char_height = 100

        self.x = None
        self.y_base = None
        self.y = None

        self.is_jumping = False
        self.jump_velocity = 0

    def set_character_size(self, char_width, char_height, initial_center_x=None):
        self.char_width = int(char_width * self.scale)
        self.char_height = int(char_height * self.scale)
        self.y_base = self.canvas_height - self.char_height
        self.y = self.y_base

        if initial_center_x is not None:
            self.x = int(initial_center_x - self.char_width // 2)
        else:
            self.x = self.canvas_width // 2 - self.char_width // 2

        # 確保初始位置不會超出畫面
        self._clamp_position()

    def update(self, action):
        if action == 'left':
            self.x -= self.speed
        elif action == 'right':
            self.x += self.speed
        elif action == 'jump' and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = -15

        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity += 2
            if self.y >= self.y_base:
                self.y = self.y_base
                self.is_jumping = False

        self._clamp_position()

    def _clamp_position(self):
        self.x = max(0, min(self.canvas_width - self.char_width, self.x))
        self.y = max(0, min(self.canvas_height - self.char_height, self.y))

    def get_position(self):
        return self.x, self.y