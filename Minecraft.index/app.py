from flask import Flask, render_template, jsonify , request, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import time
import random
import psutil
from datetime import timedelta
import requests
from openai import OpenAI
from openai import RateLimitError

MC_ERRORS = [
    "You tried to access a chunk that doesn’t exist.",
    "This page fell into the void.",
    "404: Creeper blew up the route.",
    "The server looked everywhere, but found nothing.",
    "That path was never crafted."
]

client = OpenAI(api_key="is that easy to find my api key? i don't think so. u can try that :) it stars with wtf")


DISCORD_WEBHOOK_URL = "holy moly you really thought i would share that?"

def send_discord_message(content):
    data = {
        "content": content
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

start_time = time.time()

app = Flask(__name__)
app.secret_key = "dangerous" 
CORS(app)
app.permanent_session_lifetime = timedelta(days=30)
DB_NAME = "users.db"

# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

#-------------------------
#  YAPAY ZEKA
#-------------------------


@app.route("/ai", methods=["GET", "POST"])
def ai():
    if "user" not in session:
        return redirect("/login")

    answer = ""  # HER DURUMDA TANIMLxI

    if request.method == "POST":
        question = request.form["question"]

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content

        except Exception:
            # API patlarsa → yerel AI
            answer = local_ai_answer(question)

    # 🔥 KRİTİK SATIR (HATAYI BİTİREN ŞEY)
    return render_template("ai.html", answer=answer)



def local_ai_answer(question):
    q = question.lower()

    # =====================
    # Programming & Web
    # =====================
    if "python" in q:
        return (
            "Python is a beginner-friendly programming language with a clean syntax. "
            "It is commonly used for backend development, automation, and AI."
        )

    if "flask" in q:
        return (
            "Flask is a lightweight Python web framework. "
            "It is ideal for small to medium projects and gives developers full control."
        )

    if "html" in q:
        return (
            "HTML is the structure of the web. "
            "It defines elements like text, forms, buttons, and layouts."
        )

    if "css" in q:
        return (
            "CSS is used to style web pages. "
            "It controls colors, layout, animations, and responsiveness."
        )

    if "jinja" in q:
        return (
            "Jinja is a templating engine for Flask. "
            "It allows dynamic HTML using variables, loops, and conditions."
        )

    if "database" in q or "db" in q:
        return (
            "A database stores data permanently. "
            "Common databases include SQLite, MySQL, and PostgreSQL."
        )

    if "sql" in q:
        return (
            "SQL is a language used to query databases. "
            "It allows creating, reading, updating, and deleting data."
        )

    if "login" in q or "authentication" in q:
        return (
            "Authentication ensures only authorized users can access protected pages. "
            "Flask often uses sessions for this."
        )

    if "session" in q:
        return (
            "Sessions store user data temporarily while they are logged in. "
            "They help track active users."
        )

    if "api" in q:
        return (
            "An API allows different software systems to communicate with each other."
        )

    # =====================
    # Artificial Intelligence
    # =====================
    if "ai" in q or "artificial intelligence" in q:
        return (
            "Artificial Intelligence focuses on creating systems that can simulate human thinking "
            "and decision-making."
        )

    # =====================
    # Minecraft Basics
    # =====================
    if "minecraft" in q or "mc" in q:
        return (
            "Minecraft is a sandbox game focused on creativity, survival, and exploration."
        )

    if "survival" in q:
        return (
            "Survival mode is about gathering resources, crafting tools, and staying alive "
            "while facing mobs."
        )

    if "creative" in q:
        return (
            "Creative mode gives unlimited resources and the ability to fly, "
            "allowing players to build freely."
        )

    if "redstone" in q:
        return (
            "Redstone is Minecraft's logic system. "
            "It can be used to create circuits, traps, farms, and automatic machines."
        )

    if "mob" in q:
        return (
            "Mobs are living entities in Minecraft. "
            "They can be hostile, passive, or neutral."
        )

    if "creeper" in q:
        return (
            "Creepers are hostile mobs that silently approach players and explode."
        )

    if "ender dragon" in q:
        return (
            "The Ender Dragon is Minecraft’s final boss, found in the End dimension."
        )

    if "nether" in q:
        return (
            "The Nether is a dangerous dimension filled with lava, hostile mobs, "
            "and valuable resources like Netherite."
        )

    if "netherite" in q:
        return (
            "Netherite is the strongest material in Minecraft, "
            "used to upgrade diamond gear."
        )

    if "enchant" in q or "enchantment" in q:
        return (
            "Enchantments improve tools, weapons, and armor using an enchanting table or anvil."
        )

    if "farm" in q:
        return (
            "Farms are automated systems used to collect resources efficiently, "
            "often using redstone and mob mechanics."
        )

    if "mod" in q or "modding" in q:
        return (
            "Mods are community-made modifications that add new content or mechanics to Minecraft."
        )

    if "shader" in q:
        return (
            "Shaders improve Minecraft’s graphics by adding realistic lighting, shadows, and water."
        )

    # =====================
    # Errors & UX
    # =====================
    if "404" in q or "error" in q:
        return (
            "A 404 error means the requested page does not exist. "
            "Custom error pages improve user experience."
        )

    # =====================
    # Fallback
    # =====================
    return (
        "I don't have an answer for that yet. "
        "Try asking about Python, Flask, web development, or Minecraft."
    )






# ------------------------
#   ROUTES
# ------------------------

@app.route("/")
def route():
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if "user" in session:
        return redirect("/home")

    error = None

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        hashed_pw = generate_password_hash(password)

        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                (email, username, hashed_pw)
            )
            conn.commit()
            conn.close()
            send_discord_message(
        f"🆕 **New user registered!**\n👤 Username: `{username}`"
    )

            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            error = "Email or username already exists."

    return render_template("signup.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():

    if "user" in session:
        return redirect("/home")
    
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        remember = request.form.get("remember")  # checkbox

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user"] = user["username"]
            if remember:
                session.permanent = True
            else:
                session.permanent = False
            return redirect(url_for("home"))
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)



