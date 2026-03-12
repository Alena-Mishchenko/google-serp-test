from flask import Flask, request, jsonify, render_template
from app.search import fetch_google_results


app = Flask(__name__)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search")
def search_api():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"error": "Query is missing (parametr 'q')."}), 400

    try:
        results = fetch_google_results(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
