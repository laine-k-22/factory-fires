import scrapy
from urllib.parse import urlencode
from urllib.parse import urlparse
import json

API_KEY = '5a20db4a9d1d2bb075e8e760340281e4'


def get_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'autoparse': 'true', 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


# Num parameter indicates results per page. (max is 100)
def create_google_url(query, site=''):
    google_dict = {'q': query, 'num': 100, }
    if site:
        web = urlparse(site).netloc
        google_dict['as_sitesearch'] = web
        return 'http://www.google.com/search?' + urlencode(google_dict)
    return 'http://www.google.com/search?' + urlencode(google_dict)


class GoogleSpider(scrapy.Spider):

    name = 'google'
    allowed_domains = ['api.scraperapi.com']
    custom_settings = {'ROBOTSTXT_OBEY': False,
                       'LOG_LEVEL': 'INFO',
                       'CONCURRENT_REQUESTS_PER_DOMAIN': 15,
                       'RETRY_TIMES': 5,
                       'DOWNLOAD_DELAY': 10,
                       'AUTOTHROTTLE_ENABLE': True}

    def start_requests(self):

        queries = ["poultry+plant+fire",
                   "food+facility+fire",
                   "food+factory+fire",
                   "juice+factory+fire",
                   "grain+factory+fire",
                   "rice+plant+fire",
                   "wheat+factory+fire",
                   "meat+processing+plant+fire",
                   "food+processing+plant+fire",
                   "food+processing+facility+fire",
                   "meat+processing+facility+fire",
                   "pork+plant+fire",
                   "milk+powder+plant+fire",
                   "food+pantry+fire",
                   "beef+plant+fire",
                   "meat+company+fire",
                   "milk+parlor+fire",
                   "soy+processing+plant+fire",
                   "fertilizer+plant+fire"

                   "Kellogg's+plant+fire"
                   "Nestle+factory+fire",
                   "tyson+foods+factory+fire",
                   "JBS+USA+factory+fire",
                   "kraft+heinz+co+factory+fire",
                   "PepsiCo+factory+fire",
                   "Archer+Daniels+Midland+company+factory+fire",
                   "Cargill+factory+fire",
                   "Sysco+Corporation+factory+fire",
                   "George+Weston+factory+fire",
                   "Danone+factory+fire",
                   "Mondelez+factory+fire",
                   "Coca-Cola+factory+fire",
                   "Smithfield+Foods+factory+fire",
                   "Lactalis+factory+fire",
                   "Kraft+Heinz+factory+fire",
                   "Danone+factory+fire",
                   "CHS+Inc+factory+fire",
                   "Mars+factory+fire",
                   "Associated+British+Foods+PLC+factory+fire",
                   "ABP+Food+Group+factory+fire",
                   "Noble+Foods+factory+fire",
                   "Unilever+factory+fire",
                   "Glendale+Foods+factory+fire",
                   "The+Little+Big+Food+Company+factory+fire",
                   "Fresh+Food+Company+factory+fire",
                   "Weetabix+Food+Company+factory+fire",
                   "Grace+Foods+UK+factory+fire",
                   "2+Sisters+Food+Group+factory+fire",
                   "Greencore+Convenience+Foods+factory+fire",
                   "Arla+Foods+UK+factory+fire",
                   "Muller+UK+factory+fire",
                   "Unilever+factory+fire",
                   "Bakkavor+factory+fire",
                   "Mondelez+factory+fire"
                   ]

        for query in queries:
            url = create_google_url(query)
            yield scrapy.Request(get_url(url), callback=self.parse, meta={'pos': 0})

    def parse(self, response):

        di = json.loads(response.text)
        pos = response.meta['pos']

        for result in di['organic_results']:
            title = result['title']
            snippet = result['snippet']
            link = result['link']
            item = {'title': title, 'snippet': snippet, 'link': link, 'position': pos}
            pos += 1
            yield item
        next_page = di['pagination']['nextPageUrl']
        if next_page:
            yield scrapy.Request(get_url(next_page), callback=self.parse, meta={'pos': pos})
