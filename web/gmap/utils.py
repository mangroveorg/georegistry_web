import pycurl, StringIO
from django.conf import settings

def query_georegistry(URL,
                  GR_SERVER=settings.GR_SERVER,
                  USERNAME=settings.GR_USER,
                  PASSWORD=settings.GR_PASS):
    """Query GR"""
    response_dict={}
    user_and_pass="%s:%s" % (USERNAME, PASSWORD)
    URL= GR_SERVER + str(URL)
    c = pycurl.Curl()
    c.setopt(pycurl.URL, URL)
    c.setopt(c.SSL_VERIFYPEER, False)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    json_string= b.getvalue()
    return json_string