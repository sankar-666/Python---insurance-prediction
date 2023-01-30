from flask import *
from database import *


agent=Blueprint('agent',__name__)

@agent.route('/agenthome',methods=['get','post'])
def agenthome():
    return render_template('agenthome.html')