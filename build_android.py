#!/usr/bin/env python3
"""
Сборка APK для Android
"""

import subprocess
import sys
import os

def check_kivy():
    """Проверка Kivy"""
    try:
        import kivy
        print(f"✅ Kivy {kivy.__version__} найден")
        return True
    except ImportError:
        print("❌ Kivy не установлен")
        print("Запустите: python install_kivy.py")
        return False

def check_buildozer():
    """Проверка buildozer"""
    try:
        result = subprocess.run("buildozer version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Buildozer найден")
            return True
        else:
            print("❌ Buildozer не работает")
            return False
    except:
        print("❌ Buildozer не найден")
        print("Запустите: python install_kivy.py")
        return False

def test_game():
    """Тестирование игры на компьютере"""
    print("\n🎮 Тестирование игры...")
    try:
        from android_hockey import AirHockeyApp
        print("✅ Игра загружается без ошибок")
        
        # Спрашиваем пользователя
        test = input("Хотите протестировать игру на компьютере? (y/n): ").lower()
        if test == 'y':
            print("🚀 Запуск игры для тестирования...")
            app = AirHockeyApp()
            app.run()
        
        return True
    except Exception as e:
        print(f"❌ Ошибка в игре: {e}")
        return False

def build_apk():
    """Сборка APK"""
    print("\n📱 Сборка APK для Android...")
    
    # Очистка
    print("🧹 Очистка предыдущих сборок...")
    subprocess.run("buildozer android clean", shell=True)
    
    # Сборка
    print("🔨 Сборка APK (это может занять много времени)...")
    result = subprocess.run("buildozer android debug", shell=True)
    
    if result.returncode == 0:
        print("\n🎉 APK успешно собран!")
        
        # Поиск APK файла
        bin_dir = "bin"
        if os.path.exists(bin_dir):
            apk_files = [f for f in os.listdir(bin_dir) if f.endswith('.apk')]
            if apk_files:
                for apk in apk_files:
                    apk_path = os.path.join(bin_dir, apk)
                    size = os.path.getsize(apk_path) / (1024 * 1024)  # MB
                    print(f"📱 APK: {apk_path} ({size:.1f} MB)")
                
                print("\n📋 Инструкции по установке:")
                print("1. Скопируйте APK файл на Android устройство")
                print("2. Включите 'Установка из неизвестных источников'")
                print("3. Откройте APK файл для установки")
                return True
        
        print("❌ APK файл не найден в папке bin/")
        return False
    else:
        print("❌ Ошибка при сборке APK")
        print("Проверьте логи выше для диагностики")
        return False

def main():
    """Главная функция"""
    print("🏒 Сборка Аэрохоккея для Android")
    print("=" * 40)
    
    # Проверка зависимостей
    if not check_kivy():
        return False
    
    if not check_buildozer():
        return False
    
    # Тестирование игры
    if not test_game():
        print("❌ Игра содержит ошибки, сборка отменена")
        return False
    
    # Подтверждение сборки
    print("\n" + "=" * 40)
    confirm = input("Начать сборку APK? Это займет 10-30 минут (y/n): ").lower()
    
    if confirm != 'y':
        print("❌ Сборка отменена")
        return False
    
    # Сборка APK
    return build_apk()

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Готово! APK файл создан.")
        else:
            print("\n❌ Сборка не удалась.")
    except KeyboardInterrupt:
        print("\n❌ Сборка прервана пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
    
    input("\nНажмите Enter для выхода...")