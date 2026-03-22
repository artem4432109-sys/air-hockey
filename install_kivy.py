#!/usr/bin/env python3
"""
Установка Kivy для сборки Android APK
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Выполнить команду"""
    print(f"\n🔄 {description}")
    print(f"Команда: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - успешно")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ошибка")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    """Установка Kivy и buildozer"""
    print("🏒 Установка Kivy для Аэрохоккея")
    print("=" * 40)
    
    # Обновление pip
    run_command("python -m pip install --upgrade pip", "Обновление pip")
    
    # Установка Kivy
    if not run_command("pip install kivy", "Установка Kivy"):
        print("\n❌ Не удалось установить Kivy")
        print("Попробуйте альтернативные способы:")
        print("1. pip install kivy[base]")
        print("2. pip install --pre kivy")
        print("3. conda install kivy (если используете Anaconda)")
        return False
    
    # Установка buildozer
    if not run_command("pip install buildozer", "Установка Buildozer"):
        print("\n❌ Не удалось установить Buildozer")
        return False
    
    # Проверка установки
    print("\n🔍 Проверка установки...")
    
    try:
        import kivy
        print(f"✅ Kivy {kivy.__version__} установлен")
    except ImportError:
        print("❌ Kivy не найден")
        return False
    
    try:
        result = subprocess.run("buildozer version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Buildozer установлен")
        else:
            print("❌ Buildozer не работает")
            return False
    except:
        print("❌ Buildozer не найден")
        return False
    
    print("\n🎉 Установка завершена успешно!")
    print("\nТеперь можете:")
    print("1. Тестировать на компьютере: python android_hockey.py")
    print("2. Собрать APK: python build_android.py")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Установка прервана")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
    
    input("\nНажмите Enter для выхода...")