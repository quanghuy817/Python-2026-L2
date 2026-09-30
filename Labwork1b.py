"""
Practical work 1: Student mark management
USTH Advanced Programming with Python 2026

Chức năng:
  - Input functions: nhập số lượng sinh viên, thông tin sinh viên,
    số lượng môn học, thông tin môn học, nhập điểm cho sinh viên theo môn
  - Listing functions: liệt kê môn học, liệt kê sinh viên,
    hiển thị điểm của sinh viên theo môn học
"""

# ========== INPUT FUNCTIONS ==========

def input_number_of_students():
    while True:
        try:
            n = int(input("Nhập số lượng sinh viên: "))
            if n > 0:
                return n
            print("Số lượng phải lớn hơn 0.")
        except ValueError:
            print("Vui lòng nhập một số nguyên.")


def input_students(n):
    students = []
    for i in range(n):
        print(f"\n-- Nhập thông tin sinh viên thứ {i + 1} --")
        sid = input("  ID: ")
        name = input("  Họ tên: ")
        dob = input("  Ngày sinh (dd/mm/yyyy): ")
        students.append({"id": sid, "name": name, "dob": dob, "marks": {}})
    return students


def input_number_of_courses():
    while True:
        try:
            n = int(input("Nhập số lượng môn học: "))
            if n > 0:
                return n
            print("Số lượng phải lớn hơn 0.")
        except ValueError:
            print("Vui lòng nhập một số nguyên.")


def input_courses(n):

    courses = []
    for i in range(n):
        print(f"\n-- Nhập thông tin môn học thứ {i + 1} --")
        cid = input("  Mã môn: ")
        cname = input("  Tên môn: ")
        courses.append({"id": cid, "name": cname})
    return courses


def select_course(courses):
    list_courses(courses)
    while True:
        cid = input("Nhập mã môn muốn chọn: ")
        for course in courses:
            if course["id"] == cid:
                return course
        print("Không tìm thấy mã môn này, thử lại.")


def input_marks_for_course(students, course):
    print(f"\nNhập điểm cho môn: {course['name']} ({course['id']})")
    for student in students:
        while True:
            try:
                mark = float(input(f"  Điểm của {student['name']} ({student['id']}): "))
                if 0 <= mark <= 10:
                    student["marks"][course["id"]] = mark
                    break
                print("  Điểm phải nằm trong khoảng 0-10.")
            except ValueError:
                print("  Vui lòng nhập một số.")


# ========== LISTING FUNCTIONS ==========

def list_courses(courses):
    print("\n=== DANH SÁCH MÔN HỌC ===")
    if not courses:
        print("  (chưa có môn học nào)")
        return
    for course in courses:
        print(f"  - {course['id']}: {course['name']}")


def list_students(students):
    print("\n=== DANH SÁCH SINH VIÊN ===")
    if not students:
        print("  (chưa có sinh viên nào)")
        return
    for student in students:
        print(f"  - {student['id']}: {student['name']} (Sinh: {student['dob']})")


def show_marks_for_course(students, course):
    print(f"\n=== ĐIỂM MÔN {course['name']} ({course['id']}) ===")
    for student in students:
        mark = student["marks"].get(course["id"], "Chưa có điểm")
        print(f"  - {student['name']} ({student['id']}): {mark}")


# ========== MAIN PROGRAM ==========

def main():
    print("===== CHƯƠNG TRÌNH QUẢN LÝ ĐIỂM SINH VIÊN =====")

    num_students = input_number_of_students()
    students = input_students(num_students)

    num_courses = input_number_of_courses()
    courses = input_courses(num_courses)

    while True:
        print("\n--------- MENU ---------")
        print("1. Liệt kê môn học")
        print("2. Liệt kê sinh viên")
        print("3. Nhập điểm cho một môn học")
        print("4. Xem điểm sinh viên theo môn")
        print("0. Thoát")
        choice = input("Chọn chức năng: ")

        if choice == "1":
            list_courses(courses)
        elif choice == "2":
            list_students(students)
        elif choice == "3":
            course = select_course(courses)
            input_marks_for_course(students, course)
        elif choice == "4":
            course = select_course(courses)
            show_marks_for_course(students, course)
        elif choice == "0":
            print("Kết thúc chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ, thử lại.")


if __name__ == "__main__":
    main()