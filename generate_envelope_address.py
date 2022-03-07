# -*- coding: utf-8 -*-
"""
@date Sun Mar  6 13:59:56 2022

@brief Generate SVG files to write out names/addresses to address envelopes
    for wedding invitations and save the dates.

@author: aweiss
"""

import pandas as pd
import svgwrite
import os
import re
import glob

# column mapping
column_map = {
    'name'      : 0,
    'address'   : 1,
    'city'      : 2,
    'state'     : 3,
    'zip'       : 4,
    'country'   : 5,
    'tag'       : 6,
}

#%% Function to generate images for envelopes

line_spacing = 12
font_size = 12
font_fmt = '{}pt'

def generate_envelope(address_info:dict, return_address_info:dict = {}, out_dir:str = './output',
                      refs=False, number=None, **kwargs):
    '''
    @brief generate an envelope image based on input data
    @param[in] address_info - info of addressee with the fields 
        name, address, city, state, zip, country
    @param[in] return_address_info - return address dictionary with the same
        fields as the address_info parameter
    @param[in/OPT] out_dir - output directory
    @param[in/OPT] refs - include reference lines or not
    @return handle to SVG file
    '''
    # generate the file name
    fname_out = address_info['name'].lower()
    fname_out = re.sub('[\&\.\-\_]+','',fname_out)
    fname_out = re.sub('[ \t]+','_',fname_out)
    # verify the name doesnt already exist with a different number
    fname_glob = glob.glob(os.path.join(out_dir,f"*{fname_out}*"))
    if fname_glob:
        card_number = int(os.path.basename(fname_glob[0]).split('_')[0])
        if card_number != number:
            raise Exception(f"Recipients {address_info['name']} has a previously generated invite with a different number ({card_number} not {number})") 
    # add a number if were not repeating with a new number
    if number is not None: fname_out = str(number)+'_'+fname_out 
    fname_out += '.svg'
    
    # now generate the svg
    svg_params = {'insert':None, 'size':('6in','4.25in')}
    dwg = svgwrite.Drawing(os.path.join(out_dir,fname_out),**svg_params)
    
    # add envelope rectangle for reference only
    if refs:
        dwg.add(dwg.rect((0,0),("6in","4.25in"),style='fill:none;stroke:black;stroke-width:5px;stroke-dasharray:5'))
    
    # add addresses
    dwg.add(get_address_text(return_address_info,'3cm','.25cm'))
    dwg.add(get_address_text(address_info,'50%','45%'))
    
    # add number if we want
    if number is not None:
        dwg.add(dwg.text('{}'.format(number),x=['95%'],y=['95%'],style='font-size:12pt;font-family:wedding;'))
    
    # and save
    dwg.save()
    
    return dwg
    

def get_address_text(address_info:dict,x,y,**kwargs):
    '''@brief get a Text element for a given address at x,y positions'''
    
    # parent element
    text_elem = svgwrite.text.Text('',x=[x],y=[y])
    
    # now the rest of the span elements
    tspan_kwargs = {'dy':['1.05em'],'x':[x],
                    'style':'text-anchor:middle;font-family:wedding;font-size:24pt'}
    name_span  = svgwrite.text.TSpan(address_info['name'],**tspan_kwargs)
    addr_span  = svgwrite.text.TSpan(address_info['address'],**tspan_kwargs)
    
    # combine city/state/zip
    addr2_str = "{}, {}, {}, {}".format(address_info['city'],address_info['state'],
                                      address_info['zip'],address_info['country'])
    addr2_span = svgwrite.text.TSpan(addr2_str,**tspan_kwargs)
    
    # now add to the text element
    text_elem.add(name_span)
    text_elem.add(addr_span)
    text_elem.add(addr2_span)
    
    return text_elem


def unpack_spreadsheet(fpath,sheet_name=None):
    '''@brief unpack a spreadsheet into a set of dictionary addresses'''
    data = pd.read_excel(fpath,sheet_name=sheet_name)
    dict_list = []
    for idx in data.index:
        # get the info as a dict
        tmp_dict = data.loc[idx].to_dict()
        # now remove any unnamed columns (they are trash right now)
        tmp_dict = {k:v for k,v in tmp_dict.items() if 'unnamed' not in k.lower()}
        # append to our list
        dict_list.append(tmp_dict)
    return dict_list


def validate_address(address_info:dict):
    '''@brief validate everything is how we expect it'''
    REQUIRED_KEYS = ['name','address','city','state','zip','country']
    for rk in REQUIRED_KEYS:
        if pd.isna(address_info[rk]):
            raise Exception(f"Field '{rk}' required, but is NA for {address_info['name']}")
        
    
    
#%% Testing
if __name__=="__main__":
    
    # path of source file
    fpath = r"C:\Users\aweis\Downloads\Wedding.xlsx"
    sheet_name = 'Address List'
    
    font_path = r"C:\Users\aweis\Downloads\monopente-font\Monopente-1GEaZ.otf"
    
    # load in the files
    address_list = unpack_spreadsheet(fpath,sheet_name)
    
    return_address_info = {
        "name":"We the people",
        "address":"11450 Colony Row, Unit 214",
        "city":"Broomfield",
        "state":"Colorado",
        "zip":"80021",
        "country":"USA"
        }
    
    dwg_list = []
    #address_list = address_list[:2] # cut down for testing
    for i,addr in enumerate(address_list):
        print("Generating address {}/{} - {}".format(i+1,len(address_list),addr['name']))
        validate_address(addr)
        dwg = generate_envelope(address_info=addr,
                                return_address_info=return_address_info,
                                refs=True,number=i+1)
    
        dwg.embed_font('wedding',font_path)
        dwg.save()
        dwg_list.append(dwg)
    
    
    
    
    