import os
from threading import Lock
from app import app, db, sio
from app.models import Card, Player
from app.forms import AddChipsForm
from flask import Flask, render_template, session, request, copy_current_request_context, url_for
from flask_socketio import send, emit, join_room, leave_room, close_room, rooms, disconnect
import random

thread = None
thread_lock = Lock()

def background_thread():
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('message', {'data': 'Server generated event', 'count': count})

def deal_cards(num_cards):
    cards = []
    for i in range(num_cards):
        card_id = random.randint(0,51)
        card = Card.query.filter_by(id=card_id)
        cards.append(card)
    return cards

def determineCardHands():
    pass

@app.route('/')
def index():
    return render_template('index.html', async_mode=sio.async_mode)

@app.route('/poker')
def poker():
    return render_template('poker.html', async_mode=sio.async_mode)

@app.route('/add_chips')
def add_chips():
    form = AddChipsForm()
    if form.validate_on_submit():
        player = Player.query.filter_by(name=form.name.data).first()
        if player is not None:
            player.chips = player.chips + form.chips.data
        db.session.commit()
    return render_template('add_chips.html')

@sio.event
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', 
        {
        'data': f'In rooms {", ".join(rooms())}',
        'count': session['receive_count']
        })

@sio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = sio.start_background_task(background_thread)
    emit('message', {'data': 'Connected', 'count': 0, })

@sio.on('message')
def message(msg):
    print(msg)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('message', {'data': msg['data'], 'count': session['receive_count']}, broadcast=True)

@sio.on('poker_start')
def poker_start():
    pass

@sio.on('set_player_name')
def set_player_name(data):
    player = Player.query.filter_by(name=data['username']).first()
    if player is None:
        player = Player(name=data['username'], chips=0)
        db.session.add(player)
        db.session.commit()
    player_obj = {
        "name": player.name,
        "chips": player.chips
    }
    emit('set_player_name', {
        "id": data['username'],
        "player": player_obj
    })

@sio.on('player_poker_start')
def player_poker_start():
    cards = deal_cards(2)

@app.route('/initial_setup')
def initial_setup():
    cards = Card.query.all()
    for card in cards:
        db.session.delete(card)
    db.session.commit()
    card_values = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'jack': 11,
        'queen': 12,
        'king': 13,
        'ace': 14
    }
    suits = ['spades', 'clubs', 'hearts', 'diamonds']
    for card in card_values.keys():
        for suit in suits:
            new_card = Card(suit=suit, face_value=card, img_path=url_for('static', filename=f'imgs/{card}_{suit}.svg'), value=card_values[card])
            db.session.add(new_card)
    db.session.commit()
    return 'Database updated'

if __name__ == '__main__':
    sio.run(app)