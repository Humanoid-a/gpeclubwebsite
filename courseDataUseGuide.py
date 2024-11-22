import powerschool.utilities as utils


course_name = "Chinese"

#Getting weight of course
course = utils.DEFAULT_LIBRARY.get_course(course_name)
print(course)

#Adding a course
new_course = utils.CoursePrefab(name = "Biology", weight=1)
utils.DEFAULT_LIBRARY.add_course(new_course)
print(utils.DEFAULT_LIBRARY.serialize())

#Reloading course library from file
utils.ReloadDefaultLibrary()

#Saving course library to file
utils.SaveDefaultLibrary()