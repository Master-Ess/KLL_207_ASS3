from flask import *
from datetime import datetime
import re

app = Flask(__name__,template_folder='../KLL_207_ASS3')

 
# currently no operation - now there is 

data = str(5)

@app.route("/")




def index():
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)   