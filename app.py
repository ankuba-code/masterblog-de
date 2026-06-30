# Standardbibliothek: JSON lesen/schreiben
import json
# Pfad zur posts.json relativ zur aktuellen Datei
from pathlib import Path

# Flask-Hilfsfunktionen für Web-App, Templates, Formulare und Weiterleitungen
from flask import Flask, render_template, request, redirect, url_for

# Flask-Anwendung initialisieren
app = Flask(__name__)

# Pfad zur JSON-Datei im gleichen Ordner wie app.py
POSTS_FILE = Path(__file__).parent / "posts.json"


def load_posts():
    """Blogbeiträge aus der JSON-Datei laden."""
    with open(POSTS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_posts(posts):
    """Blogbeiträge in die JSON-Datei schreiben."""
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        # indent=4: lesbare Formatierung; ensure_ascii=False: Umlaute bleiben erhalten
        json.dump(posts, f, indent=4, ensure_ascii=False)


def next_id(posts):
    """Nächste eindeutige ID ermitteln."""
    if not posts:
        return 1  # Erster Beitrag bekommt ID 1
    return max(post["id"] for post in posts) + 1


def fetch_post_by_id(post_id):
    """Blogbeitrag anhand der ID finden."""
    for post in load_posts():
        if post["id"] == post_id:
            return post
    return None  # Kein Beitrag mit dieser ID gefunden


@app.route("/")
def index():
    """Startseite: alle Blogbeiträge anzeigen."""
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Neuen Blogbeitrag erstellen."""
    if request.method == "POST":
        # Formulardaten aus dem POST-Request lesen
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        blog_posts = load_posts()
        new_post = {
            "id": next_id(blog_posts),
            "author": author,
            "title": title,
            "content": content,
            "likes": 0,  # Neuer Beitrag startet mit 0 Likes
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for("index"))  # Zurück zur Startseite

    # GET: leeres Formular anzeigen
    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    """Blogbeitrag anhand der ID löschen."""
    blog_posts = load_posts()
    # Nur Beiträge behalten, deren ID nicht der gelöschten entspricht
    blog_posts = [post for post in blog_posts if post["id"] != post_id]
    save_posts(blog_posts)
    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """Bestehenden Blogbeitrag bearbeiten."""
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404  # HTTP-Fehler, wenn ID nicht existiert

    if request.method == "POST":
        blog_posts = load_posts()
        for p in blog_posts:
            if p["id"] == post_id:
                # Nur Textfelder aktualisieren; likes bleibt unverändert
                p["author"] = request.form.get("author")
                p["title"] = request.form.get("title")
                p["content"] = request.form.get("content")
                break
        save_posts(blog_posts)
        return redirect(url_for("index"))

    # GET: Formular mit bestehenden Daten anzeigen
    return render_template("update.html", post=post)


@app.route("/like/<int:post_id>")
def like(post_id):
    """Like-Zähler eines Beitrags um 1 erhöhen."""
    blog_posts = load_posts()
    for post in blog_posts:
        if post["id"] == post_id:
            # get("likes", 0): Fallback für alte Einträge ohne likes-Feld
            post["likes"] = post.get("likes", 0) + 1
            break
    save_posts(blog_posts)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Entwicklungsserver starten
    app.run(host="0.0.0.0", port=5000, debug=True)