from collections.abc import Callable
from dataclasses import dataclass
import base64
from urllib.parse import quote, unquote


@dataclass(frozen=True)
class Conversion:
    key: str
    label: str
    hint: str
    example: str
    output_label: str
    converter: Callable[[str], object]


def decimal_to_binary(value: int) -> str:
    if value < 0:
        raise ValueError("Decimal value must be non-negative")
    if value == 0:
        return "0"
    return bin(value).replace("0b", "")


def binary_to_decimal(bits: str) -> int:
    cleaned = bits.replace(" ", "").replace(",", "")
    if not cleaned or any(char not in "01" for char in cleaned):
        raise ValueError("Binary must contain only 0 and 1.")
    return int(cleaned, 2)


def ascii_to_binary(text: str) -> list[str]:
    return [format(ord(char), "08b") for char in text]


def binary_to_ascii(bits: str) -> str:
    cleaned = bits.replace(" ", "").replace(",", "")
    if len(cleaned) % 8 != 0:
        raise ValueError("Binary must be grouped into 8-bit bytes.")

    chars = []
    for i in range(0, len(cleaned), 8):
        byte = cleaned[i : i + 8]
        value = int(byte, 2)
        if value > 127:
            raise ValueError("This binary data is not valid ASCII.")
        chars.append(chr(value))
    return "".join(chars)


# --- New: Text <-> Binary (full Unicode via UTF-8, unlike the ASCII-only pair above) ---

def text_to_binary(text: str) -> list[str]:
    return [format(byte, "08b") for byte in text.encode("utf-8")]


def binary_to_text(bits: str) -> str:
    cleaned = bits.replace(" ", "").replace(",", "")
    if len(cleaned) % 8 != 0:
        raise ValueError("Binary must be grouped into 8-bit bytes.")
    byte_values = []
    for i in range(0, len(cleaned), 8):
        byte_values.append(int(cleaned[i : i + 8], 2))
    try:
        return bytes(byte_values).decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("This binary data is not valid UTF-8 text.") from error


def ascii_to_utf8_bytes(text: str) -> list[int]:
    return list(text.encode("utf-8"))


def utf8_to_ascii(values: str) -> str:
    numbers = parse_decimal_values(values)
    if any(number < 0 or number > 255 for number in numbers):
        raise ValueError("UTF-8 byte values must be between 0 and 255.")
    try:
        return bytes(numbers).decode("ascii")
    except UnicodeDecodeError as error:
        raise ValueError("These byte values are not valid ASCII text.") from error


def ascii_to_decimal(text: str) -> list[int]:
    return [ord(char) for char in text]


def decimal_to_ascii(values: str) -> str:
    numbers = parse_decimal_values(values)
    return "".join(chr(number) for number in numbers)


def utf8_to_decimal(text: str) -> list[int]:
    return list(text.encode("utf-8"))


def decimal_to_utf8(values: str) -> str:
    numbers = parse_decimal_values(values)
    if any(number < 0 or number > 255 for number in numbers):
        raise ValueError("UTF-8 byte values must be between 0 and 255.")

    if len(numbers) == 1:
        try:
            return bytes(numbers).decode("utf-8")
        except UnicodeDecodeError:
            return chr(numbers[0])

    try:
        return bytes(numbers).decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("These byte values do not form valid UTF-8 text.") from error


def parse_decimal_values(values: str) -> list[int]:
    try:
        numbers = [int(item.strip()) for item in values.replace(",", " ").split() if item.strip()]
    except ValueError as error:
        raise ValueError("Decimal values must be whole numbers separated by spaces or commas.") from error

    if not numbers:
        raise ValueError("Please enter at least one decimal value.")
    return numbers


# --- New: Base64 -----------------------------------------------------------

def text_to_base64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def base64_to_text(value: str) -> str:
    cleaned = value.strip()
    try:
        decoded_bytes = base64.b64decode(cleaned, validate=True)
    except Exception as error:
        raise ValueError("This is not valid Base64 text.") from error
    try:
        return decoded_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("Decoded Base64 data is not valid UTF-8 text.") from error


