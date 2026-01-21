from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health", methods=['GET'])
def health():
    return jsonify({"message": "I AM ALIVE"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)