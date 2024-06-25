# Markdown to HTML Converter

Цей консольний застосунок конвертує файли з розміткою Markdown у HTML. 

## Вимоги
- Python 3.x

## Встановлення

1. **Клонування репозиторію:**
    ```sh
    git clone https://github.com/yourusername/MTRPZ_1

    cd MTRPZ_1
    ```
```

## Використання

У проекті вже є файл markdown.md, в якому є приклад з markdown розміткою в тексті. 
За бажанням текст всередені можна змінити

### Перетворення Markdown у HTML

1. **Виведення HTML у стандартний вивід (stdout):**
    ```sh
    python app.py /path/to/valid/markdown.md
    ```

2. **Запис HTML у файл:**
    ```sh
    python app.py /path/to/valid/markdown.md --out /path/to/output.html
    ```

### Обробка помилок

1. **При обробці невалідного Markdown файл:**
    ```sh
    python app.py /path/to/invalid/markdown.md
    ```

    
tests can be useful and I need to learn how to use them, at least because I've been told at work that I'll have to use them sooner or later. 
Unfortunately, I was unable to implement the tests in this repository
