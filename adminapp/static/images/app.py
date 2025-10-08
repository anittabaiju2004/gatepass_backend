# from flask import Flask, render_template, request, redirect, session
# import joblib
# from material_budget import get_material_budget

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# #Load model and encoder
# plan_model = joblib.load('models/plan_model.pkl')
# plan_encoder = joblib.load('models/plan_encoder.pkl')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/search_plans', methods=['POST'])
# def search_plans():
#     sqft = int(request.form['squarefeet'])
#     cents = int(request.form['cents'])
#     budget = int(request.form['budget'])

#     session['inputs'] = {'squarefeet': sqft, 'cents': cents, 'budget': budget}

#     prediction = plan_model.predict([[sqft, cents, budget]])
#     predicted_plan = plan_encoder.inverse_transform(prediction)[0]

#     all_plans = list(plan_encoder.classes_)
#     suggestions = [predicted_plan] + [p for p in all_plans if p != predicted_plan][:2]

#     return render_template('plan_selection.html', suggestions=suggestions)

# @app.route('/material_budget', methods=['POST'])
# def material_budget():
#     selected_plan = request.form['selected_plan']
#     items, total = get_material_budget(selected_plan)
#     return render_template('material_result.html', plan=selected_plan, items=items, total_cost=total)

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, session
import joblib
from material_budget import get_material_budget

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load model and encoder
plan_model = joblib.load('models/plan_model1.pkl')
plan_encoder = joblib.load('models/plan_encoder1.pkl')

def get_category_id(sqft, budget):
    """
    Simple logic to assign CategoryID based on sqft and budget
    Adjust according to your dataset
    """
    if sqft <= 1200 and budget <= 1800000:
        return 1  # 2BHK
    elif sqft <= 1800 and budget <= 2400000:
        return 2  # 3BHK
    else:
        return 3  # Duplex

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_plans', methods=['POST'])
def search_plans():
    # Get cents and budget from user input
    cents = float(request.form['cents'])
    budget = int(request.form['budget'])

    # Calculate square feet from cents
    sqft = round(cents * 435.6, 2)

    # Determine CategoryID
    category_id = get_category_id(sqft, budget)

    session['inputs'] = {
        'cents': cents,
        'budget': budget,
        'squarefeet': sqft,
        'category_id': category_id
    }

    # Predict plan using 4 features: sqft, cents, budget, category_id
    prediction = plan_model.predict([[sqft, cents, budget, category_id]])
    predicted_plan = plan_encoder.inverse_transform(prediction)[0]

    all_plans = list(plan_encoder.classes_)
    suggestions = [predicted_plan] + [p for p in all_plans if p != predicted_plan][:2]

    return render_template('plan_selection.html', suggestions=suggestions)

@app.route('/material_budget', methods=['POST'])
def material_budget():
    selected_plan = request.form['selected_plan']
    # Pass cents to scale materials
    cents = session['inputs']['cents']
    items, total = get_material_budget(selected_plan, cents)
    return render_template('material_result.html', plan=selected_plan, items=items, total_cost=total)

if __name__ == '__main__':
    app.run(debug=True)
