from time import sleep, time
from IPython.core.display import clear_output
from random import randint
from requests import get
from bs4 import BeautifulSoup
import csv

base_url = 'https://security.stackexchange.com'
questionList = []
urlList = []
questionContentList = []
answerContentList = []
users_list = []
start_time = time()
# final lists of data to be pushed to csv file
full_question_list = []
full_answer_list = []
# change the range of pages to increase the amount of pages. 1 page = 50 questions.
pages = [str(i) for i in range(1,2)]

def scrape_pages(url):
    requests = 0
    for page in pages:
        print(f'Making request to: {url + page}')

        # make a get request
        response = get(url + page + '&sort=newest&pagesize=50')

        # pause the loop
        sleep(randint(13,45))

        # monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print(f"Request:{requests} || {elapsed_time/60}")
        clear_output(wait = True)

        # parse the content of the request with BeautifulSoup
        html = BeautifulSoup(response.text, 'html.parser')

        # remove questions with similar class that are not relevant
        for a in html.find_all('a', 'js-gps-track question-hyperlink mb0'):
            a.decompose()

        # scrape all div containers for each question
        question_containers = html.find_all('div', 'question-summary')
        # scrape all href values of each anchor tag (these are the URL's to each question)
        raw_links = html.find_all('a', 'question-hyperlink', href=True)

        # iterate over the question_containers ResultSet to select only answered questions
        for question in question_containers:
            if question.div.find('div', 'status unanswered'):
                pass
            else:
                questionList.append(question.h3.a.text)
                urlList.append(question.h3.a['href'])
    print('Number of questions collected:' + str(len(questionList)))
    print('Number of URLs collected:' + str(len(urlList)) + '\n')



