import os, math, shutil, re, random, argparse, struct
from itertools import chain
from itertools import repeat

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
print ("| \ \ video index ripper                 |")
print ("|                                        |")
print ("|________________________________________|")
print ("|                                        |")
print ("| dev@niklausiff.ch                      |")
print ("| https://www.niklausiff.ch              |")
print ("|________________________________________|")
print (" ")

print (">>> 0/5 settings")
print ("__________________________________________")

# settings
end = 0
mode = ''
firstframe = 0
countframes = 0
positframes = 0
kill = 0.7
audio = 0

# input settings
print (" ")
print "how long sequences for cutting?"
end = input("> sequence lengths in seconds: ")
print (" ")
print "choose mode (void, random, reverse, invert, bloom, pulse, jiggle, overlape)"
mode = raw_input("> mode: ")
print (" ")
print "keep the first frame? (0 = no, 1 = yes)"
firstframe = input("> value: ")
print (" ")
if mode in ["bloom", "pulse", "overlap"]:
    print "how many times to duplicate p-frame"
    countframes = input("> value: ")
    print (" ")
else:
    pass
if mode in ["bloom", "pulse", "overlap", "jiggle"]:  
    print "how many frames for the duplication"
    positframes = input("> value: ")
    print (" ")
else:
    pass
print "kill frames with too much data (0 - 1, recommended 0.7)"
kill = input("> value: ")
print (" ")

# stuff for the cutting
start = 0
name = 1
namec = 1
nameb = 1

print ("__________________________________________")
print (" ")
print (">>> 1/5 create folders")
print ("__________________________________________")

# create folders
path = './'
directory = 'cutted'
files = os.listdir(path)
newpath = os.path.join(path, directory)
os.mkdir(newpath)
pathe = './'
directoryc = 'ripped'
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
print (">>> 2/5 convert video // delete metadta")
print ("__________________________________________")

# get video
for filename in os.listdir(path):
    if filename.endswith('.avi') or filename.endswith('.mp4') or filename.endswith('.mov'):
        getVideo.append(filename)
        shutil.move('./'+getVideo[0], './og'+filename[-4]+filename[-3]+filename[-2]+filename[-1])
        ogvideo = './og'+filename[-4]+filename[-3]+filename[-2]+filename[-1]
    else:
        continue
for filename in os.listdir(path):
    if filename.endswith('.avi') or filename.endswith('.mp4') or filename.endswith('.mov'):
        og.append(filename)
    else:
        continue

# convert video // delete metadata
os.system('ffmpeg -i '+og[0]+' -map_metadata -1 nometa.avi -hide_banner -loglevel panic')

# get video length
lengths = os.popen('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 nometa.avi').readlines()
lenghtoflentghts = len(lengths[0])
minusaids = lengths[0][:lenghtoflentghts - 2]

# calculate how many videos
howv = float(minusaids)/end
rhowv = math.ceil(howv)

print (" ")
print ">>> 3/5 cut video to ", rhowv, " pieces"
print ("__________________________________________")

# cut video into parts
for filename in os.listdir(path):
    for x in range(int(rhowv)):
        if filename.endswith('.avi'):
            os.system('ffmpeg -i nometa.avi -ss '+str(start)+' -t '+str(end)+' '+newpath+'/'+str(name)+'.avi -hide_banner -loglevel panic')
            start += end
            name += 1
        else:
            continue
howmany = os.listdir(newpath)

print (" ")
print (">>> 4/5 destroy videos")
print ("__________________________________________")

