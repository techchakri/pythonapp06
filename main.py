### Integrate HTML With Flask
### HTTP verb GET And POST

### Jinja2 template engine

'''
{% ... %} conditions, for statements
{{     }} expressions to print output
{#....#}  this is for comments
'''

from flask import Flask, redirect , url_for , render_template , request
import os
import time
# from flask_healthz import Healthz

app = Flask(__name__)
# Healthz(app, no_log=True)
'''
  oxygenLevels: "90"
  quarantine: "13"
  liters: "6"
  temparatureLevels: "99 - 101"
'''

@app.route('/')
def welcome():
    return render_template('index.html',oxygenLevels=os.environ.get("guidelines.oxygenLevels","90"),quarantine=os.environ.get("guidelines.quarantine",default="7days"),liters=os.environ.get("guidelines.liters",default="6"),temperatureLevels=os.environ.get("guidelines.temperatureLevels",default="90-99"))

@app.route('/success/<int:score>')
def success(score):
    res=""
    if score >= 50:
        res="PASS"
    else:
        res="FAIL"
    exp = {'score':score,'res':res}
    return render_template('result.html',result=exp)

@app.route('/fail/<int:score>')
def fail(score):
    return render_template('result.html',score=score)

### Result checker
@app.route('/results/<int:marks>')
def results(marks):
    result=""
    if marks<50:
        result='fail'
    else:
        result='success'
    return redirect(url_for(result,score=marks))

### Result checker submit html page
@app.route("/submit",methods=['POST','GET'])
def submit():
    total_score=0
    if request.method =='POST':
        science      = float(request.form['science'])
        maths        = float(request.form['maths'])
        c            = float(request.form['c'])
        data_science = float(request.form['datascience'])
        total_score=(science+maths+c+data_science)/4
    return redirect(url_for("success",score=total_score))

@app.route('/liveness')
def healthx():
  time.sleep(2);
  return "OK"
  
@app.route('/readiness')
def healthz():
  time.sleep(20);
  return "OK"



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=8080);