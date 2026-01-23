from university import University, College, Program, StudentStats, FacultyStats
import random
import json

def run_semester(university):
    university.year += 1
    university.university_points = 0

    for college in university.colleges:
        university.budget -= college.base_expenses
        college.college_points = 0

        for program in college.programs:
            if program.student_stats.total < program.capacity:
                admit_students_roll(program, university)

            f = program.faculty_stats
            quality_increase = f.class_s * 3 + f.class_a * 2 + f.class_b * 1
            program.quality = min(program.quality + quality_increase, 100)

            student_points = (
                program.student_stats.class_s * 10 +
                program.student_stats.class_a * 6 +
                program.student_stats.class_b * 4 +
                program.student_stats.class_c * 2 +
                program.student_stats.class_d * 1
            )

            faculty_points = (
                f.class_s * 10 +
                f.class_a * 7 +
                f.class_b * 5 +
                f.class_c * 3 +
                f.class_d * 1
            )

            program.program_points = student_points + faculty_points
            college.college_points += program.program_points

            s_leave = int(program.student_stats.class_s * 0.1)
            a_leave = int(program.student_stats.class_a * 0.05)
            d_leave = int(program.student_stats.class_d * 0.2)

            total_leaving = s_leave + a_leave + d_leave

            program.student_stats.total -= total_leaving
            program.student_stats.class_s -= s_leave
            program.student_stats.class_a -= a_leave
            program.student_stats.class_d -= d_leave

            university.budget -= f.total_expenses

        university.university_points += college.college_points

    return {
        "year": university.year,
        "budget": university.budget,
        "points": university.university_points
    }

def view_status(uni):
    data = {
        "name": uni.name,
        "budget": uni.budget,
        "year": uni.year,
        "university_points": uni.university_points,
        "ranking": uni.university_ranking,
        "colleges": []
    }

    for college in uni.colleges:
        college_data = {
            "id": college.id,
            "name": college.name,
            "tuition": college.tuition_fee,
            "college_points": college.college_points,
            "ranking": college.college_ranking,
            "programs": []
        }

        for program in college.programs:
            p = {
                "id": program.id,
                "name": program.name,
                "quality": program.quality,
                "points": program.program_points,
                "capacity": program.capacity,
                "students": program.student_stats.total,
                "faculty": vars(program.faculty_stats),
                "student_stats": vars(program.student_stats)
            }
            college_data["programs"].append(p)

        data["colleges"].append(college_data)

    return data

def create_college(university, name, tuition_fee=20000, base_expenses=50000, year_established=None):
    if year_established is None:
        year_established = university.year

    college_id = len(university.colleges) + 1
    college = College(college_id, name, year_established, tuition_fee, base_expenses)
    university.colleges.append(college)

    return college

def create_program(college, program_name, capacity, university):
    program_id = len(college.programs) + 1

    program = Program(program_id, program_name, university.year, capacity)
    college.programs.append(program)

    return program

def hire_faculty(program, university, tier):
    stats = program.faculty_stats

    if tier == "S":
        salary = stats.class_s_expense
    elif tier == "A":
        salary = stats.class_a_expense
    elif tier == "B":
        salary = stats.class_b_expense
    elif tier == "C":
        salary = stats.class_c_expense
    elif tier == "D":
        salary = stats.class_d_expense
    else:
        return {"error": "Invalid tier"}

    if university.budget < salary:
        return {"error": "Not enough budget"}

    university.budget -= salary
    stats.total += 1

    if tier == "S":
        stats.class_s += 1
    elif tier == "A":
        stats.class_a += 1
    elif tier == "B":
        stats.class_b += 1
    elif tier == "C":
        stats.class_c += 1
    elif tier == "D":
        stats.class_d += 1

    return {"message": f"Hired Class {tier} faculty"}

def admit_students_roll(program, university):
    remaining_capacity = program.capacity - program.student_stats.total
    if remaining_capacity <= 0:
        return {"error": "Program is full"}

    base_demand = random.randint(int(0.5 * program.capacity), int(1.5 * program.capacity))
    raw_admitted = int(base_demand * (0.5 + program.quality / 10))
    admitted = min(raw_admitted, remaining_capacity)

    if remaining_capacity >= 10:
        admitted = max(10, admitted)

    program.student_stats.total += admitted

    s_pct = min(0.05 + program.quality / 100, 0.1)
    a_pct = 0.2 + program.quality / 50
    b_pct = 0.25
    c_pct = 0.2

    s_count = int(admitted * s_pct)
    a_count = int(admitted * a_pct)
    b_count = int(admitted * b_pct)
    c_count = int(admitted * c_pct)
    d_count = admitted - (s_count + a_count + b_count + c_count)

    program.student_stats.class_s += s_count
    program.student_stats.class_a += a_count
    program.student_stats.class_b += b_count
    program.student_stats.class_c += c_count
    program.student_stats.class_d += d_count

    college_tuition = None
    for college in university.colleges:
        if program in college.programs:
            college_tuition = college.tuition_fee
            break

    if college_tuition is None:
        college_tuition = 10000

    university.budget += admitted * college_tuition

    return {"admitted": admitted}

def save_game(university, filename="savegame.json"):
    data = {
        "name": university.name,
        "year_established": university.year_established,
        "year": university.year,
        "budget": university.budget,
        "university_points": university.university_points,
        "university_ranking": university.university_ranking,
        "colleges": []
    }

    for college in university.colleges:
        college_data = {
            "id": college.id,
            "name": college.name,
            "year_established": college.year_established,
            "tuition_fee": college.tuition_fee,
            "base_expenses": college.base_expenses,
            "college_points": college.college_points,
            "college_ranking": college.college_ranking,
            "programs": []
        }

        for program in college.programs:
            program_data = {
                "id": program.id,
                "name": program.name,
                "year_established": program.year_established,
                "capacity": program.capacity,
                "size": program.size,
                "quality": program.quality,
                "program_points": program.program_points,
                "program_ranking": program.program_ranking,
                "student_stats": vars(program.student_stats),
                "faculty_stats": vars(program.faculty_stats)
            }
            college_data["programs"].append(program_data)

        data["colleges"].append(college_data)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_game(filename="savegame.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        uni = University(data["name"], data["year_established"], data["budget"])
        uni.year = data.get("year", 1)
        uni.university_points = data.get("university_points", 0)
        uni.university_ranking = data.get("university_ranking", 0)

        for college_data in data.get("colleges", []):
            college = College(
                college_data["id"],
                college_data["name"],
                college_data["year_established"],
                college_data["tuition_fee"],
                college_data["base_expenses"]
            )
            college.college_points = college_data.get("college_points", 0)
            college.college_ranking = college_data.get("college_ranking", 0)

            for program_data in college_data.get("programs", []):
                program = Program(
                    program_data["id"],
                    program_data["name"],
                    program_data["year_established"],
                    program_data["capacity"]
                )
                program.size = program_data["size"]
                program.quality = program_data["quality"]
                program.program_points = program_data["program_points"]
                program.program_ranking = program_data.get("program_ranking", 0)

                s_stats = StudentStats()
                f_stats = FacultyStats()

                for key, value in program_data["student_stats"].items():
                    setattr(s_stats, key, value)

                for key, value in program_data["faculty_stats"].items():
                    setattr(f_stats, key, value)

                program.student_stats = s_stats
                program.faculty_stats = f_stats

                college.programs.append(program)

            uni.colleges.append(college)

        return uni

    except FileNotFoundError:
        return None