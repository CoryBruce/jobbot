from datetime import datetime
from datetime import timedelta
import sys
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd



# to do
# get data for search from user (title, pay, remote)
# save data for next time user uses application
# add other sites like zip recruiter
# have a timer set to pull page data every so often
    # check data for double post and remove those from list
# double check job descriptions against user search criteria
# alert me via sms and email of job matches

# if interested in job have bot apply for me (later)



#indeed tut
#https://www.youtube.com/watch?v=PPcgtx0sI2E

def extract(page):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}
    url = (f'https://www.indeed.com/jobs?q=remote+work+from+home+$28,000&l=remote&sort=date&start={page}')
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup, job_list):
    divs = soup.find_all('div', class_='jobsearch-SerpJobCard')
    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('span', class_='company').text.strip()
        try: #use try except block cause not every job has this field so if none then pay = ''
            pay = item.find('span', class_='salaryText').text.strip()
        except:
            pay = 'not posted'
        job_summary = item.find('div', {'class' : "summary"}).text.strip().replace('\n', '') # this replaces the \n in the text with ''
        job_link = item.find('a', href=True)
        link = 'indeed.com' + job_link['href']
        try:
            remote = item.find('span', {'class' : "remote"}).text.strip()
        except:
            remote = 'not displaying remote'
        try:
            location = item.find('div', class_='location accessible-contrast-color-location').text.strip()
        except:
            location = 'no info'
        try:
            rating = item.find('span', class_="ratingsContent").text.strip()
        except:
            rating = 'no rating'
        job = {
            'title': title,
            'company': company,
            'rating': rating,
            'pay': pay,
            'location': location,
            'summary': job_summary,
            'remote': remote,
            'link': link
        }
        job_list.append(job)
    return

def create_data_table(job_list):
     df = pd.DataFrame(job_list) # this creates a panda data frame from the job list
    # print(df.head())
     df.to_csv('jobs.csv') # this creates a csv of the data frame

def search_list(file, search_for):
    print(f'Searching through {len(file)} jobs for matches')
    results = []
    for item in file:
        #print(item)
        for info in item:
            #print(item[info])
            if search_for in item[info]:
                #print("match \n")
                results.append(item)
    print(f'Found {len(results)} matching jobs!')
    return results

def update_job_info():
    jobs = input('Please enter desired job titles: ')
    wanted_titles = jobs.split()
    print('Thank you.')
    pay = input('Please enter desired hourly wage')
    print('Thank you. Searching database for jobs')

def display_full_table(list):
    print('display table')
    #print(f'{len(list)} in list')
    for item in list:
        #print(item)
        print('\n')
        for info in item:
            print(info, item[info])

def display_short_table(list):
    # this prints out index number, title, company, and pay
    print('display table')
    i = 1
    for item in list:
        print('\n')
        print(i)
        for info in item:
            if info == 'title':
                print(item[info])
            if info == 'company':
                print(item[info])
            if info == 'pay':
                print(item[info])
                i += 1
            # remember that if user enters a number off the index for here to -1 from each cause list starts at 0
def login():
    print('   ___       _     _           _    \n  |_  |     | |   | |         | |   \n    | | ___ | |__ | |__   ___ | |_  \n    | |/ _ \|  _ \|  _ \ / _ \| __| \n/\__/ / (_) | |_) | |_) | (_) | |_  \n\____/ \___/|_.__/|_.__/ \___/ \__| \n\n\n')
    user_name = input('Enter username or new for new user: ')
    if user_name == 'new':
        #create_new_user()
        pass
    else:
        # load_data()
        # read user_name from data file and check for user input in file
        #if user_name == loaded_data.user_name:
            #password = input(f'Thank you {user_name}, please enter password:')
            #if password == loaded_data.password:
                #main_menu(loaded_data)
            #else:
                #print('Incorrect password')
                # loop back through the password check or ask to enter different user_name
        pass

def main():
    job_results = []
    user_name = ''
    updated = False
    update_time = ''


    running = True
    while running:
        #clear = lambda: os.system('cls')
        #clear()
        print('\nJobbot \n-------------')
        print(f'Welcome back {user_name}')
        if updated:
            print(f'Last search on {update_time.strftime("%Y-%m-%d %H:%M")}.\nFound {len(job_results)} matching jobs!')
        print('\n')
        print('\n')
        print('1.Search jobs       2.Update Info     3.Display Results    4.Automation Settings        5.Exit')
        #choice = int(input('choice: '))
        choice = input('choice:')
        try:
            choice = int(choice)
        except:
            input("Please enter a valid option")
        if choice == 1:
            print('\n')
            print('Searching for jobs')
            print('-------------------')
            print('\n \n \n')
            job_list = search_jobsite()
            create_data_table(job_list)
            results = search_list(job_list, 'Customer')
            update_time = datetime.now()
            updated = True
            job_results = results
        if choice == 2:
            print('\n')
            print('Update Info')
            print('------------------------')
            print('\n \n \n')
            update_job_info()
        if choice == 3:
            print('\n')
            print('Display Results')
            print('------------------------')
            print('\n \n \n')
            print('1. View Saved Jobs        2. View recent search')
            view = input('choice: ')
            view = int(view)
            print(f'You chose {view}')
            if view == 1: # these if statements aren't working for some reason
                print('Feature will be available later')
            if view == 2:
                print(f'You chose {view}')
                display_short_table(job_results)
                pick = input('\nwhich job(s) are you interested in?')
                # for number in pick: # this is due to list starting at 0 need to -1 from every number entered
                    # number = number -1
                # add these jobs to a saved jobs list
        if choice == 4:
            print('\nAutomation Settings\n------------------------')
            print('\n\n\n1. Change auto scanner time')
        if choice == 5:
            print('Please come back soon! \nExiting Jobbot..')
            write_data_txtfile()
            running = False
            sys.exit()

def search_jobsite():
    job_list = []
    for i in range(0, 50, 10):  # (starting, end, increments)
        print(f'Searching page {int(i/10) + 1}')
        first_page = extract(0)
        transform(first_page, job_list)
    return job_list

def write_data_txtfile():
    # call this when user is exiting app
    # write filtered search results list to a text file for future use
    # write updated user info data
    pass
def load_data():
    # if data.txt file:
        # read the txt file
        # assign user data to class values
        # self.login = True
    pass
def display_login():
    # after data is loaded this is called
    # if self.login:
        # display login info
    pass
def display_logo():
    # create a huge text logo
    #print(-----------------------------)
    # display_login()

    pass
def set_automation():
    #this sets up automatic searches based on times of the day and user desired times
    pass

login()
main()

