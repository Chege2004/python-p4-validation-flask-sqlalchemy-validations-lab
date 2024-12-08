from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validate 'name'
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError('Name is required')
        
        # Check for uniqueness
        existing_author = Author.query.filter(Author.name == value).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError(f"An author with the name '{value}' already exists.")
        
        return value

    # Validate 'phone_number'
    # Validate 'phone_number'
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if value and len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        if value and not value.isdigit():
            raise ValueError("Phone number must contain only digits.")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError('Title is required.')
        if len(value) > 250:  # Assuming titles should not exceed 250 characters
            raise ValueError('Title must be 250 characters or less.')
        
        # Check for clickbait phrases
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError(f"Title must contain at least one of the following phrases: {', '.join(clickbait_phrases)}.")
        
        return value

    @validates('content')
    def validate_content(self, key, value):
        if value and len(value) < 250:  # Check only if content is provided
            raise ValueError('Content is too short. It must be at least 250 characters.')
        return value
    
    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) > 250:  # Check only if content is provided
            raise ValueError('Summary is too long. It must be at most 250 characters.')
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        if not value:
            raise ValueError('Category is required.')
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be either Fiction or Non-Fiction.')
        return value
    
    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})"
