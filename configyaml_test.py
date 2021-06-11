#!/usr/bin/env python3
import yaml
with open('config.yaml') as f:
    docs = yaml.load_all(f, Loader=yaml.FullLoader)
    for doc in docs:
        #print(doc)
        for k, v in doc.items():
            print(k,v)