def step_into_url():
    post_id = 1
    user_id = 1
    print('\nIterating over URLs. Please wait...\n')
    while True:
        try:
            for url in urlList:
                try:
                    i = 0
                    full_url = base_url + url
                    print(f'{post_id}/{len(urlList)} | {url}')
                    response = get(full_url)
                    html = BeautifulSoup(response.text, 'html.parser')
                    # remove "this question already has an answer here" div
                    for div in html.find_all('div', 'question-status question-originals-of-duplicate'):
                        div.decompose()
                    # scrape the header, question, and answer(s)
                    vote_count = html.find('div', 'question').find('span', 'vote-count-post ' ).text
                    answer_count = html.find('div', 'subheader answers-subheader').h2.get('data-answercount')
                    view_count = html.find_all('p', 'label-key')
                    header = html.find('div', {'id': 'question-header'}).h1.a.text
                    question = html.find('div', 'postcell post-layout--right').div.text
                    question_date = html.find('div', 'user-action-time').span['title']
                    answer_containers = html.find_all('div', 'answer')
                    user_question = html.find('div', 'post-signature owner grid--cell').find('div', 'user-details').a.text
                    user_question_img = html.find('div', 'post-signature owner grid--cell').img['src']
                    user_question_url = html.find('div', 'post-signature owner grid--cell').find('div', 'user-details').a['href']
                    user_answer = html.find_all('div', 'grid mb0 fw-wrap ai-start jc-end gs8 gsy')

                except:
                    print('\nSet Variable Error.\n')
                    continue
                try:
                    # This try block collects the ANSWER USERS ONLY
                    k = 0
                    for user in user_answer:
                        if len(user_answer[i].find_all('div', 'post-signature grid--cell fl0')) == 1:
                            user = user_answer[i].find('div', 'user-details').a.text
                            user_img = user_answer[i].find('div', 'gravatar-wrapper-32').img['src']
                            checklist = []
                            if post_id != 1:
                                for users in users_list:
                                    if user not in users:
                                        checklist.append('false')
                                    else:
                                        checklist.append('true')
                                if 'true' in checklist:
                                    pass
                                elif 'false' in checklist:
                                    user_url = user_answer[i].find('div', 'user-details').a['href']
                                    print(f'\tStepping into {user_url}')
                                    sleep(randint(15,27))
                                    response1 = get(base_url + user_url)
                                    html1 = BeautifulSoup(response1.text, 'html.parser')
                                    # user_data is the whole grid that contains pertinent metrics that we will be using
                                    user_data = html1.find('div', 'fc-medium mb16')
                                    user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')

                                    user_num_answers = user_metrics[0].text
                                    user_num_questions = user_metrics[1].text
                                    user_num_reached = user_metrics[2].text

                                    users_list.append(tuple((user_id, user, user_img, user_num_answers, user_num_questions, user_num_reached, base_url + user_url)))

                                    user_id += 1

                            elif post_id == 1:
                                user_url = user_answer[i].find('div', 'user-details').a['href']
                                print(f'\tStepping into {user_url}')
                                sleep(randint(15,27))
                                response1 = get(base_url + user_url)
                                html1 = BeautifulSoup(response1.text, 'html.parser')
                                # user_data is the whole grid that contains pertinent metrics that we will be using
                                user_data = html1.find('div', 'fc-medium mb16')
                                user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')

                                user_num_answers = user_metrics[0].text
                                user_num_questions = user_metrics[1].text
                                user_num_reached = user_metrics[2].text

                                users_list.append(tuple((user_id, user, user_img, user_num_answers, user_num_questions, user_num_reached, base_url + user_url)))

                                user_id += 1
                            i += 1

                        elif len(user_answer[i].find_all('div', 'post-signature grid--cell fl0')) != 1:
                            user = user_answer[i].find('div','post-signature grid--cell fl0')
                            user.decompose()
                            user = user_answer[i].find('div','user-details').a.text
                            user_img = user_answer[i].find('div', 'gravatar-wrapper-32').img['src']
                            checklist = []
                            if post_id != 1:
                                for users in users_list:
                                    if user not in users:
                                        checklist.append('false')
                                    else:
                                        checklist.append('true')
                                if 'true' in checklist:
                                    pass
                                elif 'false' in checklist:
                                    user_url = user_answer[i].find('div', 'user-details').a['href']
                                    print(f'\tStepping into {user_url}')
                                    sleep(randint(15,27))
                                    response1 = get(base_url + user_url)
                                    html1 = BeautifulSoup(response1.text, 'html.parser')
                                    # user_data is the whole grid that contains pertinent metrics that we will be using
                                    user_data = html1.find('div', 'fc-medium mb16')
                                    user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')

                                    user_num_answers = user_metrics[0].text
                                    user_num_questions = user_metrics[1].text
                                    user_num_reached = user_metrics[2].text

                                    users_list.append(tuple((user_id, user, user_img, user_num_answers, user_num_questions, user_num_reached, base_url + user_url)))

                                    user_id += 1

                            elif post_id == 1:
                                user_url = user_answer[i].find('div', 'user-details').a['href']
                                print(f'\tStepping into {user_url}')
                                sleep(randint(15,27))
                                response1 = get(base_url + user_url)
                                html1 = BeautifulSoup(response1.text, 'html.parser')
                                # user_data is the whole grid that contains pertinent metrics that we will be using
                                user_data = html1.find('div', 'fc-medium mb16')
                                user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')

                                user_num_answers = user_metrics[0].text
                                user_num_questions = user_metrics[1].text
                                user_num_reached = user_metrics[2].text

                                users_list.append(tuple((user_id, user, user_img, user_num_answers, user_num_questions, user_num_reached, base_url + user_url)))

                                user_id += 1
                            i += 1
                        k += 1
                except:
                    print(f'\nInner skip: {post_id}\n')
                    continue

                try:
                    # This loop and conditionals checks whether or not the user_question name is in the users_list; if not, it adds the user_question to the users_list.
                    checklist = []
                    for users in users_list:
                        if user_question not in users:
                            checklist.append('false')
                        else:
                            checklist.append('true')
                    if 'true' in checklist:
                        pass
                    elif 'false' in checklist:
                        print(f'\tStepping into {user_question_url}')
                        sleep(randint(15,27))
                        response1 = get(base_url + user_question_url)
                        html1 = BeautifulSoup(response1.text, 'html.parser')
                        # user_data is the whole grid that contains pertinent metrics that we will be using
                        user_data = html1.find('div', 'fc-medium mb16')
                        user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')

                        user_num_answers = user_metrics[0].text
                        user_num_questions = user_metrics[1].text
                        user_num_reached = user_metrics[2].text

                        users_list.append(tuple((user_id, user_question, user_question_img, user_num_answers, user_num_questions, user_num_reached, base_url + user_question_url)))

                        user_id += 1
                    # This loop iterates over the users_list until the user_question (name) matches one of the tuples in users_list. When there is a match it takes the tuple's user_id. The user_id is then used in a tuple that is appended to the full_question_list that gets written to a csv.
                    user_question_id = 0
                    for users in users_list:
                        if user_question in users:
                            user_question_id = users[0]
                        else:
                            pass
                    full_question_list.append(tuple((post_id, header, question, user_question_id, vote_count, answer_count, view_count[3].b.text, question_date, url, base_url + url)))
                    # iterate over the answer_containers list, add the post_id, and append to full_answer_list
                    i = 0
                    j = 0
                    for answer in answer_containers:
                        answer = answer_containers[j].find('div', 'post-text').text
                        vote_score = answer_containers[j].find('span', 'vote-count-post ').text
                        answer_date = answer_containers[j].find('div', 'user-action-time').span['title']
                        user_answer_id = 0
                        length = len(user_answer[i].find_all('div', 'post-signature grid--cell fl0'))
                        owner_length = len(user_answer[i].find_all('div', 'post-signature owner grid--cell fl0'))
                        combined_length = length + owner_length
                        for user in user_answer:
                            if combined_length == 1:
                                user = user_answer[i].find('div', 'user-details').a.text
                            elif combined_length != 1:
                                user = user_answer[i].find('div','post-signature grid--cell fl0')
                                user.decompose()
                                user = user_answer[i].find('div','user-details').a.text
                            else:
                                pass
                            for users in users_list:
                                if user in users:
                                    user_answer_id = users[0]
                                else:
                                    pass
                        i += 1
                        full_answer_list.append(tuple((post_id, answer, vote_score, answer_date, user_answer_id)))
                        j += 1
                    post_id += 1
                except:
                    print(f'\nSecond Inner skip: {post_id}\n')
                    continue
        except:
            print(f'\nOuter skip: {post_id}\n')
            pass
        break
    print(f'Number of Questions collected: {len(full_question_list)}')
    print(f'Number of Answers collected: {len(full_answer_list)}')
    print(f'Number of Users collected: {len(users_list)}')
    write_questions_to_csv(full_question_list)
    write_answers_to_csv(full_answer_list)
    write_users_to_csv(users_list)


def write_questions_to_csv(full_question_list):
    with open('questions.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Post ID', 'Title', 'Question', 'User ID', 'Vote Score', 'Answer Count', 'View Count', 'Date', 'URL', 'Full URL'])
        for row in full_question_list:
            csv_out.writerow(row)
        print("Questions successfully written to csv.")

def write_answers_to_csv(full_answer_list):
    with open('answers.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Post ID', 'Answer', 'Vote Score', 'Date', 'User ID'])
        for row in full_answer_list:
            csv_out.writerow(row)
        print("Answers successfully written to csv.")

def write_users_to_csv(users_list):
    with open('users.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['User ID', 'Username', 'Image', 'Answers', 'Questions', 'Reached', 'URL'])
        for row in users_list:
            csv_out.writerow(row)
        print("Users successfully written to csv.")
