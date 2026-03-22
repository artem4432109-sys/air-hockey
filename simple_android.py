#!/usr/bin/env python3
"""
Простая версия аэрохоккея для сборки APK через онлайн-сервисы
Без сложных зависимостей
"""

# Попытка импорта Kivy с обработкой ошибок
try:
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.boxlayout import BoxLayout
    from kivy.clock import Clock
    from kivy.graphics import Color, Ellipse, Rectangle, Line
    from kivy.core.window import Window
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False
    print("Kivy не найден. Используйте для сборки APK онлайн-сервисы.")

import random
import math

if KIVY_AVAILABLE:
    class HockeyGame(Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            
            # Игровые объекты
            self.reset_game()
            
            # Запуск игрового цикла
            Clock.schedule_interval(self.update, 1.0/60.0)
            
            # Привязка касаний
            self.bind(on_touch_down=self.on_touch_down)
            self.bind(on_touch_move=self.on_touch_move)
            
        def reset_game(self):
            """Сброс игры"""
            w, h = Window.width, Window.height
            
            self.player = {'x': w//2, 'y': 80, 'r': 30}
            self.ai = {'x': w//2, 'y': h-80, 'r': 30}
            self.puck = {'x': w//2, 'y': h//2, 'r': 15, 'vx': 3, 'vy': 3}
            
            self.player_score = 0
            self.ai_score = 0
            
        def on_touch_down(self, touch):
            if touch.y < Window.height // 2:
                dist = ((touch.x - self.player['x'])**2 + (touch.y - self.player['y'])**2)**0.5
                return dist < self.player['r'] * 2
            return False
            
        def on_touch_move(self, touch):
            if touch.y < Window.height // 2:
                self.player['x'] = max(40, min(Window.width-40, touch.x))
                self.player['y'] = max(40, min(Window.height//2-40, touch.y))
                return True
            return False
            
        def update(self, dt):
            """Игровой цикл"""
            # ИИ
            if abs(self.ai['x'] - self.puck['x']) > 5:
                if self.ai['x'] < self.puck['x']:
                    self.ai['x'] += 4
                else:
                    self.ai['x'] -= 4
            self.ai['x'] = max(40, min(Window.width-40, self.ai['x']))
            
            # Шайба
            self.puck['x'] += self.puck['vx']
            self.puck['y'] += self.puck['vy']
            
            # Отскоки от стен
            if self.puck['x'] <= 20 or self.puck['x'] >= Window.width-20:
                self.puck['vx'] *= -1
            
            # Голы
            if self.puck['y'] <= 20:
                if Window.width//2-60 <= self.puck['x'] <= Window.width//2+60:
                    self.player_score += 1
                    self.reset_puck()
            elif self.puck['y'] >= Window.height-20:
                if Window.width//2-60 <= self.puck['x'] <= Window.width//2+60:
                    self.ai_score += 1
                    self.reset_puck()
            elif self.puck['y'] <= 20 or self.puck['y'] >= Window.height-20:
                self.puck['vy'] *= -1
            
            # Столкновения
            for paddle in [self.player, self.ai]:
                dist = ((self.puck['x'] - paddle['x'])**2 + (self.puck['y'] - paddle['y'])**2)**0.5
                if dist < paddle['r'] + self.puck['r']:
                    dx = self.puck['x'] - paddle['x']
                    dy = self.puck['y'] - paddle['y']
                    if dist > 0:
                        dx /= dist
                        dy /= dist
                        self.puck['vx'] = dx * 6
                        self.puck['vy'] = dy * 6
            
            # Отрисовка
            self.canvas.clear()
            self.draw()
            
        def reset_puck(self):
            """Сброс шайбы"""
            self.puck['x'] = Window.width // 2
            self.puck['y'] = Window.height // 2
            self.puck['vx'] = random.choice([-4, 4])
            self.puck['vy'] = random.choice([-4, 4])
            
        def draw(self):
            """Отрисовка"""
            with self.canvas:
                # Фон
                Color(0.1, 0.1, 0.2, 1)
                Rectangle(pos=(0, 0), size=Window.size)
                
                # Поле
                Color(0, 1, 1, 1)
                Line(rectangle=(10, 10, Window.width-20, Window.height-20), width=2)
                Line(points=[10, Window.height//2, Window.width-10, Window.height//2], width=2)
                
                # Ворота
                Color(1, 0, 0, 1)
                gw = 120
                gx = (Window.width - gw) // 2
                Rectangle(pos=(gx, 10), size=(gw, 10))
                Rectangle(pos=(gx, Window.height-20), size=(gw, 10))
                
                # Игрок
                Color(0, 0, 1, 1)
                p = self.player
                Ellipse(pos=(p['x']-p['r'], p['y']-p['r']), size=(p['r']*2, p['r']*2))
                
                # ИИ
                Color(1, 0, 0, 1)
                a = self.ai
                Ellipse(pos=(a['x']-a['r'], a['y']-a['r']), size=(a['r']*2, a['r']*2))
                
                # Шайба
                Color(1, 1, 0, 1)
                pk = self.puck
                Ellipse(pos=(pk['x']-pk['r'], pk['y']-pk['r']), size=(pk['r']*2, pk['r']*2))

    class HockeyApp(App):
        def build(self):
            """Построение приложения"""
            Window.clearcolor = (0.1, 0.1, 0.2, 1)
            
            # Основной layout
            root = BoxLayout(orientation='vertical')
            
            # Счет
            self.score_label = Label(
                text='Игрок: 0 | ИИ: 0', 
                size_hint_y=None, 
                height=50,
                font_size='20sp'
            )
            root.add_widget(self.score_label)
            
            # Игра
            self.game = HockeyGame()
            root.add_widget(self.game)
            
            # Кнопки
            btn_layout = BoxLayout(size_hint_y=None, height=60)
            
            reset_btn = Button(text='Сброс')
            reset_btn.bind(on_press=lambda x: self.game.reset_puck())
            
            new_btn = Button(text='Новая игра')
            new_btn.bind(on_press=lambda x: self.game.reset_game())
            
            btn_layout.add_widget(reset_btn)
            btn_layout.add_widget(new_btn)
            root.add_widget(btn_layout)
            
            # Обновление счета
            Clock.schedule_interval(self.update_score, 0.1)
            
            return root
            
        def update_score(self, dt):
            """Обновление счета"""
            self.score_label.text = f'Игрок: {self.game.player_score} | ИИ: {self.game.ai_score}'

    if __name__ == '__main__':
        HockeyApp().run()

else:
    print("Для создания APK:")
    print("1. Установите Kivy: pip install kivy")
    print("2. Или используйте онлайн-сервисы:")
    print("   - Replit")
    print("   - Google Colab + buildozer")
    print("   - GitHub Actions")