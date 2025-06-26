from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from .models import nob_db
from .models import User, Contacts, Messages
from .NOB_AI import NOB, Dennis
from sqlalchemy import or_, and_
# The routes.py define the routes for the different pages 
routes = Blueprint('routes',__name__)

@routes.route('/home', methods=["GET", "POST"])
@login_required
def home():
    
    contacts = Contacts.query.filter_by(user_id=current_user.id).all()
    print(contacts)
    contact_yourself_exists = Contacts.query.filter_by(user_id=current_user.id, contact_id=current_user.id).first()  #check if user's self exists as a contacts
    
    nob_ai = User.query.filter_by(username='N.O.B').first()   #get user N.O.B
    dennis_ai = User.query.filter_by(username='Dennis').first()  #get user Dennis
    contact_nob_exists = None
    if nob_ai:
        contact_nob_exists = Contacts.query.filter_by(user_id=current_user.id, contact_id=nob_ai.id).first() #check if N.O.B exists as a contacts
    contact_dennis_exists = None
    if dennis_ai:
        contact_dennis_exists = Contacts.query.filter_by(user_id=current_user.id, contact_id=dennis_ai.id).first() #check if Dennis exists as a contacts
    if not contact_yourself_exists or not contact_nob_exists or not contact_dennis_exists:
        try:
            if not contact_yourself_exists:
                contact_yourself= Contacts(user_id=current_user.id, contact_id=current_user.id, contact_name=current_user.username+'(Yourself)', contact_number=current_user.user_number, contact_image_path='static/images/defaultimg.jpg') #add user's self as a contact
                nob_db.session.add(contact_yourself)
            if nob_ai and not contact_nob_exists:
                contact_nob = Contacts(user_id=current_user.id, contact_id=nob_ai.id,contact_name='N.O.B', contact_number='0000001',contact_image_path='static/images/defaultimg.jpg')#add N.O.B as a contact
                nob_db.session.add(contact_nob)
            if dennis_ai and not contact_dennis_exists:
                contact_dennis = Contacts(user_id=current_user.id,contact_id=dennis_ai.id, contact_name='Dennis', contact_number='0000002', contact_image_path='static/images/defaultimg.jpg') #add Dennis as a contact
                nob_db.session.add(contact_dennis)
           
            
            
            nob_db.session.commit()
            return redirect('/home')
        except Exception as e:
            nob_db.session.rollback() # go back to previous state before commit
            #print(e)
            return "Error: 101"
    contacts = Contacts.query.filter_by(user_id=current_user.id).all()  
    return render_template('home.html', contacts=contacts, user=current_user)
    
@routes.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
@routes.route('/chat/<int:id>', methods=['GET', 'POST'])
@login_required
def chat(id):
    contacts = Contacts.query.filter_by(user_id=current_user.id).all()
    user_contacts_entry = Contacts.query.filter_by(id=id, user_id=current_user.id).first_or_404()  # get a table consisting of the contacts associated with a user from the Contacts table
    user_to_chatwith = User.query.get_or_404(user_contacts_entry.contact_id)                     #  get the contact/user to chat with from the users table
    messages = Messages.query.filter(
     or_(
         and_(Messages.user_id == current_user.id, Messages.contact_id == user_to_chatwith.id),
         and_(Messages.user_id == user_to_chatwith.id, Messages.contact_id == current_user.id)
     )).order_by(Messages.time).all()                                                                       #Get user and contacts messages
    print(messages)
    if request.method== 'POST':
        user_message=request.form.get('user_message')
        
        chat_messages = Messages(user_id= current_user.id, contact_id=user_to_chatwith.id, message=user_message)
        ai_message = None
        if user_contacts_entry.contact_name== 'N.O.B':
            try:
                contact_nob_message = NOB(user_message)
            except:
                return redirect(url_for('routes.chat', id=id))
            ai_message = Messages(user_id= user_to_chatwith.id, contact_id=current_user.id, message=contact_nob_message)
            
        if user_contacts_entry.contact_name== 'Dennis':
            try:
                contact_dennis_message = Dennis(user_message)
            except:
                return redirect(url_for('routes.chat', id=id))
            ai_message = Messages(user_id= user_to_chatwith.id, contact_id=current_user.id, message=contact_dennis_message)
           
        try:
            nob_db.session.add(chat_messages)
            if ai_message:
                nob_db.session.add(ai_message)
            nob_db.session.commit()
            print("Saved message:", chat_messages.user_id)
            print("Saved message:", current_user.id)
            #messages = Messages.query.filter((Messages.user_id==current_user.id and Messages.contact_id==contact.id) | (Messages.user_id==contact.id and Messages.contact_id==current_user.id)).all()
            return redirect(url_for('routes.chat', id=id))
        except Exception as e:
            print(e)
            return "Error 201: Failed to send message"
    return render_template('chat.html', contacts=contacts, user=current_user, messages=messages,contact=user_contacts_entry, user_to_chatwith=user_to_chatwith)

    # return render_template('chat.html', contacts=contacts, user=current_user, messages=messages, reverse_messages=reverse_messages, contact=contact)

@routes.route('/search', methods=['GET'])
def search():
    users_to_find = request.args.get('search')
    print(users_to_find)
    users_found = User.query.filter(User.username.ilike(f"%{users_to_find}%")| User.user_number.ilike(f"%{users_to_find}%")).all()
    return render_template('users.html', users=users_found, users_to_find=users_to_find)

@routes.route('/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add_contact(id):
    contact_found = User.query.get_or_404(id) # get a user if they exist
    contact = Contacts(user_id=current_user.id,contact_id=contact_found.id, contact_name=contact_found.username, contact_number=contact_found.user_number, contact_image_path='static/images/defaultimg.jpg')
    # contact = Contacts(user_id=current_user.id,contact_name=contact_found.username, contact_number=contact_found.user_number, contact_image_path='static/images/defaultimg.jpg')
    reverse_contact = Contacts(user_id=contact_found.id, contact_id=current_user.id, contact_name=current_user.username, contact_number=current_user.user_number, contact_image_path='static/images/defaultimg.jpg')
    #reverse_contact = Contacts(user_id=contact_found.id,contact_name=current_user.username, contact_number=current_user.user_number, contact_image_path='static/images/defaultimg.jpg')

    if contact_found.username == current_user.username:
        return redirect('/home')
    contact_exists = Contacts.query.filter_by(user_id=current_user.id, contact_name=contact_found.username).first()
    reverse_contact_exists = Contacts.query.filter_by(user_id=contact_found.id, contact_name=current_user.username).first()
    print(contact_exists)
    if contact_exists or reverse_contact_exists:
        return redirect('/home')
    
    try:
        nob_db.session.add(contact)
        nob_db.session.add(reverse_contact)
        nob_db.session.commit()
        print("successful")
        return redirect('/home')
    except Exception as e:
        print(e)
        return "Error 311: Failed to add contact"
    return redirect('/home')

