from flask import Flask, render_template, request, redirect, url_for
from models import db, ErrorLog
from error_engine import analyze_error
from sqlalchemy import func
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'errors.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    latest_error = None
    if request.method == 'POST':
        error_text = request.form.get('error_text', '')
        if error_text:
            response = analyze_error(error_text)
            new_log = ErrorLog(
                error_text=error_text,
                category=response['category'],
                confidence=response['confidence'],
                explanation=response['explanation'],
                root_cause=response['root_cause'],
                fix=response['fix'],
                example_incorrect=response['example']['incorrect'],
                example_correct=response['example']['correct']
            )
            db.session.add(new_log)
            db.session.commit()
            return redirect(url_for('index', id=new_log.id))
            
    log_id = request.args.get('id')
    if log_id:
        latest_error = ErrorLog.query.get(log_id)
    else:
        latest_error = ErrorLog.query.order_by(ErrorLog.created_at.desc()).first()
        
    recent_errors = ErrorLog.query.order_by(ErrorLog.created_at.desc()).limit(5).all()
    return render_template('index.html', latest_error=latest_error, recent_errors=recent_errors)

@app.route('/history')
def history():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    logs_query = ErrorLog.query
    if query:
        logs_query = logs_query.filter(ErrorLog.error_text.ilike(f'%{query}%') | ErrorLog.explanation.ilike(f'%{query}%'))
    if category:
        logs_query = logs_query.filter(ErrorLog.category == category)
        
    logs = logs_query.order_by(ErrorLog.created_at.desc()).all()
    
    # Analytics Data Processing natively via DB groupings
    total_errors = ErrorLog.query.count()
    category_counts = db.session.query(ErrorLog.category, func.count(ErrorLog.category)).group_by(ErrorLog.category).all()
    most_common_category = max(category_counts, key=lambda x: x[1])[0] if category_counts else "N/A"
    
    # Map valid filtering variables
    categories = [c[0] for c in db.session.query(ErrorLog.category).distinct().all() if c[0]]
    
    return render_template('history.html', 
                         logs=logs, 
                         query=query, 
                         selected_category=category, 
                         categories=categories,
                         total_errors=total_errors,
                         most_common_category=most_common_category,
                         category_distribution=category_counts)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    log = ErrorLog.query.get_or_404(id)
    if request.method == 'POST':
        new_error_text = request.form.get('error_text', '')
        if new_error_text:
            response = analyze_error(new_error_text)
            log.error_text = new_error_text
            log.category = response['category']
            log.confidence = response['confidence']
            log.explanation = response['explanation']
            log.root_cause = response['root_cause']
            log.fix = response['fix']
            log.example_incorrect = response['example']['incorrect']
            log.example_correct = response['example']['correct']
            db.session.commit()
            return redirect(url_for('history'))
    return render_template('edit.html', log=log)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    log = ErrorLog.query.get_or_404(id)
    db.session.delete(log)
    db.session.commit()
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
