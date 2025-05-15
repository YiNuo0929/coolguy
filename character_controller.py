class CharacterController:
    def __init__(self, canvas_width, canvas_height, scale=0.3, speed=10, jump_height=60):
        self.scale = scale
        self.speed = speed
        self.jump_height = jump_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # 預設人物大小（初始化後會根據實際圖片動態設定）
        self.char_width = 100
        self.char_height = 100

        # 初始位置：水平中央，底部預留 30px
        self.x = canvas_width // 2
        self.y_base = canvas_height - int(self.char_height * self.scale) - 30
        self.y = self.y_base

        # 跳躍狀態
        self.is_jumping = False
        self.jump_velocity = 0

    def set_character_size(self, char_width, char_height):
        """由主程式設定實際人物尺寸（在第一次 resize 後呼叫）"""
        self.char_width = int(char_width * self.scale)
        self.char_height = int(char_height * self.scale)
        self.y_base = self.canvas_height - self.char_height - 30
        self.y = self.y_base

    def update(self, action):
        """根據偵測的動作更新人物位置與跳躍狀態"""
        if action == 'left':
            self.x -= self.speed
        elif action == 'right':
            self.x += self.speed
        elif action == 'jump' and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = -15  # 向上初速度

        # 處理跳躍
        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity += 2  # 模擬重力
            if self.y >= self.y_base:
                self.y = self.y_base
                self.is_jumping = False

        # 限制邊界（避免人物跑出畫面）
        self.x = max(0, min(self.canvas_width - self.char_width, self.x))
        self.y = max(0, min(self.canvas_height - self.char_height, self.y))

    def get_position(self):
        """取得目前人物 (x, y) 貼圖位置"""
        return self.x, self.y