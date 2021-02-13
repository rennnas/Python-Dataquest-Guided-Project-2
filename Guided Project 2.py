#!/usr/bin/env python
# coding: utf-8

# # Guided Project: Exploring Hacker News Posts
# 
# Hacker News is a site started by the startup incubator Y Combinator, where user-submitted posts are voted and commented upon, similar to reddit. Hacker News is extremely popular in technology and startup circles, and posts that make it to the top of Hacker News' listings can get hundreds of thousands of visitors as a result.
# 
# The data set has been reduced from almost 300,000 rows to approximately 20,000 rows by removing all submissions that did not receive any comments, and then randomly sampling from the remaining submissions.
# 
# We're specifically interested in posts whose titles begin with either Ask HN or Show HN. Users submit Ask HN posts to ask the Hacker News community a specific question.
# 
# We'll compare these two types of posts to determine the following:
# 
# - Do Ask HN or Show HN receive more comments on average?
# - Do posts created at a certain time receive more comments on average?
# 

# In[10]:


from csv import reader
hn = list(reader(open("hacker_news.csv")))
print(hn[:5])


# ## Cleaning the Data

# Notice that the first list in the inner lists contains the column headers, and the lists after contain the data for one row. In order to analyze our data, we need to first remove the row containing the column headers. Let's remove that first row next.

# In[11]:


headers = hn[0]
hn = hn[1:]

print(headers)


# In[12]:


print(hn[:5])


# Since we're only concerned with post titles beginning with Ask HN or Show HN, we'll create new lists of lists containing just the data for those titles.

# In[27]:


ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = row[1]
    title = title.lower()
    
    if title.startswith("ask hn"):
        ask_posts.append(row)
    elif title.startswith("show hn"):
        show_posts.append(row)
    else:
        other_posts.append(row)

print("Number of Ask HN posts:",len(ask_posts))
print("Number of Show HN posts:",len(show_posts))
print("Number of other posts:",len(other_posts))
        


# ## Data Analysis
# ### 1.
# 
# Let's determine if ask posts or show posts receive more comments on average.

# In[32]:


total_ask_comments = 0
total_show_comments = 0

for row in ask_posts:
    num_comments = int(row[4])
    total_ask_comments += num_comments
    
avg_ask_comments = total_ask_comments / len(ask_posts)
print('Average number of ask comments:' ,avg_ask_comments)

for row in show_posts:
    num_comments = int(row[4])
    total_show_comments += num_comments

avg_show_comments = total_show_comments / len(show_posts)
print('Average number of show comments:' ,avg_show_comments)


# We can see that on average, the Ask HN posts receive more comments (around 14) thant the Show HN posts (around 10). We can conclude that ask posts are more likely to receive comments.

# ### 2.
# Since ask posts are more likely to receive comments, we'll focus our analysis in this group of posts. We will determine now if ask posts created at a certain time are more likely to attract comments. For this we will:
# 
# - 1. Calculate the amount of ask posts created in each hour of the day, along with the number of comments received.
# - 2. Calculate the average number of comments ask posts receive by hour created.

# In[33]:


import datetime as dt

result_list = []
counts_by_hour = {}
comments_by_hour ={}

for row in ask_posts:
    created_at = row[6]
    num_comments = int(row[4])
    result_list.append([created_at ,num_comments])


for result in result_list:
    created_at_result = result[0]
    comments_result= result[1]
    created_at_result_dt = dt.datetime.strptime(created_at_result, '%m/%d/%Y %H:%M')
    creation_hour = created_at_result_dt.strftime('%H')
    
    if creation_hour in counts_by_hour:
        counts_by_hour[creation_hour] += 1
        comments_by_hour[creation_hour] += comments_result
    else:
        counts_by_hour[creation_hour] = 1
        comments_by_hour[creation_hour] = comments_result
        
print(counts_by_hour)
print('\n')
print(comments_by_hour)
    
    


# Next, we'll use the two dictionaries previously created to calculate the average number of comments for posts created during each hour of the day.

# In[34]:


avg_comments_by_hour = []

for hour in comments_by_hour:
    avg_comments_per_post = round((comments_by_hour[hour])/counts_by_hour[hour],1)
    avg_comments_by_hour.append([hour, avg_comments_per_post])
    
print(avg_comments_by_hour)


# Although we now have the results we need, this format makes it hard to identify the hours with the highest values. Let's finish by sorting the list of lists and printing the five highest values in a format that's easier to read.

# In[35]:


swap_avg_by_hour = []
for row in avg_comments_by_hour:
    swap_avg_by_hour.append((row[1], row[0])) # row[1]= average comments per post  row[0]= hour
    
print(swap_avg_by_hour)


# In[36]:


sorted_swap = sorted(swap_avg_by_hour, reverse=True)
print("The Top Five Hours for Ask Posts Comments:")

for row in sorted_swap[:5]:
    # US/Eastern timezone (EST) - UTC-06
    est_hour_dt = dt.datetime.strptime(row[1], '%H')
    est_hour_str = est_hour_dt.strftime('%H:%M')
    
    # Germany Time Zone (CET) - UTC+01: 7 hours ahead of EST
    # Converting the `Hour` from EST to CET

    our_hour_dt = dt.datetime.strptime(row[1], '%H') + dt.timedelta(hours=7)
    our_hour_str = our_hour_dt.strftime('%H:%M')
    
    print('   ', '{est_time} EST or {our_time} CET:    {avg:.1f} average comments per post'.format(est_time=est_hour_str, our_time=our_hour_str, avg=row[0])) 


# # Conclusions
# 
# Our findings show that 15:00 EST or 22:00 CET receive 38.6 average comments per post. This can be explained since it is a time when both users from US and from Europe are online.

# In[ ]:




