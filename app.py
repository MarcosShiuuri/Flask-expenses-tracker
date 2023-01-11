from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense.db'
db = SQLAlchemy(app)
db.init_app(app)

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    local = db.Column(db.String(200), nullable=False)
    payment = db.Column(db.String(200), nullable=False)
    value = db.Column(db.Float(200), nullable=False)
    def __repr__(self):
        return '<Expenses %r>' % self.id
with app.app_context():
    db.create_all()

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        exp_name = request.form.get('exp_name')
        exp_local = request.form.get('exp_local')
        exp_pay = request.form.get('exp_payment')
        exp_value = request.form.get('exp_value')
        new_expense = Expenses(name=exp_name, local=exp_local, payment=exp_pay, value=exp_value)
        try:
            db.session.add(new_expense)
            db.session.commit()
            return redirect('/')
        except:
            error = 'Expense not added, please try again.'
            return render_template('error.html', error=error)
    else:
        current_expenses = Expenses.query.order_by(Expenses.id).all()
        total = 0
        for x in current_expenses:
            total += x.value
        return render_template('index.html', exp=current_expenses, total=float(round(total,2)))

@app.route('/delete/<int:id>')
def delete(id):
    expense_delete = Expenses.query.get_or_404(id)
    try:
        db.session.delete(expense_delete)
        db.session.commit()
        return redirect('/')
    except:
        error = 'Could not delete, please try again.'
        return render_template('error.html', error=error)

if __name__ == '__main__':
    app.run()