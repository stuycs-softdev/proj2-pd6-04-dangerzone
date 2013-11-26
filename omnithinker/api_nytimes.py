import json
from urllib2 import urlopen
from collections import defaultdict

NYT_API_URL = 'http://api.nytimes.com/svc/search/v2/articlesearch'

def FindArticles(Topic):
    API_KEY = '5772CD9A42F195C96DA0E930A7182688:14:68439177'
    FORMAT = ".json"
    Q = str(Topic)
    FQ = "The New York Times"
    BEGIN_DATE = 19000101
    FACET_FIELD = "section_name"
    FACET_FILTER = 1
    HL = 1

    url = ('http://api.nytimes.com/svc/search/v2/articlesearch%s?q=%s&fq=%s&facet_field=&%s&facet_filter=%s&begin_date=%d&hl=%s&api-key=%s') % (FORMAT, Q, FQ, FACET_FIELD, FACET_FILTER, BEGIN_DATE, HL, API_KEY)
    reponse = urlopen(url)
    Json_Data = json.loads(response.read())

    NYT_Filter = dict('Title':, 'Text':, 'URL', 'Topics':)
    for x in docs:
    NYT_Filter['Title'] = NYT_Filter['Title'] + ' ' + Json_Data['docs']['headline'][0]
    NYT_Filter['Text'] = Json_Data['docs']['lead_paragraph']
    return Json_Data

if __name__ == '__main__':
    FindArticles("Apples")
