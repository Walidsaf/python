from collections.abc import Callable
from dataclasses import dataclass


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
