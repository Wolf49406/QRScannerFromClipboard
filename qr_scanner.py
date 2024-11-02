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
import tkinter as tk
from tkinter import messagebox

ICON_PATH = "qr_scanner.ico"
CHECK_INTERVAL = 2
URL_PATTERN = re.compile(r'https?://[^\s]+')

def error_notification(error):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("An Error Has Accured", error)
    root.destroy()

def get_qr_code_from_clipboard():
    try:
        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
            decoded_objects = decode(image)
            for obj in decoded_objects:
                return obj.data.decode('utf-8')
    except Exception as e:
        error_notification(f"QR decode error: {e}")
    return None

def scan_qr_codes():
    last_result = None

    while True:
        time.sleep(CHECK_INTERVAL)
        result = get_qr_code_from_clipboard()

        if result and result != last_result:
            if URL_PATTERN.match(result):
                pyperclip.copy(result)
                try:
                    webbrowser.open(result)
                except Exception as e:
                    error_notification(f"URL open error: {e}")
            last_result = result

def quit_application(icon, item):
    icon.stop()

def main():
    image = PilImage.open(ICON_PATH)
    icon = pystray.Icon(
        "QR Code Scanner",
        image,
        title="QRScannerFromClipboard",
        menu=pystray.Menu(item('Exit', quit_application))
    )

    threading.Thread(target=scan_qr_codes, daemon=True).start()
    icon.run()

if __name__ == "__main__":
    main()
