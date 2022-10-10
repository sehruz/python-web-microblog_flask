from flask import Flask, render_template, request
from datetime import datetime
from pymongo import MongoClient

app=Flask(__name__)
client=MongoClient('mongodb+srv://sehruz787:Boeing787320@microblog-app.3ef2ggs.mongodb.net/test')
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


if __name__ == '__main__':
    app.run(debug=True)