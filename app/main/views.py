from . import main
from datetime import datetime
from ..models import User,Comment,Intcom
from .forms import CommentForm,IntFormL
from flask_login import login_required, current_user
from ..requests import food2fork
from flask import render_template,request,redirect,url_for
import requests
import json


# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    return render_template("index.html")

@main.route('/options',methods = ['GET', 'POST'])
@login_required
def options():

    intial_form = IntFormL()

    if intial_form.validate_on_submit():

        comm = intial_form.comm.data
        new_incomm = Intcom(feed_content=comm, user = current_user)
        new_incomm.save_comm()

        return redirect(url_for('main.options'))

    search_food = request.args.get('food_query')

    if search_food:
        return redirect(url_for('main.test', search_food = search_food))
    else:

        all_int_comms = Intcom.get_all_comms()
        random = requests.get('https://www.food2fork.com/api/search?key=20f622f65686631876726fade51e81c7&q=chicken').json()
        return render_template("allfoods.html", intial_form = intial_form, allcom = all_int_comms,random = random)

@main.route('/reply/<int:id>',methods = ['GET','POST'])
def pitch(id):

    my_pitch = Intcom.query.get(id)
    comment_form = CommentForm()

    if id is None:
        abort(404)

    if comment_form.validate_on_submit():
        comment_data = comment_form.comment.data
        new_comment = Comment(comment_content = comment_data, pitch_id = id, user = current_user)
        new_comment.save_comment()

        return redirect(url_for('main.pitch',id=id))

    all_comments = Comment.get_comments(id)

    title = 'Comment Section'
    return render_template('comm.html',pitch = my_pitch, comment_form = comment_form, comments = all_comments, title = title)

@main.route('/search/<search_food>')
def test(search_food):
    '''
    View function to display the search results
    '''
    random = requests.get('https://www.food2fork.com/api/search?key=20f622f65686631876726fade51e81c7&q='+search_food).json()
    return render_template('test.html',random = random)
