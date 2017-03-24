import urllib
import urllib2
from bs4 import BeautifulSoup
from clint.textui import progress
import requests
import sqlite3
import time
import os
from fake_useragent import UserAgent

conn = sqlite3.connect('TVShows.sqlite')
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
cur = conn.cursor()
# ua = UserAgent()
# ua = 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>'
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36"

def showname(): # USER INPUT: Collect Title
    global sname
    sname = raw_input('Enter the Name of The Show: ').lower()

def testif(sname): #Determine what Page Cluster TV Show resides on o2tvseries.com
    if sname[0] < 'd':
        print sname[0], sname, 'Group A'
        pageurl = '/a'
    elif sname[0] >='d' and sname[0] < 'g':
        print sname[0], sname, 'Group D'
        pageurl = '/d'
    elif sname[0] >='g' and sname[0] < 'j':
        print sname[0], sname, 'Group G'
        pageurl = '/g'
    elif sname[0] >='j' and sname[0] < 'm':
        print sname[0], sname, 'Group J'
        pageurl = '/j'
    elif sname[0] >='m' and sname[0] < 'p':
        print sname[0], sname, 'Group M'
        pageurl = '/m'
    elif sname[0] >='p' and sname[0] < 's':
        print sname[0], sname, 'Group P'
        pageurl = '/p'
    elif sname[0] >='s' and sname[0] < 'v':
        print sname[0], sname, 'Group S'
        pageurl = '/s'
    elif sname[0] >='v' and sname[0] < 'y':
        print sname[0], sname, 'Group V'
        pageurl = '/v'
    elif sname[0] >='Y':
        print sname[0], sname, 'Group Y'
        pageurl = '/y'
    return pageurl

def openurl(url):
	request = urllib2.Request(url)
	opener = urllib2.build_opener()
	request.add_header('User-Agent', ua)
	data = opener.open(request).read()
    #return urllib.urlopen(url).read()
	return data

def get_tags(url):
    html = openurl(url)
    soup = BeautifulSoup(html, 'html.parser')
    #print html
    tags = soup.find_all('a')
    return tags

def id_url(): # Obtain TV Show's Home page url
    global pageno, url, found, folder,statement
    while found == False:
        tags = get_tags(url)
        #print tags
        for tag in tags:
            try:
                #print str(tag.string).lower(), type(str(tag.string)), sname[0], type(sname[0])
                #for word in sname:

                if sname[0] in str(tag.string).lower():
                    if len(sname) > 1:
                        print "yes sname is greater than 1"
                        if sname[1] in str(tag.string).lower():
                            print "yes the second word exists"
                            if len(sname) > 2:
                                if sname[2] in str(tag.string).lower():
                                    print tag
                                    url = tag.get('href')
                                    folder = tag.string
                                    print cur
                                    statement = "CREATE TABLE IF NOT EXISTS '%s' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Season TEXT, Episode TEXT, Filename TEXT, Filesize INTEGER, Download_time DATE)" % (folder)
                                    print statement
                                    cur.execute(statement)
                                    found = True
                                    return url
                                else:
                                    continue
                            print tag
                            url = tag.get('href')
                            folder = tag.string
                            print cur
                            statement = "CREATE TABLE IF NOT EXISTS '%s' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Season TEXT, Episode TEXT, Filename TEXT, Filesize INTEGER, Download_time DATE)" % (folder)
                            print statement
                            cur.execute(statement)
                            found = True
                            return url
                        else:
                            continue

                    print tag
                    url = tag.get('href')
                    folder = tag.string
                    print cur
                    statement = "CREATE TABLE IF NOT EXISTS '%s' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Season TEXT, Episode TEXT, Filename TEXT, Filesize INTEGER, Download_time DATE)" % (folder)
                    print statement
                    cur.execute(statement)
                    found = True
                    return url
                else:
                    continue
            except:
                continue
        conn.commit()
        pageno += 1
        #print pageno
        page = "/page" + str(pageno)+ ".html"
        url = urlstatic + page
        #print url
        if pageno == 10:
            print "Title not available"
            break

def get_seasons():
    seasons = []
    title = []
    season_name= []
    tags = get_tags(id_url())

    for tag in tags:
        if 'season' in str(tag.string).lower():
            #print tag.get('href')
            seasons.append(tag.get('href'))
            title.append(folder)
            season_name.append(tag.string)
    return (sorted(seasons),sorted(title), sorted(season_name))