for filename in os.listdir(newpath):
    if filename.endswith(".avi"):
        
        # create temp files
        temp_nb = random.randint(10000, 99999)
        temp_dir = "temp-" + str(temp_nb)
        temp_hdrl = temp_dir +"/hdrl.bin"
        temp_movi = temp_dir +"/movi.bin"
        temp_idx1 = temp_dir +"/idx1.bin"
        os.mkdir(temp_dir)

        # Define constrain function for jiggle :3
        def constrain(val, min_val, max_val):
            return min(max_val, max(min_val, val))

        # get files to temp
        def bstream_until_marker(bfilein, bfileout, marker=0, startpos=0):
            chunk = 1024
            filesize = os.path.getsize(bfilein)
            if marker :
                marker = str.encode(marker)

            with open(bfilein,'rb') as rd:
                with open(bfileout,'ab') as wr:
                    for pos in range(startpos, filesize, chunk):
                        rd.seek(pos)
                        buffer = rd.read(chunk)

                        if marker:
                            if buffer.find(marker) > 0 :
                                marker_pos = re.search(marker, buffer).start() # position is relative to buffer glitchedframes
                                marker_pos = marker_pos + pos # position should be absolute now
                                split = buffer.split(marker, 1)
                                wr.write(split[0])
                                return marker_pos
                            else:
                                wr.write(buffer)
                        else:
                            wr.write(buffer)

        # make 3 files, 1 for each chunk
        movi_marker_pos = bstream_until_marker('./cutted/'+str(namec)+'.avi', temp_hdrl, "movi")
        idx1_marker_pos = bstream_until_marker('./cutted/'+str(namec)+'.avi', temp_movi, "idx1", movi_marker_pos)
        bstream_until_marker('./cutted/'+str(namec)+'.avi', temp_idx1, 0, idx1_marker_pos)

        with open(temp_movi,'rb') as rd:
            chunk = 1024
            filesize = os.path.getsize(temp_movi)
            frame_table = []

            for pos in range(0, filesize, chunk):
                rd.seek(pos)
                buffer = rd.read(chunk)

                #build first list with all adresses 
                for m in (re.finditer(b'\x30\x31\x77\x62', buffer)): # find iframes
                        if audio : frame_table.append([m.start() + pos, 'sound'])		
                for m in (re.finditer(b'\x30\x30\x64\x63', buffer)): # find b frames
                    frame_table.append([m.start() + pos, 'video'])

                #then remember to sort the list
                frame_table.sort(key=lambda tup: tup[0])

            l = []
            l.append([0,0, 'void'])
            max_frame_size = 0

            #build tuples for each frame index with frame sizes
            for n in range(len(frame_table)):
                if n + 1 < len(frame_table):
                    frame_size = frame_table[n + 1][0] - frame_table[n][0]
                else:
                    frame_size = filesize - frame_table[n][0]
                max_frame_size = max(max_frame_size, frame_size)
                l.append([frame_table[n][0],frame_size, frame_table[n][1]])

        # variables that make shit work
        clean = []
        final = []

        # keep first video frame or not
        if firstframe :
            for x in l :
                if x[2] == 'video':
                    clean.append(x)
                    break

        # clean the list by killing "big" frames
        for x in l:
            if x[1] <= (max_frame_size * kill) :
                clean.append(x)

        # FX modes

        if mode == "void":
            final = clean

        if mode == "random":
            final = random.sample(clean,len(clean))

        if mode == "reverse":
            final = clean[::-1]

        if mode == "invert":
            final = sum(zip(clean[1::2], clean[::2]), ())

        if mode == 'bloom':
            repeat = int(countframes)
            frame = int(positframes)
            ## split list
            lista = clean[:frame]
            listb = clean[frame:]
            ## rejoin list with bloom
            final = lista + ([clean[frame]]*repeat) + listb

        if mode == 'pulse':
            pulselen = int(countframes)
            pulseryt = int(positframes)
            j = 0
            for x in clean:
                i = 0
                if(j % pulselen == 0):
                    while i < pulselen :
                        final.append(x)
                        i = i + 1
                else:
                    final.append(x)
                    j = j + 1

        if mode == "jiggle":
            #print('*needs debugging lol help thx*') # didn't pandy's branch fix this?
            amount = int(positframes)
            final = [clean[constrain(x+int(random.gauss(0,amount)),0,len(clean)-1)] for x in range(0,len(clean))]

        if mode == "overlap":
            pulselen = int(countframes)
            pulseryt = int(positframes)

            clean = [clean[i:i+pulselen] for i in range(0,len(clean),pulseryt)]
            final = [item for sublist in clean for item in sublist]

        #name new file
        cname = '-c' + str(countframes) if int(countframes) > 1 else '' 
        pname = '-n' + str(positframes) if int(positframes) > 1 else ''
        fileout = './cutted/'+str(namec)+'c.avi'

        #delete old file
        if os.path.exists(fileout):
            os.remove(fileout)

        bstream_until_marker(temp_hdrl, fileout)

        with open(temp_movi,'rb') as rd:
            filesize = os.path.getsize(temp_movi)
            with open(fileout,'ab') as wr:
                wr.write(struct.pack('<4s', b'movi'))
                for x in final:
                    if x[0] != 0 and x[1] != 0:
                        rd.seek(x[0])
                        wr.write(rd.read(x[1]))

        bstream_until_marker(temp_idx1, fileout)

        #move files // name video
        shutil.move('./cutted/'+str(namec)+'c.avi', './ripped/'+str(namec)+'c.avi')

        #remove unnecessary temporary files and folders
        os.remove(temp_hdrl)
        os.remove(temp_movi)
        os.remove(temp_idx1)
        os.rmdir(temp_dir)

        namec += 1

    else:
        continue

# move og videos
shutil.move(ogvideo, './og/'+ogvideo)
os.remove('./nometa.avi')
shutil.copyfile('./noindex.py', './og/noindex.py')

print (" ")
print (">>> 5/5 bake videos")
print ("__________________________________________")
for filename in os.listdir(newpathc):
    if filename.endswith(".avi"):
        os.system('ffmpeg -i ./ripped/'+str(nameb)+'c.avi ./ripped/'+str(nameb)+'b.mov -hide_banner -loglevel panic')
        shutil.move('./ripped/'+str(nameb)+'b.mov', './baked/'+str(nameb)+'b.mov')
        nameb += 1
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
print ("| cutted videos:                         |")
print ("| ./cutted                               |")
print ("|                                        |")
print ("| ripped videos:                         |")
print ("| ./ripped                               |")
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