# --- New: Hex ----------------------------------------------------------------

def text_to_hex(text: str) -> str:
    return text.encode("utf-8").hex(" ")


def hex_to_text(value: str) -> str:
    cleaned = value.replace(" ", "").replace(",", "").replace("0x", "").replace("\n", "")
    if len(cleaned) % 2 != 0:
        raise ValueError("Hex must have an even number of digits.")
    try:
        raw_bytes = bytes.fromhex(cleaned)
    except ValueError as error:
        raise ValueError("Enter valid hexadecimal digits (0-9, a-f).") from error
    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("These hex bytes are not valid UTF-8 text.") from error


# --- New: URL encoding ---------------------------------------------------------

def url_encode(text: str) -> str:
    return quote(text, safe="")


def url_decode(value: str) -> str:
    try:
        return unquote(value, errors="strict")
    except UnicodeDecodeError as error:
        raise ValueError("This is not valid percent-encoded text.") from error


# --- New: Morse code -----------------------------------------------------------

MORSE_CODE_MAP = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.", "!": "-.-.--",
    "/": "-..-.", "(": "-.--.", ")": "-.--.-", "&": ".-...", ":": "---...",
    ";": "-.-.-.", "=": "-...-", "+": ".-.-.", "-": "-....-", "_": "..--.-",
    '"': ".-..-.", "$": "...-..-", "@": ".--.-.",
}
MORSE_CODE_REVERSE = {code: letter for letter, code in MORSE_CODE_MAP.items()}


def text_to_morse(text: str) -> str:
    words = text.upper().split(" ")
    encoded_words = []
    for word in words:
        letters = []
        for char in word:
            code = MORSE_CODE_MAP.get(char)
            if code is None:
                raise ValueError(f"'{char}' has no Morse code mapping.")
            letters.append(code)
        encoded_words.append(" ".join(letters))
    return " / ".join(encoded_words)


def morse_to_text(value: str) -> str:
    words = value.strip().split(" / ")
    if not words or words == [""]:
        raise ValueError("Please enter Morse code (dots and dashes).")
    decoded_words = []
    for word in words:
        letters = []
        for token in word.split():
            char = MORSE_CODE_REVERSE.get(token)
            if char is None:
                raise ValueError(f"'{token}' is not valid Morse code.")
            letters.append(char)
        decoded_words.append("".join(letters))
    return " ".join(decoded_words)


# --- New: Text stats -----------------------------------------------------------

def text_stats(text: str) -> str:
    char_count = len(text)
    byte_count = len(text.encode("utf-8"))
    word_count = len(text.split())
    line_count = len(text.splitlines()) or 1
    return (
        f"Characters: {char_count} | Words: {word_count} | "
        f"UTF-8 bytes: {byte_count} | Lines: {line_count}"
    )


def format_result(result: object) -> str:
    if isinstance(result, list):
        return " ".join(str(item) for item in result)
    return str(result)


