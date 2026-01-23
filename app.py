from flask import Flask, request, jsonify
from university import University, College, Program, StudentStats, FacultyStats
from simulator import run_semester, view_status, create_program, hire_faculty, admit_students_roll, save_game, load_game

app = Flask(__name__)

app = Flask(__name__)

university = None

@app.route("/")
def home():
    return "University Simulator API is running!"

@app.route("/new_university", methods=["POST"])
def new_university():
    global university
    data = request.json
    name = data.get("name", "My University")
    budget = data.get("budget", 1000000)
    year_established = data.get("year_established", 1900)
    university = University(name, year_established, budget)
    return jsonify({"message": f"University '{name}' created!", "budget": university.budget})

@app.route("/run_semester", methods=["POST"])
def run_semester_route():
    global university
    if not university:
        return jsonify({"error": "No university loaded"}), 400
    result = run_semester(university)
    return jsonify(result)

@app.route("/status", methods=["GET"])
def status():
    global university
    if not university:
        return jsonify({"error": "No university loaded"}), 400
    return jsonify(view_status(university))

@app.route("/create_program", methods=["POST"])
def create_program_route():
    global university
    if not university:
        return jsonify({"error": "No university loaded"}), 400
    data = request.json
    college_id = data.get("college_id")
    program_name = data.get("name", "General Studies")
    capacity = data.get("capacity", 100)

    college = next((c for c in university.colleges if c.id == college_id), None)
    if not college:
        return jsonify({"error": "College not found"}), 404

    program = create_program(college, program_name, capacity, university)
    return jsonify({"message": f"Program '{program.name}' created", "capacity": program.capacity})

@app.route("/create_college", methods=["POST"])
def create_college_route():
    global university
    if not university:
        return jsonify({"error": "No university loaded"}), 400

    data = request.json
    name = data.get("name", "New College")
    tuition_fee = data.get("tuition_fee", 20000)
    base_expenses = data.get("base_expenses", 50000)
    year_established = data.get("year_established", None)

    college_id = len(university.colleges) + 1
    year_established = year_established or university.year
    college = College(college_id, name, year_established, tuition_fee, base_expenses)
    university.colleges.append(college)

    return jsonify({
        "message": f"College '{college.name}' created!",
        "college_id": college.id,
        "tuition_fee": college.tuition_fee,
        "base_expenses": college.base_expenses
    })

@app.route("/hire_faculty", methods=["POST"])
def hire_faculty_route():
    global university
    if not university:
        return jsonify({"error": "No university loaded"}), 400
    data = request.json
    college_id = data.get("college_id")
    program_id = data.get("program_id")
    tier = data.get("tier")

    college = next((c for c in university.colleges if c.id == college_id), None)
    if not college:
        return jsonify({"error": "College not found"}), 404

    program = next((p for p in college.programs if p.id == program_id), None)
    if not program:
        return jsonify({"error": "Program not found"}), 404

    result = hire_faculty(program, university, tier)
    return jsonify(result)

@app.route("/admit_students", methods=["POST"])
def admit_students_route():
    global university
    if not university:
        return jsonify({"error": "No university loaded"}), 400
    data = request.json
    college_id = data.get("college_id")
    program_id = data.get("program_id")

    college = next((c for c in university.colleges if c.id == college_id), None)
    if not college:
        return jsonify({"error": "College not found"}), 404

    program = next((p for p in college.programs if p.id == program_id), None)
    if not program:
        return jsonify({"error": "Program not found"}), 404

    result = admit_students_roll(program, university)
    return jsonify(result)

@app.route("/save_game", methods=["POST"])
def save_game_route():
    global university
    if not university:
        return jsonify({"error": "No university loaded"}), 400
    filename = request.json.get("filename", "savegame.json")
    save_game(university, filename)
    return jsonify({"message": f"Game saved to {filename}"})

@app.route("/load_game", methods=["POST"])
def load_game_route():
    global university
    filename = request.json.get("filename", "savegame.json")
    uni = load_game(filename)
    if not uni:
        return jsonify({"error": f"Save file '{filename}' not found"}), 404
    university = uni
    return jsonify({"message": f"Game loaded from {filename}"})

if __name__ == "__main__":
    app.run(debug=True)