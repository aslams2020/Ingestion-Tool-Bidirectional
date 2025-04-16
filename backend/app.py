from flask import Flask, render_template, request, jsonify, session
from utils.clickhouse_utils import ClickHouseConnector  # Add this import
from utils.file_utils import process_flat_file, generate_csv
import os

from utils.file_utils import process_flat_file, generate_csv
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'data')

# Main route
@app.route("/")
def index():
    return render_template("index.html")

# ClickHouse Connection
@app.route("/api/connect/clickhouse", methods=["POST"])
def connect_clickhouse():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    config = request.json
    required_fields = ["host", "port"]
    
    if not all(field in config for field in required_fields):
        return jsonify({
            "error": "Missing required fields",
            "required": required_fields,
            "received": list(config.keys())
        }), 400

    try:
        client = ClickHouseConnector(
            host=config["host"],
            port=config["port"],
            database=config.get("database"),
            user=config.get("user"),
            password=config.get("password"),
            jwt_token=config.get("jwt_token")
        )
        session["ch_client"] = client
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Schema Discovery
@app.route("/api/schema/discover", methods=["POST"])
def discover_schema():
    source_type = request.json.get('source_type')
    
    if source_type == 'clickhouse':
        client = session.get('ch_client')
        tables = client.get_tables()
        return jsonify({"tables": tables})
    
    elif source_type == 'flatfile':
        filepath = process_flat_file(request.files['file'])
        columns = get_csv_columns(filepath)
        return jsonify({"columns": columns})

# Data Ingestion
@app.route("/api/ingest", methods=["POST"])
def ingest_data():
    direction = request.json.get('direction')  # ch_to_file or file_to_ch
    config = request.json.get('config')
    
    if direction == 'ch_to_file':
        client = session.get('ch_client')
        data = client.execute_query(config['query'])
        output_path = generate_csv(data, config['columns'])
        return jsonify({"output_path": output_path})
    
    elif direction == 'file_to_ch':
        client = session.get('ch_client')
        result = client.insert_data(config['table'], config['filepath'])
        return jsonify({"inserted_rows": result.rowcount})

if __name__ == "__main__":
    app.run(debug=True)