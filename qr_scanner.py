import time
import webbrowser
import pyperclip
from PIL import ImageGrab, Image
from pyzbar.pyzbar import decode
import re
import pystray
from pystray import MenuItem as item
from PIL import Image as PilImage
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
                pyperclip.copy(result)
                webbrowser.open(result)
            last_result = result

def quit_app(icon, item):
    icon.stop()

def main():
    image = PilImage.open("qr_scanner.ico")
    icon = pystray.Icon("QR Code Scanner", image, title="QRScannerFromClipboard", menu=pystray.Menu(
        item('Exit', quit_app)
    ))

    threading.Thread(target=scan_qr_code, daemon=True).start()

    icon.run()

if __name__ == "__main__":
    main()
