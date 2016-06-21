# super-spoon
import os,sys
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import scipy.io as sio


f = []
dirn = []
dirp = []

root2 = 1.41421356237305

# Create Lists for:
#   ExposureTime
#   Aperture
#   Date
#   Iso
#   FocalLength
#
#   and count the entries
ExpT_List     = []
Aperture_List = []
Iso_List      = []
Focall_List   = []

mypath = 'C:\Users\Lukas\Documents\Bilder'
if not os.path.exists(mypath):
    os.makedirs(mypath)

def WRITE(text):
    wrt = open(mypath +'/path.txt','a')
    wrt.write(text+'\n')
    wrt.close()

def get_field(exif, field):
    for (k,v) in exif.iteritems():
        if TAGS.get(k) == field:
            return v

def exif(root,file,level):
    subindent = ' '*4*(level+2)
    img = Image.open(root +'/'+file)
    exif_data = img._getexif()

    # ExposureTime
    ExpT = get_field(exif_data, 'ExposureTime')
    Exp = str(ExpT[0])+'/'+str(ExpT[1])
    print  'ExposureTime = ', Exp

    # ApertureValue

    ap = []
    ap = get_field(exif_data, 'ApertureValue')
    if ap[0]>20:
        Ap = root2**(ap[0]/ap[1])
    else:
        Ap = root2**ap[0]
    print 'Aperture = ', Ap

    # Date
    Date = get_field(exif_data, 'DateTimeOriginal')
    print 'Date = ', Date

    # FocalLength
    Focall = get_field(exif_data, 'FocalLength')[0]
    print 'FocalLength = ',  Focall

    # Iso
    Iso = get_field(exif_data, 'ISOSpeedRatings')
    print 'ISO = ', Iso


    WRITE('{}{}'.format(subindent,Exp))
    WRITE('{}{}'.format(subindent,Ap))
    WRITE('{}{}'.format(subindent,Date))
    WRITE('{}{}'.format(subindent,Focall))
    WRITE('{}{}\n'.format(subindent,Iso))

    ExpT_List.append(Exp)
    Aperture_List.append(Ap)
    Focall_List.append(Focall)
    Iso_List.append(Iso)


def isjpg(pic):
    l = list(pic)
    for i in range(len(l)):
        if l[i] == '.' and l[i+1] == 'j' and l[i+2] == 'p' and l[i+3] == 'g':
            return pic
    return None

# search in all folders for pictures
# list all folders and do depth-first algorithm
def depth_frst(mypath):
    counter = 0
    for root,dirs,files in os.walk(mypath):
        level = root.replace(mypath,'').count(os.sep)
        indent = ' '*4* (level)
        temp = '{}{}/'.format(indent,os.path.basename(root))
        print(temp)
        WRITE(temp)


        subindent = ' '*4*(level+1)
        for f in files:
            # found an item - it is jpg?
            temp = '{}{}'.format(subindent,f)
            l = list(temp)
            #save only if temp is .jpg
            temp = isjpg(temp)
            if temp != None:
                print temp
                counter = counter +1
                WRITE(temp)

                exif(root,f,level)

                #wait = raw_input()

    print "total files = ",counter


depth_frst(mypath)

ExpT_List.sort()
tt = np.array(ExpT_List)
sio.savemat(mypath + '/ExpT_List.mat', {'Ex':tt})

Aperture_List.sort()
tt = np.array(Aperture_List)
sio.savemat(mypath + '/Aperture_List.mat', {'Ap':tt})

Focall_List.sort()
tt = np.array(Focall_List)
sio.savemat(mypath + '/Focall_List.mat', {'FL':tt})

Iso_List.sort()
tt = np.array(Iso_List)
sio.savemat(mypath + '/Iso_List.mat', {'ISO':tt})
