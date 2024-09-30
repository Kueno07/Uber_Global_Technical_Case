#!/usr/bin/env python
# coding: utf-8

# Challenge: we need to build a logic to estimate all products that are duplicated, ie, they have different product_ids but they share the same content.

# ### we don’t want the customer to see duplicated products.

# The unique identifier for each product on Cornershop database is the **PRODUCT_ID** attribute.

# # Script

# ### Libraries and File upload

# In[2]:


import pandas as pd
from pathlib import Path


# In[3]:


home = str(Path.home())


# In[4]:


path_read = home + '/Downloads/Base de Dados Python.csv'
df_database = pd.read_csv(path_read, dtype={'product_id': 'string',
                                            'product_name': 'string',
                                            'buy_unit': 'string',
                                            'package': 'string',
                                            'brand': 'string',
                                            'parent_category_id':'string',
                                            'category_id':'string',
                                            'parent_category_name': 'string',
                                            'category_name': 'string',
                                            'orders;;':'string'})


# In[5]:


pd.options.mode.chained_assignment = None  # default='warn'


# ### Functions

# In[6]:


def splitcom(value):
    value1 = value.split(',')
    return value1

def text_char(x):
    text_char =  unidecode.unidecode(str(x))
    return text_char

def order_clean(x):
    order_clean = str(x).replace(';','')
    return order_clean

def no_elements(list):
    count = 0
    for element in list:
        count += 1
    return count


# # Data manipulation

# In[7]:


df_database.head(3)


# In[8]:


df_len = df_database
df_len['len'] = df_len['product_id'].apply(lambda x: len(x))
df_len.rename(columns = {'orders;;': 'orders'}, inplace = True)

# Dataset ok
df_len_ok = df_len[(df_len['len']) <= 6 ]
df_len_ok = df_len_ok.drop(['len'],axis=1)

# Dataset nok
df_len_bad = df_len[(df_len['len']) > 7 ]
df_len_bad['split_list'] = df_len_bad['product_id'].apply(lambda x: splitcom(x))
df_len_bad['no_elements'] = df_len_bad['split_list'].apply(lambda x: no_elements(x))

# Dataset nok, 10 elements
df_len_bad_10 = df_len_bad[(df_len_bad['no_elements'] == 10)]
df_len_bad_10 = pd.DataFrame(df_len_bad_10['product_id'])
df_len_bad_10[['product_id_new', 'product_name','buy_unit', 'package', 'brand','parent_category_id', 'category_id','parent_category_name', 'category_name','orders']] = df_len_bad_10['product_id'].str.split(',', expand=True)
df_len_bad_10 = df_len_bad_10.drop(['product_id'],axis=1)
df_len_bad_10.rename(columns = {'product_id_new': 'product_id'}, inplace = True)
df_len_bad_10['product_name'] = df_len_bad_10['product_name'].apply(lambda x: x.replace('"',''))
df_len_bad_10['package'] = df_len_bad_10['package'].apply(lambda x: x.replace('"',''))
df_len_bad_10 = df_len_bad_10[pd.to_numeric(df_len_bad_10['product_id'], errors='coerce').notnull()]
df_len_bad_10 = df_len_bad_10[(df_len_bad_10['buy_unit'] == 'UN') | (df_len_bad_10['buy_unit'] == 'KG')]


# ## Appending datasets

# In[9]:


df_cleaned = df_len_ok.append(df_len_bad_10)

# Additional cleaning
df_cleaned['product_id'] = df_cleaned['product_id'].astype(int)
df_cleaned['parent_category_id'] = df_cleaned['parent_category_id'].astype(int)
df_cleaned['category_id'] = df_cleaned['category_id'].astype(int)
df_cleaned['orders'] = df_cleaned['orders'].apply(lambda x: order_clean(x))
df_cleaned['orders'] = df_cleaned['orders'].astype(int)
df_cleaned['package'] = df_cleaned['package'].fillna('-')
df_cleaned['brand'] = df_cleaned['brand'].fillna('-')
df_cleaned['product_name'] = df_cleaned['product_name'].apply(lambda x: x.lower())
df_cleaned['package'] = df_cleaned['package'].apply(lambda x: x.lower())
df_cleaned['brand'] = df_cleaned['brand'].apply(lambda x: x.lower())
df_cleaned['key'] = df_cleaned['product_name'] + "_" + df_cleaned['buy_unit'] + "_" + df_cleaned['package'] + "_" + df_cleaned['brand'] + "_" + df_cleaned['parent_category_id'].astype(str) + "_" + df_cleaned['category_id'].astype(str)


# ## Removing duplicated products using key

# In[10]:


# Summing up orders of duplicated products 
df_aux = df_cleaned.groupby(['key']).agg({'orders':'sum'}).reset_index()

