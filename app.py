
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
from ml.nutrition_calculator import calculate_bmr, macro_targets
from ml.dish_data import dishes
from ml.weekly_planner import generate_week_plan
from flask import Flask, render_template, request



app = Flask(__name__)
app.secret_key = 'your-secret-key-here' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    members = db.Column(db.Integer, default=2)
    diets = db.Column(db.String(200), default='')

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    cuisine = db.Column(db.String(50))
    calories = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    prep_time = db.Column(db.String(20))
    image = db.Column(db.String(200))

DISHES = [
    {"name": "Poha", "category": "breakfast", "cuisine": "Indian", "calories": 250, "protein": 6, "carbs": 45, "fat": 7, "prep_time": "15 min", "image": "https://images.unsplash.com/photo-1645177628172-a94c1f96e6db?w=400&h=300&fit=crop"},
    {"name": "Idli", "category": "breakfast", "cuisine": "South Indian", "calories": 200, "protein": 7, "carbs": 40, "fat": 3, "prep_time": "20 min", "image": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400&h=300&fit=crop"},
    {"name": "Upma", "category": "breakfast", "cuisine": "South Indian", "calories": 300, "protein": 8, "carbs": 50, "fat": 10, "prep_time": "15 min", "image": "https://images.unsplash.com/photo-1567337710282-00832b415979?w=400&h=300&fit=crop"},
    {"name": "Paratha", "category": "breakfast", "cuisine": "North Indian", "calories": 350, "protein": 9, "carbs": 45, "fat": 15, "prep_time": "25 min", "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop"},
    {"name": "Dosa", "category": "breakfast", "cuisine": "South Indian", "calories": 330, "protein": 9, "carbs": 55, "fat": 8, "prep_time": "20 min", "image": "https://images.unsplash.com/photo-1630383249896-424e482df921?w=400&h=300&fit=crop"},
    {"name": "Oats", "category": "breakfast", "cuisine": "Continental", "calories": 280, "protein": 10, "carbs": 48, "fat": 7, "prep_time": "10 min", "image": "https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=400&h=300&fit=crop"},
    {"name": "Boiled Eggs", "category": "breakfast", "cuisine": "Continental", "calories": 210, "protein": 18, "carbs": 2, "fat": 15, "prep_time": "10 min", "image": "https://images.unsplash.com/photo-1482049016530-d79f7d51d4c5?w=400&h=300&fit=crop"},
    {"name": "Dal Rice", "category": "lunch", "cuisine": "Indian", "calories": 450, "protein": 18, "carbs": 65, "fat": 8, "prep_time": "30 min", "image": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop"},
    {"name": "Rajma Rice", "category": "lunch", "cuisine": "North Indian", "calories": 480, "protein": 20, "carbs": 70, "fat": 9, "prep_time": "45 min", "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&h=300&fit=crop"},
    {"name": "Chole Rice", "category": "lunch", "cuisine": "North Indian", "calories": 500, "protein": 22, "carbs": 75, "fat": 10, "prep_time": "40 min", "image": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=400&h=300&fit=crop"},
    {"name": "Veg Pulao", "category": "lunch", "cuisine": "Indian", "calories": 400, "protein": 10, "carbs": 60, "fat": 12, "prep_time": "35 min", "image": "https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=400&h=300&fit=crop"},
    {"name": "Vegetable Khichdi", "category": "lunch", "cuisine": "Indian", "calories": 380, "protein": 14, "carbs": 55, "fat": 9, "prep_time": "30 min", "image": "https://images.unsplash.com/photo-1626132647523-66c9bed9259e?w=400&h=300&fit=crop"},
    {"name": "Curd Rice", "category": "lunch", "cuisine": "South Indian", "calories": 300, "protein": 8, "carbs": 45, "fat": 6, "prep_time": "15 min", "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400&h=300&fit=crop"},
    {"name": "Roti Sabzi", "category": "dinner", "cuisine": "North Indian", "calories": 350, "protein": 12, "carbs": 50, "fat": 8, "prep_time": "30 min", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=300&fit=crop"},
    {"name": "Paneer Curry", "category": "dinner", "cuisine": "North Indian", "calories": 420, "protein": 22, "carbs": 18, "fat": 30, "prep_time": "35 min", "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400&h=300&fit=crop"},
    {"name": "Sambar", "category": "dinner", "cuisine": "South Indian", "calories": 220, "protein": 12, "carbs": 30, "fat": 5, "prep_time": "40 min", "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop"},
    {"name": "Vegetable Curry", "category": "dinner", "cuisine": "Indian", "calories": 260, "protein": 7, "carbs": 35, "fat": 9, "prep_time": "30 min", "image": "https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=400&h=300&fit=crop"},
    {"name": "Dal Roti", "category": "dinner", "cuisine": "North Indian", "calories": 390, "protein": 16, "carbs": 52, "fat": 8, "prep_time": "35 min", "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&h=300&fit=crop"},
    {"name": "Fruit Bowl", "category": "dinner", "cuisine": "Continental", "calories": 180, "protein": 3, "carbs": 40, "fat": 1, "prep_time": "5 min", "image": "https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=400&h=300&fit=crop"},
]

GROCERY_LIST = [
    {"name": "Dals & Pulses", "product_list": ["Toor Dal (500g)", "Moong Dal (250g)", "Rajma (500g)", "Chickpeas (500g)", "Urad Dal (250g)"]},
    {"name": "Rice & Grains", "product_list": ["Basmati Rice (2kg)", "Rava (500g)", "Poha (500g)", "Oats (500g)", "Wheat Flour (2kg)"]},
    {"name": "Vegetables", "product_list": ["Onions (1kg)", "Tomatoes (500g)", "Potatoes (1kg)", "Mixed Vegetables (500g)"]},
    {"name": "Dairy", "product_list": ["Milk (2L)", "Curd (500g)", "Paneer (400g)"]},
    {"name": "Other", "product_list": ["Cooking Oil (1L)", "Eggs (12)", "Fresh Fruits (1kg)"]},
]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('family_details'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        session['user_id'] = new_user.id
        session['user_name'] = new_user.name
        flash('Account created successfully!', 'success')
        return redirect(url_for('family_details'))
    
    return render_template('signup.html')


@app.route("/ai-planner")
def ai_planner():
    return render_template("ai_plan_form.html")



@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/family-details', methods=['GET', 'POST'])
def family_details():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        members = request.form.get('members', 2)
        diets = ','.join(request.form.getlist('diet'))
        
        user = User.query.get(session['user_id'])
        user.members = members
        user.diets = diets
        db.session.commit()
        
        return redirect(url_for('select_dishes'))
    
    return render_template('family_details.html')

@app.route('/select-dishes', methods=['GET', 'POST'])
def select_dishes():
    if request.method == 'POST':
        selected = request.form.getlist('dishes')
        session['selected_dishes'] = selected
        return redirect(url_for('meal_plan'))
    
    return render_template('select_dishes.html', dishes=DISHES)
@app.route('/meal-plan')
def meal_plan():

    breakfast = [d for d in DISHES if d['category'] == 'breakfast']
    lunch = [d for d in DISHES if d['category'] == 'lunch']
    dinner = [d for d in DISHES if d['category'] == 'dinner']
    
    if not breakfast or not lunch or not dinner:
        flash("Dish data is missing!", "error")
        return redirect(url_for('index'))

    plan = []
    for i in range(7):
        plan.append({
            'Breakfast': random.choice(breakfast),
            'Lunch': random.choice(lunch),
            'Dinner': random.choice(dinner)
        })

    total = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
    for day in plan:
        for meal in day.values():
            total['calories'] += meal['calories']
            total['protein'] += meal['protein']
            total['carbs'] += meal['carbs']
            total['fat'] += meal['fat']
    
    daily_avg = {k: v // 7 for k, v in total.items()}
    
    return render_template('meal_plan.html', 
                         meal_plan=plan, 
                         daily_avg=daily_avg, 
                         weekly_total=total)
@app.route('/grocery')
def grocery():
    grocery_text = ""
    for cat in GROCERY_LIST:
        grocery_text += f"*{cat['name']}*\n"
        for item in cat['product_list']: 
            grocery_text += f"• {item}\n"
        grocery_text += "\n"
    
    return render_template('grocery.html', 
                         grocery_list=GROCERY_LIST, 
                         grocery_text=grocery_text)

@app.route("/generate_plan", methods=["POST"])
def generate_plan():
    weight = float(request.form.get("weight", 70))
    height = float(request.form.get("height", 170))
    age = int(request.form.get("age", 25))
    gender = request.form.get("gender", "male")
    activity = request.form.get("activity", "medium")
    goal = request.form.get("goal", "balanced")

    bmr_result = calculate_bmr(weight, height, age, gender, activity, goal)
    
    target = macro_targets(bmr_result)

    from ml.meal_optimizer import recommend_meals 
    optimized_meals = recommend_meals(DISHES, target)
    
    ai_plan = [{
        'Breakfast': optimized_meals[0]['dish'],
        'Lunch': optimized_meals[1]['dish'],
        'Dinner': optimized_meals[2]['dish']
    } for _ in range(7)]

    return render_template("meal_plan.html", 
                           meal_plan=ai_plan, 
                           daily_avg=target, 
                           user_bmr=bmr_result, # Added this
                           weekly_total={k: v*7 for k, v in target.items()})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


