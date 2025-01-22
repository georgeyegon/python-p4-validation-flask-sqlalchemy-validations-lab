from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError
import re

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if not name:  # Explicitly check for an empty or missing name
            raise ValueError("Name is required.")
        if Author.query.filter_by(name=name).first():
            raise ValueError("Author name must be unique.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('posts', lazy=True))

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary must be no longer than 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be either Fiction or Non-Fiction.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError("Post title must be clickbait-y and contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
        return title
