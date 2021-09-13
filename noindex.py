import os
import shutil

print (" ")
print (" ________________________________________ ")
print ("|              _           _             |")
print ("|  _ __   ___ (_)_ __   __| | _____  __  |")
print ("| | '_ \ / _ \| | '_ \ / _` |/ _ \ \/ /  |")
print ("| | | | | (_) | | | | | (_| |  __/>  <   |")
print ("| |_| |_|\___/|_|_| |_|\__,_|\___/_/\_\  |")
print ("|________________________________________|")
print ("|                                        |")
print ("| noindex.py v0.1 2021                   |")
print ("| \ \ avi compressor                     |")
print ("|                                        |")
print ("|________________________________________|")
print ("|                                        |")
print ("| dev@niklausiff.ch                      |")
print ("| https://www.niklausiff.ch              |")
print ("|________________________________________|")
print (" ")

print (">>> 0/4 settings")
print ("__________________________________________")

# input settings
print (" ")
print "video width"
w = raw_input("> value: ")
print (" ")
print "height"
h = raw_input("> value: ")
print (" ")
print "algorythm (neighbor or lanczos)"
algo = raw_input("> value: ")
print (" ")
print "motion method (dia)"
mm = raw_input("> value: ")
print (" ")
print "bitrate"
bit = raw_input("> value: ")
print (" ")
print "threshold"
thr = raw_input("> value: ")
print (" ")
print "iframes"
ifr = raw_input("> value: ")
print (" ")
print "GOD"
god = raw_input("> value: ")
print (" ")

print ("__________________________________________")
print (" ")
print (">>> 1/4 create folders")
print ("__________________________________________")

# create folders
pathe = './'
directoryc = 'compressed'
filese = os.listdir(pathe)
newpathc = os.path.join(pathe, directoryc)
os.mkdir(newpathc)
patho = './'
directoryo = 'og'
fileso = os.listdir(patho)
newpatho = os.path.join(patho, directoryo)
os.mkdir(newpatho)
pathb = './'
directoryb = 'baked'
filesb = os.listdir(pathb)
newpathb = os.path.join(pathb, directoryb)
os.mkdir(newpathb)
length = 0
howmany = 0
getVideo = []
og = []

print (" ")
print (">>> 2/4 convert video // delete metadta")
print ("__________________________________________")

# get video
for filename in os.listdir(pathe):
    if filename.endswith('.avi') or filename.endswith('.mp4') or filename.endswith('.mov'):
        getVideo.append(filename)
        shutil.move('./'+getVideo[0], './og'+filename[-4]+filename[-3]+filename[-2]+filename[-1])
        ogvideo = './og'+filename[-4]+filename[-3]+filename[-2]+filename[-1]
    else:
        continue
for filename in os.listdir(pathe):
    if filename.endswith('.avi') or filename.endswith('.mp4') or filename.endswith('.mov'):
        og.append(filename)
    else:
        continue

# convert video // delete metadata
os.system('ffmpeg -i '+og[0]+' -map_metadata -1 nometa.avi -hide_banner -loglevel panic')

print (" ")
print (">>> 3/4 compress video")
print ("__________________________________________")

os.system('ffmpeg -y -i nometa.avi -vf scale='+w+':'+h+':flags='+algo+' -c:v libx264 -x264-params "keyint='+ifr+':minkeyint='+ifr+'" -b:v '+bit+'k -sc_threshold '+thr+' -g '+god+' -me_method '+mm+' -an ./compressed/compressed.avi -hide_banner')

# move og videos
shutil.move(ogvideo, './og/'+ogvideo)
os.remove('./nometa.avi')
shutil.copyfile('./noindex.py', './og/noindex.py')

print (" ")
print (">>> 4/4 bake video")
print ("__________________________________________")

for filename in os.listdir(newpathc):
    if filename.endswith(".avi"):
        os.system('ffmpeg -i ./compressed/compressed.avi ./compressed/baked.mov -hide_banner -loglevel panic')
        shutil.move('./compressed/baked.mov', './baked/baked.mov')
    else:
        continue

print (" ")
print (" ________________________________________ ")
print ("|                                        |")
print ("| finished                               |")
print ("|________________________________________|")
print ("|                                        |")
print ("| original video:                        |")
print ("| ./og                                   |")
print ("|                                        |")
print ("| ripped videos:                         |")
print ("| ./compressed                           |")
print ("|                                        |")
print ("| baked videos:                          |")
print ("| ./baked                                |")
print ("|                                        |")
print ("|________________________________________|")
print ("|                                        |")
print ("| dev@niklausiff.ch                      |")
print ("| https://www.niklausiff.ch              |")
print ("|________________________________________|")
print (" ")