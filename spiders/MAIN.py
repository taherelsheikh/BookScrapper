import os
import json
import pandas as pd
from titlecase import titlecase
from litcharts import litcharts
from barnes import barnes
from bookrags import bookrags
from gradesaver import gradesaver
from nytimes import nytimes
from shmoop import shmoop
from sparknotes import sparknotes
from bookbrowse import bookbrowse
from goodreads import goodreads
from readinggroup import readinggroup
from enotes import enotes



"""
**** Running the following spiders ****
* Run spiders
* Export data into JSON files
"""

os.system('scrapy runspider litcharts.py -o data/litcharts.json')
os.system('scrapy runspider barnes.py -o data/barnes.json')
os.system('scrapy runspider bookrags.py -o data/bookrags.json')
os.system('scrapy runspider nytimes.py -o data/nytimes.json')
os.system('scrapy runspider shmoop.py -o data/shmoop.json')
os.system('scrapy runspider sparknotes.py -o data/sparknotes.json')
os.system('scrapy runspider bookbrowse.py -o data/bookbrowse.json')
os.system('scrapy runspider goodreads.py -o data/goodreads.json')
os.system('scrapy runspider readinggroup.py -o data/readinggroup.json')
os.system('scrapy runspider gradesaver.py -o data/gradesaver.json')
os.system('scrapy runspider enotes.py -o data/enotes.json')




import pandas as pd
from titlecase import titlecase


"""
**** Data Processing ****
* Import all JSON data
* NYTimes data processing
* e-notes data processing
* Add a provider id column for each website
* Merge all Dfs into a final Df
* Connect to database
* Import finalDf into database
* Remove all JSON files from the data folder
"""

##### Import all JSON data #####

barnesDf = pd.read_json('data/barnes.json')
bookbrowseDf = pd.read_json('data/bookbrowse.json')
bookragsDf = pd.read_json('data/bookrags.json')
shmoopDf = pd.read_json('data/shmoop.json')
sparknotesDf = pd.read_json('data/sparknotes.json')
litchartsDf = pd.read_json('data/litcharts.json')
goodreadsDf = pd.read_json('data/goodreads.json')
gradesaverDf = pd.read_json('data/gradesaver.json')
nytimesDf = pd.read_json('data/nytimes.json')
readinggroupDf = pd.read_json('data/readinggroup.json')
enotesDf = pd.read_json('data/enotes.json')



##### NYTimes data processing #####
# Convert titles to title capitalization

title = []
for i in nytimesDf['Title']:
    title.append(titlecase(i))
nytimesDf['Title'] = pd.DataFrame(title)

#### e-notes data processing ####
# Remove by in the Author column
author_cleaned_list = []
for name in enotesDf['Author']:
    name = name.split()
    length = len(name)
    if name == []:
            author_cleaned_list.append(None)
    else:
         author_cleaned_list.append(" ".join((name[1:length])))

enotesDf['new_col'] = pd.DataFrame(author_cleaned_list)
enotesDf = enotesDf[['Title', 'new_col', 'Source']]
enotesDf.columns = ['Title', 'Author', 'Source']

##### Add a provider id column for each website #####

allDfs = [barnesDf, bookbrowseDf, bookragsDf, nytimesDf,
          shmoopDf, sparknotesDf, litchartsDf, goodreadsDf,
         readinggroupDf, gradesaverDf, enotesDf]

providerID = 1
for DF in allDfs:
    DF['Provider_id'] = providerID
    providerID += 1

##### Merge all Dfs into a final Df #####

finalDf = pd.concat(allDfs)
col = ['Title', 'Author', 'Source', 'Timestamp', 'Date_published',
'Category', 'Award', 'Year', 'Rank', 'Provider_id']
finalDf = finalDf[col]
finalDf.reset_index(drop=True, inplace=True)
# Drop ()
finalDf['Date_published'] = finalDf['Date_published'].str.replace('(','')
finalDf['Date_published'] = finalDf['Date_published'].str.replace(')','')


##### Connect to database #####
# First Create a database with a default collation of utf8mb4_unicode_ci

import pymysql
from sqlalchemy import create_engine

# Import SQL credentials
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

fpath = find('sql_credentials.json', '/Users')
jstr = open(fpath)
data = json.load(jstr)

# Save SQL credentials into variables
Host = data['Host']
User = data['User']
Password = data['Password']
Database = data['Database']

# engine_setup_query = 'mysql+pymysql://USERNAME:PASSWORD@HOSTNAME/DATABASE_NAME'
engine_setup_query = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (User, Password, Host, Database)
# Connect to database
engine = create_engine(engine_setup_query, encoding = 'utf-8')

old_books_Df = pd.read_sql('Book', con=engine)
old_books_Df = old_books_Df.drop(['scraped_id', 'Timestamp', 'Source'], axis=1)

col = ['Title', 'Author', 'Date_published',
'Category', 'Award', 'Year', 'Rank', 'Provider_id']
# Merge finalDf with database df if available using a left outer join function
joinedDf = finalDf.merge(old_books_Df, on= col, how='left', indicator = True)
# Output only the new books
new_books_Df = joinedDf[joinedDf._merge != 'both']
# Remove additional columns created from the merge function
new_books_Df = new_books_Df.drop(['_merge'], axis=1)

##### Import Final DF into database #####

new_books_Df.to_sql(name = 'Book', con = engine, if_exists ="append", index=False)


##### Remove all JSON files from the data folder #####

os.system('rm data/litcharts.json')
os.system('rm data/barnes.json')
os.system('rm data/bookrags.json')
os.system('rm data/nytimes.json')
os.system('rm data/shmoop.json')
os.system('rm data/sparknotes.json')
os.system('rm data/bookbrowse.json')
os.system('rm data/goodreads.json')
os.system('rm data/readinggroup.json')
os.system('rm data/gradesaver.json')
os.system('rm data/enotes.json')
