import os


if not os.path.exists('glance.conf'):
    create_glance = open('glance.conf','w')
    create_glance.write('page=0')
    create_glance.close()

glance_conf = open('glance.conf', 'r')
cur_app = int(glance_conf.readline()[5:])
glance_conf.close()

if not os.path.exists('app.conf'):
    create_app = open('app.conf','w')
    create_app.write('numofapps=1')
    create_app.close()

app_conf = open('app.conf')
total_apps = int(app_conf.readline().split('=')[1])
app_conf.close()

next_app = (cur_app + 1) % total_apps

glance_conf = open('glance.conf', 'w')
glance_conf.write("page=" +  str(next_app))
glance_conf.close()
