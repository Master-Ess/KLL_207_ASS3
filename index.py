from flask import *
from datetime import datetime
import re
from time import *
from datetime import *

app = Flask(__name__,template_folder='../KLL_207_ASS3')

 
# currently no operation - now there is 

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
data = str("Current Time =" + current_time)

@app.route("/")




def index():
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)   