class CourseData(object):
    def __init__(self, course_name, course_letter_grade, course_number_grade):
        self.course_name = course_name
        self.course_letter_grade = course_letter_grade
        self.course_number_grade = course_number_grade

    def __str__(self):
        return '{} {} {}'.format(self.course_name,self.course_letter_grade,self.course_number_grade)

def callback_course(course: CourseData):
    print(course)