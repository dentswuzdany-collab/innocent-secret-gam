
import os
import random

from flask import (
    Flask, request, session,
    render_template_string, redirect, url_for
)

app = Flask(__name__)

# Secure session key for Render deployment
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "local-development-key"
)


# Website design (HTML + CSS)
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>INNOCENT SECRET GAME</title>

    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            background: #0f172a;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 25px 12px;
        }

        .game {
            background: #1e293b;
            max-width: 420px;
            margin: 30px auto;
            padding: 30px 20px;
            border-radius: 18px;
            box-shadow: 0 8px 30px #0008;
        }

        h1 {
            color: #4ade80;
            font-size: 26px;
        }

        .number {
            font-size: 55px;
            margin: 20px;
        }

        input {
            width: 90%;
            padding: 15px;
            font-size: 20px;
            text-align: center;
            border-radius: 10px;
            border: 2px solid #4ade80;
            background: #0f172a;
            color: white;
            margin: 15px 0;
        }

        button {
            background: #16a34a;
            color: white;
            border: none;
            padding: 14px 25px;
            border-radius: 10px;
            font-size: 17px;
            cursor: pointer;
            width: 90%;
            margin-top: 10px;
        }

        button:hover {
            background: #15803d;
        }

        .message {
            font-size: 19px;
            margin: 22px 0;
            color: #4ade80;
            font-weight: bold;
        }

        .attempts {
            color: #cbd5e1;
            margin-top: 20px;
        }

        .instructions {
            color: #cbd5e1;
            line-height: 1.6;
        }

        .footer {
            font-size: 12px;
            color: #94a3b8;
            margin-top: 25px;
        }
    </style>
</head>

<body>

<div class="game">

    <h1>🎮 INNOCENT SECRET GAME</h1>

    <div class="number">🔢</div>

    <p class="instructions">
        I have selected a secret number
        between 1 and 20.
        <br>
        Can you guess the number?
    </p>

    {% if not won %}

    <form method="POST">

        <input
            type="number"
            name="guess"
            min="1"
            max="20"
            placeholder="Enter your guess"
            required
        >

        <button type="submit">
            SUBMIT GUESS
        </button>

    </form>

    {% endif %}

    <div class="message">
        {{ message }}
    </div>

    <div class="attempts">
        Number of attempts: {{ attempts }}
    </div>

    {% if won %}

        <form action="/restart" method="GET">
            <button type="submit">
                🔄 PLAY AGAIN
            </button>
        </form>

    {% endif %}

    <div class="footer">
        Developed with Python and Flask
        <br>
        INNOCENT SECRET GAME
    </div>

</div>

</body>
</html>
"""


# Start a new game when necessary
def new_game():
    session["secret"] = random.randint(1, 20)
    session["attempts"] = 0
    session["won"] = False
    session["message"] = "Make your first guess!"


# Main website page
@app.route("/", methods=["GET", "POST"])
def home():

    if "secret" not in session:
        new_game()

    if request.method == "POST" and not session["won"]:

        try:
            guess = int(request.form.get("guess", ""))

            if guess < 1 or guess > 20:
                session["message"] = (
                    "Please enter a number from 1 to 20."
                )

            else:
                session["attempts"] += 1

                secret = session["secret"]

                if guess < secret:
                    session["message"] = (
                        "📉 Too low! Try a higher number."
                    )

                elif guess > secret:
                    session["message"] = (
                        "📈 Too high! Try a lower number."
                    )

                else:
                    session["message"] = (
                        "🏆 CONGRATULATIONS!YOU WON!Feel the energy of being a winner and next time you find difficulty in accessing, contact the developers at opokinnocent4@gmail.com"
                    )
                    session["won"] = True

        except ValueError:
            session["message"] = "Please enter a valid number."

    return render_template_string(
        HTML,
        message=session["message"],
        attempts=session["attempts"],
        won=session["won"]
    )


# Restart the game
@app.route("/restart")
def restart():

    session.clear()
    new_game()

    return redirect(url_for("home"))


# Run locally; Gunicorn imports app without executing this block
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
