
from osgeo import gdal
import numpy
from os import listdir,path,walk
import sys
import time
from numba import jit
def water(fileName,outFileName=None):
    ds=gdal.Open(fileName)
    rows=ds.RasterYSize
    columns=ds.RasterXSize
    print rows,columns
    driver = gdal.GetDriverByName('GTIFF')
    outRaster = driver.Create(outFileName, columns, rows, 1, gdal.Byte,[NBITS=2])
    outRaster.SetGeoTransform(ds.GetGeoTransform())
    outband = outRaster.GetRasterBand(1)
    outRaster.SetProjection(ds.GetProjection())
    parts=3
    for i in range(0,parts):
        if i<parts-1:
            p=columns/parts
        else:
            p=columns-i*columns/parts
        for j in range(0,parts):
            outArray=numpy.zeros((rows/parts,columns/parts),dtype=numpy.float)
            if j<parts-1:
                q=rows/parts
            else:
                q=rows-j*rows/parts
            bands=ds.ReadAsArray(i*columns/parts,j*rows/parts,p,q)
            outArray=numbaCls(q,p,bands,outArray)
            print (outArray.shape,i*columns/parts,j*rows/parts)
            outband.WriteArray(outArray,i*columns/parts,j*rows/parts)
            print "part",i,j,"done"
@jit(nopython=True,nogil=True)
def numbaCls(rows,columns,bands,outArray):
    for i in range(0,rows):
        for j in range(0,columns):
            if float(bands[0][i][j]) and float(bands[1][i][j]):
                swi=0.1747*bands[0][i][j]+0.0082*bands[1][i][j]*bands[0][i][j]+0.0023*(bands[0][i][j]*bands[0][i][j])-0.0015*(bands[1][i][j]*bands[1][i][j])+0.1904
            # print(i,j,swi)
            if (swi>0.12 and swi<2):
                outArray[i][j]=1
        # print i,j

    return outArray
if __name__=="__main__":
    water('C:\\Users\\Bharath\\Downloads\\S1A_IW_GRDH_1SDV_20171118T003949_20171118T004014_019312_020B96_9FF1.tif')
