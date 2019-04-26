from osgeo import gdal,ogr,osr
import numpy
from os import listdir,path,walk
import sys
import time
from numba import jit
def water(raster):
    ds=gdal.Open(raster)
    ds1=gdal.Open(raster[0:-5]+'3.jp2')
    rows=ds.RasterYSize
    columns=ds.RasterXSize
    print rows,columns
    driver = gdal.GetDriverByName('GTIFF')
    outRaster = driver.Create(raster[:-6]+'ndwia.tif', columns, rows, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform(ds.GetGeoTransform())
    outband = outRaster.GetRasterBand(1)
    outRaster.SetProjection(ds.GetProjection())
    outRaster1 = driver.Create(raster[:-6]+'ndwia1.tif', columns, rows, 1, gdal.GDT_Float32)
    outRaster1.SetGeoTransform(ds.GetGeoTransform())
    outband1 = outRaster1.GetRasterBand(1)
    outRaster1.SetProjection(ds.GetProjection())
    shpFile = raster[:-6]+'1.shp'
    drv = ogr.GetDriverByName("ESRI Shapefile")
    dstDs = drv.CreateDataSource(shpFile)
    dstLayer = dstDs.CreateLayer(shpFile, srs = None )
    idField = ogr.FieldDefn("pixelvalue", ogr.OFTReal)
    dstLayer.CreateField(idField)
    parts=3
    for i in range(0,parts):
        if i<parts-1:
            p=columns/parts
        else:
            p=columns-i*columns/parts
        for j in range(0,parts):
            outArray=numpy.zeros((rows/parts,columns/parts),dtype=numpy.float)
            outArray1=numpy.zeros((rows/parts,columns/parts),dtype=numpy.int8)
            if j<parts-1:
                q=rows/parts
            else:
                q=rows-j*rows/parts
            nirband=ds.ReadAsArray(i*columns/parts,j*rows/parts,p,q)
            gband=ds1.ReadAsArray(i*columns/parts,j*rows/parts,p,q)
            outArray,outArray1=numbaCls(q,p,nirband,gband,outArray,outArray1)
            print (outArray.shape,i*columns/parts,j*rows/parts)
            outband.WriteArray(outArray,i*columns/parts,j*rows/parts)
            outband1.WriteArray(outArray1,i*columns/parts,j*rows/parts)
            print "part",i,j,"done"
        outband.FlushCache()
        outband1.FlushCache()
    gdal.Polygonize( outband1, None , dstLayer, 0, [], callback=None )
    i=0
    print "filtering...."
    for feature in dstLayer:
        if feature.GetField('pixelvalue')==0:
            dstLayer.DeleteFeature(i)
        i=i+1
    spatialRef = osr.SpatialReference()
    spatialRef.ImportFromWkt(ds.GetProjection())
    spatialRef.MorphToESRI()
    f = open(shpFile[:-3]+'prj', 'w')
    f.write(spatialRef.ExportToWkt())
    f.close()
@jit(nopython=True,nogil=True)
def numbaCls(rows,columns,nirband,gband,outArray,outArray1):
    for i in range(0,rows):
        for j in range(0,columns):
            if float(gband[i][j]+nirband[i][j])!=0:
                outArray[i][j]=(float(gband[i][j])-float(nirband[i][j]))/(float(gband[i][j])+float(nirband[i][j]))
                if float(outArray[i][j])>0.1:
                    outArray1[i][j]=1

            # if float(bands[0][i][j]) and float(bands[1][i][j]):
            #     swi=0.1747*bands[0][i][j]+0.0082*bands[1][i][j]*bands[0][i][j]+0.0023*(bands[0][i][j]*bands[0][i][j])-0.0015*(bands[1][i][j]*bands[1][i][j])+0.1904
            # # print(i,j,swi)
            # if (swi>0.12 and swi<2):
            #     outArray[i][j]=1
        # print i,j

    return outArray,outArray1
if __name__=="__main__":
    nirb="C:\\Users\\Bharath\\Documents\\NHP\\Sentinel-ATP\\outputs\\validationAtp171118\\S2A_MSIL1C_20171123T052131_N0206_R062_T43PGS_20171123T091125\\S2A_MSIL1C_20171123T052131_N0206_R062_T43PGS_20171123T091125.SAFE\\GRANULE\\L1C_T43PGS_A012643_20171123T052655\\IMG_DATA\\T43PGS_20171123T052131_B08.jp2"
    water(nirb)
