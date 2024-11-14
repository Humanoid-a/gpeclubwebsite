class CourseData(object):
    def __init__(self, course_name, course_letter_grade, course_number_grade):
        self.course_name = course_name
        self.course_letter_grade = course_letter_grade
        self.course_number_grade = course_number_grade

    def __str__(self):
        return '{} {} {}'.format(self.course_name,self.course_letter_grade,self.course_number_grade)

"""
def callback_course(course: CourseData):
    print(course)
    with open('../crawled.txt', 'a', encoding='utf-8') as f:
        f.write(f"{course}\n")
"""
def callback_course(course: CourseData):
    course_str = str(course)
    print(course_str.encode('utf-8', errors='replace').decode('utf-8'))
    with open('../crawled.txt', 'a', encoding='utf-8') as f:
        f.write(f"{course_str}\n")