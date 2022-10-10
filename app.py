import os
from flask import Flask, render_template, request
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
def create_app():
    app=Flask(__name__)
    client=MongoClient(os.environ.get('MONGODB_URI'))
    app.db=client.microblog
    entries=[]

    @app.route('/', methods=['GET', 'POST'])
    def home():
        
        if request.method == 'POST':
            entry_content=request.form.get('content')
            entry_time=datetime.today().strftime('%Y-%m-%d')
            if entry_content !="":
                # entries.append((entry_content, entry_time))
                app.db.entries.insert_one({'content': entry_content, 'date': entry_time})
        
        entry_with_date=[(entry['content'], entry['date'],
        datetime.strptime(entry['date'], '%Y-%m-%d').strftime('%b %d')
        ) for entry in app.db.entries.find({})]
        return render_template('home.html', entries=entry_with_date)
    return app
