# -*- coding: utf-8 -*-
"""
@date Mon Aug 15 19:33:34 2022

@brief Information about this Module

@author: aweis
"""

import pandas as pd
import json
import numpy as np

def csv_to_table_dict(csv_path:str, rename:dict={'table number':'table'}, out_cols:list=['table'], **kwargs):
    ''' load a csv and change it to a json file in the correct format'''
    
    # load in the csv
    csv = pd.read_csv(csv_path) 
    
    # update some things
    csv.columns = csv.columns.str.lower() # all names lowercase
    csv = csv.set_index('name') # index by names
    csv = csv.rename(columns=rename) # update any names
    
    # make sure there arent any repeats, if there are, handle it
    dup = csv.index[csv.index.duplicated()]
    if len(dup) > 0:
        raise Exception(f"Duplicated names: {dup}")
    
    # now extract any names
    csv = csv[out_cols]
    
    # any renaming
    tojson_kwargs = {'orient':'index'}
    tojson_kwargs.update(kwargs)
    return csv.to_dict(**tojson_kwargs)


if __name__=='__main__':
    
    csv_path = r"C:\Users\aweis\Downloads\Wedding - Seating Chart.csv"
    out_path = "./website/site/data/sit_data.json"
    
    json_data = csv_to_table_dict(csv_path)
    
    # replace names
    rep_vals = {np.nan:"?"}
    for k,v in json_data.items():
        if v['table'] in rep_vals.keys():
            json_data[k]['table'] = rep_vals[v['table']]
            
    # and save out
    with open(out_path, "w+") as fp:
        json.dump(json_data,fp, indent=4)
    
    
    
    
    