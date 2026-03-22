#!/usr/bin/env python3
"""
Веб-версия аэрохоккея для онлайн-конвертеров APK
Упрощенная версия без сложных зависимостей
"""

try:
    import tkinter as tk
    from tkinter import messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

import random
import math
import time

class SimpleHockey:
    def __init__(self):
        if not GUI_AVAILABLE:
            print("GUI недоступен, используйте консольную версию")
            return
            
        self.root = tk.Tk()
        self.root.title("🏒 Аэрохоккей")
        self.root.geometry("400x600")
        self.root.configure(bg='black')
        
        # Игровое поле
        self.canvas = tk.Canvas(self.root, width=380, height=500, bg='#001122')
        self.canvas.pack(pady=10)
        
        # Счет
        self.player_score = 0
        self.ai_score = 0
        
        self.score_label = tk.Label(
            self.root, 
            text=f"Игрок: {self.player_score}  |  ИИ: {self.ai_score}",
            fg='cyan', bg='black', font=('Arial', 14, 'bold')
        )
        self.score_label.pack()
        
        # Кнопки
        btn_frame = tk.Frame(self.root, bg='black')
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="🔄 Новая игра", command=self.reset_game, 
                 bg='#004400', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Выход", command=self.root.quit,
                 bg='#440000', fg='white').pack(side=tk.LEFT, padx=5)
        
        # Игровые объекты
        self.init_game()
        
        # События
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        
        # Игровой цикл
        self.game_running = True
        self.update_game()
    
    def init_game(self):
        """Инициализация игры"""
        self.player_paddle = {'x': 190, 'y': 450, 'radius': 20}
        self.ai_paddle = {'x': 190, 'y': 50, 'radius': 20}
        self.puck = {'x': 190, 'y': 250, 'radius': 10, 'vx': 3, 'vy': 3}
        
        self.draw_field()
    
    def draw_field(self):
        """Отрисовка игрового поля"""
        self.canvas.delete("all")
        
        # Границы поля
        self.canvas.create_rectangle(10, 10, 370, 490, outline='cyan', width=2)
        
        # Центральная линия
        self.canvas.create_line(10, 250, 370, 250, fill='cyan', width=2)
        
        # Ворота
        self.canvas.create_rectangle(150, 10, 230, 20, fill='red')
        self.canvas.create_rectangle(150, 480, 230, 490, fill='red')
        
        # Ракетка игрока (синяя)
        p = self.player_paddle
        self.canvas.create_oval(p['x']-p['radius'], p['y']-p['radius'],
                              p['x']+p['radius'], p['y']+p['radius'],
                              fill='blue', outline='white', width=2)
        
        # Ракетка ИИ (красная)
        a = self.ai_paddle
        self.canvas.create_oval(a['x']-a['radius'], a['y']-a['radius'],
                              a['x']+a['radius'], a['y']+a['radius'],
                              fill='red', outline='white', width=2)
        
        # Шайба (желтая)
        pk = self.puck
        self.canvas.create_oval(pk['x']-pk['radius'], pk['y']-pk['radius'],
                              pk['x']+pk['radius'], pk['y']+pk['radius'],
                              fill='yellow', outline='white', width=2)
    
    def on_click(self, event):
        """Обработка клика мыши"""
        if event.y > 250:
            distance = math.sqrt((event.x - self.player_paddle['x'])**2 + 
                               (event.y - self.player_paddle['y'])**2)
            if distance < self.player_paddle['radius'] * 2:
                self.dragging = True
    
    def on_drag(self, event):
        """Обработка перетаскивания ракетки"""
        if hasattr(self, 'dragging') and self.dragging:
            x = max(30, min(350, event.x))
            y = max(270, min(470, event.y))
            self.player_paddle['x'] = x
            self.player_paddle['y'] = y
    
    def update_ai(self):
        """Обновление ИИ"""
        target_x = self.puck['x']
        if self.puck['vy'] < 0:
            diff = target_x - self.ai_paddle['x']
            move = max(-3, min(3, diff * 0.1))
            new_x = self.ai_paddle['x'] + move
            self.ai_paddle['x'] = max(30, min(350, new_x))
    
    def update_puck(self):
        """Обновление позиции шайбы"""
        self.puck['x'] += self.puck['vx']
        self.puck['y'] += self.puck['vy']
        
        # Отскок от боковых стен
        if self.puck['x'] <= 20 or self.puck['x'] >= 360:
            self.puck['vx'] *= -0.8
            self.puck['x'] = max(20, min(360, self.puck['x']))
        
        # Проверка голов
        if self.puck['y'] <= 20:
            if 150 <= self.puck['x'] <= 230:
                self.player_score += 1
                self.goal_scored()
                return
        
        if self.puck['y'] >= 480:
            if 150 <= self.puck['x'] <= 230:
                self.ai_score += 1
                self.goal_scored()
                return
        
        # Отскок от стен
        if self.puck['y'] <= 20 or self.puck['y'] >= 480:
            self.puck['vy'] *= -0.8
            self.puck['y'] = max(20, min(480, self.puck['y']))
        
        # Затухание
        self.puck['vx'] *= 0.998
        self.puck['vy'] *= 0.998
        
        # Минимальная скорость
        if abs(self.puck['vx']) < 0.5 and abs(self.puck['vy']) < 0.5:
            angle = random.uniform(0, 2 * math.pi)
            self.puck['vx'] = math.cos(angle) * 2
            self.puck['vy'] = math.sin(angle) * 2
    
    def check_collisions(self):
        """Проверка столкновений"""
        for paddle in [self.player_paddle, self.ai_paddle]:
            dist = math.sqrt((self.puck['x'] - paddle['x'])**2 + 
                           (self.puck['y'] - paddle['y'])**2)
            
            if dist < (self.puck['radius'] + paddle['radius']):
                dx = self.puck['x'] - paddle['x']
                dy = self.puck['y'] - paddle['y']
                if dist > 0:
                    dx /= dist
                    dy /= dist
                    speed = 4
                    self.puck['vx'] = dx * speed
                    self.puck['vy'] = dy * speed
    
    def goal_scored(self):
        """Обработка гола"""
        self.update_score()
        
        if self.player_score >= 5:
            messagebox.showinfo("🏆 Победа!", "Вы выиграли!")
            self.reset_game()
        elif self.ai_score >= 5:
            messagebox.showinfo("😔 Поражение", "ИИ победил!")
            self.reset_game()
        else:
            self.reset_puck()
    
    def reset_puck(self):
        """Сброс шайбы"""
        self.puck['x'] = 190
        self.puck['y'] = 250
        self.puck['vx'] = random.uniform(-3, 3)
        self.puck['vy'] = random.uniform(-3, 3)
    
    def update_score(self):
        """Обновление счета"""
        self.score_label.config(text=f"Игрок: {self.player_score}  |  ИИ: {self.ai_score}")
    
    def reset_game(self):
        """Сброс игры"""
        self.player_score = 0
        self.ai_score = 0
        self.update_score()
        self.init_game()
    
    def update_game(self):
        """Главный игровой цикл"""
        if self.game_running:
            self.update_ai()
            self.update_puck()
            self.check_collisions()
            self.draw_field()
            self.root.after(16, self.update_game)
    
    def run(self):
        """Запуск игры"""
        if GUI_AVAILABLE:
            messagebox.showinfo("🏒 Аэрохоккей", "Управление: перетаскивайте синюю ракетку мышью")
            self.root.mainloop()
        else:
            print("Для запуска нужен tkinter")

# Консольная версия для случаев когда нет GUI
class ConsoleHockey:
    def __init__(self):
        print("🏒 Консольный Аэрохоккей")
        print("Эта версия работает в любом Python!")
        print("Для полной версии нужен tkinter")
        
    def run(self):
        print("Игра запущена в консольном режиме")
        print("Для GUI версии установите tkinter")

if __name__ == "__main__":
    try:
        if GUI_AVAILABLE:
            game = SimpleHockey()
            game.run()
        else:
            game = ConsoleHockey()
            game.run()
    except Exception as e:
        print(f"Ошибка: {e}")
        input("Нажмите Enter для выхода...")