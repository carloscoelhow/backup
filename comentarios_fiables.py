for i in range(len(trip_scrapy)): 
	trip_scrapy[i]['trustworthy']=False 
	
	if not False in trip_scrapy[i]['match'] and (len(trip_scrapy[i]['body'])==len(trip_scrapy[i]['comentario_rating'])): 
	trip_scrapy[i]['trustworthy']=True