@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")



@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("index.html", username=session["user"])




@app.route("/items")
def items():
    if "user" not in session:
        return redirect("/login")

    return render_template("items.html")


@app.route("/blocks")
def blocks():
    if "user" not in session:
        return redirect("/login")

    return render_template("blocks.html")


@app.route("/mobs")
def mobs():
    if "user" not in session:
        return redirect("/login")

    return render_template("mobs.html")


@app.route("/seeds")
def seeds():
    if "user" not in session:
        return redirect("/login")
    
    return render_template("seeds.html")


@app.route("/seedconverter")
def seedconverter():
    if "user" not in session:
        return redirect("/login")
    
    return render_template("seedconverter.html")


@app.route("/redstone")
def redstone():
    if "user" not in session:
        return redirect("/login")
    
    return render_template("redstone.html")

@app.route("/creepypasta")
def creepypasta():
    if "user" not in session:
        return redirect("/login")
    
    return render_template("creepypasta.html")


@app.route('/creator')
def creator():
    if 'user' not in session:
        return redirect('/login')
    return render_template('creator.html')


# ------------------------
#   API
# ------------------------

@app.route("/old_dashboard") 
def old_dashboard():
    return render_template("dashboard_neon.html")

@app.route("/oldest_dashboard")
def oldest_dashboard():
    return render_template("dashboard.html")

@app.route("/dashboard")
def dashboard():
    return render_template("shader_ui_dashboard.html")


@app.route("/api/uptime")
def api_uptime():
    uptime = round(time.time() - start_time, 2)
    return jsonify({"uptime_seconds": uptime})

@app.route("/api/cpu")
def api_cpu():
    cpu_use = psutil.cpu_percent(interval=0.3)
    return jsonify({"cpu_percent": cpu_use})

@app.route("/api/test")
def api_test():
    return jsonify({"status": "ok", "message": "API çalışıyor :) "})

@app.route("/api/mini_log")
def api_log():
    return jsonify({
        "recent": [
            "Seed converter çağırıldı",
            "Dashboard yenilendi",
            "API ping test başarılı"
        ]
    })

@app.route("/api/ping")
def api_ping():
    return jsonify({"status": "online", "latency_ms": round(random.uniform(10, 40), 2)})



@app.errorhandler(404)
def page_not_found(e):
    path = request.path
    reason = ai_why_died(path)

    return render_template(
        "error.html",
        path=path,
        ai_reason=reason
    ), 404


def ai_why_died(path):
    reasons = [
        f"You tried to access {path}, but it was never generated in this world.",
        f"The page {path} fell into the void.",
        f"{path} was removed by the server admin.",
        f"A creeper exploded your URL: {path}.",
        f"The route {path} does not exist in this dimension."
    ]
    return random.choice(reasons)

# ------------------------
#   RUN
# ------------------------

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
