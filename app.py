from flask import Flask, render_template, request, jsonify
from agent import PatientEngagementAgent

app = Flask(__name__)

agent = PatientEngagementAgent()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    response = agent.handle_message(user_message)

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)