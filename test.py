import sys

from converter import CONVERSIONS, CONVERSIONS_BY_KEY, CONVERSIONS_BY_LABEL, run_conversion


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
    for conversion in CONVERSIONS:
        print(f" {conversion.key:>2}. {conversion.label}: {conversion.example}")
    print()


def show_menu() -> None:
    print("Main menu")
    for conversion in CONVERSIONS:
        print(f"{conversion.key}. {conversion.label}")
    print("11. Help")
    print("Type 'exit' to leave")
    print("-" * 36)


def main_cli() -> None:
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

        conversion = CONVERSIONS_BY_KEY.get(choice)
        if conversion is None:
            print("Invalid choice. Please enter a number from 1 to 10, or type help.")
            print("-" * 36)
            continue

        raw_value = input(f"{conversion.hint} Example: {conversion.example}: ").strip()
        if raw_value.lower() in {"back", "b", "menu"}:
            continue

        try:
            print(f"{conversion.output_label}: {run_conversion(choice, raw_value)}")
        except ValueError as error:
            print(f"Error: {error}")

        print("-" * 36)


def launch_gui() -> None:
    try:
        import tkinter as tk
        from tkinter import ttk
    except ModuleNotFoundError:
        print("Tkinter is not installed on this computer.")
        print("On Ubuntu/Debian, install it with: sudo apt install python3-tk")
        print("You can still use the terminal version with: python3 test.py --cli")
        return

    root = tk.Tk()
    root.title("Encoding Explorer")
    root.geometry("940x620")
    root.minsize(760, 540)

    colors = {
        "bg": "#f4f1ea",
        "panel": "#ffffff",
        "panel_alt": "#eef5f1",
        "text": "#1b2528",
        "muted": "#5a686d",
        "accent": "#1f7a5b",
        "accent_dark": "#155a43",
        "border": "#d6ddd8",
        "error": "#b3261e",
        "history": "#f9fbfa",
    }

    root.configure(background=colors["bg"])
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Root.TFrame", background=colors["bg"])
    style.configure("Panel.TFrame", background=colors["panel"], relief="flat")
    style.configure("Side.TFrame", background=colors["panel_alt"], relief="flat")
    style.configure("Title.TLabel", background=colors["panel"], foreground=colors["text"], font=("Arial", 24, "bold"))
    style.configure("SideTitle.TLabel", background=colors["panel_alt"], foreground=colors["text"], font=("Arial", 16, "bold"))
    style.configure("Body.TLabel", background=colors["panel"], foreground=colors["muted"], font=("Arial", 11))
    style.configure("SideBody.TLabel", background=colors["panel_alt"], foreground=colors["muted"], font=("Arial", 10))
    style.configure("Field.TLabel", background=colors["panel"], foreground=colors["text"], font=("Arial", 11, "bold"))
    style.configure("Status.TLabel", background=colors["panel"], foreground=colors["accent"], font=("Arial", 10, "bold"))
    style.configure("Error.TLabel", background=colors["panel"], foreground=colors["error"], font=("Arial", 10, "bold"))
    style.configure("Accent.TButton", background=colors["accent"], foreground="#ffffff", font=("Arial", 10, "bold"), padding=9)
    style.map("Accent.TButton", background=[("active", colors["accent_dark"])])
    style.configure("TButton", font=("Arial", 10), padding=9)
    style.configure("TCombobox", padding=7)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    shell = ttk.Frame(root, style="Root.TFrame", padding=18)
    shell.grid(row=0, column=0, sticky="nsew")
    shell.columnconfigure(0, weight=3)
    shell.columnconfigure(1, weight=2)
    shell.rowconfigure(0, weight=1)

    workspace = ttk.Frame(shell, style="Panel.TFrame", padding=22)
    workspace.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
    workspace.columnconfigure(0, weight=1)
    workspace.rowconfigure(5, weight=1)
    workspace.rowconfigure(8, weight=1)

    sidebar = ttk.Frame(shell, style="Side.TFrame", padding=18)
    sidebar.grid(row=0, column=1, sticky="nsew")
    sidebar.columnconfigure(0, weight=1)
    sidebar.rowconfigure(3, weight=1)

    title = ttk.Label(workspace, text="Encoding Explorer", style="Title.TLabel")
    title.grid(row=0, column=0, sticky="w")

    subtitle = ttk.Label(
        workspace,
        text="Convert decimal, binary, ASCII, and UTF-8 values with quick examples and history.",
        style="Body.TLabel",
    )
    subtitle.grid(row=1, column=0, sticky="w", pady=(4, 18))

    selected_conversion = tk.StringVar(value=CONVERSIONS[0].label)
    status_value = tk.StringVar(value=CONVERSIONS[0].hint)

    conversion_menu = ttk.Combobox(
        workspace,
        textvariable=selected_conversion,
        values=[conversion.label for conversion in CONVERSIONS],
        state="readonly",
        font=("Arial", 11),
    )
    conversion_menu.grid(row=2, column=0, sticky="ew", pady=(0, 14))

    hint_label = ttk.Label(workspace, textvariable=status_value, style="Status.TLabel")
    hint_label.grid(row=3, column=0, sticky="w", pady=(0, 10))

    input_label = ttk.Label(workspace, text="Input", style="Field.TLabel")
    input_label.grid(row=4, column=0, sticky="w")

    input_box = tk.Text(
        workspace,
        height=7,
        wrap="word",
        font=("Consolas", 12),
        foreground=colors["text"],
        background="#fffdfa",
        insertbackground=colors["text"],
        relief="solid",
        borderwidth=1,
        padx=10,
        pady=10,
    )
    input_box.grid(row=5, column=0, sticky="nsew", pady=(6, 14))

    button_frame = ttk.Frame(workspace, style="Panel.TFrame")
    button_frame.grid(row=6, column=0, sticky="ew", pady=(0, 14))
    button_frame.columnconfigure(5, weight=1)

    output_label = ttk.Label(workspace, text="Output", style="Field.TLabel")
    output_label.grid(row=7, column=0, sticky="w")

    output_box = tk.Text(
        workspace,
        height=7,
        wrap="word",
        font=("Consolas", 12),
        foreground=colors["text"],
        background="#f9fbfa",
        relief="solid",
        borderwidth=1,
        padx=10,
        pady=10,
        state="disabled",
    )
    output_box.grid(row=8, column=0, sticky="nsew", pady=(6, 0))

    history_title = ttk.Label(sidebar, text="History", style="SideTitle.TLabel")
    history_title.grid(row=0, column=0, sticky="w")

    history_hint = ttk.Label(sidebar, text="Recent conversions appear here.", style="SideBody.TLabel")
    history_hint.grid(row=1, column=0, sticky="w", pady=(2, 12))

    history_list = tk.Listbox(
        sidebar,
        height=14,
        activestyle="none",
        background=colors["history"],
        foreground=colors["text"],
        selectbackground=colors["accent"],
        selectforeground="#ffffff",
        relief="solid",
        borderwidth=1,
        font=("Arial", 10),
    )
    history_list.grid(row=3, column=0, sticky="nsew")

    side_buttons = ttk.Frame(sidebar, style="Side.TFrame")
    side_buttons.grid(row=4, column=0, sticky="ew", pady=(12, 0))
    side_buttons.columnconfigure(0, weight=1)
    side_buttons.columnconfigure(1, weight=1)

    shortcuts = ttk.Label(
        sidebar,
        text="Ctrl+Enter converts. Escape clears.",
        style="SideBody.TLabel",
    )
    shortcuts.grid(row=5, column=0, sticky="w", pady=(16, 0))

    history_items: list[dict[str, str]] = []

    def current_conversion():
        return CONVERSIONS_BY_LABEL[selected_conversion.get()]

    def set_output(text: str) -> None:
        output_box.configure(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", text)
        output_box.configure(state="disabled")

    def set_status(text: str, error: bool = False) -> None:
        hint_label.configure(style="Error.TLabel" if error else "Status.TLabel")
        status_value.set(text)

    def add_history(label: str, raw_text: str, result: str) -> None:
        item = {
            "label": label,
            "input": raw_text,
            "output": result,
        }
        history_items.insert(0, item)
        del history_items[20:]

        history_list.delete(0, tk.END)
        for entry in history_items:
            summary_input = entry["input"].replace("\n", " ")
            summary_output = entry["output"].replace("\n", " ")
            if len(summary_input) > 22:
                summary_input = summary_input[:19] + "..."
            if len(summary_output) > 22:
                summary_output = summary_output[:19] + "..."
            history_list.insert(tk.END, f"{entry['label']}: {summary_input} -> {summary_output}")

    def convert() -> None:
        conversion = current_conversion()
        raw_text = input_box.get("1.0", tk.END).strip()
        try:
            result = run_conversion(conversion.key, raw_text)
        except ValueError as error:
            set_output("")
            set_status(f"Error: {error}", error=True)
            return

        set_output(result)
        set_status(f"{conversion.output_label} ready.")
        add_history(conversion.label, raw_text, result)

    def clear() -> None:
        input_box.delete("1.0", tk.END)
        set_output("")
        set_status(current_conversion().hint)
        input_box.focus_set()

    def fill_example() -> None:
        conversion = current_conversion()
        input_box.delete("1.0", tk.END)
        input_box.insert("1.0", conversion.example)
        set_output("")
        set_status("Example loaded.")
        input_box.focus_set()

    def copy_output() -> None:
        text = output_box.get("1.0", tk.END).strip()
        if not text:
            set_status("Nothing to copy yet.", error=True)
            return
        root.clipboard_clear()
        root.clipboard_append(text)
        set_status("Output copied.")

    def clear_history() -> None:
        history_items.clear()
        history_list.delete(0, tk.END)
        set_status("History cleared.")

    def reuse_history(event: object | None = None) -> None:
        selection = history_list.curselection()
        if not selection:
            return
        item = history_items[selection[0]]
        selected_conversion.set(item["label"])
        input_box.delete("1.0", tk.END)
        input_box.insert("1.0", item["input"])
        set_output(item["output"])
        set_status("History item loaded.")

    def update_hint(event: object | None = None) -> None:
        set_status(current_conversion().hint)
        set_output("")
        input_box.focus_set()

    convert_button = ttk.Button(button_frame, text="Convert", style="Accent.TButton", command=convert)
    convert_button.grid(row=0, column=0, sticky="w")

    example_button = ttk.Button(button_frame, text="Example", command=fill_example)
    example_button.grid(row=0, column=1, sticky="w", padx=(8, 0))

    clear_button = ttk.Button(button_frame, text="Clear", command=clear)
    clear_button.grid(row=0, column=2, sticky="w", padx=(8, 0))

    copy_button = ttk.Button(button_frame, text="Copy Output", command=copy_output)
    copy_button.grid(row=0, column=3, sticky="w", padx=(8, 0))

    reuse_button = ttk.Button(side_buttons, text="Reuse", command=reuse_history)
    reuse_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))

    clear_history_button = ttk.Button(side_buttons, text="Clear", command=clear_history)
    clear_history_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))

    conversion_menu.bind("<<ComboboxSelected>>", update_hint)
    history_list.bind("<Double-Button-1>", reuse_history)
    input_box.bind("<Control-Return>", lambda event: convert())
    root.bind("<Escape>", lambda event: clear())

    fill_example()
    root.mainloop()


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] in {"--cli", "-c"}:
        main_cli()
    else:
        launch_gui()


if __name__ == "__main__":
    main()
