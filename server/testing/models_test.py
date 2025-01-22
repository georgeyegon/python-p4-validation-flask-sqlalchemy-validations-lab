import pytest
from models import db, Author
from faker import Faker
from app import app  # Import your Flask app here

def test_requires_ten_digit_phone_number():
    '''requires each phone number to be exactly ten digits.'''

    with app.app_context():  # Make sure app context is used
        # valid phone number
        author1 = Author(name=Faker().name(), phone_number='1231144321')
        db.session.add(author1)
        db.session.commit()

        # invalid phone number (less than 10 digits)
        with pytest.raises(ValueError, match="Phone number must be exactly 10 digits."):
            author2 = Author(name=Faker().name(), phone_number='12345')
            db.session.add(author2)
            db.session.commit()

        # invalid phone number (more than 10 digits)
        with pytest.raises(ValueError, match="Phone number must be exactly 10 digits."):
            author3 = Author(name=Faker().name(), phone_number='123456789012')
            db.session.add(author3)
            db.session.commit()

        # invalid phone number (non-numeric)
        with pytest.raises(ValueError, match="Phone number must be exactly 10 digits."):
            author4 = Author(name=Faker().name(), phone_number='1234ABCDE9')
            db.session.add(author4)
            db.session.commit()
