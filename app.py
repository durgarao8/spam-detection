import pickle
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "spam_secret_key"

# Load trained MNB model
model = pickle.load(open("model.pkl", "rb"))

# Load vectorizer
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Login page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # simple login (can change later)
        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect(url_for("predict"))
        else:
            return render_template("login.html", error="Invalid Credentials")
    return render_template("login.html")

# Prediction page
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("login"))

    result = ""
    probability_percent = ""

    if request.method == "POST":
        message = request.form["message"]

        # Transform text
        vector = vectorizer.transform([message])

        # Prediction using MultinomialNB
        prediction = model.predict(vector)[0]
        probability = model.predict_proba(vector)

        if prediction == 1:
            result = "Spam Message"
            # Index 1 = probability of being Spam
            spam_prob = probability[0][1] * 100
            probability_percent = f"{spam_prob:.2f}% probability of being Spam"
        else:
            result = "Not Spam"
            # Index 0 = probability of being Not Spam
            not_spam_prob = probability[0][0] * 100
            probability_percent = f"{not_spam_prob:.2f}% probability of being Not Spam"

        print(f"[PREDICTION] Result: {result} | {probability_percent}")

    return render_template("predict.html", prediction=result, probability=probability_percent)

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)