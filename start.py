#!/usr/bin/env python3
"""
Запуск игры Аэрохоккей
"""

try:
    print("🏒 Запуск Аэрохоккея...")
    from fast_hockey import FastHockey
    
    game = FastHockey()
    game.run()
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("\nПопробуйте:")
    print("python fast_hockey.py")
    input("\nНажмите Enter для выхода...")