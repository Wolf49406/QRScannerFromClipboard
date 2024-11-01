import time
import webbrowser
from PIL import ImageGrab, Image
from pyzbar.pyzbar import decode
import re
import pystray
from pystray import MenuItem as item
from PIL import Image as PilImage  # Избегаем конфликта имен
import threading

def get_qr_code_from_clipboard():
    image = ImageGrab.grabclipboard()
    if isinstance(image, Image.Image):
        decoded_objects = decode(image)
        for obj in decoded_objects:
            return obj.data.decode('utf-8')
    return None

def scan_qr_code():
    last_result = None
    url_pattern = re.compile(r'https?://[^\s]+')

    while True:
        time.sleep(2)
        result = get_qr_code_from_clipboard()

        if result and result != last_result:
            if url_pattern.match(result):
                webbrowser.open(result)
            last_result = result

def quit_app(icon, item):
    icon.stop()  # Закрытие иконки в трее и завершение программы

def main():
    # Настройка иконки для трея
    image = PilImage.open("qr_scanner.ico") # Иконка
    icon = pystray.Icon("QR Code Scanner", image, menu=pystray.Menu(
        item('Exit', quit_app)  # Добавление пункта меню для выхода
    ))

    # Запускаем сканер QR-кодов в отдельном потоке
    threading.Thread(target=scan_qr_code, daemon=True).start()

    # Отображение иконки в трее
    icon.run()

if __name__ == "__main__":
    main()
