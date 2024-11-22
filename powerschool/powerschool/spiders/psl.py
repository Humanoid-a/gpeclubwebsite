import scrapy
from scrapy.http import FormRequest


USERNAME = ''
PWD = ''
avg = 0

class PslSpider(scrapy.Spider):
    name = "psl"
    allowed_domains = ["power.this.edu.cn"]
    start_urls = ["https://power.this.edu.cn/public/"]

    def parse(self, response):
        return self.login(username=USERNAME, pwd=PWD)

    def login(self, username, pwd):
        self.username = username
        self.pwd = pwd
        formdata = {
            'dbpw':pwd,
            'translator_username': '',
            'translator_password': '',
            'translator_ldappassword': '',
            'returnUrl': '',
            'serviceName': 'PS Parent Portal',
            'serviceTicket': '',
            'pcasServerUrl':'/',
            'credentialType': 'User Id and Password Credential',
            #'request_locale': 'zh_CN',
            'request_locale': 'en_US',
            'account': username,
            'pw': pwd,
            'translatorpw':'',
            '': 'Enter'
        }
        form = FormRequest(
            url='https://power.this.edu.cn/guardian/home.html',
            formdata=formdata,
            callback=self.afterlogin,
            #dont_filter=True
        )
        return form

    def extract_course_name(self, raw_name):
        course_name = str(raw_name).split('<br>')[0].split('>')[1]
        return course_name

    def extract_grade(self, raw_grade):
        raw = raw_grade.css('a').extract_first()
        left, right = str(raw).split('<br>')
        lgrade = left.split('>')[1].strip()
        ngrade = int(right.split('<')[0].strip())
        return (lgrade, ngrade)

    def afterlogin(self, response):
        #print('-'*50)
        #print('Login!')
        from .. import PSLData as psl
        global avg
        TD_TAG = 'td'
        COURSE_TAG = 'tr + .center'
        grade_sum = 0
        courses = []
        num = 0

        for course in response.css(COURSE_TAG):

            columns = list(course.css(TD_TAG))
            if len(columns) == 0:
                continue

            course_time, course_name_raw, sem1, sem2 = columns
            course_name = self.extract_course_name(course_name_raw)
            try:
                course_grades = self.extract_grade(sem1)
                l_grade = course_grades[0]
                n_grade = course_grades[1]
                if l_grade == 'A+': grade = 4.3
                elif l_grade == 'A': grade = 4.0
                elif l_grade == 'A-': grade = 3.7
                elif l_grade == 'B+': grade = 3.3
                elif l_grade == 'B': grade = 3.0
                elif l_grade == 'B-': grade = 2.7
                elif l_grade == 'C+': grade = 2.3
                elif l_grade == 'C': grade = 2.0
                elif l_grade == 'C-': grade = 1.7
                elif l_grade == 'D+': grade = 1.3
                elif l_grade == 'D': grade = 1.0
                elif l_grade == 'D-': grade = 0.7
                elif l_grade == 'F': grade = 0.0
                else: grade = 0.0
                if 'AP' in course_name: grade += 0.3
                with open('powerschool/grades/main_courses.txt', 'r', encoding='gbk') as f:
                    for line in f:
                        if line in course_name:
                            grade *= 1
                grade_sum += grade
                course_data = psl.CourseData(course_name, l_grade, n_grade)
                courses.append(course_data)
                psl.callback_course(course_data)
                num += 1

                #print(grade, num)
            except:
                #l_grade = 'None'
                #n_grade = 0
                continue

        grades_data = psl.GradesData(self.username, courses)
        psl.callback_gradefile(grades_data)
        avg = grade_sum / num
        import math
        avg = round(avg, 2)
        print (grade_sum, num, avg)
        psl.callback_avg(avg, grades_data)



