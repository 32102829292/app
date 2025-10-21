from flask import Flask, render_template, request, redirect, flash
from models import db, Medicine
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    medicines = Medicine.query.all()
    return render_template('index.html', medicines=medicines)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        med = Medicine(
            name=request.form['name'],
            type=request.form['type'],
            stock=request.form['stock']
        )
        db.session.add(med)
        db.session.commit()
        flash('Medicine added successfully!')
        return redirect('/')
    return render_template('med/add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    med = Medicine.query.get_or_404(id)
    if request.method == 'POST':
        med.name = request.form['name']
        med.type = request.form['type']
        med.stock = request.form['stock']
        db.session.commit()
        flash('Medicine updated successfully!')
        return redirect('/')
    return render_template('med/edit.html', med=med)

@app.route('/delete/<int:id>')
def delete(id):
    med = Medicine.query.get_or_404(id)
    db.session.delete(med)
    db.session.commit()
    flash('Medicine deleted successfully!')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