def get_episodes():
    seasons_and_titles = get_seasons()
    seasons = seasons_and_titles[0]
    titles = seasons_and_titles[1]
    season_names = seasons_and_titles[2]


    season_name = []


    seasons2 ={}
    print season_names
    for item in range(len(seasons)):
        episodes = []
        episode_name = []
        pages = 1
        tags = get_tags(seasons[item])
        #print seasons[item]
        while True:
            for tag in tags:
                try:
                    #strtag = str(tag.string).lower()
                    #print 'strtag is ', strtag
                    if 'episode' in tag.string.lower():
                        #print tag.get('href')
                        episodes.append(tag.get('href'))
                        episode_name.append(tag.string)
                        show_name.append(titles[item])
                        #print season_names
                except:
                    continue

            #season_name.append(season_names[item])
            pages += 1
            nxtpage = 'page'+ str(pages)+ '.html'
            #print 'nextpage is', nxtpage

            for tag in tags:
                #print tag
                if nxtpage in str(tag).lower():
                    tags = get_tags(seasons[item][:-10]+ nxtpage)
                    #print seasons[item][:-10]+ nxtpage
                    break
                else:
                    continue
            else:
                break
            #print seasons2
        episodes2 = {}
        for items in range(len(episodes)):
            #print episodes[items]
            episodes2[episode_name[items]] = episodes[items]
            #print episodes[items], episode_name[items]
            #print 'item is ' , item, season_name[item]
            #print season_name

        seasons2[season_names[item]] = episodes2


    return (sorted(episodes),sorted(episode_name), sorted(season_names), folder, seasons2)

def get_referrer():
    referrer = []
    filename = []
    alldata = get_episodes()
    #episodes = alldata[0]
    #episode_names = alldata[1]
    season_names = alldata[2]
    show_names = alldata[3]
    seasons2 = alldata[4]
    episodes = []

    #print season_names

    for season in season_names:
        #print season, " and ", seasons2[season]
        for episode, url in seasons2[season].iteritems():
            # print episode, ' and ', url
            tags = get_tags(url)
            for tag in tags:
                if '.mp4' in str(tag.string).lower():
                    episodes.append([folder, season, episode, url, tag.get('href'), tag.string])





    '''for item in range(len(episodes)):
        tags = get_tags(episodes[item])
        for tag in tags:
            if '.mp4' in str(tag.string).lower():
                referrer.append(tag.get('href'))
                filename.append(tag.string)
                episode_url.append(episodes[item])
                episode_name.append(episode_names[item])
                season_name.append(season_names[item])
                show_name.append(show_names[item])
                #print tag.get('href')
    return [referrer,filename,episode_url,episode_name,season_name,show_name]'''
    return episodes

def rest_of_program(show_name):
    global sname, url, urlstatic
    sname = show_name.lower()
    url = source + testif(sname)
    urlstatic = url
    print url
    print sname
    sname = sname.split()
    print sname

    files = get_referrer()
    filename = files[1]
    referrer = files[0]
    episode_url = files[2]
    episode_name = files[3]
    season_name = files[4]
    show_name = files[5]


    statement2 = "SELECT Season, Episode from '%s'" % (folder)
    cur.execute(statement2)
    dbcheck = cur.fetchall()



    for item in sorted(files):
        if (item[1],item[2]) in dbcheck:
            print (item[1],item[2]), 'has been downloaded'
        else:
            print (item[1],item[2]), 'has not been downloaded'
            #print item[0],item[1],item[2],item[3],item[4],item[5]
            name= "/Users/simulations/Downloads/TVshows/%s/%s/%s" % (folder,item[1],item[5])
            folderpath = "/Users/simulations/Downloads/TVshows/%s/%s" % (folder,item[1])
            if not os.path.exists(folderpath):
               os.makedirs(folderpath)
               os.chmod(folderpath, 0o777)
            """print "Downloading....."
            urllib.urlretrieve(referrer[item],filename=name)
            break"""
            r = requests.get(str(item[4]), stream=True)
            #total_length = int(r.headers.get('content-length'))
            path = name
            with open(path, 'wb') as f:
                #print item[4]
                total_length = int(r.headers.get('content-length'))
                print item[5]
                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            statement3 = "INSERT INTO '%s' (Season, Episode, Filename, Filesize, Download_time) VALUES(?, ?, ?, ?, ?)" % (folder)
            cur.execute(statement3, (item[1],item[2],item[5],total_length,time.strftime("%d/%m/%Y|%H:%M:%S")))
        conn.commit()

def start_program():
    global sname, source, pageno, found, folder, statement
    actionact = raw_input("Download New Show or Update Current Show Repertoire? Enter 'New' or 'Update'").lower()
    if actionact == 'new':
        sname = None
        showname()
        sname = sname.lower()
        source = 'http://o2tvseries.com'
        # source = 'http://tvshows4mobile.com'
        pageno = 1
        found = False
        folder = None
        statement = None
        rest_of_program(sname)

    elif actionact == 'update':
        tvshows =[
        'Arrow','Legends of tomorrow',
        'Blindspot','Agents of shield','Empire',
        'Daredevil','Game of Thrones', 'Gotham',
        'Greys Anatomy','How to get away with murder',
        'Heroes Reborn','Mistresses', 'Orange is the new black',
        'Modern family', 'Reign', 'Quantico', 'The flash',
        'Scandal','Vikings','Jessica Jones', 'Luke Cage', 'Supergirl']
        for show in sorted(tvshows):
            sname = None
            sname = show.lower()
            source = 'http://o2tvseries.com'
            # source = 'http://tvshows4mobile.com'
            pageno = 1
            found = False
            folder = None
            statement = None
            #showname()
            rest_of_program(sname)

    else:
        print "Invalid Entry, Please Thy Again"
        start_program()


start_program()

#Power
