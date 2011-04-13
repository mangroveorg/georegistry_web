from georegistry_web.web.gmap.utils import query_georegistry
import json

def fetch_total_count():
    """Get list of countries and total objects"""
    URL="api/1.0/counters/cached-total"
    r= query_georegistry(URL)
    total=json.loads(r)
    print total
    return total['count']

def fetch_countries_count():
    """Get list of countries and total objects"""
    URL="api/1.0/features/countries"
    r= query_georegistry(URL)
    countries=json.loads(r)
    cl=[]
    for c in countries:
        URL="api/1.0/counters/cached-country/%s" % (c.keys()[0])
        count= query_georegistry(URL)
        count=json.loads(count)

        if count.has_key('count'):
            c[c.keys()[0]].update({'count':count['count']})
            cl.append(c)

    """Get list of categories and total objects in each"""
    return cl
    
def fetch_categories_count():
    URL="api/1.0/features/classifiers"
    r= query_georegistry(URL)
    classifiers=json.loads(r)
    catlist=[]
    countlist=[]
    for cl in classifiers:
        catlist.append(cl['category'])
    catlist=list(set(catlist))
    print catlist
    
    for i in catlist:
        URL="api/1.0/counters/cached-classifier/category/%s" % (i)
        r= query_georegistry(URL)
        cat=json.loads(r)
        if cat.has_key('count'):
            if cat['count'] > 0:
                countlist.append({i :cat['count']})
    print countlist

    return countlist