from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "adminpass")

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        for row in data:
            cur.execute(
                "INSERT INTO sensor_data (id, name, value) VALUES (%s, %s, %s)",
                (row["id"], row["name"], row["value"])
            )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 10")
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        data = [dict(zip(colnames, row)) for row in rows]
        cur.close()
        conn.close()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
