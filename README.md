# 🧮 Base Converter Tool

A clean Python utility script to convert numbers and text between different computing bases.

## 🚀 Features
* **Decimal to Binary:** Converts whole numbers to structured binary strings.
* **Binary to Decimal:** Parses binary inputs into integers with error checking.
* **ASCII to Binary:** Encodes standard text characters into 8-bit bytes.
* **Binary to ASCII:** Decodes 8-bit structured bytes back into human-readable text.
* **GUI app:** Includes examples, copy output, keyboard shortcuts, and conversion history.
* **Clean structure:** Conversion logic lives in `converter.py`, and the app entry point is `test.py`.

## 🛠️ Usage
Run the GUI using Python 3:
```bash
python3 test.py
```

If Tkinter is missing, install it first:
```bash
sudo apt install python3-tk
```

You can still run the old terminal menu:
```bash
python3 test.py --cli
```

## Keyboard Shortcuts
* **Ctrl+Enter:** Run the selected conversion.
* **Escape:** Clear the current input and output.
   
