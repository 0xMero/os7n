from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/home', methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        return "POST"
    else:
        return render_template('skills.html')
if __name__ == "__main__":
    app.run(debug=True)