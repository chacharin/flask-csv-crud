from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)
DATA_FILE = "data.csv"
FILEDNAMES = ["id","name","age"]

def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline='', encoding="utf-8") as f:
            writer =csv.DictWriter(f, fieldnames=FILEDNAMES)
            writer.writeheader()
            
def load_data():
    ensure_data_file()
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
    
def save_data(d):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FILEDNAMES)
        writer.writeheader()
        writer.writerows(d)
        
@app.route("/students/<student_id>", methods=["DELETE"])
def del_student(student_id):
    data = load_data()
    new_data = []
    found = False
    for std in data:
        if std["id"] == student_id:
            found = True
        else:
            new_data.append(std)
    if not found:
        return jsonify({"error":"ไม่พบ ID ที่ต้องการลบ"})
    save_data(new_data)
    return jsonify({"message": "ลบข้อมูลเรียบร้อยแล้ว"})
    

@app.route("/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    data = load_data()
    for std in data:
        if std["id"] == student_id:
            std.update(request.json)
            save_data(data)
            return jsonify({"message": "อัพเดทเรียบร้อยแล้ว"})
    return jsonify({"error":"ไม่พบ ID ที่ระบุ"})

@app.route("/students", methods = ["POST"])
def add_student():
    new_student = request.json
    data = load_data()
    
    for std  in data:
        if std["id"] == new_student["id"]:
            return jsonify({"error": "ID นี้มีอยู่แล้ว"})
    data.append(new_student)
    save_data(data)
    return jsonify({"message": "เพิ่มข้อมูลเรียบร้อยแล้ว"})
    
@app.route("/students", methods = ["GET"])
def get_student():
    data = load_data()
    return jsonify(data)

@app.route("/")
def home():
    return "Start API server"

if __name__ == "__main__":
    ensure_data_file()
    app.run()