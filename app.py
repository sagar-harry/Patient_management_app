from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Patient(db.Model):
    PatientId = db.Column(db.Integer, primary_key=True)
    PatientName = db.Column(db.String(300), default="Name")
    Content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>'%self.PatientId

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=="POST":
        record_name = request.form['PatientName']
        record_content = request.form['Content']
        new_patient = Patient(PatientName=record_name, Content=record_content)
        try:
            db.session.add(new_patient)
            db.session.commit()
            return redirect("/")
        except:
            return "Hello world!"
    else:
        records = Patient.query.order_by(Patient.PatientId).all()
        return render_template('index.html', records=records)

@app.route("/Delete/<int:id>", methods=["POST", "GET"])
def delete(id):
    PatientToBeDeleted = Patient.query.get_or_404(id)
    try:
        db.session.delete(PatientToBeDeleted)
        db.session.commit()
        return redirect("/")
    except:
        return "Hello world!"

@app.route("/Update/<int:id>", methods=["POST", "GET"])
def update(id):
    PatientToBeUpdated = Patient.query.get_or_404(id)

    if request.method == "POST":
        PatientToBeUpdated.PatientName = request.form["PatientName"]
        PatientToBeUpdated.Content = request.form["Content"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Hello world!"
    else:
        return render_template('update.html', patient=PatientToBeUpdated)


if __name__=="__main__":
    app.run(debug=True)