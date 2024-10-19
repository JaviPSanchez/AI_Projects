print('Importing libraries...')
import joblib
from flask import Flask, request, json, jsonify, render_template
from werkzeug.exceptions import HTTPException
print('Done!')
print()
print('Loading model...')
MODEL_PATH = 'models/classifier.joblib'
print('Done!')
print()
print('Loading server app...')
app = Flask(__name__)
print('Done!')
print()

@app.errorhandler(HTTPException)
def handle_exception(e):
    """
    Return JSON instead of HTML for HTTP errors (which is the basic error
    response with Flask).
    """
    # Start with the correct headers and status code from the error
    response = e.get_response()
    # Replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

class MissingKeyError(HTTPException):
    # We can define our own error for the missing key
    code = 422
    name = "Missing key error"
    description = "JSON content missing key 'input'."

class MissingJSON(HTTPException):
    # We can define our own error for missing JSON
    code = 400
    name = "Missing JSON"
    description = "Missing JSON."

def make_prediction(value: float):
    # Load model
    classifier = joblib.load(MODEL_PATH)
    print("1")
    print(classifier)
    # Make prediction (the model expects a 2D array that is why we put input in a list of list) and return it
    prediction = classifier.predict(value)
    print("2")
    print(prediction)
    return prediction


@app.route("/predict", methods=["POST", "GET"])
def predict():
    if request.json:
        json_input = request.json
        print("3")
        print(json_input) # {'input': [[9.8, 0.36, 0.46, 10.5, 'NaN', 4.0, 83.0, 0.9956, 2.89, 0.3, 10.1]]}
        if "input" not in json_input:
            raise MissingKeyError()
        prediction = make_prediction(json_input["input"])
        print("4")
        print(prediction)
        # Pipeline(steps=[('imputer', SimpleImputer()), ('scaler', StandardScaler()),
        #             ('classifier', RandomForestClassifier())])
        # C:\Users\javie\AppData\Roaming\Python\Python39\site-packages\sklearn\base.py:445: UserWarning: X does not have valid feature names, but SimpleImputer was fitted with feature names
        # warnings.warn(
        # [4]
        response = {
            "quality": str(prediction),
        }
        print("5")
        print(response) #{'quality': '[4]'}
        return jsonify(response), 200
    raise MissingJSON()


    # if request.json:
    #     # Get JSON as dictionnary
    #     json_input = request.get_json()
    #     if "input" not in json_input:
    #         raise MissingKeyError()
    #     prediction = make_prediction((json_input["input"]))
    #     response = {
    #         "quality": str(prediction),
    #     }
    #     return jsonify(response), 200
    # raise MissingJSON()


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=4000)