from flask import Flask, render_template, request, jsonify
from food import get_gemini_response, input_image_setup, generate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    input_data = request.form.get('input')
    input_data1 = request.form.get('input1')
    image_file = request.files['image']
    format = """-->

    1. item1_name: calories: no of calories 
                    carbohydrates: carbohydrates in grams 
                    protein: protein in grams 
                    fat: fat in grams
    
    item2_name: ...."""
    input_prompt="You are an expert in nutritionist, you need to see the food items from the image and calculate the total calories, also provide the nutritional details of every food item with calorie intake in below format" + format
     
    if input_data and image_file:
        mime_type = image_file.mimetype  # Get the MIME type of the uploaded file
        image_data = input_image_setup(image_file, mime_type)
        response = get_gemini_response(input_data, image_data, input_prompt)
        return jsonify({'response': response})
    elif input_data1:
        response =  generate(input_data1)
        return jsonify({'response': response})
    else:
        return jsonify({'error': 'Please provide both input and image'})

if __name__ == '__main__':
    app.run(debug=True)
