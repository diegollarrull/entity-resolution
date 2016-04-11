import json
import pandas as pd
import numpy as np
import re


def clean_phones(phone):
    if phone is not None:
        res = re.sub('[^0-9]','', phone)
        return res


PATH = "./"
FILES = {
    "foursquare_test": "foursquare_test_hard.json",
    "locu_test": "locu_test_hard.json",
    "matches": "matches_train_hard.csv",
    "foursquare_train": "foursquare_train_hard.json",
    "locu_train": "locu_train_hard.json"
}

foursquare_test = json.loads(open(PATH + FILES["foursquare_test"]).read())
fs_train = pd.read_json(open(PATH + FILES["foursquare_train"]))
fs_train['phone'] = fs_train['phone'].apply(clean_phones)
fs_test = pd.read_json(open(PATH + FILES["foursquare_test"]))
lc_train = pd.read_json(open(PATH + FILES["locu_train"]))
lc_train['phone'] = lc_train['phone'].apply(clean_phones)
lc_test = pd.read_json(open(PATH + FILES["locu_test"]))
matches = pd.read_csv(open(PATH + FILES["matches"]))

fs_train.replace([''], [None], inplace=True)
fs_test.replace([''], [None], inplace=True)
lc_train.replace([''], [None], inplace=True)
lc_test.replace([''], [None], inplace=True)

path2= "./"
fs_train.to_csv(path2 + "fs_train_2.csv", encoding = 'utf8')

from difflib import SequenceMatcher
import re


def similar(a, b):
   if (a is not None) and (b is not None):
       return SequenceMatcher(None, a, b).ratio()
   else:
       return None

import streetaddress as sa
import numpy as np

def addr_parse(address):
    if address is not None:
        addr_parser = sa.StreetAddressParser()
        addr = addr_parser.parse(address)
        if addr is None:
            print
        rv = pd.DataFrame(data={'house': [addr['house']],\
                                'street_name' : [addr['street_name']],\
                                'street_type' : [addr['street_type']],\
                                'suite_num' : [addr['suite_num']],\
                                'suite_type' : [addr['suite_type']]})
        return rv
    else:
        rv = pd.DataFrame(data={'house': [None],\
                                'street_name' : [None],\
                                'street_type' : [None],\
                                'suite_num' : [None],\
                                'suite_type' : [None]})
        return rv



def nones_(address):
    global i
    if address is None:
        j = i
        i = i + 1
        return j
    else:
        i = i + 1
        return None

i = 0
c = lc_train['street_address'].apply(addr_parse)
nones = lc_train['street_address'].apply(nones_)
cols = pd.concat([i for i in c]).reset_index(drop=True)
lc_train_expanded = pd.concat([lc_train,cols], axis = 1)
x = pd.Series([i for i in nones if i is not None]).dropna()

i = 0
c2 = fs_train['street_address'].apply(addr_parse)
nones2 = fs_train['street_address'].apply(nones_)
cols2 = pd.concat([i for i in c2]).reset_index(drop=True)
fs_train_expanded = pd.concat([fs_train,cols2], axis = 1)
x2 = pd.Series([i for i in nones2 if i is not None]).dropna()

lc_train_expanded

### features
#define NONE when there is a NA value
#Country: remove
#id: remove
#lat and long: W func
#locality: remove
#name: similar function
#phone: similar function
#postal code: similar function
#telephone: similar function
#street adress: remove
#website: normalize and similar function
#house:
#street_name:
#street_type:
#suite_num:
#suite_type: similar function

#define a function
import pandas as pd
import numpy as np


def pairwise_dist(dict_feat_func, four, locu,y_dict):
    mat_dist = pd.DataFrame(columns=dict_feat_func.keys())
    ys = pd.Series([])

    for col in dict_feat_func.keys():
        dist_func = dict_feat_func[col]
        row = 1
        for [id,l] in locu[['id',col]].iterrows():
            if id in y_dict.keys():
                v = y_dict[id]
            else:
                v = None
            for f in four[col]:
                print row
                mat_dist[row,col] = dist_func(l,f)
                if v is not None and (v == four[f,'id']):
                    ys[row] = 1
                else:
                    ys[row] = 0
                row = row + 1
    return (mat_dist, ys)

dict_feat_func = {'name': similar , 'phone': similar}
y_dict = dict(matches.to_dict(orient='split')['data'])

(xs,ys) = pairwise_dist(dict_feat_func, fs_train_expanded, lc_train_expanded, y_dict)
xs.to_csv(path2 + "xs.csv", encoding = 'utf8')
ys.to_csv(path2 + "ys.csv", encoding = 'utf8')