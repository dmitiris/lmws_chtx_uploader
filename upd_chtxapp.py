__author__ = 'dmitry'

import os, sys, psycopg2
os.environ['DJANGO_SETTINGS_MODULE']='lmws.settings'

try: sys.path.append('/home/dmitry/lmws')
except: print 'Something wrong with sys.path'

try: sys.path.append('/home/dmitry/lmws/lmws')
except: print 'Something wrong'

try:
    import django
    django.setup()
except:
    print 'No django module available'

def perbar(data, counter):
    ''' ver. 10.04.2015 '''
    if type(data) != int:
        l = len(data)
    else:
        l = data
    if l < 10:
        print 'No items to count'
        return False
    elif counter == l:
        print 'Completed 100%', str(counter), 'out of', str(l)
        return True
    per = l/10
    if counter % per == 0:
        print 'Completed', str(counter/per*10)+'%', str(counter), 'out of', str(l)
        return True


def connect():
    conn = psycopg2.connect('dbname=chdb')
    cur = conn.cursor()
    return conn, cur

def read_model():
    from chtx.models import chtxApp
    return chtxApp

def read_apps():
    Model = read_model()
    conn, cur = connect()
    counter = 0
    cur.execute("SELECT count(*) FROM lmws_export_new;")
    limit = cur.fetchone()[0]
    print limit
    cur.execute("SELECT * FROM lmws_export_new;")
    for record in cur:
        perbar(limit, counter)
        app_obj = Model()
        app_obj.app_num = record[0]
        app_obj.text = record[1]
        app_obj.category = 'fresh'
        app_obj.save()
        counter += 1