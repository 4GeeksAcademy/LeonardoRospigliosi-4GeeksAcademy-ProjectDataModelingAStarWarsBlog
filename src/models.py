from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table, Column, DateTime,Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from eralchemy2 import render_er

# Initialize Flask-SQLAlchemy 2.0
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    #id = Column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    #username = Column(String(40), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(db.String(40), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(db.String(200), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    created: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    #favorites = relationship('Favorite', backref='user', lazy=True)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")

class Planet(db.Model):
    __tablename__ = 'planet'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    diameter: Mapped[str] = mapped_column(db.String(100), nullable=False)
    rotation_period: Mapped[str] = mapped_column(db.String(100), nullable=False)
    orbital_period: Mapped[str] = mapped_column(db.String(100), nullable=False)
    gravity: Mapped[str] = mapped_column(db.String(100), nullable=False)
    population: Mapped[str] = mapped_column(db.String(100), nullable=False)
    climate: Mapped[str] = mapped_column(db.String(100), nullable=False)
    terrain: Mapped[str] = mapped_column(db.String(100), nullable=False)
    surface_water: Mapped[str] = mapped_column(db.String(100), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    model: Mapped[str] = mapped_column(db.String(100), nullable=False)
    vehicle_class: Mapped[str] = mapped_column(db.String(100), nullable=False)
    manufacturer: Mapped[str] = mapped_column(db.String(100), nullable=False)
    length: Mapped[str] = mapped_column(db.String(100), nullable=False)
    cost_in_credits: Mapped[str] = mapped_column(db.String(100), nullable=False)
    crew: Mapped[str] = mapped_column(db.String(100), nullable=False)
    max_atmosphering_speed: Mapped[str] = mapped_column(db.String(100), nullable=False)
    cargo_capacity: Mapped[str] = mapped_column(db.String(100), nullable=False)
    consumables: Mapped[str] = mapped_column(db.String(100), nullable=False)
    url: Mapped[str] = mapped_column(db.String(200), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="vehicle")

class People(db.Model):
    __tablename__ = 'people'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    birth_year: Mapped[str] = mapped_column(db.String(100), nullable=False)
    eye_color: Mapped[str] = mapped_column(db.String(100), nullable=False)
    gender: Mapped[str] = mapped_column(db.String(100), nullable=False)
    hair_color: Mapped[str] = mapped_column(db.String(100), nullable=False)
    height: Mapped[str] = mapped_column(db.String(20), nullable=False)
    mass: Mapped[str] = mapped_column(db.String(40), nullable=False)
    skin_color: Mapped[str] = mapped_column(db.String(20), nullable=False)
    homeworld: Mapped[str] = mapped_column(db.String(40), nullable=False)
    url: Mapped[str] = mapped_column(db.String(100), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="people")

class Favorite(db.Model):
    __tablename__ = 'favorite'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    people_id = Column(Integer, ForeignKey('people.id'), nullable=True)
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'), nullable=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    people: Mapped["People | None"] = relationship(back_populates="favorites")
    vehicle: Mapped["Vehicle | None"] = relationship(back_populates="favorites")
    planet: Mapped["Planet | None"] = relationship(back_populates="favorites")

# Generate a diagram for the database schema
render_er(db.Model, 'diagram.png')