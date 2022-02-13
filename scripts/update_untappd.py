import requests
import pandas as pd
import numpy as np
import os

#parameters
begin_request = 'https://api.untappd.com/v4/'
beer_info = 'user/beers/'
user = 'cwpace97'
client_id = os.environ.get('untappd_clientid')
client_secret = os.environ.get('untappd_clientsecret')
end_request = '?client_id='+client_id+'&client_secret='+client_secret

#create empty dataframe, loop through first 1000 available user beers and add
df = pd.DataFrame()
for i in np.arange(20):
    try :
        r = requests.get('https://api.untappd.com/v4/user/beers/'+user+end_request+'&limit=50&offset='+str(i*50))
        print('Batch #',str(i),':  ',r)
        beer_list = r.json()['response']['beers']['items']
        df_temp = pd.json_normalize(beer_list)

        df_temp = df_temp.drop(columns = [
            'first_created_at',
            'first_checkin_id',
            'recent_created_at_timezone',
            'first_had',
            'user_auth_rating_score',
            'beer.bid',
            'beer.beer_description',
            'beer.has_had',
            'brewery.brewery_id',
            'brewery.brewery_page_url',
            'brewery.contact.twitter',
            'brewery.contact.facebook',
            'brewery.contact.instagram',
            'brewery.contact.url',
            'beer.beer_label',
            'brewery.brewery_label',
            'beer.beer_slug',
            'brewery.brewery_slug'
        ])

        #fix date time
        df_temp['recent_created_at']= pd.to_datetime(df_temp['recent_created_at'])
        df_temp['beer.created_at']= pd.to_datetime(df_temp['beer.created_at'])

        #splitting the beer_style into category then style
        df_temp[['beer.beer_category','beer.beer_subcategory']] = df_temp['beer.beer_style'].str.split('-',expand=True)
        df = df.append(df_temp)
    except:
        print('No Beers in This Batch')

df = df.drop_duplicates(subset=['recent_checkin_id'])
df = df.reset_index(drop=True)
df['beer.created_at_year'] = pd.DatetimeIndex(df['beer.created_at']).year
df['rating_difference'] = df['rating_score']-df['beer.rating_score']

df.to_csv(r"C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io\data\untappd_data.csv")