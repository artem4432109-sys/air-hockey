#!/usr/bin/env python3
"""
Аэрохоккей для Android на Kivy
Быстрая физика, оптимизировано для мобильных устройств
"""

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import random
import math

kivy.require('2.0.0')

class GameScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Игровые объекты
        self.player_paddle = {'x': Window.width // 2, 'y': 100, 'radius': 40}
        self.ai_paddle = {'x': Window.width // 2, 'y': Window.height - 100, 'radius': 40}
        
        # Шайба с хорошей начальной скоростью
        self.puck = {
            'x': Window.width // 2, 
            'y': Window.height // 2, 
            'radius': 20,
            'vx': random.uniform(-6, 6), 
            'vy': random.uniform(-8, 8)
        }
        
        # Убеждаемся что шайба движется
        if abs(self.puck['vx']) < 3:
            self.puck['vx'] = 4 if self.puck['vx'] >= 0 else -4
        if abs(self.puck['vy']) < 3:
            self.puck['vy'] = 4 if self.puck['vy'] >= 0 else -4
        
        # Счет
        self.player_score = 0
        self.ai_score = 0
        
        # Зоны ракеток
        self.player_zone = {'top': Window.height // 2 - 50, 'bottom': Window.height - 50}
        self.ai_zone = {'top': 50, 'bottom': Window.height // 2 + 50}
        
        # Эффекты
        self.goal_flash = 0
        
        # Запуск игрового цикла
        Clock.schedule_interval(self.update, 1.0/60.0)
        
        # Привязка касаний
        self.bind(on_touch_down=self.on_touch_down)
        self.bind(on_touch_move=self.on_touch_move)
        
    def on_touch_down(self, touch):
        # Проверяем касание в зоне игрока (нижняя половина)
        if touch.y < Window.height // 2:
            distance = math.sqrt((touch.x - self.player_paddle['x'])**2 + 
                               (touch.y - self.player_paddle['y'])**2)
            if distance < self.player_paddle['radius'] * 1.5:
                return True
        return False
        
    def on_touch_move(self, touch):
        # Движение ракетки игрока
        if touch.y < Window.height // 2:
            # Ограничения движения
            new_x = max(50, min(Window.width - 50, touch.x))
            new_y = max(self.player_zone['top'], min(self.player_zone['bottom'], touch.y))
            
            self.player_paddle['x'] = new_x
            self.player_paddle['y'] = new_y
            return True
        return False
        
    def update_ai(self):
        """Быстрый и активный ИИ"""
        target_x = self.puck['x']
        
        # ИИ всегда активен
        diff = target_x - self.ai_paddle['x']
        
        # Быстрое движение
        if abs(diff) > 10:
            move_speed = 8
            if diff > 0:
                self.ai_paddle['x'] += move_speed
            else:
                self.ai_paddle['x'] -= move_speed
        
        # Ограничения
        self.ai_paddle['x'] = max(50, min(Window.width - 50, self.ai_paddle['x']))
    
    def update_puck(self):
        """Быстрая физика шайбы"""
        # Движение
        self.puck['x'] += self.puck['vx']
        self.puck['y'] += self.puck['vy']
        
        # Отскок от боковых стен
        if self.puck['x'] <= 30 or self.puck['x'] >= Window.width - 30:
            self.puck['vx'] *= -0.9
            self.puck['x'] = max(30, min(Window.width - 30, self.puck['x']))
        
        # Проверка голов
        goal_width = 150
        goal_left = (Window.width - goal_width) // 2
        goal_right = goal_left + goal_width
        
        if self.puck['y'] <= 30:
            if goal_left <= self.puck['x'] <= goal_right:
                self.player_score += 1
                self.goal_flash = 30
                self.reset_puck()
                return "player_goal"
        
        if self.puck['y'] >= Window.height - 30:
            if goal_left <= self.puck['x'] <= goal_right:
                self.ai_score += 1
                self.goal_flash = 30
                self.reset_puck()
                return "ai_goal"
        
        # Отскок от верхней и нижней стен
        if self.puck['y'] <= 30 or self.puck['y'] >= Window.height - 30:
            self.puck['vy'] *= -0.9
            self.puck['y'] = max(30, min(Window.height - 30, self.puck['y']))
        
        # Минимальное затухание
        self.puck['vx'] *= 0.999
        self.puck['vy'] *= 0.999
        
        # Антизастревание
        speed = math.sqrt(self.puck['vx']**2 + self.puck['vy']**2)
        if speed < 2:
            angle = random.uniform(0, 2 * math.pi)
            self.puck['vx'] += math.cos(angle) * 3
            self.puck['vy'] += math.sin(angle) * 3
        
        # Ограничение максимальной скорости
        max_speed = 15
        if speed > max_speed:
            self.puck['vx'] = (self.puck['vx'] / speed) * max_speed
            self.puck['vy'] = (self.puck['vy'] / speed) * max_speed
        
        return None
    
    def check_collision(self, paddle):
        """Проверка столкновения с ракеткой"""
        distance = math.sqrt((paddle['x'] - self.puck['x'])**2 + 
                           (paddle['y'] - self.puck['y'])**2)
        return distance < (paddle['radius'] + self.puck['radius'])
    
    def handle_collision(self, paddle):
        """Энергичная обработка столкновений"""
        # Вектор от ракетки к шайбе
        dx = self.puck['x'] - paddle['x']
        dy = self.puck['y'] - paddle['y']
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Нормализация
            dx /= distance
            dy /= distance
            
            # Сильный отскок
            base_speed = 8
            self.puck['vx'] = dx * base_speed
            self.puck['vy'] = dy * base_speed
            
            # Случайность
            self.puck['vx'] += random.uniform(-2, 2)
            self.puck['vy'] += random.uniform(-2, 2)
            
            # Разделение объектов
            overlap = (paddle['radius'] + self.puck['radius']) - distance + 3
            self.puck['x'] += dx * overlap
            self.puck['y'] += dy * overlap
    
    def reset_puck(self):
        """Сброс шайбы с хорошей скоростью"""
        self.puck['x'] = Window.width // 2
        self.puck['y'] = Window.height // 2
        
        # Хорошая начальная скорость
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(5, 8)
        
        self.puck['vx'] = math.cos(angle) * speed
        self.puck['vy'] = math.sin(angle) * speed
    
    def update(self, dt):
        """Главный игровой цикл"""
        # Обновление ИИ
        self.update_ai()
        
        # Обновление шайбы
        result = self.update_puck()
        
        # Проверка столкновений
        if self.check_collision(self.player_paddle):
            self.handle_collision(self.player_paddle)
        if self.check_collision(self.ai_paddle):
            self.handle_collision(self.ai_paddle)
        
        # Эффекты
        if self.goal_flash > 0:
            self.goal_flash -= 1
        
        # Перерисовка
        self.canvas.clear()
        self.draw_game()
    
    def draw_game(self):
        """Отрисовка игры"""
        with self.canvas:
            # Фон с эффектом мигания
            if self.goal_flash > 0 and self.goal_flash % 10 < 5:
                Color(0.2, 0.05, 0.05, 1)
            else:
                Color(0.05, 0.05, 0.15, 1)
            Rectangle(pos=(0, 0), size=(Window.width, Window.height))
            
            # Границы поля
            Color(0, 1, 1, 0.8)
            Line(points=[0, 0, Window.width, 0, Window.width, Window.height, 0, Window.height, 0, 0], width=4)
            
            # Центральная линия
            Color(0, 1, 1, 0.6)
            Line(points=[0, Window.height//2, Window.width, Window.height//2], width=3)
            
            # Центральный круг
            Color(0, 1, 1, 0.4)
            center_x, center_y = Window.width//2, Window.height//2
            Line(circle=(center_x, center_y, 80), width=3)
            
            # Ворота
            goal_width = 150
            goal_x = (Window.width - goal_width) // 2
            
            # Верхние ворота (ИИ)
            Color(1, 0, 0, 1)
            Rectangle(pos=(goal_x, Window.height - 20), size=(goal_width, 20))
            Color(1, 0.5, 0.5, 0.3)
            Rectangle(pos=(goal_x, Window.height - 40), size=(goal_width, 20))
            
            # Нижние ворота (игрок)
            Color(1, 0, 0, 1)
            Rectangle(pos=(goal_x, 0), size=(goal_width, 20))
            Color(1, 0.5, 0.5, 0.3)
            Rectangle(pos=(goal_x, 20), size=(goal_width, 20))
            
            # Ракетка игрока (синяя с эффектом)
            px, py, pr = self.player_paddle['x'], self.player_paddle['y'], self.player_paddle['radius']
            Color(0.2, 0.6, 1, 0.3)
            Ellipse(pos=(px - pr - 10, py - pr - 10), size=((pr + 10) * 2, (pr + 10) * 2))
            Color(0.2, 0.6, 1, 1)
            Ellipse(pos=(px - pr, py - pr), size=(pr * 2, pr * 2))
            Color(0.8, 0.9, 1, 1)
            Ellipse(pos=(px - pr//2, py - pr//2), size=(pr, pr))
            
            # Ракетка ИИ (красная с эффектом)
            ax, ay, ar = self.ai_paddle['x'], self.ai_paddle['y'], self.ai_paddle['radius']
            Color(1, 0.2, 0.2, 0.3)
            Ellipse(pos=(ax - ar - 10, ay - ar - 10), size=((ar + 10) * 2, (ar + 10) * 2))
            Color(1, 0.2, 0.2, 1)
            Ellipse(pos=(ax - ar, ay - ar), size=(ar * 2, ar * 2))
            Color(1, 0.8, 0.8, 1)
            Ellipse(pos=(ax - ar//2, ay - ar//2), size=(ar, ar))
            
            # Шайба (яркая желтая с эффектом)
            sx, sy, sr = self.puck['x'], self.puck['y'], self.puck['radius']
            Color(1, 1, 0, 0.2)
            Ellipse(pos=(sx - sr - 15, sy - sr - 15), size=((sr + 15) * 2, (sr + 15) * 2))
            Color(1, 1, 0, 0.4)
            Ellipse(pos=(sx - sr - 8, sy - sr - 8), size=((sr + 8) * 2, (sr + 8) * 2))
            Color(1, 1, 0, 1)
            Ellipse(pos=(sx - sr, sy - sr), size=(sr * 2, sr * 2))
            Color(1, 1, 1, 1)
            Ellipse(pos=(sx - sr//2, sy - sr//2), size=(sr, sr))

class GamePlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Основной игровой виджет
        self.game = GameScreen()
        
        # Интерфейс счета
        score_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), pos_hint={'top': 1})
        
        self.player_score_label = Label(text='Игрок: 0', font_size='20sp', color=(0, 1, 1, 1))
        self.ai_score_label = Label(text='ИИ: 0', font_size='20sp', color=(1, 0.2, 0.2, 1))
        
        score_layout.add_widget(self.player_score_label)
        score_layout.add_widget(self.ai_score_label)
        
        # Кнопки управления
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), pos_hint={'bottom': 1})
        
        reset_btn = Button(text='Сброс', size_hint=(0.25, 1), font_size='16sp')
        reset_btn.bind(on_press=self.reset_puck)
        
        speed_btn = Button(text='Ускорить', size_hint=(0.25, 1), font_size='16sp')
        speed_btn.bind(on_press=self.speed_up)
        
        new_game_btn = Button(text='Новая игра', size_hint=(0.25, 1), font_size='16sp')
        new_game_btn.bind(on_press=self.new_game)
        
        exit_btn = Button(text='Выход', size_hint=(0.25, 1), font_size='16sp')
        exit_btn.bind(on_press=self.exit_game)
        
        btn_layout.add_widget(reset_btn)
        btn_layout.add_widget(speed_btn)
        btn_layout.add_widget(new_game_btn)
        btn_layout.add_widget(exit_btn)
        
        self.add_widget(self.game)
        self.add_widget(score_layout)
        self.add_widget(btn_layout)
        
        # Обновление счета
        Clock.schedule_interval(self.update_score, 1.0/10.0)
    
    def update_score(self, dt):
        """Обновление отображения счета"""
        self.player_score_label.text = f'Игрок: {self.game.player_score}'
        self.ai_score_label.text = f'ИИ: {self.game.ai_score}'
        
        # Проверка победы
        if self.game.player_score >= 7:
            self.show_victory("Вы выиграли!")
        elif self.game.ai_score >= 7:
            self.show_victory("ИИ победил!")
    
    def show_victory(self, message):
        """Показ сообщения о победе"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        content.add_widget(Label(text=message, font_size='24sp'))
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        new_game_btn = Button(text='Новая игра', size_hint=(0.5, 1))
        new_game_btn.bind(on_press=lambda x: (popup.dismiss(), self.new_game(x)))
        
        exit_btn = Button(text='Выход', size_hint=(0.5, 1))
        exit_btn.bind(on_press=lambda x: (popup.dismiss(), self.exit_game(x)))
        
        btn_layout.add_widget(new_game_btn)
        btn_layout.add_widget(exit_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(title='Игра окончена', content=content, size_hint=(0.8, 0.4))
        popup.open()
    
    def reset_puck(self, instance):
        """Сброс позиции шайбы"""
        self.game.reset_puck()
    
    def speed_up(self, instance):
        """Ускорение шайбы"""
        speed = math.sqrt(self.game.puck['vx']**2 + self.game.puck['vy']**2)
        if speed < 5:
            if speed > 0:
                multiplier = 8 / speed
                self.game.puck['vx'] *= multiplier
                self.game.puck['vy'] *= multiplier
            else:
                angle = random.uniform(0, 2 * math.pi)
                self.game.puck['vx'] = math.cos(angle) * 8
                self.game.puck['vy'] = math.sin(angle) * 8
    
    def new_game(self, instance):
        """Новая игра"""
        self.game.player_score = 0
        self.game.ai_score = 0
        self.game.reset_puck()
    
    def exit_game(self, instance):
        """Выход из игры"""
        App.get_running_app().stop()

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', spacing=30, padding=50)
        
        # Заголовок
        title = Label(text='🏒 АЭРОХОККЕЙ', font_size='40sp', color=(0, 1, 1, 1))
        layout.add_widget(title)
        
        # Подзаголовок
        subtitle = Label(text='Быстрая версия для Android', font_size='18sp', color=(1, 1, 1, 0.8))
        layout.add_widget(subtitle)
        
        # Кнопка начала игры
        start_btn = Button(text='НАЧАТЬ ИГРУ', size_hint=(1, 0.2), font_size='24sp')
        start_btn.bind(on_press=self.start_game)
        layout.add_widget(start_btn)
        
        # Инструкции
        instructions = Label(
            text='Управление: перетаскивайте синюю ракетку\nЦель: забить 7 голов первым\nИспользуйте кнопки для управления игрой',
            font_size='14sp', 
            color=(1, 1, 1, 0.7),
            text_size=(None, None),
            halign='center'
        )
        layout.add_widget(instructions)
        
        # Кнопка выхода
        exit_btn = Button(text='ВЫХОД', size_hint=(1, 0.15), font_size='20sp')
        exit_btn.bind(on_press=self.exit_game)
        layout.add_widget(exit_btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        """Начать игру"""
        self.manager.current = 'game'
    
    def exit_game(self, instance):
        """Выход"""
        App.get_running_app().stop()

class AirHockeyApp(App):
    def build(self):
        """Построение приложения"""
        # Настройка окна
        Window.clearcolor = (0.05, 0.05, 0.15, 1)
        
        # Менеджер экранов
        sm = ScreenManager()
        
        # Добавление экранов
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GamePlayScreen(name='game'))
        
        return sm

if __name__ == '__main__':
    AirHockeyApp().run()
