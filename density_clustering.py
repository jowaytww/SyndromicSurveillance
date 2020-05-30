# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 14:28:14 2020

@author: Jayakrishnan Ajayakumar
"""


from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPoint
import psycopg2
import pandas as pd
import datetime
from dateutil import parser
import numpy as np
import geopandas as gpd
from dateutil import parser

#accepts a csv file with headers lat,lon,date. maxdistance is the distance for a neighbor relation, minneighbors is the
#minimum number of points for a cluster,start_date is the beginning date for grouping clusters by time (if None will automatically assign the first date from the dataset)
#end_date is the last date for grouping clusters by time. By default it is the current date
def runClusterAnalysis(datafile,maxdistance=100,minneighbors=2,start_date=None,end_date=datetime.datetime.now().date()):
    if not datafile.endswith('.csv'):
        print ('Only accepts csv file')
        return None
    data=pd.read_csv(datafile)
    if not ('lon' in data.columns and 'lat' in data.columns and 'date' in data.columns):
        print ('Data file should have columns lat,lon,date')
        return None
    data.date=[parser.parse(t).date() for t in data.date]
    if start_date is None:
        start_date=np.min(data.date.values)
    #headers for the cluster file
    recheader=['id','centroid_x','centroid_y']
    #generate date columns
    datevals=[start_date+datetime.timedelta(days=i) for i in range((end_date-start_date).days+1)]
    recheader.extend(datevals)
    #need to convert lat/lon to meters. Reprojecting to UTM 17N
    gpframe=gpd.GeoDataFrame(data,geometry=gpd.points_from_xy(data.lon, data.lat))
    gpframe.crs={'init': 'epsg:4326'}
    gpframe=gpframe.to_crs({'init': 'epsg:26917'})
    data['x']=[geom.x for geom in gpframe.geometry]
    data['y']=[geom.y for geom in gpframe.geometry]
    #remove the additional geometry column
    data=data.drop(columns=['geometry'])
    xy=data[['x','y']].values
    latlon=data[['lon','lat']].values
    dates=data['date'].values
    #empty data frame for storing clusters
    clusterData=pd.DataFrame(columns=recheader)
    #run DB scan clustering algorithm
    clustering = DBSCAN(eps=maxdistance, min_samples=minneighbors,algorithm='kd_tree').fit(xy)
    #cluster labels
    labels = clustering.labels_
    total_clusters = len(set(labels))
    k=0
    geometries=[]
    ids=[]
    #for each cluster get the members and group by date
    for i in range(total_clusters):
        ltln=latlon[labels==i]
        date=dates[labels==i]
        prjpoints=xy[labels==i]
        if len(ltln)!=0 and len(ltln)>=minneighbors:
            tdframe=pd.DataFrame(columns=['date'])
            tdframe.date=datevals
            newdframe=pd.DataFrame(columns=['date','counts'])
            #aggregate counts based on date
            unique, counts = np.unique(date, return_counts=True)
            newdframe.date=unique
            newdframe.counts=counts
            tdframe=tdframe.merge(newdframe,on='date',how='outer')
            tdframe=tdframe.fillna(0)
            #cumulative sum for the dates
            cnts=np.cumsum(tdframe.counts.values)
            #set zero for total neighbors
            cnts[cnts<minneighbors]=0
            tdframe.counts=cnts
            #for generating centroids
            geom=MultiPoint(ltln)
            dat=[k,geom.centroid.x,geom.centroid.y]
            ids.append(k)
            geom_proj=MultiPoint(prjpoints)
            #convex hulls based on all members
            geom_hull=geom_proj.convex_hull
            if geom_hull.geom_type!='Polygon':
                geom_hull=geom_hull.buffer(maxdistance)
            geometries.append(geom_hull)
            dat.extend(tdframe.counts.values.tolist())
            clusterData.loc[len(clusterData)]=dat
            k+=1
    #write cluster data to csv file
    clusterData.to_csv(datafile.replace('.csv','')+"_centroids_"+str(maxdistance)+"_"+str(minneighbors)+'.csv',index=False)
    #write cluster shapes to CSV
    gdf = gpd.GeoDataFrame(pd.DataFrame(ids,columns=['id']), geometry=geometries,crs={'init': 'epsg:26917'})
    gdf.to_file(datafile.replace('.csv','')+"_shapes_"+str(maxdistance)+"_"+str(minneighbors)+'.shp') 

#Test
#runClusterAnalysis(r'E:/data-1590796735022.csv',maxdistance=1000,minneighbors=10)      
