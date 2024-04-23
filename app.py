from flask import Flask, render_template
import ai
from flask import Flask, render_template, jsonify
import ai

app = Flask(__name__)

@app.route('/')
def home():
    recommendations = ai.run_analysis()
    return render_template('1.html', recommendations=recommendations)

@app.route('/refresh', methods=['POST'])
def refresh():
    recommendations = ai.run_analysis()
    return jsonify(recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

