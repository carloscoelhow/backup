import os
import json
import hashlib
from functions.training import FEATURES
from functions.transformations.transformer_parallel import Transformer
import requests
from functions.utils import SKYNET_URL

def skynet_request(text, url=SKYNET_URL):
    """This function sends a request to a Skynet server so it analyses a piece of text
    and returns its category.

    Args:
        text (str): Text to analyze.
        url (str, optional): Defaults to SKYNET_URL. Url of the Skynet server.

    Returns:
        (str): String with the detected category
    """

    data_dict = {
        'text': text,
        'url': 'placeholder',
        'endpoint': False
    }
    request = requests.post(url=url, data=json.dumps(data_dict))
    if request.status_code == 200:
        category = request.json()['categories']['category'][0]
        subcategory = request.json()['categories']['subcategory'][0]
        if subcategory:
            category += '_' + request.json()['categories']['subcategory'][0]
    else:
        category = 'None'
    return category

def get_category(text):
    text = text
            
    text = text.replace(u'\xa0', u' ').replace('\'', '').replace(u'\t', u' ')
    category = skynet_request(text)
    return category


NOT_NEGATIVE = ['1', 'not_neg']
NEGATIVE = ['2', 'neg', 'ç', 'çç', 'ççç']
REALLY_NEGATIVE = ['3', 'really_neg']
TRASH = ['4', 'x', '+', '++', '+++']

DATA_JSON = 'data_url_pos_seedtag2.json'


FOLDERS = {1: 'not_negative',
            2: 'negative',
            3: 'really_negative',
            4: 'trash'}


def get_filenames(folder):
    files = []
    for file_ in os.listdir(folder):
        if file_.endswith(".txt"):
            files.append(file_)
    return files

def read_file(filename):
    with open(filename,'r', encoding='utf8') as f:
        text = f.read()
    return text

'''def move_file(file_path, destination_folder):
    filename = file_path.split('/')[-1]
    destination = os.path.join('.', destination_folder, filename)
    os.rename(file_path, destination)
'''
def show_text(text):
    print(text.replace('\n',' '))

def get_answer():
    ans = input('\n\n ------ \n please, classify this text [not_neg-1 or "enter" /neg-2, ç/really_neg-3/trash-4, "+"]:').lower()
    output = 1
    if ans in NOT_NEGATIVE:
        output = 1
    elif ans in NEGATIVE:
        output = 2
    elif ans in REALLY_NEGATIVE:
        output = 3
    elif ans in TRASH:
        output = 4
    return output

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def read_json():
   
    with open(DATA_JSON) as f:
        data = json.load(f)['data']

    return data

def extract_urls():
    data = read_json()
    url_list = []
    category = []
    for i in range(len(data)):
        dic={}
        dic = {k: v for k, v in data[i].items()}
        if 'sports' in list(dic.values()) or '-' in list(dic.values()):
            url_list.append(data[i]['url'])
            category.append(data[i]['category'])
    return url_list, category


def save_already_done_list(already_done_list):
    with open('already_done.txt', 'w') as f:
        for url in already_done_list:
            f.write("%s\n" % url)

def load_already_done():
    try:
        with open('already_done.txt', 'r') as f:
            content = f.read().splitlines()
    except:
        content = []
    return content

def write_file(text, folder_number):
    file_name = hashlib.md5(text.encode()).hexdigest()
    folder = FOLDERS[folder_number]

    create_folder(folder)

    with open("{}/{}.txt".format(folder, file_name), "w") as text_file:
        text_file.write(text)

def print_count():
    I = [1,2,3,4]
    suma = 0
    for i in I:
        try:
            folder = FOLDERS[i]
            n_files = len(get_filenames(folder))
            suma += n_files
            print('{}: {}'.format(folder, n_files))
        except:
            print('{}: {}'.format(folder, 0))
    print('-'*10)
    print ('total =', suma)
    print('-'*10)

        
def classify_article(text):
    ''' downloads, prints and ask for classification
    for some url'''
    show_text(text)
    answer = get_answer()
    write_file(text, answer)

def main():
    words = ['morre', 'dopping', 'maconha','cocaína','incêndio','incendio','insulto','cusparada','cupiu','cuspir','violencia',
    'racis','preso','presídio','presidio','prisão','corrup','abusos sexuais','abuso sexual', 'morre','mort','assassi']
    #words=['abusos sexuais','abuso sexual', 'morre','mort','assassi']
    
    folder= 'full_dataset_2018_08_21 2/news_gossip'
    files_names = get_filenames(folder)
    already_done = load_already_done()
    os.system('clear')
    for file_ in files_names:
        if not file_ in already_done:
            text = read_file(folder+'/'+file_)
            text =text.replace(u'\xa0', u' ').replace('\'', '').replace(u'\t', u' ').replace('"',' ').replace("'",' ').replace('‘',' ').replace('’',' ')
            if any (t in text for t in words):
                category_skynet = get_category(text)
                if category_skynet in ['gossip', 'news_gossip']:
                   print('category: ',category_skynet)
                   print_count()
                   classify_article(text)
                   already_done.append(file_)
                   os.system('clear')
        save_already_done_list(already_done)
    print('\n'*10 + ' '*50 + '¡Done!' + '\n'*10)

if __name__ == '__main__':
    main()