import json
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

POSTS_FILE = Path(__file__).parent / "posts.json"


def load_posts():
    """Blogbeiträge aus der JSON-Datei laden."""
    with open(POSTS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_posts(posts):
    """Blogbeiträge in die JSON-Datei schreiben."""
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)


def next_id(posts):
    """Nächste eindeutige ID ermitteln."""
    if not posts:
        return 1
    return max(post["id"] for post in posts) + 1


@app.route("/")
def index():
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        blog_posts = load_posts()
        new_post = {
            "id": next_id(blog_posts),
            "author": author,
            "title": title,
            "content": content,
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for("index"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)