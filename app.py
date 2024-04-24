from flask import Flask, render_template, request, jsonify
from food import get_gemini_response, input_image_setup
from FoodNutritionValories import total_model
from forms import Main_Form
import os
import base64

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    input_data = request.form.get('input')
    image_file = request.files['image']
    input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----


""" 
     
    if image_file:
        mime_type = image_file.mimetype  # Get the MIME type of the uploaded file
        image_data = input_image_setup(image_file, mime_type)
        response = get_gemini_response(image_data, input_prompt)
        return {'response': response},200
    elif input_data:
        response = get_gemini_response(input_data, input_prompt)
        return jsonify({'response': response})
    else:
        return jsonify({'error': 'Please provide image'})

@app.route('/meal', methods = ['GET','POST'])
def meal():
    form = Main_Form()
    if form.validate_on_submit():
        form_data = request.form.to_dict()
        weight = form_data['weight']
        calorie = form_data['calorie']
        result = total_model(int(weight), int(calorie))

        return render_template('meal.html', form = form, result = result)


    return render_template ('meal.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)
