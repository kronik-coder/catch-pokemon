from sqlalchemy.orm import backref
from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

caught_pokemon = db.Table(
    'caught_pokemon',
    db.Column('pokemon_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(200), unique=True, index=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User',
                    secondary=followers,
                    primaryjoin=(followers.c.follower_id == id),
                    secondaryjoin=(followers.c.followed_id == id),
                    backref=db.backref('followers', lazy='dynamic'),
                    lazy='dynamic'
                    )
    pokemons = db.relationship('CatchPokemon', backref='trainer', lazy='dynamic')
    caught = db.relationship('User',
                    secondary = caught_pokemon,
                    primaryjoin = (caught_pokemon.c.pokemon_id == id),
                    backref = db.backref('caught_pokemon', lazy='dynamic'),
                    lazy = 'dynamic'
                    )

    # check if pokemon has already been caught
    def is_caught(self, pokemon):
        return self.caught.filter(caught_pokemon.c.pokemon_id == pokemon.id).count > 0

    # catch a pokemon
    def catch(self, pokemon):
        if not self.is_caught(pokemon):
            self.caught.append(pokemon)
            db.session.commit()
    ####
    #### 
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()
        
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()
        
    def all_follower_posts(self):
        followed = Post.query.join(followers, Post.user_id == followers.c.followed_id).filter(followers.c.follower_id == self.id)
        self_posts = Post.query.filter_by(user_id = self.id)

        all_posts = followed.union(self_posts).order_by(Post.date_posted.desc())

        return all_posts

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def save(self):
        db.session.add(self)
        db.session.commit()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=dt.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<id: {self.id} | Post: {self.body[:15]}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, new_body):
        self.body = new_body
        self.save()

class CatchPokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def addPokemon(self):
        pass

