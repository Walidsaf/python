from flask import Flask, jsonify, render_template, request

from converter import CONVERSIONS, CONVERSIONS_BY_KEY, run_conversion


app = Flask(__name__)


def conversion_payload() -> list[dict[str, str]]:
    return [
        {
            "key": conversion.key,
            "label": conversion.label,
            "hint": conversion.hint,
            "example": conversion.example,
            "outputLabel": conversion.output_label,
        }
        for conversion in CONVERSIONS
    ]


@app.get("/")
def index():
    return render_template("index.html", conversions=conversion_payload())


@app.get("/api/conversions")
def list_conversions():
    return jsonify({"conversions": conversion_payload()})


@app.post("/api/convert")
def convert():
    data = request.get_json(silent=True) or {}
    choice = str(data.get("choice", "")).strip()
    value = str(data.get("value", ""))
    conversion = CONVERSIONS_BY_KEY.get(choice)

    if conversion is None:
        return jsonify({"ok": False, "error": "Please choose a valid conversion."}), 400

    try:
        result = run_conversion(choice, value)
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 400

    return jsonify(
        {
            "ok": True,
            "result": result,
            "conversion": {
                "key": conversion.key,
                "label": conversion.label,
                "outputLabel": conversion.output_label,
            },
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
