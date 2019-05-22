import os
import bs4
import json
from time import sleep
from selenium import webdriver
import json
import time
import sys


def read_comments_done(file_name):
    try:    
        with open(file_name, 'r') as json_file:
            comments_=json.load(json_file)
        comments=[]
        for i in range(len(comments_)):
            try:
                dic={}
                dic['url']=comments_[i]['url']
                dic['comments']=comments_[i]['comments']
                comments.append(dic)
            except:
                pass
        urls=[]
        for i in range(len(comments_)):
            try:
                urls.append(comments_[i]['url'])
            except:
                pass
    except:
        comments=[]
        urls=''

    return comments, urls

def read_urls(file_):
    with open (file_, 'r') as f:
        urls=f.read().splitlines()
    return urls

def save_already_done_list(already_done_list):
    with open('already_done.txt', 'w') as f:
        for url in already_done_list:
            f.write("%s\n" % url)


def robot(url,driver):
    dic={}
    try:
        driver.get(url)
        sleep(0.2)
        driver.find_element_by_css_selector("span.taLnk.ulBlueLinks").click()
        sleep(0.5)
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        comments=soup.find_all('p', attrs={"class":"partial_entry"})
        comments= [j.text for j in comments]
        dic['url']= url
        dic['comments']=comments
    except:
        dic['url']=url
        dic['comments']=['-']
        print('\nerror:',url)

    conteo=0
    for i in range(len(dic['comments'])):
        if 'Más' in dic['comments'][i][-5:] or '-' in dic['comments'][i][-1:]:
            conteo=1
            break
    if conteo==1 or len(dic['comments'])==0:
        try:
            driver.get(url)
            print('\nha pillado mal la url:\n',url)
            sleep(2)
            driver.find_element_by_css_selector("span.taLnk.ulBlueLinks").click()
            sleep(3)
            soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
            comments=soup.find_all('p', attrs={"class":"partial_entry"})
            comments= [j.text for j in comments]
            dic['url']= url
            dic['comments']=comments
            print('-'*100)
            print('segundo intento exitoso:\n',url)
            print('-'*100)
        except:
            dic['url']=url
            dic['comments']=['-']
            print('-'*50)
            print('segundo intento con error, probable que no tenga "más":\n',url)
            print('-'*50)

    return dic

def save_data(data,files_):
    with open(files_, 'w') as outfile:
        json.dump(data, outfile)
        print('-'*50)
        print('\nnew file saved:',files_)

def main():
    start=time.time()
    driver=webdriver.Chrome()
    sleep(1)
    file_name=sys.argv[1]
    datos=read_comments_done(file_name)
    data=datos[0]
    already_done=datos[1]
    urls=read_urls('urls.txt')
    for url in urls:
        if not url in already_done:
            dic=robot(url,driver)
            data.append(dic)
            print('\n{} urls done: {}'.format(urls.index(url)+1,url))
            if urls.index(url) % 100 == 0:
                save_data(data,file_name)
                end = time.time()
                hours, rem = divmod(end-start, 3600)
                minutes, seconds = divmod(rem, 60)
                print('-'*100)
                print("\n{} urls of {} processed in {:0>2}:{:0>2}:{:05.2f} hours\n".format(urls.index(url)+1,len(urls),int(hours),int(minutes),seconds))
                print('-'*100)
    save_data(data,file_name)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print('-'*50)
    print("\nall urls processed in {:0>2}:{:0>2}:{:05.2f} hours\n".format(int(hours),int(minutes),seconds))
    print('-'*50)
    driver.close()

if __name__ == '__main__':
    main()
