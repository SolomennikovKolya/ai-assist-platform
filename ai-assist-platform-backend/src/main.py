from graph import Graph
from utils import print_green_text
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/api/test", methods=["POST"])
def test():
    return jsonify({"response": "test message from server"})


@app.route("/api/generate", methods=["POST"])
def generate():
    print(request.json)
    agent_description = request.json["agent_description"]
    api_key = request.json["api_key"]["_value"]
    
    graph_data = Graph.generate(agent_description, api_key)
    if isinstance(graph_data, str):
        return jsonify({"warning": "Failed to generate a graph"})
    else:
        return jsonify(graph_data)


@app.route("/api/start", methods=["POST"])
def start():
    data = request.json

    graph = Graph()
    if (warning := graph.load(data)) != None:
        return jsonify({"warning": warning})
    print(graph)

    result = graph.calculate()
    for key in result:
        print(f"[{key}]:")
        print_green_text(result[key])
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

# Чтобы отправить HTTP-запрос с данными из файла test_data.json:
# curl -X POST http://127.0.0.1:5000/api/start -H "Content-Type: application/json" -d @test_data3.json
