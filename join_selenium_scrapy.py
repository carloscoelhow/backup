import json


with open('tripadvisor_selenium.json','r') as f: 
    trip_selenium=json.load(f)

with open('tripadvisor_scrapy.json','r') as f: 
    trip_scrapy=json.load(f)


urls_done=[] 
for i in range(len(trip_scrapy)): 
    if trip_scrapy[i]['url_found']==False: 
        trip_scrapy[i]['comments_complete']=['not_found']*len(trip_scrapy[i]['body']) 
        trip_scrapy[i]['match']=[False]*len(trip_scrapy[i]['body']) 
        trip_scrapy[i]['url_found']=False 
        for k in range(len(trip_selenium)): 
            if trip_scrapy[i]['url']==trip_selenium[k]['url']: 
                trip_scrapy[i]['url_found']=True 
                if not trip_selenium[k]['url'] in urls_done: 
                    urls_done.append(trip_scrapy[i]['url']) 
                    for j in range(len(trip_scrapy[i]['body'])): 
                        for q in range(len(trip_selenium[k]['comments'])): 
                            if trip_scrapy[i]['body'][j][:100]==trip_selenium[k]['comments'][q][:100]:  
                                trip_scrapy[i]['comments_complete'][j]=trip_selenium[k]['comments'][q] 
                                trip_scrapy[i]['match'][j]=True 
        if trip_scrapy[i]['url_found']==True: 
            for w in range(len(trip_scrapy[i]['comments_complete'])): 
                if trip_scrapy[i]['comments_complete'][w]=='not_found': 
                    trip_scrapy[i]['comments_complete'][w]=trip_scrapy[i]['body'][w] 
        #if len(urls_done) % 100 == 0 and trip_scrapy[i]['url_found']==True: 
        #   print('\n{} urls done'.format(len(urls_done)))