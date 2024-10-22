from . import models
from django.core.files.uploadedfile import SimpleUploadedFile

def clearDatas():
    a = models.Project.objects.all()
    for _ in range(len(a)):
        a[0].delete()

def project_cover_path(name):
    return 'imgs/project_covers/{}'.format(name)

#---------------------------------------------
#actual code below----------------------------
#---------------------------------------------


clearDatas()

#super tic tac toe project
models.Project.objects.create(
    project_id=1,
    project_name='Super TicTacToe',
    project_url='projects/supertictactoe/',
    project_version='1.0.0',
    project_description='super tictactoe!',
    project_cover=project_cover_path('1.png'),
)

#photo1
models.Project.objects.create(
    project_id=0,
    project_name='Photo Album 1',
    project_url='projects/photo1/',
    project_version='1.0.0',
    project_description='Miniature world',
    project_cover=project_cover_path('2.png'),
)


"""
python manage.py shell
import gpeclub.data_initiator
quit(
"""