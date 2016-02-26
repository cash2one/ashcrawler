# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Feb 25, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


import urllib2,urllib,json
import sqlite3, time
import sys, os
import ssl, socket
from shutil import copy

COUNT = 50
COUNT2 = 100
reload(sys)
sys.setdefaultencoding('utf-8')

current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]


def getResponseObject(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    request = urllib2.Request(url = url,headers = headers)
    content = "{}"
    msg = 'Something wrong with this crawler server.'
    #print url
    #time.sleep(1)
    try:
        response = urllib2.urlopen(request, timeout = 5)
        content = response.read()
    except urllib2.URLError, e:
        msg = msg + '\n' + url + '\n' + str(e)
        if str(e) == 'HTTP Error 403: Forbidden':
            #over the limits
            #sendEmail('jakobzhao@gmail.com', msg, '')
            print "this service has been shut down."
            sys.exit(0)
        if str(e) == 'HTTP Error 400: Bad Request':
            print "this service has been shut down."
            sys.exit(0)
    except ssl.SSLError,e:
        msg = msg + '\n' + url + '\n' + str(e)
        print msg
        #sendEmail('jakobzhao@gmail.com', msg, '')
    if 'error' in json.loads(content):
        msg = msg + json.loads(content)['error'] + '\n' + url
        print msg
        #sendEmail('jakobzhao@gmail.com', msg, '')
        sys.exit(0)
    try:
        obj = json.loads(content)
    except ValueError, e:
        print "********************************************"
        print "the content of the response is:" + content
        obj = json.loads('{}')
        print  "json loading value error!", e.args[0]
    return obj

def searchTermsFromUser(uid, terms, database, page):
    #heuristic searching
    #if topic ="", then it means to search all the statuses of this weibo.
    obj = getResponseObject('https://api.weibo.com/2/statuses/user_timeline.json?source=2933540621&count=1&uid=' + str(uid) + '&page=1&access_token=' + TOKEN)
    total_number = obj['total_number']
    while total_number >= COUNT2 * page:
        print "----------------------------Page" + str(page) + " starts----------------------------"
        obj = getResponseObject('https://api.weibo.com/2/statuses/user_timeline.json?source=2933540621&count=' + str(COUNT2)  + '&uid=' + str(uid) + '&page=' + str(page) +'&access_token=' + TOKEN)
        if obj == {}:
            continue
        for status in obj['statuses']:
            #if this status is related to the topic, then get it in.
            flag = False
            for term in terms:
                flag = flag or (term in status['text'])
            if flag and ('deleted' not in status.keys()):
                print status['text']
                processStatus(database, status)

        page = page + 1
        if page * COUNT2 > obj['total_number']:
            completed = 1
        else:
            completed = page * COUNT2/float(obj['total_number'])
        print "----------------------------Page" + str(page-1) + " ends.----------------------------"
        print "----------------------Retrieving Statuses:" +  str(round(completed*100,2)) + "%----------------------"
    print "Totally Finished!"

def processStatus(database, status):
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    keys = status.keys()

    if 'thumbnail_pic' not in keys:
        status['thumbnail_pic'] = 'None'
    if str(status['geo']) == '':
        status['geo'] = 'None'
    if str(status['geo']) != 'None':
        status['geo'] = str(status['geo']['coordinates'][0]) + "," + str(status['geo']['coordinates'][1])

    ############################statuses################################
    query_body_statuses = str(status['id']) + ", 0, '" + status['text'].replace("'", "''") + "', " + "datetime('" +  parseTime(status['created_at']) + "')" + ", '" + status['source'] + "', '" + str(status['geo']) +  "', '" + status['thumbnail_pic'] + "', '" + str(status['user']['id']) +  "', '" + status['user']['screen_name'] + "', " + str(status['reposts_count']) +  ", " + str(status['comments_count']) + ")"
    try:
        cursor.execute(query_header_statuses + query_body_statuses)
    except sqlite3.Error, e:
        #print  "This status has already been inserted.", e.args[0]
        pass

    ############################users################################
    query_body_users   = str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', '" + str(status['user']['province']) + "', '" + str(status['user']['city']) + "', '" + status['user']['location'] + "', '" + status['user']['description'].replace("'", "''") + "', '" + status['user']['url'] + "', '" + status['user']['profile_image_url'] + "', '" + status['user']['profile_url'] + "', '" + status['user']['domain'] + "', '" + str(status['user']['weihao']) + "', '" + status['user']['gender'] + "', " + "datetime('" +  parseTime(status['user']['created_at']) + "')" + ", '" + str(status['user']['geo_enabled']) + "', '" + str(status['user']['verified']) + "', '" + status['user']['avatar_large'] + "', '" + status['user']['verified_reason'] + "', '" + status['user']['lang'] + "', " + str(status['user']['bi_followers_count']) + ", " + str(status['user']['followers_count']) + ", " + str(status['user']['friends_count']) + ", " + str(status['user']['statuses_count']) + ", " + str(status['user']['favourites_count']) + ")"
    try:
        cursor.execute(query_header_users + query_body_users)
    except sqlite3.Error, e:
        #print  "This user has already been inserted.", e.args[0]
        pass

    ############################retweets################################
    if 'retweeted_status' in keys:
        cursor.execute("update statuses set status_type=1 where id == " + str(status['id']))
        if 'user' in status['retweeted_status'].keys():
            query_body_retweets = str(status['retweeted_status']['id'] + status['id']) + ", 1," + str(status['retweeted_status']['id']) + ", " + str(status['retweeted_status']['user']['id']) + ", '" + status['retweeted_status']['user']['screen_name'] + "', " + str(status['id']) + ", " + str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', " + "datetime('" +  parseTime(status['created_at']) + "')"  + ")"
            try:
                cursor.execute(query_header_retweets + query_body_retweets)
            except sqlite3.Error, e:
                #print  "This retweeted relationship has already been inserted.", e.args[0]
                pass

            query_body_users = str(status['retweeted_status']['user']['id']) + ", '" + status['retweeted_status']['user']['screen_name'] + "', '" + str(status['retweeted_status']['user']['province']) + "', '" + str(status['retweeted_status']['user']['city']) + "', '" + status['retweeted_status']['user']['location'] + "', '" + status['retweeted_status']['user']['description'].replace("'", "''") + "', '" + status['retweeted_status']['user']['url'] + "', '" + status['retweeted_status']['user']['profile_image_url'] + "', '" + status['retweeted_status']['user']['profile_url'] + "', '" + status['retweeted_status']['user']['domain'] + "', '" + str(status['retweeted_status']['user']['weihao']) + "', '" + status['retweeted_status']['user']['gender'] + "', " + "datetime('" +  parseTime(status['retweeted_status']['user']['created_at']) + "')" + ", '" + str(status['retweeted_status']['user']['geo_enabled']) + "', '" + str(status['retweeted_status']['user']['verified']) + "', '" + status['retweeted_status']['user']['avatar_large'] + "', '" + status['retweeted_status']['user']['verified_reason'] + "', '" + status['retweeted_status']['user']['lang'] + "', " + str(status['retweeted_status']['user']['bi_followers_count']) + ", " + str(status['retweeted_status']['user']['followers_count']) + ", " + str(status['retweeted_status']['user']['friends_count']) + ", " + str(status['retweeted_status']['user']['statuses_count']) + ", " + str(status['retweeted_status']['user']['favourites_count']) + ")"
            try:
                cursor.execute(query_header_users + query_body_users)
            except sqlite3.Error, e:
                #print  "This user has already been inserted.", e.args[0]
                pass

    ############################reposts##############################
    if status['reposts_count'] != 0:
        reposts_max_id = 0
        n = 0
        while status['reposts_count'] >= COUNT * n:
            if (n+1)*COUNT > status['reposts_count']:
                completed = 1
            else:
                completed = (n+1)*COUNT/float(status['reposts_count'])
            #print "Retrieving Reposts:" +  str(completed*100) + "%"
            n = n + 1
            reposts_obj = getResponseObject('https://api.weibo.com/2/statuses/repost_timeline.json?source=2933540621&id=' + str(status['id']) + '&count=' + str(COUNT) + '&max_id=' + str(reposts_max_id) + '&access_token=' + TOKEN)
            if reposts_obj == {} or reposts_obj == []:
                continue
            reposts_max_id = reposts_obj['next_cursor']
            for repost in reposts_obj['reposts']:
                keys_repost = repost.keys()

                if 'deleted' in keys_repost:
                    continue
                if str(repost['geo']) == '':
                    repost['geo'] = 'None'
                if str(repost['geo']) != 'None' :
                    repost['geo'] = str(repost['geo']['coordinates'][0]) + "," + str(repost['geo']['coordinates'][1])

                query_body_retweets  = str(repost['id'] + status['id']) + ", 1," + str(status['id']) + ", " + str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', " + str(repost['id']) + ", " + str(repost['user']['id']) + ", '" + repost['user']['screen_name'] + "', " + "datetime('" +  parseTime(repost['created_at']) + "')" + ")"
                query_body_statuses = str(repost['id']) + ", 1, '" + repost['text'].replace("'", "''") + "', " + "datetime('" +  parseTime(repost['created_at']) + "')" + ", '" + repost['source'] + "', '" + str(repost['geo']) +  "', '" + "None" +  "', '" + str(repost['user']['id']) +  "', '" + repost['user']['screen_name'] + "', " + str(repost['reposts_count']) +  ", " + str(repost['comments_count']) + ")"

                try:
                    cursor.execute(query_header_retweets + query_body_retweets)
                except sqlite3.Error, e:
                    #print "This repost relationship has been inserted,", e.args[0]
                    pass

                try:
                    cursor.execute(query_header_statuses + query_body_statuses)
                except sqlite3.Error, e:
                    #print  "This repost has already been inserted.", e.args[0]
                    pass

                query_body_users   = str(repost['user']['id']) + ", '" + repost['user']['screen_name'] + "', '" + str(repost['user']['province']) + "', '" + str(repost['user']['city']) + "', '" + repost['user']['location'] + "', '" + repost['user']['description'].replace("'", "''") + "', '" + repost['user']['url'] + "', '" + repost['user']['profile_image_url'] + "', '" + repost['user']['profile_url'] + "', '" + repost['user']['domain'] + "', '" + str(repost['user']['weihao']) + "', '" + repost['user']['gender'] + "', " + "datetime('" +  parseTime(repost['user']['created_at'])  + "')" + ", '" + str(repost['user']['geo_enabled']) + "', '" + str(repost['user']['verified']) + "', '" + repost['user']['avatar_large'] + "', '" + repost['user']['verified_reason'] + "', '" + repost['user']['lang'] + "', " + str(repost['user']['bi_followers_count']) + ", " + str(repost['user']['followers_count']) + ", " + str(repost['user']['friends_count']) + ", " + str(repost['user']['statuses_count']) + ", " + str(repost['user']['favourites_count']) + ")"
                try:
                    cursor.execute(query_header_users + query_body_users)
                except sqlite3.Error, e:
                    #print  "This user has already been inserted.", e.args[0]
                    pass

    ############################comments################################
    if status['comments_count'] != 0:
        #print 'comments:' + str(status['comments_count'])
        #print str(status['id'])
        comments_max_id = 0
        n = 0
        while status['comments_count'] >= COUNT*n:
            if (n+1)*COUNT > status['comments_count']:
                completed = 1
            else:
                completed = (n+1)*COUNT/float(status['comments_count'])
            #print "Retrieving Comments:" +  str(completed*100) + "%"
            n = n + 1
            #time.sleep(2) #helpful when try to limit the request to a certain amount
            comments_obj = getResponseObject('https://api.weibo.com/2/comments/show.json?source=2933540621&id=' + str(status['id']) + '&count=' + str(COUNT) + '&max_id=' + str(comments_max_id) + '&access_token=' + TOKEN)
            if comments_obj == {}:
                continue
            comments_max_id = comments_obj['next_cursor']

            for comment in comments_obj['comments']:
                keys_comment = comment.keys()
                query_body_retweets  = str(comment['id'] + status['id']) + ", 2," + str(status['id']) + ", " + str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', " + str(comment['id']) + ", " + str(comment['user']['id']) + ", '" + comment['user']['screen_name'] + "', " + "datetime('" +  parseTime(comment['created_at']) + "')" + ")"
                query_body_comments = str(comment['id']) + ", 2, '" + comment['text'].replace("'", "''") + "', " + "datetime('" +  parseTime(comment['created_at']) + "')" + ", '" + comment['source'] + "', '" + str(comment['user']['id']) +  "', '" + comment['user']['screen_name'] + "')"

                try:
                    cursor.execute(query_header_retweets + query_body_retweets)
                except sqlite3.Error, e:
                    #print "This comment relationship has already been inserted.", e.args[0]
                    pass

                try:
                    cursor.execute(query_header_comments + query_body_comments)
                except sqlite3.Error, e:
                    #print  "This comment has already been inserted.", e.args[0]
                    pass

                query_body_users   = str(comment['user']['id']) + ", '" + comment['user']['screen_name'] + "', '" + str(comment['user']['province']) + "', '" + str(comment['user']['city']) + "', '" + comment['user']['location'] + "', '" + comment['user']['description'].replace("'", "''") + "', '" + comment['user']['url'] + "', '" + comment['user']['profile_image_url'] + "', '" + comment['user']['profile_url'] + "', '" + comment['user']['domain'] + "', '" + str(comment['user']['weihao']) + "', '" + comment['user']['gender'] + "', " + "datetime('" +  parseTime(comment['user']['created_at'])  + "')" + ", '" + str(comment['user']['geo_enabled']) + "', '" + str(comment['user']['verified']) + "', '" + status['user']['avatar_large'] + "', '" + comment['user']['verified_reason'] + "', '" + comment['user']['lang'] + "', " + str(comment['user']['bi_followers_count']) + ", " + str(comment['user']['followers_count']) + ", " + str(comment['user']['friends_count']) + ", " + str(comment['user']['statuses_count']) + ", " + str(comment['user']['favourites_count']) + ")"
                try:
                    cursor.execute(query_header_users + query_body_users)
                except sqlite3.Error, e:
                    #print  "This user has already been inserted.", e.args[0]
                    pass

                if 'reply_comment' in keys_comment:
                    query_body_retweets  = str(comment['id'] + comment['reply_comment']['id']) + ", 3," + str(comment['reply_comment']['id']) + ", " + str(comment['reply_comment']['user']['id']) + ", '" + comment['reply_comment']['user']['screen_name'] + "', "  +  str(comment['id']) + ", " + str(comment['user']['id']) + ", '" + comment['user']['screen_name'] +  "', datetime('" +  parseTime(comment['created_at']) + "') )"
                    try:
                        cursor.execute(query_header_retweets + query_body_retweets)
                    except sqlite3.Error, e:
                        #print  "This reply-comment relationship has already been inserted.", e.args[0]
                        pass
    #t = t + 1
    #print '--------------------------------------' + str(round(t/float(len(obj['statuses']))*100/4,2)+ (t-1)*100/4) + '%' + '--------------------------------------'
    conn.commit()
    conn.close()

