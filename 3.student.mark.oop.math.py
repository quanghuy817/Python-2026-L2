import curses
import math

import numpy as np


# ---------------------------------------------------------------- domain ---
class Student:
    def __init__(self, sid, name, dob):
        self.id = sid
        self.name = name
        self.dob = dob
        self.marks = {}  # course id -> mark

    def set_mark(self, course_id, mark):
        self.marks[course_id] = mark

    def __str__(self):
        return f"{self.id:<8} {self.name:<24} {self.dob}"


class Course:
    def __init__(self, cid, name, credits):
        self.id = cid
        self.name = name
        self.credits = credits

    def __str__(self):
        return f"{self.id:<8} {self.name:<24} {self.credits} credit(s)"


class School:
    def __init__(self):
        self.students = []
        self.courses = []

    def find_student(self, sid):
        return next((s for s in self.students if s.id == sid), None)

    def find_course(self, cid):
        return next((c for c in self.courses if c.id == cid), None)

    @staticmethod
    def floor_mark(mark):
        """Round DOWN to 1 decimal digit with math.floor (e.g. 15.87 -> 15.8)."""
        return math.floor(round(mark * 10, 6)) / 10

    def gpa(self, student):
        """Weighted average: sum(mark * credits) / sum(credits), using numpy arrays."""
        pairs = [(m, self.find_course(cid).credits)
                 for cid, m in student.marks.items() if self.find_course(cid)]
        if not pairs:
            return 0.0
        marks = np.array([p[0] for p in pairs], dtype=float)
        credits = np.array([p[1] for p in pairs], dtype=float)
        return float(np.sum(marks * credits) / np.sum(credits))

    def sort_by_gpa(self):
        """Sort student list by GPA descending (in place)."""
        if not self.students:
            return
        gpas = np.array([self.gpa(s) for s in self.students])
        order = np.argsort(-gpas, kind="stable")
        self.students = [self.students[i] for i in order]


# -------------------------------------------------------------------- UI ---
TITLE, OK, WARN, HILITE = 1, 2, 3, 4


def put(win, y, x, text, attr=0):
    """addstr that never crashes when the terminal window is too small."""
    try:
        win.addstr(y, x, text, attr)
    except curses.error:
        pass


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(TITLE, curses.COLOR_RED, -1)
    curses.init_pair(OK, curses.COLOR_GREEN, -1)
    curses.init_pair(WARN, curses.COLOR_YELLOW, -1)
    curses.init_pair(HILITE, curses.COLOR_BLACK, curses.COLOR_CYAN)


def header(scr, text):
    scr.clear()
    _, w = scr.getmaxyx()
    scr.attron(curses.color_pair(TITLE) | curses.A_BOLD)
    put(scr, 0, 0, f" {text} ".center(w - 1, "="))
    scr.attroff(curses.color_pair(TITLE) | curses.A_BOLD)


def ask(scr, row, label):
    put(scr, row, 2, label)
    curses.echo()
    curses.curs_set(1)
    value = scr.getstr(row, 2 + len(label), 40).decode().strip()
    curses.noecho()
    curses.curs_set(0)
    return value


def message(scr, row, text, color=OK):
    put(scr, row, 2, text, curses.color_pair(color))


def wait(scr, row):
    put(scr, row, 2, "Press any key to go back...", curses.A_DIM)
    scr.getch()


def show_lines(scr, title, lines):
    header(scr, title)
    h, _ = scr.getmaxyx()
    for i, line in enumerate(lines[: h - 4]):
        put(scr, 2 + i, 2, line)
    wait(scr, min(h - 1, 3 + len(lines)))


# --------------------------------------------------------------- screens ---
def add_student(scr, school):
    header(scr, "Add student")
    sid = ask(scr, 2, "Student id: ")
    if school.find_student(sid):
        message(scr, 6, "That id already exists.", WARN)
    else:
        school.students.append(Student(sid, ask(scr, 3, "Name: "), ask(scr, 4, "DoB: ")))
        message(scr, 6, "Student added.")
    wait(scr, 8)


def add_course(scr, school):
    header(scr, "Add course")
    cid = ask(scr, 2, "Course id: ")
    if school.find_course(cid):
        message(scr, 6, "That id already exists.", WARN)
    else:
        name = ask(scr, 3, "Name: ")
        try:
            credits = int(ask(scr, 4, "Credits: "))
            school.courses.append(Course(cid, name, credits))
            message(scr, 6, "Course added.")
        except ValueError:
            message(scr, 6, "Credits must be an integer.", WARN)
    wait(scr, 8)


def input_marks(scr, school):
    header(scr, "Input marks")
    course = school.find_course(ask(scr, 2, "Course id: "))
    if not course:
        message(scr, 4, "Unknown course.", WARN)
        return wait(scr, 6)
    row = 4
    for s in school.students:
        h, _ = scr.getmaxyx()
        if row >= h - 2:
            header(scr, f"Input marks - {course.name}")
            row = 2
        try:
            mark = school.floor_mark(float(ask(scr, row, f"{s.name} ({s.id}): ")))
            s.set_mark(course.id, mark)
        except ValueError:
            message(scr, row, f"{s.name}: invalid, skipped", WARN)
        row += 1
    wait(scr, min(row + 1, scr.getmaxyx()[0] - 1))


def list_students(scr, school):
    show_lines(scr, "Students", [str(s) for s in school.students] or ["(none)"])


def list_courses(scr, school):
    show_lines(scr, "Courses", [str(c) for c in school.courses] or ["(none)"])


def show_course_marks(scr, school):
    header(scr, "Marks of a course")
    course = school.find_course(ask(scr, 2, "Course id: "))
    if not course:
        message(scr, 4, "Unknown course.", WARN)
        return wait(scr, 6)
    lines = [f"{s.name:<24} {s.marks.get(course.id, '-')}" for s in school.students]
    show_lines(scr, f"Marks - {course.name}", lines or ["(none)"])


def show_ranking(scr, school):
    school.sort_by_gpa()
    lines = [f"{i:>2}. {s.name:<24} GPA {school.gpa(s):6.2f}"
             for i, s in enumerate(school.students, 1)]
    show_lines(scr, "GPA ranking (descending)", lines or ["(none)"])


MENU = [
    ("Add student", add_student),
    ("Add course", add_course),
    ("Input marks for a course", input_marks),
    ("List students", list_students),
    ("List courses", list_courses),
    ("Show marks of a course", show_course_marks),
    ("Sort students by GPA and show", show_ranking),
    ("Exit", None),
]


def main(scr):
    init_colors()
    curses.curs_set(0)
    school = School()
    sel = 0
    while True:
        header(scr, "Student Mark Management")
        for i, (label, _) in enumerate(MENU):
            attr = curses.color_pair(HILITE) if i == sel else curses.A_NORMAL
            put(scr, 2 + i, 4, f" {i + 1}. {label:<34}", attr)
        put(scr, 3 + len(MENU), 4, "Up/Down + Enter, or press a number", curses.A_DIM)
        key = scr.getch()
        if key == curses.KEY_UP:
            sel = (sel - 1) % len(MENU)
        elif key == curses.KEY_DOWN:
            sel = (sel + 1) % len(MENU)
        elif ord("1") <= key <= ord(str(len(MENU))):
            sel, key = key - ord("1"), curses.KEY_ENTER
        if key in (curses.KEY_ENTER, 10, 13):
            action = MENU[sel][1]
            if action is None:
                break
            action(scr, school)


if __name__ == "__main__":
    curses.wrapper(main)