#!/usr/bin/env python
# coding: utf-8

# # Data Analysis for Android and iOS mobile apps
# 
# ** This project(what is the project all about)Android and iOS mobile apps
# ** For this project, we'll pretend we're working as data analysts for a company that builds Android and iOS mobile apps. We make our apps available on Google Play and the App Store.
# 
# ** We only build apps that are free to download and install, and our main source of revenue consists of in-app ads. This means our revenue for any given app is mostly influenced by the number of users who use our app — the more users that see and engage with the ads, the better. Our goal for this project is to analyze data to help our developers understand what type of apps are likely to attract more users on Google Play and the App Store.
# 

# In[1]:


from csv import reader

open_file = open('googleplaystore.csv')
read_file = reader(open_file)
android = list(read_file)
android_header = android[0]
android_data = android[1:]

open_file = open('AppleStore.csv')
read_file = reader(open_file)
ios = list(read_file)
ios_header = ios[0]
ios_data = ios[1:]



# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))
        


# In[3]:


print(explore_data(ios_data,1,3))
#the above is equivalent to 'print(ios_data[1,3])
print(explore_data(android_data,1,4))
#the above is equivalent to 'print(andriod_data[1,3])


# In[4]:


print(len(android))
print(len(ios))
print(ios_header)
print(android_header)


# In[5]:


#cleaning wrong data in Android
print(android_data[10472])  # incorrect row
print('\n')
print(android_header)  # header
print('\n')
del android_data[10472]
print(android_data[10472])


# ## Removing duplicated rows
# 
# ** On closely examining the `Google Play data set`, i noticed some apps have duplicated entries. These entries were posibly dublicated without tracks because the forth colum being the `Review` column has unique identifier for apps that are non distint.
# 
# ** To correct this error, an attempt to loop through the app is made. After which, we select `Reviews` with hightest digit. This paramenter of selection is adopted as a criterion for removing duplicated entires because reviews with the highest entires are more recent review carried out on the app.

# In[6]:


duplicate_apps = []
distinct_apps = []

for app in android:
    name = app[0]
    if name in distinct_apps:
        duplicate_apps.append(name)
    else:
        distinct_apps.append(name)
        
print('Number of duplicated apps: ', len(duplicate_apps)) 
print('\n')
print('Examples of duplicated apps: ', duplicate_apps[:10])


# **Below we write a code to do the following
# 
# 
#     1) Create a dictionary where each key is a unique app name and the corresponding dictionary value is the highest number of `reviews` of that app.
#     2) Use the dictionary you created above to remove the duplicate rows:
# 

# In[ ]:





# In[7]:


reviews_max ={}

for app in android_data:
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
print(len(reviews_max))
            
        
    


# In[8]:


android_clean = []
already_added = []

for app in android_data:
    name = app[0]
    n_reviews = float(app[3])
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)
    
    
print(len(android_clean))  


# In[9]:



def is_english(string):
    
    for character in string:
        if ord(character) > 127:
            return False
    
    return True

print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# In[10]:


def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    if non_ascii > 3:
        return False
    else:
        return True
    
print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))



# ** Using the function `is_english` to filter the ios dataset and android dataset

# In[11]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios_data:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# ## Isolating the free Apps
# __ As we mentioned in the introduction, we only build apps that are free to download and install, and our main source of revenue consists of in-app ads. Our data sets contain both free and non-free apps, and we'll need to isolate only the free apps for our analysis. Below, we isolate the free apps for both our data sets

# In[12]:


android_final = []
ios_final = []

#Getting the free apps for Android
for element in android_english:
    free_android = element[7]
    if free_android == '0':
        android_final.append(element)
        
print(len(android_final))

#Getting the free apps for ios
for element in ios_english:
    free_ios = element[4]
    if free_ios == '0.0':
        ios_final.append(element)
        
print(len(ios_final))
    


# ## Most commin Apps by Genre: Part One
# 
# our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# 
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# Build a minimal Android version of the app, and add it to Google Play.
# If the app has a good response from users, we develop it further.
# If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# Because our end goal is to add the app on both Google Play and the App Store, we need to find app profiles that are successful on both markets. For instance, a profile that works well for both markets might be a productivity app that makes use of gamification.
# 
# **We'll build two functions we can use to analyze the frequency tables:
# 
#     1)One function to generate frequency tables that show percentages
#     2)Another function that we can use to display the percentages in a descending order

# In[13]:


def frequency_table(data_set, index):
    freq_table = {}
    total = 0
    
    for element in data_set:
        total += 1
        value = element[index]
        if value in freq_table:
            freq_table[value] += 1
        else:
            freq_table[value] = 1
            
    table_percentages = {}
    for key in freq_table:
        percentage = (freq_table[key] / total) * 100
        table_percentages[key] = percentage 

    return table_percentages
            
print(frequency_table(ios_final, 11))
print('\n')
print(frequency_table(android_final, 1)) #according to category
print('\n')
print(frequency_table(android_final, 9)) #according to genre


        
        


# In[14]:


def display_table(dataset, index):
    freq_table = frequency_table(dataset, index)
    table_display = []
    for key in freq_table:
        key_val_as_tuple = (freq_table[key], key)
        table_display.append(key_val_as_tuple)
        
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        
display_table(ios_final, 11)


# In[15]:


#according to category
display_table(android_final, 1)


# In[16]:


#according to genre
display_table(android_final, 9)


# ## Most popular Apps by Genre on App Store
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but this information is missing for the App Store data set. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.
# 
# Let's start with calculating the average number of user ratings per app genre on the App Store. To do that, we'll need to:
# 
#     *Isolate the apps of each genre.
#     *Sum up the user ratings for the apps of that genre.
#     *Divide the sum by the number of apps belonging to that genre (not by the total number of apps).

# In[22]:



genres_ios = frequency_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_ratings = total/len_genre
    print(genre, ':', avg_ratings)
   


# ## Most popular Apps by Genre on Google Play
# We have data about the number of installs for the Google Play market, so we should be able to get a clearer picture about genre popularity. However, the install numbers don't seem precise enough — we can see that most values are open-ended (100+, 1,000+, 5,000+, etc.):
# 

# In[23]:


display_table(android_final, 5)


# For instance, we don't know whether an app with 100,000+ installs has 100,000 installs, 200,000, or 350,000. However, we don't need very precise data for our purposes — we only want to find out which app genres attract the most users, and we don't need perfect precision with respect to the number of users.
# 
# We're going to leave the numbers as they are, which means that we'll consider that an app with 100,000+ installs has 100,000 installs, and an app with 1,000,000+ installs has 1,000,000 installs, and so on. To perform computations, however, we'll need to convert each install number from string to float. This means we need to remove the commas and the plus characters, otherwise the conversion will fail and raise an error.

# In[24]:


categories_android = frequency_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# In[ ]:




