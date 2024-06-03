import os,subprocess,argparse,shutil

print (" ")
print (" ________________________________________ ")
print ("|              _           _             |")
print ("|  _ __   ___ (_)_ __   __| | _____  __  |")
print ("| | '_ \ / _ \| | '_ \ / _` |/ _ \ \/ /  |")
print ("| | | | | (_) | | | | | (_| |  __/>  <   |")
print ("| |_| |_|\___/|_|_| |_|\__,_|\___/_/\_\  |")
print ("|________________________________________|")
print ("|                                        |")
print ("| noindex.py v1.0 2024                   |")
print ("| >> mp4 compressor                      |")
print ("|                                        |")
print ("|________________________________________|")
print ("|                                        |")
print ("| dev@niklausiff.ch                      |")
print ("| https://www.niklausiff.ch              |")
print ("|________________________________________|")
print (" ")

## functions
# compress video
def compressVideo(video,w,h,scaleAlgo,cc,vbit,sc,gop,noa,nom,out):
    print (">>> compressing video")
    if (h == None or w == None or scaleAlgo == None):
        scale = ''
    else:
        scale = ' -vf scale='+w+':'+h+',setsar=1 -sws_flags '+scaleAlgo
    if (cc == None):
        codec = ' -c:v libx264'
    else:
        codec = ' -c:v '+cc
    if (vbit == None):
        bitrate = ''
    else: 
        bitrate = ' -b:v '+vbit+'K'
    if (sc == None or gop == None):
        keyframes = ''
    else: 
        keyframes = ' -sc_threshold '+sc+' -g '+gop
    if (noa == True):
        noaudio = ' -an'
    else:
        noaudio = ''
    if (nom == True):
        nometa = ' -map_metadata -1 '
    else:
        nometa = ''
    if (vbit == None and sc == None):
        newVideo = video[:-4]+'_compressed'+'.mp4'
    elif (vbit == None):
        newVideo = video[:-4]+'_'+gop+'gop'+'.mp4'
    elif (sc == None):
        newVideo = video[:-4]+'_'+vbit+'bit'+'.mp4'
    else: 
        newVideo = video[:-4]+'_'+vbit+'bit'+'_'+gop+'gop'+'.mp4'
    if (out == None):
        output = ' '+newVideo
    else: 
        output = ' '+out
    nolog = ' -hide_banner -loglevel panic'
    os.system('ffmpeg -y -i '+video+scale+codec+bitrate+keyframes+noaudio+nometa+output+nolog)
    if (noi == True):
        ifr = output[1:]
        removeIFR(ifr,None)
# remove iframes
def removeIFR(video,out):
    print (">> removing iframes")
    outTerm = subprocess.run(['ffprobe',video,'-show_frames','-hide_banner','-v','quiet'], stdout=subprocess.PIPE).stdout.splitlines()
    decodedOut = []
    iframes = []
    for i in outTerm:
        decodedOut.append(i.decode('utf-8'))
    for idx, x in enumerate(decodedOut):
        if x.startswith('pict_type=I'):
            iframes.append(outTerm[idx-14].decode('utf-8')[4:])
    for idx, x in enumerate(iframes):
        iframes[idx] = '\,'+iframes[idx]
    if (len(iframes)==0):
        print ("> no iframes found")
    else:
        iframes.pop(0)
        if (out == None):
            output = video[:-4]+'_noifr.mp4'
        else: 
            output = ' '+out
        nolog = ' -hide_banner -loglevel panic'
        temp = 'temp'
        newFolder = os.path.join('./', temp)
        os.mkdir(newFolder)
        for idx,x in enumerate(iframes):
            index = '{:05d}'.format(idx)
            if (idx==0):
                output = './temp/'+output[:-4]+str(index)+'.mp4'
                os.system('ffmpeg -y -copyts -i '+video+' -c copy -enc_time_base -1 -bsf:v:0 "noise=drop=eq(pts'+iframes[idx]+')" '+output+nolog)
            else:
                if (len(iframes)>2):
                    idxLast = idx+1
                    if (idx==1):
                        inp = output
                        output = inp[:-9]+str(index)+'.mp4'
                    elif (idxLast==len(iframes)):
                        indexCounterInp = '{:05d}'.format(idx-1)
                        inp = output[:-9]+str(indexCounterInp)+'.mp4'
                        output = output[:-9]+'.mp4'
                        output = output[7:]
                    else:
                        indexCounterInp = '{:05d}'.format(idx-1)
                        indexCounterOut = '{:05d}'.format(idx)
                        inp = output[:-9]+str(indexCounterInp)+'.mp4'
                        output = output[:-9]+str(indexCounterOut)+'.mp4'
                else:
                    inp = output
                    output = output[:-9]+'.mp4'
                    output = output[7:]
                os.system('ffmpeg -y -copyts -i '+inp+' -c copy -enc_time_base -1 -bsf:v:0 "noise=drop=eq(pts'+iframes[idx]+')" '+output+nolog)
        shutil.rmtree(newFolder)
