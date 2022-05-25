from flask import Flask, render_template, request
from model import get_top5

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # get user from the html form
    username = request.form['username']
    top5_list=get_top5(username)
    if len(top5_list)>0:
        #top5=' <br>'.join(top5_list)
        #return top5_list
        return render_template("index.html", list_rec=top5_list)
    else:
        #print('User not found!!!')
        #return('User not found!!!')
        return render_template("index.html", placeholder_text="User not found!!!")

if __name__ == '__main__':
    app.run()