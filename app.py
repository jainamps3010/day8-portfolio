from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# ===========================
# DATABASE MODEL
# ===========================
class Message(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(100), nullable=False)
    email     = db.Column(db.String(100), nullable=False)
    subject   = db.Column(db.String(200), nullable=False)
    message   = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.String(50), default=datetime.now().strftime("%d %b %Y, %I:%M %p"))

    def __repr__(self):
        return f"Message from {self.name}"


with app.app_context():
    db.create_all()
    print("Database ready!")


# ===========================
# ROUTES
# ===========================

# HOME PAGE
@app.route("/")
def index():
    # Your projects data
    projects = [
        {
            "title": "Student Database App",
            "description": "A full CRUD web app built with Flask and SQLite. Allows adding, editing and deleting student records.",
            "tech": ["Python", "Flask", "SQLite", "HTML", "CSS"],
            "link": "https://github.com/jainamps3010/day7-database"
        },
        {
            "title": "JavaScript Projects",
            "description": "5 interactive JavaScript projects — Greeting Machine, Calculator, To Do List, Color Changer and Countdown Timer.",
            "tech": ["HTML", "CSS", "JavaScript"],
            "link": "https://github.com/jainamps3010/day5-javascript"
        },
        {
            "title": "Portfolio Website",
            "description": "This portfolio itself! Built with Flask, SQLAlchemy and a contact form that saves messages to database.",
            "tech": ["Python", "Flask", "SQLite", "HTML", "CSS", "JS"],
            "link": "https://github.com/jainamps3010/day8-portfolio"
        }
    ]

    skills = [
        {"name": "Python",     "emoji": "🐍", "level": "90%"},
        {"name": "Flask",      "emoji": "⚗️", "level": "75%"},
        {"name": "HTML",       "emoji": "🌐", "level": "85%"},
        {"name": "CSS",        "emoji": "🎨", "level": "80%"},
        {"name": "JavaScript", "emoji": "⚡", "level": "70%"},
        {"name": "SQLite",     "emoji": "💾", "level": "75%"},
        {"name": "Git",        "emoji": "🔧", "level": "80%"},
    ]

    return render_template("index.html", projects=projects, skills=skills)


# CONTACT FORM — Save message to database
@app.route("/contact", methods=["POST"])
def contact():
    name    = request.form["name"]
    email   = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]

    new_message = Message(
        name=name,
        email=email,
        subject=subject,
        message=message
    )

    db.session.add(new_message)
    db.session.commit()

    # Redirect back to homepage with success flag
    return redirect(url_for("index") + "#contact-success")


# ADMIN PAGE — View all messages
@app.route("/admin")
def admin():
    all_messages = Message.query.order_by(Message.id.desc()).all()
    total = Message.query.count()
    return render_template("admin.html",
                           messages=all_messages,
                           total=total)


# DELETE MESSAGE from admin
@app.route("/delete-message/<int:id>")
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)