# Replacing orders to sum of orders
df_cleaned_dup = df_cleaned
df_cleaned_dup.drop_duplicates(subset ='key', keep = 'first', inplace = True)
df_cleaned_dup = df_cleaned_dup.drop(['orders'],axis=1)
df_cleaned_dup = pd.merge(df_cleaned_dup, df_aux ,how="left", on=['key'])
df_cleaned_dup = df_cleaned_dup.drop(['key'],axis=1)


# In[11]:


print('''
No. of rows in the raw dataset: {}
No. of rows in the cleaned dataset: {}
--------------------------------------------
Data loss: {:.2f}%
'''.format(df_database.shape[0], df_cleaned_dup.shape[0], ((df_cleaned_dup.shape[0]/df_database.shape[0])-1)*100))


# ## Getting a list of duplicated products

# In[12]:


df_list_dup = df_database
df_list_dup['key'] = df_list_dup['product_name'] + "_" + df_list_dup['buy_unit'] + "_" + df_list_dup['package'] + "_" + df_list_dup['brand'] + "_" + df_list_dup['parent_category_id'].astype(str) + "_" + df_list_dup['category_id'].astype(str)

df_list_dup =  df_database.groupby(['key', 'brand']).agg({'product_id':'count'}).reset_index()
df_list_dup = df_list_dup[(df_list_dup['product_id']) > 1]
df_list_dup.sort_values(by=['product_id'],ascending=False, inplace=True)
list_dup = df_list_dup['key'].tolist()
df_list_dup_final = df_database[df_database['key'].isin(list_dup)]
df_list_dup_final.sort_values(by=['key','orders'],ascending=False, inplace=True)
df_list_dup_final = df_list_dup_final.drop(['len','key'],axis=1)
df_list_dup_final['orders'] = df_list_dup_final['orders'].apply(lambda x: order_clean(x))
df_list_dup_final['product_id'] = df_list_dup_final['product_id'].astype(int)
df_list_dup_final['parent_category_id'] = df_list_dup_final['parent_category_id'].astype(int)
df_list_dup_final['category_id'] = df_list_dup_final['category_id'].astype(int)
df_list_dup_final


# ## Exporting file as xlsx

# In[18]:


path_download = home + '/Downloads/DCA_test_Kokuda.xlsx'

with pd.ExcelWriter(path_download) as writer:
    df_cleaned_dup.to_excel(writer, sheet_name='dataset_cleaned',index=False)
    df_list_dup_final.to_excel(writer, sheet_name='list_of_duplications',index=False)


# # This was used for discovery only

# In[13]:


df_len_bad.groupby(['no_elements']).agg({'product_id':'count'}).reset_index()


# In[14]:


df_len_bad.head()


# In[15]:


x = df_len_bad[(df_len_bad['no_elements'] == 10)]
list_x = x['split_list'].tolist()[:5]
x = pd.DataFrame(list_x).T
x


# In[16]:


x = df_len_bad[(df_len_bad['no_elements'] == 11)]
list_x = x['split_list'].tolist()[:5]
x = pd.DataFrame(list_x).T
x


# In[324]:


x = df_len_bad[(df_len_bad['no_elements'] == 12)]
list_x = x['split_list'].tolist()[:5]
x = pd.DataFrame(list_x).T
x


# In[343]:


test_len_ok = df_len_ok
test_len_ok['key1'] = test_len_ok['product_name'] + "_" + test_len_ok['buy_unit'] + "_" + test_len_ok['package'] + "_" + test_len_ok['brand'] + "_" + test_len_ok['parent_category_id'].astype(str) + "_" + test_len_ok['category_id'].astype(str)
test_len_ok['key2'] = test_len_ok['buy_unit'] + "_" + test_len_ok['package'] + "_" + test_len_ok['brand'] + "_" + test_len_ok['parent_category_id'].astype(str) + "_" + test_len_ok['category_id'].astype(str)
test_len_ok


# In[344]:


df_dsclean_dupcheck2 =  test_len_ok.groupby(['key2']).agg({'product_id':'count'}).reset_index()
df_dsclean_dupcheck2 = df_dsclean_dupcheck2[(df_dsclean_dupcheck2['product_id']) > 1]
df_dsclean_dupcheck2.sort_values(by=['product_id'],ascending=False, inplace=True)
df_dsclean_dupcheck2


# In[347]:


df_dsclean_dupcheck1 =  test_len_ok.groupby(['key1', 'brand']).agg({'product_id':'count'}).reset_index()
df_dsclean_dupcheck1 = df_dsclean_dupcheck1[(df_dsclean_dupcheck1['product_id']) > 1]
df_dsclean_dupcheck1.sort_values(by=['product_id'],ascending=False, inplace=True)
df_dsclean_dupcheck1


# In[ ]:




