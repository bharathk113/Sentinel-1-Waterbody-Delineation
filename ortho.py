import os,sys
from os import listdir,path,walk
import swisar
def filesinsidefolder(myPath,form):
    fileNames=[]
    fullFileNames=[]
    for dirpath, dirnames, filenames in walk(myPath):
        for filename in [f for f in filenames if form in f]:
            if '.aux' in filename:
                pass
            else:
                fullFileNames.append(path.join(dirpath, filename))
                fileNames.append(filename)
    return fullFileNames,fileNames
if __name__=='__main__':
    files=filesinsidefolder('\\\\192.168.192.121\\WBIS_processing\\SOP\\S1_downloading\\','.zip')
    outputDir='\\\\192.168.192.121\\WBIS_processing\\SOP\\test\\'
    i=0
    for f1 in files[0]:
        f2=files[1][i]
        cmd='gpt -q 32 D:\NHP\dev\sentinelProcessing\graphfile.xml -Pfile1="'+str(f1)+'" -Pfile2="'+outputDir+str(f2)[:-3]+'tif'+'"'
        swisar.water(str(f1),outputDir+str(f2)[:-3]+'tif')
        print cmd
        os.system(cmd)
        i=i+1





# 'gpt -q 32 C:\Users\Bharath\Documents\NHP\dev\sentinelProcessing\graphfile10m.xml -Pfile1="C:\Users\Bharath\Downloads\nizamSagar\june\S1A_IW_GRDH_1SDV_20170627T003805_20170627T003830_017212_01CB6C_CF39.zip" -Pfile2="C:\Users\Bharath\Downloads\S1A_IW_GRDH_1SDV_20170416T003916_20170416T003941_016162_01AB45_68E5.tif"'