# check for iframes
def checkIFR(video):
    print (">> check for iframes")
    lastOut = subprocess.run(['ffprobe',video,'-show_frames','-hide_banner','-v','quiet'], stdout=subprocess.PIPE).stdout.splitlines()
    lastOutDecoded = []
    iframesCheck = []
    for i in lastOut:
        lastOutDecoded.append(i.decode('utf-8'))
    for idx, x in enumerate(lastOutDecoded):
        if x.startswith('pict_type=I'):
            iframesCheck.append(lastOut[idx-14].decode('utf-8')[4:])
    print('> '+str(len(iframesCheck))+' iframes found')
# bake video
def bakeVideo(video):
    print (">> bake video")
    output = video[:-4]+'_baked.mov'
    nolog = ' -hide_banner -loglevel panic'
    os.system('ffmpeg -y -i '+video+' '+output+nolog)
# combine videos WIP
def combineVideos(videos,out):
    print (">> combine videos")
    videos = videos.split(',')
    if (out == None):
        output = ' combined.mp4'
    else: 
        output = ' '+out
    nolog = ' -hide_banner -loglevel panic'
    print(videos,output,nolog)
# path handling
# def handlePath(path):


## arguments
# initialise args
parser = argparse.ArgumentParser()
parser.add_argument('-i',type=str,help='enter video path')
parser.add_argument('-vw',type=str,help='enter video width')
parser.add_argument('-vh',type=str,help='enter video height')
parser.add_argument('-sa',type=str,help='enter scale alogrithm (neighbor,gauss,lanczos,experimental)')
parser.add_argument('-c',type=str,help='enter video codec (libx264,libxvid)')
parser.add_argument('-b',type=str,help='enter video bitrate')
parser.add_argument('-sc',type=str,help='enter scenecut threshold')
parser.add_argument('-gop',metavar='gop',type=str,help='enter video gop')
parser.add_argument('-noa',action='store_true',help='remove audio track')
parser.add_argument('-nom',action='store_true',help='remove metadata')
parser.add_argument('-noi',action='store_true',help='remove iframes')
parser.add_argument('-o',type=str,help='enter output name')
parser.add_argument('-ifr',type=str,help='enter video path to remove iframes')
parser.add_argument('-ifrC',type=str,help='enter video path to check for iframes')
parser.add_argument('-bake',type=str,help='enter video path for baking')
parser.add_argument('-comb',type=str,help='enter video paths comma separated')
args = parser.parse_args()
# set args
video = args.i
w = args.vw
h = args.vh
scaleAlgo = args.sa
cc = args.c
vbit = args.b
sc = args.sc
gop = args.gop
noa = args.noa
nom = args.nom
noi = args.noi
out = args.o
ifrRemove = args.ifr
ifrCheck = args.ifrC
bakeI = args.bake
videos = args.comb

## handling arguments
if (video != None):
    compressVideo(video,w,h,scaleAlgo,cc,vbit,sc,gop,noa,nom,out)
if (ifrRemove != None):
    removeIFR(ifrRemove,out)
if (ifrCheck != None):
    checkIFR(ifrCheck)
if (bakeI != None):
    bakeVideo(bakeI)
if (videos != None):
    combineVideos(videos,out)