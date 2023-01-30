from flask import Flask
from public import public
from agent import agent
from admin import admin


app=Flask(__name__)
app.secret_key="prayulla"
app.register_blueprint(admin,url_prefix="/admin")
app.register_blueprint(agent,url_prefix="/agent")
app.register_blueprint(public)


app.run(debug=True,port=5043,host="0.0.0.0")