CONVERSIONS: tuple[Conversion, ...] = (
    Conversion(
        "1",
        "Decimal -> Binary",
        "Enter a non-negative whole number.",
        "42",
        "Binary",
        lambda value: decimal_to_binary(int(value.strip())),
    ),
    Conversion(
        "2",
        "Binary -> Decimal",
        "Enter binary digits. Spaces and commas are allowed.",
        "101010",
        "Decimal",
        binary_to_decimal,
    ),
    Conversion(
        "3",
        "ASCII -> Binary",
        "Enter plain ASCII text.",
        "Hello",
        "Binary bytes",
        ascii_to_binary,
    ),
    Conversion(
        "4",
        "Binary -> ASCII",
        "Enter 8-bit binary bytes.",
        "01001000 01100101 01101100 01101100 01101111",
        "ASCII text",
        binary_to_ascii,
    ),
    Conversion(
        "5",
        "ASCII -> UTF-8 bytes",
        "Enter ASCII text.",
        "Hello",
        "UTF-8 bytes",
        ascii_to_utf8_bytes,
    ),
    Conversion(
        "6",
        "UTF-8 bytes -> ASCII",
        "Enter decimal byte values from 0 to 127.",
        "72 101 108 108 111",
        "ASCII text",
        utf8_to_ascii,
    ),
    Conversion(
        "7",
        "ASCII -> Decimal",
        "Enter ASCII text.",
        "ABC",
        "Decimal values",
        ascii_to_decimal,
    ),
    Conversion(
        "8",
        "Decimal -> ASCII",
        "Enter decimal character values.",
        "65 66 67",
        "ASCII text",
        decimal_to_ascii,
    ),
    Conversion(
        "9",
        "UTF-8 -> Decimal",
        "Enter any UTF-8 text.",
        "cafe",
        "UTF-8 bytes",
        utf8_to_decimal,
    ),
    Conversion(
        "10",
        "Decimal -> UTF-8",
        "Enter decimal bytes or one code point.",
        "195 169",
        "UTF-8 text",
        decimal_to_utf8,
    ),
    Conversion(
        "11",
        "Text -> Base64",
        "Enter any text.",
        "Hello, World!",
        "Base64",
        text_to_base64,
    ),
    Conversion(
        "12",
        "Base64 -> Text",
        "Enter Base64-encoded text.",
        "SGVsbG8sIFdvcmxkIQ==",
        "Text",
        base64_to_text,
    ),
    Conversion(
        "13",
        "Text -> Hex",
        "Enter any text.",
        "Hello",
        "Hex bytes",
        text_to_hex,
    ),
    Conversion(
        "14",
        "Hex -> Text",
        "Enter hex bytes. Spaces are optional.",
        "48 65 6c 6c 6f",
        "Text",
        hex_to_text,
    ),
    Conversion(
        "15",
        "URL Encode",
        "Enter text or a URL to percent-encode.",
        "hello world!",
        "URL-encoded text",
        url_encode,
    ),
    Conversion(
        "16",
        "URL Decode",
        "Enter percent-encoded text.",
        "hello%20world%21",
        "Decoded text",
        url_decode,
    ),
    Conversion(
        "17",
        "Text -> Morse Code",
        "Enter letters, numbers, and basic punctuation.",
        "SOS",
        "Morse code",
        text_to_morse,
    ),
    Conversion(
        "18",
        "Morse Code -> Text",
        "Enter Morse code. Space between letters, / between words.",
        "... --- ...",
        "Text",
        morse_to_text,
    ),
    Conversion(
        "19",
        "Text Length / Byte Counter",
        "Enter any text to count characters, words, bytes, and lines.",
        "Hello, World!",
        "Stats",
        text_stats,
    ),
    Conversion(
        "20",
        "Text -> Binary",
        "Enter any text (full Unicode supported, not just ASCII).",
        "Cafe \u2615",
        "Binary bytes",
        text_to_binary,
    ),
    Conversion(
        "21",
        "Binary -> Text",
        "Enter 8-bit binary bytes (supports full Unicode/UTF-8, not just ASCII).",
        "01000011 01100001 01100110 01100101 00100000 11100010 10011000 10010101",
        "Text",
        binary_to_text,
    ),
)

CONVERSIONS_BY_KEY = {conversion.key: conversion for conversion in CONVERSIONS}
CONVERSIONS_BY_LABEL = {conversion.label: conversion for conversion in CONVERSIONS}


def run_conversion(choice: str, raw_value: str) -> str:
    conversion = CONVERSIONS_BY_KEY.get(choice)
    if conversion is None:
        raise ValueError("Please choose a valid conversion.")
    if not raw_value.strip():
        raise ValueError("Please enter a value to convert.")

    try:
        result = conversion.converter(raw_value)
    except ValueError:
        raise
    except UnicodeEncodeError as error:
        raise ValueError("That text contains characters outside the selected encoding.") from error

    return format_result(result)