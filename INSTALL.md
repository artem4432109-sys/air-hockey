# Инструкция по установке и сборке Аэрохоккей

## Быстрый старт

### 1. Установка зависимостей

```bash
# Установка Python зависимостей
pip install -r requirements.txt

# Для Linux/Ubuntu дополнительно:
sudo apt-get install python3-dev build-essential libffi-dev libssl-dev

# Для Windows: установите Visual Studio Build Tools
```

### 2. Тестирование на компьютере

```bash
python main.py
```

### 3. Сборка APK

#### Автоматическая сборка:
```bash
python build.py
```

#### Ручная сборка:
```bash
# Инициализация (только первый раз)
buildozer init

# Сборка debug версии
buildozer android debug

# Сборка release версии (для публикации)
buildozer android release
```

## Требования для сборки Android APK

### Системные требования:
- Python 3.8+
- Java Development Kit (JDK) 8 или 11
- Android SDK (автоматически загружается buildozer)
- Android NDK (автоматически загружается buildozer)
- Git

### Настройка окружения:

#### Windows:
1. Установите Python с python.org
2. Установите JDK от Oracle или OpenJDK
3. Установите Git
4. Добавьте Python и Java в PATH

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-dev build-essential
sudo apt install openjdk-11-jdk git
sudo apt install libffi-dev libssl-dev
```

#### macOS:
```bash
brew install python java git
```

## Структура проекта

```
airhockey/
├── main.py              # Основной код игры
├── settings.py          # Настройки игры
├── utils.py            # Вспомогательные функции
├── buildozer.spec      # Конфигурация сборки
├── requirements.txt    # Python зависимости
├── build.py           # Скрипт автосборки
├── README.md          # Описание проекта
└── bin/               # Готовые APK файлы (после сборки)
```

## Настройка игры

Отредактируйте `settings.py` для изменения:
- Сложности ИИ
- Скорости игры
- Цветовой схемы
- Физических параметров

## Устранение проблем

### Ошибка "buildozer command not found":
```bash
pip install --user buildozer
# Добавьте ~/.local/bin в PATH
```

### Ошибка Java/JDK:
```bash
# Проверьте установку Java
java -version
javac -version

# Установите переменную JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### Ошибки сборки Android:
```bash
# Очистите кэш buildozer
buildozer android clean

# Обновите buildozer
pip install --upgrade buildozer
```

### Проблемы с правами (Linux):
```bash
# Добавьте пользователя в группу
sudo usermod -a -G plugdev $USER
```

## Тестирование APK

1. Включите "Установка из неизвестных источников" на Android
2. Скопируйте APK файл на устройство
3. Установите через файловый менеджер
4. Запустите игру

## Публикация в Google Play

1. Создайте release версию:
```bash
buildozer android release
```

2. Подпишите APK с помощью Android Studio или jarsigner
3. Загрузите в Google Play Console

## Поддержка

При возникновении проблем:
1. Проверьте логи buildozer
2. Убедитесь в правильности установки зависимостей
3. Проверьте версии Python и Java
4. Очистите кэш и пересоберите проект