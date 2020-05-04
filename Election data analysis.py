#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''Election Data Project - Polls and Donors
In this Data Project we will be looking at data from the 2012 election.

In this project we will analyze two datasets. The first data set will be the results of political polls. We will analyze this aggregated poll data and answer some questions:

1.) Who was being polled and what was their party affiliation?
2.) Did the poll results favor Romney or Obama?
3.) How do undecided voters effect the poll?
4.) Can we account for the undecided voters?
5.) How did voter sentiment change over time?
6.) Can we see an effect in the polls from the debates?'''


# In[2]:


from __future__ import division
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
# For visualization
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[9]:


# Set poll data as pandas DataFrame
poll_df = pd.read_csv('2012-general-election-romney-vs-obama.csv')

# Let's get a glimpse at the data
poll_df.info()


# In[10]:


poll_df.head()


# In[16]:


sns.countplot('Affiliation',data=poll_df,hue='Population')


# In[21]:


avg = pd.DataFrame(poll_df.mean())
avg.drop("Number of Observations",axis=0,inplace=True)
avg.drop("Question Text",axis=0,inplace=True)


# In[22]:


avg.head()


# In[23]:


std = pd.DataFrame(poll_df.std())
std.drop("Number of Observations",axis=0,inplace=True)
std.drop("Question Text",axis=0,inplace=True)


# In[24]:


std.head()


# In[25]:


avg.plot(yerr=std,kind="bar",legend=False)


# In[26]:


poll_avg = pd.concat([avg,std],axis=1)
poll_avg


# In[27]:


poll_avg.columns=['Average','STD']
poll_avg


# In[28]:


poll_df.plot(x='End Date',y=['Obama','Romney','Undecided'],linestyle='',marker='o')


# In[29]:


from datetime import datetime


# In[31]:


poll_df['Difference'] = (poll_df.Obama - poll_df.Romney)/100
poll_df.head()


# In[32]:


poll_df = poll_df.groupby(['Start Date'],as_index=False).mean()
poll_df.head()


# In[33]:


poll_df.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle="-",color='purple')


# In[37]:


row_in = 0
xlimit = []
for date in poll_df['Start Date']:
    if date[0:7] == '2012-10':
        xlimit.append(row_in)
    row_in += 1
print(min(xlimit))
print(max(xlimit))


# In[40]:


poll_df.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle="-",color='purple',xlim=(325,352))
# Oct 3rd
plt.axvline(x=325+2,linewidth=4,color='grey')
# Oct 11th
plt.axvline(x=325+10,linewidth=4,color='grey')
# Oct 22nd
plt.axvline(x=325+21,linewidth=4,color='grey')


# In[ ]:


# Surprisingly, thse polls reflect a dip for Obama after the second debate against Romney, even though memory serves that he performed much worse against Romney during the first debate.


# In[ ]:


# Donor Dataset


# In[ ]:


'''The questions we will be trying to answer while looking at this Data Set is:

1.) How much was donated and what was the average donation?
2.) How did the donations differ between candidates?
3.) How did the donations differ between Democrats and Republicans?
4.) What were the demographics of the donors?
5.) Is there a pattern to donation amounts?'''


# In[41]:


# Set the DataFrame as the csv file
donor_df = pd.read_csv('Election_Donor_Data.csv')
# Get a quick overview
donor_df.info()


# In[42]:


# let's also just take a glimpse
donor_df.head()


# In[43]:


# Get a quick look at the various donation amounts
donor_df['contb_receipt_amt'].value_counts()


# In[46]:


don_mean = donor_df['contb_receipt_amt'].mean()
don_std = donor_df['contb_receipt_amt'].std()
print(don_mean,don_std)


# In[48]:


top_donor = donor_df['contb_receipt_amt'].copy()
top_donor.sort_values()
top_donor


# In[52]:


top_donor = top_donor[top_donor>0]
top_donor.sort_values()
top_donor


# In[53]:


top_donor.value_counts().head(10)


# In[56]:


com_don = top_donor[top_donor<2500]
com_don.hist(bins=100)


# In[58]:


candidate = donor_df.cand_nm.unique()
candidate


# In[59]:


# Dictionary of party affiliation
party_map = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}

# Now map the party with candidate
donor_df['Party'] = donor_df.cand_nm.map(party_map)


# In[61]:


donor_df = donor_df[donor_df.contb_receipt_amt>0]
donor_df.head()


# In[64]:


donor_df.groupby('cand_nm')['contb_receipt_amt'].count()


# In[65]:


donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()


# In[67]:


cand_amount = donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()
i=0
for don in cand_amount:
    print('The candidate ',cand_amount.index[i],' of dollar ',don)
    i+=1


# In[68]:


# PLot out total donation amounts
cand_amount.plot(kind='bar')


# In[69]:


donor_df.groupby('Party')['contb_receipt_amt'].sum().plot(kind='bar')


# In[ ]:


# Looks like Obama couldn't compete against all the republicans, but he certainly has the advantage of their funding being splintered across multiple candidates.


# In[71]:


# Use a pivot table to extract and organize the data by the donor occupation
occupation_df = donor_df.pivot_table('contb_receipt_amt',
                                index='contbr_occupation',
                                columns='Party', aggfunc='sum')
occupation_df


# In[72]:


occupation_df.shape


# In[75]:


occupation_df = occupation_df[occupation_df.sum(1)>1000000]
occupation_df.shape


# In[76]:


occupation_df.plot(kind='bar')


# In[79]:


occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')


# In[ ]:


# Looks like there are some occupations that are either mislabeled or aren't really occupations. Let's get rid of: Information Requested occupations and let's combine CEO and C.E.O.


# In[81]:


# Drop the unavailble occupations
occupation_df.drop(['INFORMATION REQUESTED PER BEST EFFORTS','INFORMATION REQUESTED'],axis=0,inplace=True)


# In[84]:


occupation_df.loc['CEO'] = occupation_df.loc['CEO']+occupation_df.loc['C.E.O.']
occupation_df.drop('C.E.O.',inplace=True)


# In[86]:


occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')


# In[ ]:


# Looks like CEOs are a little more conservative leaning, this may be due to the tax philosphies of each party during the election.

