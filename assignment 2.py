#!/usr/bin/env python
# coding: utf-8

# In[22]:


def main():
    import urllib2
    from itertools import islice
    from pprint import pprint
    from datetime import datetime
    import logging
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default = "https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv", type=str)
    parser.add_argument("--id", type=int, help="Person ID", default=None)
    args = parser.parse_args()
    if (args.input == None and args.length == None):
        sys.exit()    

url = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'
        
if __name__ == "__main__":
    
    def downloadData(url):
        import urllib.request
        import pandas as pd
        from io import StringIO
        
        global df
        
        link = urllib.request.urlopen(url)
        html = link.read()
        
        s=str(html,'utf-8')
        
        data = StringIO(s) 
        
        df=pd.read_csv(data)
    
    def processData(df):   
        
        downloadData(url)
        
        global dict 
        
        LOG_FILENAME = 'errors.log'
        logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)
        
        dict = {}
        for ind in df.index: 
            import datetime
            
            try:
                i = df['id'][ind]
                n = df['name'][ind]
                b = df['birthday'][ind]
                converted_date = datetime.datetime.strptime(b, '%d/%m/%Y').strftime("%x")
                dict.update({i: (n, converted_date)})
            except Exception as e: 
                i = df['id'][ind]
                row = df.index[i]
                
                logging.error("Error processing line # {} for ID# {}: Exception Detail: {}".format(row, i, e), exc_info=True)
                pass
            
        print(dict)
    
    def displayPerson(id):
        import sys
        
        processData(df)
        if id <= 0:
            sys.exit()
        else:
            try:
                print("Person #{} is {} with a birthday of {}".format(id, dict[id][0], dict[id][1]))
            except KeyError:
                print("No user found with that id")
                pass

downloadData(url)
processData(df)
displayPerson(3)


# In[ ]:




