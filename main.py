from datetime import datetime
import sys
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd



        # TO-DO:
# fix job titles to loop input asking for a new title each time, when empty thats end and append list
# fix update option in menu
# have a timer set to run search Automation
# check data for double post and remove those from csv
# alert me via sms and email of job matches

def extract_local(zipcode, page):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}
    url = (f'https://www.indeed.com/jobs?q=&l={zipcode}&start={page}')
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

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
    #print(f'Searching through {len(file)} jobs for matches')
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

def multi_search_list(file, search_list): # still needs a little work
    results = []
    list = search_list.split(' ')
    for i in range(len(list)):
        search_item = list[i]
        print(f'Searching database for {search_item} jobs')
        for item in file:
            for info in item:
                capitalized = search_item.capitalize()
                #print(item[info])
                if capitalized in item[info]:
                    #print('match')
                    results.append(item)
    return results

def automation_check(now, auto): #just keeps looping need to work on this
    #now = datetime.now()
    next = now.replace(second=5)
    while auto:
        if now > next:
            print('yes')
            now = datetime.now()
            next = now.replace(second=5)
    #difference = now - time
    #print(difference)
    #if difference >= timedelta(seconds=10):
     #   print('auto check')
      #  time += now

def update_job_info():
    jobs = input('Please enter desired job titles: ') # do a loop for titles and append to jobs list instead of split
    wanted_titles = jobs.split(' ')
    pay = input('Please enter desired hourly wage: ')
    zipcode = input('Please enter your zipcode: ')
    return jobs, pay, zipcode

def display_full_table(list):
    print('display table \n ------------------')
    #print(f'{len(list)} in list')
    for item in list:
        #print(item)
        print('\n')
        for info in item:
            print(info, item[info])

def display_short_table(list):
    # this prints out index number, title, company, and pay
    print('display table\n -----------')
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
        create_new_user()
    else:
        unauth = True
        data = load_data()
        while unauth:
            if user_name == data[0]:
                password = input(f'Thank you {user_name}, please enter password: ')
                if password == data[1]:
                    print(f'Login Successful \n Loading preferences now...')
                    unauth = False
                else:
                    print('Incorrect password')
            if user_name != data[0]:
                print('No registered user by that name lets make an account \n')
                unauth = False
                create_new_user()

def create_new_user():
    empty, empty2 = True, True
    user = ''
    pwd = ''
    while empty:
        user_name = input("Please enter your username: ")
        answer = input(f'You entered {user_name} is that correct? \n yes/no? ')
        answer.lower()
        if answer == 'yes' or 'y': #passing when not entering yes
            user = user_name
            empty = False
        #if answer == 'no':
        else:
            pass
    while empty2:
        password = input('Please enter a password ')
        password2 = input('Please enter password one more time ')
        if password == password2:
            pwd = password
            empty2 = False
        else:
            print('Passwords dont match')
    job_titles, desired_pay, zipcode = update_job_info()
    data = [user, pwd, job_titles, zipcode, desired_pay]
    write_data_txtfile(data)

def main():
    job_results = []
    job_preferences = []
    time = ''
    zip = 0
    user_name = ''
    updated = False
    update_time = ''
    matches = ''
    data = load_data()
    searched = load_search_data()
    auto = False
    if len(searched) > 0:
        #print(searched[1])
        update_time = searched[0]
        matches = searched[1].strip('\n')
        updated = True
    if len(data) > 0:
        user_name = data[0]
        job_preferences = data[2]
        zip = data[3]

    running = True
    while running:
        print('\nJobbot \n-------------')
        print(f'Welcome {user_name}')
        if updated:
            print(f'Last search on {update_time}')
            if int(matches) > 0:
                print(f'Found {matches} matching jobs!')

        print('\n \n')
        print('1.Search jobs       2.Update Info     3.Display Results    4.Automation Settings        5.Exit')
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
            search_mode = True
            while search_mode:
                option = input("1.Local search      2.Remote Search     3.Search Both\n ")
                try:
                    int(option)
                    if int(option) < 4:
                        if int(option) > 0:
                            search_mode = False
                except:
                    print("Please enter one of the options")
            if option == '1':
               job_list = local_search_jobsite(zip)
            if option == '2':
                job_list = remote_search_jobsite()
            if option == '3':
                job_list3 = local_search_jobsite(zip)
                job_list2 = remote_search_jobsite()
                job_list = job_list2 + job_list3

            create_data_table(job_list)
            results = multi_search_list(job_list, job_preferences)
            update_time = datetime.now()
            timestamp = update_time.strftime("%Y-%m-%d %H:%M")
            time = update_time
            auto = True
            update_time = timestamp
            updated = True
            job_results = results
            matches = len(job_results)
            write_search_file(timestamp, matches, results)
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
            now = datetime.now()
            automation_check(now, auto)
            #print('\n\n\n1. Change auto scanner time')
        if choice == 5:
            print('Please come back soon! \nExiting Jobbot..')
            running = False
            sys.exit()

def local_search_jobsite(zip):
    job_list = []
    for i in range(0, 50, 10):  # (starting, end, increments)
        print(f'Searching page {int(i/10) + 1}')
        first_page = extract_local(zip, 0)
        transform(first_page, job_list)
    return job_list

def remote_search_jobsite():
    job_list = []
    for i in range(0, 50, 10):  # (starting, end, increments)
        print(f'Searching page {int(i/10) + 1}')
        first_page = extract(0)
        transform(first_page, job_list)
    return job_list

def write_data_txtfile(list):
    with open('data.txt', 'w') as f:
        data = list
        for item in data:
            f.write(item)
            f.write('\n')

def write_search_file(timestamp, match_number, jobs):
    with open('jobsearch.txt', 'w') as f:
        f.write(timestamp)
        f.write(',\n')
        matches = str(match_number)
        f.write(matches)
        f.write(',\n')
        for list in jobs:
            f.write(',\n')
            for items in list:
                f.write(list[items])
                f.write('\n')

def load_search_data():
    with open('jobsearch.txt', 'r') as f:
        data = f.read()
        new_data = data.split(',')
        return new_data

def load_data():
   with open('data.txt', 'r') as f:
        data = f.read()
        new_data = data.split('\n')
        #print(new_data[0])
        return new_data

def set_automation():
    #this sets up automatic searches based on times of the day and user desired times
    pass


login()
main()