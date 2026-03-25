"""seed.py – Run once: py seed.py"""
from app import app, db, User, Item
from werkzeug.security import generate_password_hash
import datetime

with app.app_context():
    db.create_all()

    # Create real user for demo
    demo = User.query.filter_by(email='rahul@lostandfound.in').first()
    if not demo:
        demo = User(name='Rahul Sharma', email='rahul@lostandfound.in',
                    password_hash=generate_password_hash('password123'))
        db.session.add(demo)
        db.session.commit()

    samples = [
        dict(item_type='lost', category='Wallet/Purse', title='Black Leather Wallet',
             description='Bifold black leather wallet. Contains Aadhaar card, debit card, and about ₹500 cash.',
             location='Main Building Entrance, near security desk',
             incident_date='2026-03-24', incident_time='14:30',
             contact_name='Rahul Sharma', contact_phone='+91 98765 43210',
             contact_email='rahul@lostandfound.in', image='lost_wallet.png',
             status='open'),

        dict(item_type='lost', category='Keys', title='House & Car Keys (Red Keychain)',
             description='Honda car key + 2 house keys on a red metal keychain with a small flashlight.',
             location='Block B – 2nd Floor Staircase',
             incident_date='2026-03-23', incident_time='09:15',
             contact_name='Rahul Sharma', contact_phone='+91 98765 43210',
             contact_email='rahul@lostandfound.in', image='lost_keys.png',
             status='resolved'), # Marked as solved

        dict(item_type='found', category='Bag/Backpack', title='Dark Blue Nike Backpack',
             description='Nike backpack, slightly worn. Contains a laptop (Dell), charger, and some notebooks. Handed to library helpdesk.',
             location='Central Library – Ground Floor, bench near window',
             incident_date='2026-03-25', incident_time='11:00',
             contact_name='Priya Patel', contact_phone='+91 91234 56789',
             contact_email='priya.patel@example.in', image='lost_backpack.png',
             status='open'),

        dict(item_type='found', category='Electronics', title='iPhone with Cracked Corner',
             description='Black iPhone, cracked at bottom-left corner, passcode locked. Screen is intact otherwise.',
             location='Campus Cafeteria – Table near window side',
             incident_date='2026-03-25', incident_time='12:45',
             contact_name='Amit Singh', contact_phone='+91 99887 76655',
             contact_email='amit.singh@example.in', image='found_phone.png',
             status='open'),

        dict(item_type='lost', category='Documents', title='Blue Document Folder',
             description='Contains important marksheets and certificates. Has a white label with "Sneha Gupta" written on it.',
             location='Admin Block Waiting Area',
             incident_date='2026-03-26', incident_time='10:30',
             contact_name='Sneha Gupta', contact_phone='+91 88776 65544',
             contact_email='sneha.gupta@example.in', image='',
             status='resolved'), # Marked as solved
    ]

    for s in samples:
        if not Item.query.filter_by(title=s['title'], user_id=demo.id).first():
            db.session.add(Item(**s, user_id=demo.id))

    db.session.commit()
    print("✅ Seeded! Login → rahul@lostandfound.in / password123")
