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
    numbers = [int(item.strip()) for item in values.replace(",", " ").split() if item.strip()]
    if not numbers:
        raise ValueError("Please enter at least one decimal value.")
    if any(number < 0 or number > 255 for number in numbers):
        raise ValueError("UTF-8 byte values must be between 0 and 255.")
    return bytes(numbers).decode("ascii")


def ascii_to_decimal(text: str) -> list[int]:
    return [ord(char) for char in text]


def decimal_to_ascii(values: str) -> str:
    numbers = [int(item.strip()) for item in values.replace(",", " ").split() if item.strip()]
    if not numbers:
        raise ValueError("Please enter at least one decimal value.")
    return "".join(chr(number) for number in numbers)


def utf8_to_decimal(text: str) -> list[int]:
    return list(text.encode("utf-8"))


def decimal_to_utf8(values: str) -> str:
    numbers = [int(item.strip()) for item in values.replace(",", " ").split() if item.strip()]
    if not numbers:
        raise ValueError("Please enter at least one decimal value.")
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


def show_intro() -> None:
    print("Welcome to the Encoding Explorer")
    print("=" * 36)
    print("Why this matters:")
    print("Computers store everything as numbers. Text is represented")
    print("with binary, ASCII uses simple 8-bit values, and UTF-8 supports")
    print("many languages, symbols, and emojis.")
    print("Learning these conversions helps you understand how digital text works.")
    print()


def show_help() -> None:
    print("Help guide")
    print("- Type a number from the menu to choose a conversion")
    print("- Type 'back' to return to the main menu")
    print("- Type 'exit' to stop the program")
    print("Examples:")
    print("  1. Decimal -> Binary: 42")
    print("  2. Binary -> Decimal: 101010")
    print("  3. ASCII -> Binary: Hello")
    print("  4. Binary -> ASCII: 01001000 01100101")
    print("  5. ASCII -> UTF-8 bytes: Hello")
    print("  6. UTF-8 bytes -> ASCII: 72 101 108 108 111")
    print("  7. ASCII -> Decimal: ABC")
    print("  8. Decimal -> ASCII: 65 66 67")
    print("  9. UTF-8 -> Decimal: café")
    print(" 10. Decimal -> UTF-8: 195 169")
    print()


def show_menu() -> None:
    print("Main menu")
    print("1. Decimal -> Binary")
    print("2. Binary -> Decimal")
    print("3. ASCII -> Binary")
    print("4. Binary -> ASCII")
    print("5. ASCII -> UTF-8 bytes")
    print("6. UTF-8 -> ASCII")
    print("7. ASCII -> Decimal")
    print("8. Decimal -> ASCII")
    print("9. UTF-8 -> Decimal")
    print("10. Decimal -> UTF-8")
    print("11. Help")
    print("Type 'exit' to leave")
    print("-" * 36)


def main() -> None:
    show_intro()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip().lower()

        if choice == "exit":
            print("Goodbye! Keep exploring encoding and digital text.")
            break

        if choice in {"help", "h", "11"}:
            show_help()
            print("-" * 36)
            continue

        try:
            if choice == "1":
                raw_value = input("Enter a decimal number: ").strip()
                if raw_value.lower() in {"back", "b", "menu"}:
                    continue
                value = int(raw_value)
                print(f"Binary: {decimal_to_binary(value)}")
            elif choice == "2":
                raw_bits = input("Enter binary digits (example: 101010): ").strip()
                if raw_bits.lower() in {"back", "b", "menu"}:
                    continue
                print(f"Decimal: {binary_to_decimal(raw_bits)}")
            elif choice == "3":
                text = input("Enter ASCII text (example: Hello): ").strip()
                if text.lower() in {"back", "b", "menu"}:
                    continue
                print("Binary bytes:", ascii_to_binary(text))
            elif choice == "4":
                bits = input("Enter 8-bit binary bytes (example: 01001000 01100101): ").strip()
                if bits.lower() in {"back", "b", "menu"}:
                    continue
                print("ASCII text:", binary_to_ascii(bits))
            elif choice == "5":
                text = input("Enter ASCII text (example: Hello): ").strip()
                if text.lower() in {"back", "b", "menu"}:
                    continue
                print("UTF-8 bytes (decimal):", ascii_to_utf8_bytes(text))
            elif choice == "6":
                raw_values = input("Enter UTF-8 byte values (example: 72 101 108 108 111): ").strip()
                if raw_values.lower() in {"back", "b", "menu"}:
                    continue
                print("ASCII text:", utf8_to_ascii(raw_values))
            elif choice == "7":
                text = input("Enter ASCII text (example: ABC): ").strip()
                if text.lower() in {"back", "b", "menu"}:
                    continue
                print("Decimal values:", ascii_to_decimal(text))
            elif choice == "8":
                raw_values = input("Enter decimal values (example: 65 66 67): ").strip()
                if raw_values.lower() in {"back", "b", "menu"}:
                    continue
                print("ASCII text:", decimal_to_ascii(raw_values))
            elif choice == "9":
                text = input("Enter UTF-8 text (example: café): ").strip()
                if text.lower() in {"back", "b", "menu"}:
                    continue
                print("UTF-8 bytes (decimal):", utf8_to_decimal(text))
            elif choice == "10":
                raw_values = input("Enter decimal bytes or a code point (example: 195 169 or 233): ").strip()
                if raw_values.lower() in {"back", "b", "menu"}:
                    continue
                print("UTF-8 text:", decimal_to_utf8(raw_values))
            else:
                print("Invalid choice. Please enter a number from 1 to 10, or type help.")
        except ValueError as error:
            print(f"Error: {error}")

        print("-" * 36)


if __name__ == "__main__":
    main()
