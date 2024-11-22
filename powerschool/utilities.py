import os
import json
import copy

DEFAULT_LOAD_LIBRARY = 'CourseLibrary.json'

def LoadLibrary(path):
    courseLibrary = CourseLibrary()
    if os.path.exists(path):
        courseLibrary.load(path)
    else:
        print('[PSL Model] no course course library found or created. Generating new.')

    return courseLibrary

class CoursePrefab(object):
    def __init__(self,name, weight):
        self.name = name
        self.weight = weight

    def serialize(self):
        return [self.name, self.weight]

    def __str__(self):
        return f"[COURSE: {self.name}][WEIGHT: {self.weight}]"


class CourseLibrary(object):
    def __init__(self):
        self.courseDict = {}

    def get_course(self, courseName):
        return self.courseDict[courseName]

    def add_course(self, course: CoursePrefab):
        self.courseDict[course.name] = course

    def load(self, path):
        with open(path, 'r') as f:
            self.loadrawData(f.read())

    def loadrawData(self, rawData):
        data = json.loads(rawData)
        self.deserializeOnSelf(data)

    def save(self, path):
        data = self.serialize()
        data = json.dumps(data)
        with open(path, 'w') as f:
            f.write(data)

    def serialize(self):
        data = copy.copy(self.__dict__)
        courses = []
        for course in self.courseDict:
            courseData = self.courseDict[course]
            courses.append([courseData.name, courseData.weight])
        data['courseDict'] = courses
        return data

    def deserializeOnSelf(self, data):
        for key in data:
            attrData = data[key]
            if key == 'courseDict':
                self.courseDict = {}
                for courseName, courseWeight in attrData:
                    self.courseDict[courseName] = CoursePrefab(courseName, courseWeight)
            else:
                setattr(self, key, attrData)



DEFAULT_LIBRARY = LoadLibrary(DEFAULT_LOAD_LIBRARY)
DEFAULT_LIBRARY.add_course(CoursePrefab("ELA",1))
print("Loaded course library: {}".format(DEFAULT_LIBRARY.serialize()))
DEFAULT_LIBRARY.save(DEFAULT_LOAD_LIBRARY)

def SaveDefaultLibrary():
    DEFAULT_LIBRARY.save(DEFAULT_LOAD_LIBRARY)

def ReloadDefaultLibrary():
    global DEFAULT_LIBRARY
    DEFAULT_LIBRARY = LoadLibrary(DEFAULT_LOAD_LIBRARY)