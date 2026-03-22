#!/usr/bin/env python3
"""
Быстрая и динамичная версия Аэрохоккея
Исправлена физика движения
"""

import tkinter as tk
from tkinter import messagebox
import math
import random
import time

class FastHockey:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏒 Быстрый Аэрохоккей")
        self.root.geometry("450x650")
        self.root.configure(bg='black')
        
        # Игровое поле
        self.canvas = tk.Canvas(self.root, width=420, height=550, bg='#001122')
        self.canvas.pack(pady=10)
        
        # Счет
        self.score_frame = tk.Frame(self.root, bg='black')
        self.score_frame.pack()
        
        self.player_score = 0
        self.ai_score = 0
        
        self.score_label = tk.Label(
            self.score_frame, 
            text=f"Игрок: {self.player_score}  |  ИИ: {self.ai_score}",
            fg='cyan', bg='black', font=('Arial', 16, 'bold')
        )
        self.score_label.pack()
        
        # Кнопки
        btn_frame = tk.Frame(self.root, bg='black')
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="🔄 Новая игра", command=self.reset_game, 
                 bg='#004400', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="🏒 Сброс шайбы", command=self.reset_puck_position, 
                 bg='#444400', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="⚡ Ускорить", command=self.speed_up_puck, 
                 bg='#440044', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="❌ Выход", command=self.root.quit,
                 bg='#440000', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=3)
        
        # Игровые объекты
        self.init_game()
        
        # События
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        
        # Игровой цикл
        self.game_running = True
        self.dragging = False
        self.last_paddle_x = 210
        self.last_paddle_y = 480
        self.update_game()
    
    def init_game(self):
        """Инициализация игры"""
        # Ракетки
        self.player_paddle = {'x': 210, 'y': 480, 'radius': 25}
        self.ai_paddle = {'x': 210, 'y': 70, 'radius': 25}
        
        # Шайба с нормальной скоростью
        self.puck = {
            'x': 210, 'y': 275, 'radius': 12,
            'vx': random.uniform(-4, 4), 'vy': random.uniform(-5, 5)
        }
        
        # Убеждаемся что шайба движется
        if abs(self.puck['vx']) < 2:
            self.puck['vx'] = 3 if self.puck['vx'] >= 0 else -3
        if abs(self.puck['vy']) < 2:
            self.puck['vy'] = 3 if self.puck['vy'] >= 0 else -3
        
        # Ограничения для ракеток
        self.player_zone = {'top': 275, 'bottom': 520}
        self.ai_zone = {'top': 30, 'bottom': 275}
        
        self.draw_field()
    
    def draw_field(self):
        """Отрисовка игрового поля"""
        self.canvas.delete("all")
        
        # Границы поля
        self.canvas.create_rectangle(15, 15, 405, 535, outline='cyan', width=3)
        
        # Центральная линия
        self.canvas.create_line(15, 275, 405, 275, fill='cyan', width=3)
        
        # Центральный круг
        self.canvas.create_oval(160, 225, 260, 325, outline='cyan', width=2)
        
        # Ворота
        goal_width = 80
        goal_x = (420 - goal_width) // 2
        
        # Верхние ворота (ИИ)
        self.canvas.create_rectangle(goal_x, 15, goal_x + goal_width, 25, 
                                   fill='red', outline='white', width=2)
        
        # Нижние ворота (игрок)
        self.canvas.create_rectangle(goal_x, 525, goal_x + goal_width, 535, 
                                   fill='red', outline='white', width=2)
        
        # Ракетка игрока (синяя)
        px, py, pr = self.player_paddle['x'], self.player_paddle['y'], self.player_paddle['radius']
        self.canvas.create_oval(px - pr, py - pr, px + pr, py + pr,
                              fill='#0066ff', outline='white', width=3)
        
        # Ракетка ИИ (оранжевая)
        ax, ay, ar = self.ai_paddle['x'], self.ai_paddle['y'], self.ai_paddle['radius']
        self.canvas.create_oval(ax - ar, ay - ar, ax + ar, ay + ar,
                              fill='#ff6600', outline='white', width=3)
        
        # Шайба (желтая)
        sx, sy, sr = self.puck['x'], self.puck['y'], self.puck['radius']
        self.canvas.create_oval(sx - sr, sy - sr, sx + sr, sy + sr,
                              fill='yellow', outline='white', width=3)
        
        # Показываем скорость шайбы
        speed = math.sqrt(self.puck['vx']**2 + self.puck['vy']**2)
        self.canvas.create_text(50, 50, text=f"Скорость: {speed:.1f}", 
                              fill='white', font=('Arial', 10))
    
    def on_click(self, event):
        """Обработка клика мыши"""
        if event.y > 275:  # Зона игрока
            distance = math.sqrt((event.x - self.player_paddle['x'])**2 + 
                               (event.y - self.player_paddle['y'])**2)
            if distance < self.player_paddle['radius'] * 1.5:
                self.dragging = True
                self.last_paddle_x = self.player_paddle['x']
                self.last_paddle_y = self.player_paddle['y']
    
    def on_drag(self, event):
        """Обработка перетаскивания ракетки"""
        if self.dragging:
            # Ограничиваем движение
            new_x = max(40, min(380, event.x))
            new_y = max(self.player_zone['top'], min(self.player_zone['bottom'], event.y))
            
            self.player_paddle['x'] = new_x
            self.player_paddle['y'] = new_y
    
    def on_release(self, event):
        """Отпускание мыши"""
        self.dragging = False
    
    def update_ai(self):
        """Простой и быстрый ИИ"""
        # ИИ всегда активен и быстро реагирует
        target_x = self.puck['x']
        
        # Простое следование за шайбой
        diff = target_x - self.ai_paddle['x']
        
        # Быстрое движение ИИ
        if abs(diff) > 5:
            move_speed = 4
            if diff > 0:
                self.ai_paddle['x'] += move_speed
            else:
                self.ai_paddle['x'] -= move_speed
        
        # Ограничения
        self.ai_paddle['x'] = max(40, min(380, self.ai_paddle['x']))
    
    def update_puck(self):
        """Обновление позиции шайбы - БЫСТРАЯ ФИЗИКА"""
        # Движение шайбы
        self.puck['x'] += self.puck['vx']
        self.puck['y'] += self.puck['vy']
        
        # Отскок от боковых стен
        if self.puck['x'] <= 27 or self.puck['x'] >= 393:
            self.puck['vx'] *= -0.9  # Меньше потерь энергии
            self.puck['x'] = max(27, min(393, self.puck['x']))
        
        # Проверка голов
        goal_left, goal_right = 170, 250
        
        if self.puck['y'] <= 27:
            if goal_left <= self.puck['x'] <= goal_right:
                self.player_score += 1
                self.goal_scored()
                return
        
        if self.puck['y'] >= 523:
            if goal_left <= self.puck['x'] <= goal_right:
                self.ai_score += 1
                self.goal_scored()
                return
        
        # Отскок от верхней и нижней стен
        if self.puck['y'] <= 27 or self.puck['y'] >= 523:
            self.puck['vy'] *= -0.9  # Меньше потерь энергии
            self.puck['y'] = max(27, min(523, self.puck['y']))
        
        # МИНИМАЛЬНОЕ затухание - шайба должна быстро двигаться!
        self.puck['vx'] *= 0.999  # Почти без затухания
        self.puck['vy'] *= 0.999
        
        # Проверка на слишком медленное движение
        speed = math.sqrt(self.puck['vx']**2 + self.puck['vy']**2)
        if speed < 1.5:  # Если слишком медленно
            # Добавляем энергии
            angle = random.uniform(0, 2 * math.pi)
            self.puck['vx'] += math.cos(angle) * 2
            self.puck['vy'] += math.sin(angle) * 2
        
        # Ограничение максимальной скорости
        max_speed = 12  # Увеличили максимальную скорость
        if speed > max_speed:
            self.puck['vx'] = (self.puck['vx'] / speed) * max_speed
            self.puck['vy'] = (self.puck['vy'] / speed) * max_speed
    
    def check_collisions(self):
        """Проверка столкновений"""
        # Столкновение с ракеткой игрока
        dist_player = math.sqrt((self.puck['x'] - self.player_paddle['x'])**2 + 
                               (self.puck['y'] - self.player_paddle['y'])**2)
        
        if dist_player < (self.puck['radius'] + self.player_paddle['radius']):
            self.handle_collision(self.player_paddle)
        
        # Столкновение с ракеткой ИИ
        dist_ai = math.sqrt((self.puck['x'] - self.ai_paddle['x'])**2 + 
                           (self.puck['y'] - self.ai_paddle['y'])**2)
        
        if dist_ai < (self.puck['radius'] + self.ai_paddle['radius']):
            self.handle_collision(self.ai_paddle)
    
    def handle_collision(self, paddle):
        """Простая и энергичная обработка столкновений"""
        # Вектор от ракетки к шайбе
        dx = self.puck['x'] - paddle['x']
        dy = self.puck['y'] - paddle['y']
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Нормализация
            dx /= distance
            dy /= distance
            
            # СИЛЬНЫЙ отскок - добавляем энергии!
            base_speed = 6  # Базовая скорость отскока
            
            self.puck['vx'] = dx * base_speed
            self.puck['vy'] = dy * base_speed
            
            # Добавляем случайность для интереса
            self.puck['vx'] += random.uniform(-1, 1)
            self.puck['vy'] += random.uniform(-1, 1)
            
            # Разделение объектов
            overlap = (paddle['radius'] + self.puck['radius']) - distance + 2
            self.puck['x'] += dx * overlap
            self.puck['y'] += dy * overlap
    
    def goal_scored(self):
        """Обработка гола"""
        self.update_score()
        
        # Проверка победы
        if self.player_score >= 5:
            messagebox.showinfo("🏆 ПОБЕДА!", f"Вы выиграли {self.player_score}:{self.ai_score}!")
            self.reset_game()
        elif self.ai_score >= 5:
            messagebox.showinfo("😔 Поражение", f"ИИ победил {self.ai_score}:{self.player_score}")
            self.reset_game()
        else:
            # Быстрый сброс шайбы
            self.root.after(500, self.reset_puck_position)
    
    def update_score(self):
        """Обновление счета"""
        self.score_label.config(text=f"Игрок: {self.player_score}  |  ИИ: {self.ai_score}")
    
    def reset_game(self):
        """Сброс игры"""
        self.player_score = 0
        self.ai_score = 0
        self.update_score()
        self.init_game()
    
    def reset_puck_position(self):
        """Сброс позиции шайбы с хорошей скоростью"""
        self.puck['x'] = 210
        self.puck['y'] = 275
        
        # Случайное направление с хорошей скоростью
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(4, 6)  # Хорошая начальная скорость
        
        self.puck['vx'] = math.cos(angle) * speed
        self.puck['vy'] = math.sin(angle) * speed
    
    def speed_up_puck(self):
        """Ускорение шайбы если она медленная"""
        current_speed = math.sqrt(self.puck['vx']**2 + self.puck['vy']**2)
        
        if current_speed < 3:
            # Ускоряем в текущем направлении
            if current_speed > 0:
                multiplier = 5 / current_speed
                self.puck['vx'] *= multiplier
                self.puck['vy'] *= multiplier
            else:
                # Если стоит, даем случайное направление
                angle = random.uniform(0, 2 * math.pi)
                self.puck['vx'] = math.cos(angle) * 5
                self.puck['vy'] = math.sin(angle) * 5
        
        messagebox.showinfo("⚡", "Шайба ускорена!")
    
    def update_game(self):
        """Главный игровой цикл - 60 FPS"""
        if self.game_running:
            self.update_ai()
            self.update_puck()
            self.check_collisions()
            self.draw_field()
            
            # Быстрый цикл - 16мс = ~60 FPS
            self.root.after(16, self.update_game)
    
    def run(self):
        """Запуск игры"""
        messagebox.showinfo(
            "🏒 Быстрый Аэрохоккей", 
            "Исправленная физика!\n\n"
            "• Шайба движется быстро\n"
            "• ИИ активно играет\n"
            "• Кнопка ускорения шайбы\n"
            "• Энергичные отскоки\n\n"
            "Управление: перетаскивайте синюю ракетку\n"
            "Удачи!"
        )
        
        self.root.mainloop()

if __name__ == "__main__":
    try:
        game = FastHockey()
        game.run()
    except Exception as e:
        print(f"Ошибка: {e}")
        input("Нажмите Enter для выхода...")