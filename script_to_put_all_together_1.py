import json 
import sys

def read_json(file): 
    with open (file, 'r') as f: 
        data=json.load(f) 
    return data 



def add_file(data,trip_selenium): 
    parametro=[]
    if len(trip_selenium)>0: 
        for r in range(len(trip_selenium)):
            '''if not trip_selenium[r]['url'] in parametro:'''
            parametro.append(trip_selenium[r]['url'])
    
    for i in range(len(data)): 
        if not data[i]['url'] in parametro: 
            trip_selenium.append(data[i])
    print ('{} urls processed'.format(len(trip_selenium)))
    return trip_selenium

def save_data (trip_selenium):
    with open('trip_selenium_all_files_1.json','w') as f: 
        json.dump(trip_selenium,f)

def main():
    file_1=sys.argv[1]
    file_2=sys.argv[2]
    file_to_be_done=read_json(file_2)
    trip_selenium=read_json(file_1)
    trip_selenium=add_file(file_to_be_done,trip_selenium)
    save_data(trip_selenium)


if __name__ == '__main__':
    main()