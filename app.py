from flask import Flask
from flask import request, request-handler, render_template
import Utils
app = Flask(__name__)

#Home page...
#get method returns page to choose your topic
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("index.html")
    #Otherwise we're posting: so lets get the topic and redirect
    topic = request.form['topic']
    #Maybe we need to do some clean up on topic here, aka
    #lowercasing or checking for validity
    topic = Utils.cleanTopic(topic)
    return redirect(url_for('write')) 

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        #return the template (also deal with js?)
        headlines = Utils.getHeadlines(topic) #Maybe make this dynamic instead, requires js though
        return render_template("write.html", headlines=headlines)
    #Otherwise they're posting their essay, so show a submission page for printing?
    submission = request.form['submission']
    return render_template("submit.html", submission=submission)
#Otherwise we are receiving what 
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

