import scrapy
from scrapy.http import FormRequest
from .. import PSLData as psl

USERNAME = ''
PWD = ''

class PslSpider(scrapy.Spider):
    name = "psl"
    allowed_domains = ["power.this.edu.cn"]
    start_urls = ["https://power.this.edu.cn/public/"]

    def parse(self, response):
        return self.login(username=USERNAME, pwd=PWD)

    def login(self, username, pwd):
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

        TD_TAG = 'td'
        COURSE_TAG = 'tr + .center'

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
            except:
                l_grade = 'None'
                n_grade = 0

            course_data = psl.CourseData(course_name, l_grade, n_grade)
            psl.callback_course(course_data)