from flask import Flask, render_template
import os

app = Flask(
    __name__,
    template_folder="templates",
)


@app.get("/")
def dashboard():
    return render_template("index.html")


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    app.run(
        port=5001,
        debug=debug_mode,
    )