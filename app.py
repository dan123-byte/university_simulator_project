from flask import Flask, request, jsonify, render_template, redirect, url_for
from university import University, College, Program, StudentStats, FacultyStats
from simulator import run_semester, view_status, create_program, hire_faculty, admit_students_roll, save_game, load_game

app = Flask(__name__)

app = Flask(__name__)

university = None

@app.route("/")
def home():
    return render_template("index.html", university=university)

@app.route("/status")
def status_page():
    if not university:
        return redirect(url_for("home"))
    data = view_status(university)
    return render_template("status.html", data=data)

@app.route("/new_university", methods=["POST"])
def new_university():
    global university
    name = request.form.get("name", "My University")
    budget = int(request.form.get("budget", 1000000))
    year_established = int(request.form.get("year_established", 1900))
    university = University(name, year_established, budget)
    return redirect(url_for("home"))

@app.route("/create_college", methods=["GET", "POST"])
def create_college_page():
    global university
    if request.method == "POST":
        name = request.form.get("name", "New College")
        tuition_fee = int(request.form.get("tuition_fee", 20000))
        base_expenses = int(request.form.get("base_expenses", 50000))
        year_established = int(request.form.get("year_established", 1900))
        college = College(name, tuition_fee, base_expenses, year_established)
        university.colleges.append(college)
        return redirect(url_for("status_page"))
    return render_template("create_college.html")

@app.route("/create_program", methods=["GET", "POST"])
def create_program_page():
    global university
    if request.method == "POST":
        college_id = int(request.form.get("college_id"))
        program_name = request.form.get("name", "General Studies")
        capacity = int(request.form.get("capacity", 100))
        college = next((c for c in university.colleges if c.id == college_id), None)
        if college:
            create_program(college, program_name, capacity, university)
        return redirect(url_for("status_page"))
    return render_template("create_program.html", university=university)

@app.route("/hire_faculty", methods=["GET", "POST"])
def hire_faculty_page():
    global university
    if request.method == "POST":
        college_id = int(request.form.get("college_id"))
        program_id = int(request.form.get("program_id"))
        tier = request.form.get("tier")
        college = next((c for c in university.colleges if c.id == college_id), None)
        if college:
            program = next((p for p in college.programs if p.id == program_id), None)
            if program:
                hire_faculty(program, university, tier)
        return redirect(url_for("status_page"))
    return render_template("hire_faculty.html", university=university)

@app.route("/run_semester")
def run_semester_page():
    global university
    if university:
        run_semester(university)
    return redirect(url_for("status_page"))

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