def parseTime(timestring):
    struct_time = time.strptime(timestring, '%a %b %d %H:%M:%S +0800 %Y')
    return time.strftime('%Y-%m-%d %H:%M:%S',struct_time)

def processTerms(terms, pages, database):
    for term in terms:
        processTerm(term, pages, database)

def processTerm(term, pages, database):
    i = 0
    while i < pages:
        i = i + 1
        obj = getResponseObject('https://api.weibo.com/2/search/topics.json?source=2933540621&q='+ urllib.quote(term) + '&count=50&page=' + str(i))
        if obj == {}:
            continue
        t = 0
        for status in obj['statuses']:
            if 'deleted' not in status.keys():
                processStatus(database, status)
            t = t + 1
            print '--------------------------------------' + str(round(t/float(len(obj['statuses']))*100/4,2)+ (i-1)*100/4) + '%' + '--------------------------------------'
    print "Congrat! it's done!"

# def save(shapePath, geoLocations, proj4):
#     'Save points in the given shapePath'
#     # Get driver
#     driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
#     # Create shapeData
#     shapePath = validateShapePath(shapePath)
#     if os.path.exists(shapePath):
#         os.remove(shapePath)
#     shapeData = driver.CreateDataSource(shapePath)
#     # Create spatialReference
#     spatialReference = getSpatialReferenceFromProj4(proj4)
#     # Create layer
#     layerName = os.path.splitext(os.path.split(shapePath)[1])[0]
#     layer = shapeData.CreateLayer(layerName, spatialReference, osgeo.ogr.wkbPoint)
#     layerDefinition = layer.GetLayerDefn()
#     # For each point,
#     for pointIndex, geoLocation in enumerate(geoLocations):
#         # Create point
#         geometry = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
#         geometry.SetPoint(0, geoLocation[0], geoLocation[1])
#         # Create feature
#         feature = osgeo.ogr.Feature(layerDefinition)
#         feature.SetGeometry(geometry)
#         feature.SetFID(pointIndex)
#         # Save feature
#         layer.CreateFeature(feature)
#         # Cleanup
#         geometry.Destroy()
#         feature.Destroy()
#     # Cleanup
#     shapeData.Destroy()
#     # Return
#     return shapePath
#
# def load(shapePath):
#     'Given a shapePath, return a list of points in GIS coordinates'
#     # Open shapeData
#     shapeData = osgeo.ogr.Open(validateShapePath(shapePath))
#     # Validate shapeData
#     validateShapeData(shapeData)
#     # Get the first layer
#     layer = shapeData.GetLayer()
#     # Initialize
#     points = []
#     # For each point,
#     for index in xrange(layer.GetFeatureCount()):
#         # Get
#         feature = layer.GetFeature(index)
#         geometry = feature.GetGeometryRef()
#         # Make sure that it is a point
#         if geometry.GetGeometryType() != osgeo.ogr.wkbPoint:
#             raise ShapeDataError('This module can only load points; use geometry_store.py')
#         # Get pointCoordinates
#         pointCoordinates = geometry.GetX(), geometry.GetY()
#         # Append
#         points.append(pointCoordinates)
#         # Cleanup
#         feature.Destroy()
#     # Get spatial reference as proj4
#     proj4 = layer.GetSpatialRef().ExportToProj4()
#     # Cleanup
#     shapeData.Destroy()
#     # Return
#     return points, proj4
#
# def merge(sourcePaths, targetPath):
#     'Merge a list of shapefiles into a single shapefile'
#     # Load
#     items = [load(validateShapePath(x)) for x in sourcePaths]
#     pointLists = [x[0] for x in items]
#     points = reduce(lambda x,y: x+y, pointLists)
#     spatialReferences= [x[1] for x in items]
#     # Make sure that all the spatial references are the same
#     if len(set(spatialReferences)) != 1:
#         raise ShapeDataError('The shapefiles must have the same spatial reference')
#     spatialReference = spatialReferences[0]
#     # Save
#     save(validateShapePath(targetPath), points, spatialReference)
#
# def getSpatialReferenceFromProj4(proj4):
#     'Return GDAL spatial reference object from proj4 string'
#     spatialReference = osgeo.osr.SpatialReference()
#     spatialReference.ImportFromProj4(proj4)
#     return spatialReference


# Validate

def validateShapePath(shapePath):
    'Validate shapefile extension'
    return os.path.splitext(str(shapePath))[0] + '.shp'

def validateShapeData(shapeData):
    'Make sure we can access the shapefile'
    # Make sure the shapefile exists
    if not shapeData:
        raise ShapeDataError('The shapefile is invalid')
    # Make sure there is exactly one layer
    if shapeData.GetLayerCount() != 1:
        raise ShapeDataError('The shapefile must have exactly one layer')
def ShapeDataError(msg):
    print msg
    pass
