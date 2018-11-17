from time import sleep, time
from IPython.core.display import clear_output
from random import randint
from requests import get
from bs4 import BeautifulSoup
import csv
import re

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
full_comment_list = []
# change the range of pages to increase the amount of pages. 1 page = 50 questions.
pages = [str(i) for i in range(1,2)]

def scrape_pages(url):
    requests = 0
    for page in pages:
        print(f'Making request to: {url + page}')

        # make a get request
        response = get(url + page + '&sort=newest&pagesize=50')

        # pause the loop
        #sleep(randint(13,45))
        sleep(randint(3,5))

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
        # for question in question_containers:
        #     if question.div.find('div', 'status unanswered'):
        #         pass
        #     else:
        #         questionList.append(question.h3.a.text)
        #         urlList.append(question.h3.a['href'])

        for question in question_containers:
            isNotAnswered = question.div.find('div', 'status unsanswered')
            answerCountList = question.find('div', 'stats').find_all('strong')
            answerCount = int(answerCountList[1].text)
            if not isNotAnswered and answerCount >= 2:
                questionList.append(question.h3.a.text)
                urlList.append(question.h3.a['href'])
            else:
                pass
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
                    #answer_containers = html.find_all('div', 'grid mb0 fw-wrap ai-start jc-end gs8 gsy')
                    #TEST#
                    #answer_containers = html.find_all('div', 'answer')
                    #comment_containers = html.find('div', 'question').find_all('div', 'comment-body')

                except:
                    print('\nSet Variable Error.\n')
                    continue
                try:
                    # This try block collects the ANSWER USERS ONLY
                    k = 0
                    #print(f'# of Answers: {len(answer_containers)}')
                    for user in answer_containers:
                        # comment_user_urls = []

                        answer_comment_containers = user.find_all('div', 'comment-text js-comment-text-and-form')
                        print('\n\n  NEW ANSWER')
                        #print(len(answer_comment_containers))
                        try:
                            for comment in answer_comment_containers:
                                #print('start of comment loop')
                                comment_body = comment.find('span', 'comment-copy').text
                                comment_user = comment.find('a', 'comment-user').text
                                # comment_user_urls.append(comment.find('div', 'comment-body').a['href'])
                                comment_user_url = comment.find('div', 'comment-body').find('a', 'comment-user')['href']
                                #print(comment_user_url)
                                checklist = []
                                #print('before if post_id != 1')
                                if user_id != 1:
                                    #print('in "if post_id != 1"')
                                    for users in users_list:
                                        if comment_user not in users:
                                            #print('Not in Checklist')
                                            checklist.append('false')
                                        else:
                                            #print('In Checklist')
                                            checklist.append('true')
                                            break

                                    #print(checklist)
                                    if 'true' in checklist:
                                        print(f'\tSkip Commenter: {comment_user}')
                                        continue
                                    elif 'false' in checklist:
                                        #print('FALSE')
                                        #user_url = answer_containers[i].find('div', 'user-details').a['href']
                                        print(f'\tCommenter: {comment_user}')
                                        sleep(randint(3,5))
                                        response1 = get(base_url + comment_user_url)
                                        html1 = BeautifulSoup(response1.text, 'html.parser')
                                        comment_user_img = html1.find('div', 'gravatar-wrapper-164').img['src']

                                        # user_data is the whole grid that contains pertinent metrics that we will be using
                                        try:
                                            user_data = html1.find('div', 'fc-medium mb16')
                                            user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')
                                            #user_metrics_cont = html1.find_all('div', 'grid gs8 gsx ai-center')
                                            #print(user_id)
                                            #print(comment_user)
                                            #print(comment_user_img)

                                            user_num_answers = user_metrics[0].text
                                            #print('num_answers good')
                                            user_num_questions = user_metrics[1].text
                                            #print('num_questions good')
                                            user_num_reached = user_metrics[2].text
                                            #print('num_reached good')
                                            #print('correct2')
                                        except:
                                            response2 = get(base_url + comment_user_url + '?tab=topactivity')
                                            #print('activity url entered')
                                            html2 = BeautifulSoup(response2.text, 'html.parser')
                                            user_num_answers = html2.find('div', id='user-panel-answers').h3.a.text.strip()
                                            user_num_answers = user_num_answers.translate({ord(c): '' for c in 'Answers ()'})
                                            #print(f'num_answers {user_num_answers}')
                                            user_num_questions = html2.find('div', id='user-panel-questions').h3.a.text.strip()
                                            user_num_questions = user_num_questions.translate({ord(c): '' for c in 'Questions ()'})
                                            #print(f'num_questions {user_num_questions}')
                                            user_num_reached = html2.find('div', 'grid--cell fs-body3 fc-dark lh-sm').text.strip()

                                        arbitrary_tags = html1.find_all('div', 'grid gs8 gsx ai-center')
                                        for arbitrary_tag in arbitrary_tags:
                                            if arbitrary_tag.find(text=re.compile('Member for ')):
                                                user_joined_date = arbitrary_tag.span['title']
                                                #print('joined_date good')
                                            if arbitrary_tag.find(text=re.compile(' profile views')):
                                                user_profile_views = arbitrary_tag.find('div', 'grid--cell fl1').text
                                                #print('profile_views good')
                                        #print(f'Joined Date: {user_joined_date}')
                                        #print(f'Views: {user_profile_views}')
                                        user_reputation = html1.find('div', 'grid--cell fs-title fc-dark').text
                                        #print('reputation good')
                                        #print(f'Reputation Obtained: {user_reputation}')
                                        #print(base_url + comment_user_url)

                                        users_list.append(tuple((user_id, comment_user, comment_user_img, user_num_answers, user_num_questions, user_num_reached, user_joined_date, user_profile_views, user_reputation, base_url + comment_user_url)))
                                        #print('append good')
                                        user_id += 1
                                        #print('+1 user good')
                                        #print('\n')

                                elif user_id == 1:
                                    #user_url = answer_containers[i].find('div', 'user-details').a['href']
                                    print(f'\tCommenter: {comment_user}')
                                    sleep(randint(3,5))
                                    response1 = get(base_url + comment_user_url)
                                    html1 = BeautifulSoup(response1.text, 'html.parser')
                                    comment_user_img = html1.find('div', 'gravatar-wrapper-164').img['src']

                                    # user_data is the whole grid that contains pertinent metrics that we will be using
                                    user_data = html1.find('div', 'fc-medium mb16')
                                    user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')
                                    #user_metrics_cont = html1.find_all('div', 'grid gs8 gsx ai-center')
                                    #print(user_id)
                                    #print(comment_user)
                                    #print(comment_user_img)

                                    user_num_answers = user_metrics[0].text
                                    #print('num_answers good')
                                    user_num_questions = user_metrics[1].text
                                    #print('num_questions good')
                                    user_num_reached = user_metrics[2].text
                                    #print('num_reached good')
                                    #print('correct2')
                                    arbitrary_tags = html1.find_all('div', 'grid gs8 gsx ai-center')
                                    for arbitrary_tag in arbitrary_tags:
                                        if arbitrary_tag.find(text=re.compile('Member for ')):
                                            user_joined_date = arbitrary_tag.span['title']
                                            #print('joined_date good')
                                        if arbitrary_tag.find(text=re.compile(' profile views')):
                                            user_profile_views = arbitrary_tag.find('div', 'grid--cell fl1').text
                                            #print('profile_views good')
                                    #print(f'Joined Date: {user_joined_date}')
                                    #print(f'Views: {user_profile_views}')
                                    user_reputation = html1.find('div', 'grid--cell fs-title fc-dark').text
                                    #print('reputation good')
                                    #print(f'Reputation Obtained: {user_reputation}')
                                    #print(base_url + comment_user_url)

                                    users_list.append(tuple((user_id, comment_user, comment_user_img, user_num_answers, user_num_questions, user_num_reached, user_joined_date, user_profile_views, user_reputation, base_url + comment_user_url)))
                                    #print('append good')
                                    user_id += 1
                                    #print('+1 user good')
                                    #print('\n')
                        except Exception as e:
                            print(e)
                            continue
    #             except Exception as e:
    #                 print(e)
    #
    #     except Exception as e:
    #         print(e)
    #     break
    # print(users_list)
                        # If this length is == 1 that means the answer was not edited.
                        if len(answer_containers[i].find_all('div', 'post-signature grid--cell fl0')) == 1:
                            user = answer_containers[i].find('div', 'user-details').a.text
                            user_img = answer_containers[i].find('div', 'gravatar-wrapper-32').img['src']
                            checklist = []
                            print('#' + str(len(users_list)))
                            if post_id != 1:
                                for users in users_list:
                                    if user not in users:
                                        checklist.append('false')
                                    else:
                                        checklist.append('true')
                                        break
                                if 'true' in checklist:
                                    print(f'\tSkip Answerer: {user}')
                                    pass
                                elif 'false' in checklist:
                                    user_url = answer_containers[i].find('div', 'user-details').a['href']
                                    print(f'\tAnswerer: {user}')
                                    sleep(randint(15,27))
                                    response1 = get(base_url + user_url)
                                    html1 = BeautifulSoup(response1.text, 'html.parser')
                                    # user_data is the whole grid that contains pertinent metrics that we will be using
                                    user_data = html1.find('div', 'fc-medium mb16')
                                    user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')
                                    user_metrics_cont = html1.find_all('div', 'grid gs8 gsx ai-center')

                                    user_num_answers = user_metrics[0].text
                                    user_num_questions = user_metrics[1].text
                                    user_num_reached = user_metrics[2].text
                                    #print('correct1')
                                    arbitrary_tags = html1.find_all('div', 'grid gs8 gsx ai-center')
                                    for arbitrary_tag in arbitrary_tags:
                                        if arbitrary_tag.find(text=re.compile('Member for ')):
                                            user_joined_date = arbitrary_tag.span['title']
                                        if arbitrary_tag.find(text=re.compile(' profile views')):
                                            user_profile_views = arbitrary_tag.find('div', 'grid--cell fl1').text
                                    #print(f'Joined Date: {user_joined_date}')
                                    #print(f'Views: {user_profile_views}')
                                    user_reputation = html1.find('div', 'grid--cell fs-title fc-dark').text
                                    #print(f'Reputation Obtained: {user_reputation}')

                                    users_list.append(tuple((user_id, user, user_img, user_num_answers, user_num_questions, user_num_reached, user_joined_date, user_profile_views, user_reputation, base_url + user_url)))

                                    user_id += 1
                                    #print(comment_user)


                            elif post_id == 1:
                                for users in users_list:
                                    if user not in users:
                                        checklist.append('false')
                                    else:
                                        checklist.append('true')
                                        break
                                if 'true' in checklist:
                                    print(f'\tSkip Answerer: {user}')
                                    pass
                                elif 'false' in checklist:
                                    user_url = answer_containers[i].find('div', 'user-details').a['href']
                                    print(f'\tAnswerer: {user}')
                                    sleep(randint(3,5))
                                    response1 = get(base_url + user_url)
                                    html1 = BeautifulSoup(response1.text, 'html.parser')
                                    # user_data is the whole grid that contains pertinent metrics that we will be using
                                    user_data = html1.find('div', 'fc-medium mb16')
                                    user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')
                                    #user_metrics_cont = html1.find_all('div', 'grid gs8 gsx ai-center')

                                    user_num_answers = user_metrics[0].text
                                    user_num_questions = user_metrics[1].text
                                    user_num_reached = user_metrics[2].text
                                    #print('correct2')
                                    arbitrary_tags = html1.find_all('div', 'grid gs8 gsx ai-center')
                                    for arbitrary_tag in arbitrary_tags:
                                        if arbitrary_tag.find(text=re.compile('Member for ')):
                                            user_joined_date = arbitrary_tag.span['title']
                                        if arbitrary_tag.find(text=re.compile(' profile views')):
                                            user_profile_views = arbitrary_tag.find('div', 'grid--cell fl1').text
                                    #print(f'Joined Date: {user_joined_date}')
                                    #print(f'Views: {user_profile_views}')
                                    user_reputation = html1.find('div', 'grid--cell fs-title fc-dark').text
                                    #print(f'Reputation Obtained: {user_reputation}')


                                    users_list.append(tuple((user_id, user, user_img, user_num_answers, user_num_questions, user_num_reached, user_joined_date, user_profile_views, user_reputation, base_url + user_url)))

                                    user_id += 1
                            i += 1

                        elif len(answer_containers[i].find_all('div', 'post-signature grid--cell fl0')) != 1:
                            user = answer_containers[i].find('div','post-signature grid--cell fl0')
                            user.decompose()
                            user = answer_containers[i].find('div','user-details').a.text
                            user_img = answer_containers[i].find('div', 'gravatar-wrapper-32').img['src']
                            checklist = []
                            if post_id != 1:
                                for users in users_list:
                                    if user not in users:
                                        checklist.append('false')
                                    else:
                                        checklist.append('true')
                                        break
                                if 'true' in checklist:
                                    print(f'\tSkip Answerer: {user}')
                                    pass
                                elif 'false' in checklist:
                                    user_url = answer_containers[i].find('div', 'user-details').a['href']
                                    print(f'\tAnswerer: {user}')
                                    sleep(randint(15,27))
                                    response1 = get(base_url + user_url)
                                    html1 = BeautifulSoup(response1.text, 'html.parser')
                                    # user_data is the whole grid that contains pertinent metrics that we will be using
                                    user_data = html1.find('div', 'fc-medium mb16')
                                    user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')
                                    user_metrics_cont = html1.find_all('div', 'grid gs8 gsx ai-center')

                                    user_num_answers = user_metrics[0].text
                                    user_num_questions = user_metrics[1].text
                                    user_num_reached = user_metrics[2].text
                                    #print('correct3')
                                    arbitrary_tags = html1.find_all('div', 'grid gs8 gsx ai-center')
                                    for arbitrary_tag in arbitrary_tags:
                                        if arbitrary_tag.find(text=re.compile('Member for ')):
                                            user_joined_date = arbitrary_tag.span['title']
                                        if arbitrary_tag.find(text=re.compile(' profile views')):
                                            user_profile_views = arbitrary_tag.find('div', 'grid--cell fl1').text
                                    #print(f'Joined Date: {user_joined_date}')
                                    #print(f'Views: {user_profile_views}')
                                    user_reputation = html1.find('div', 'grid--cell fs-title fc-dark').text
                                    #print(f'Reputation Obtained: {user_reputation}')


                                    users_list.append(tuple((user_id, user, user_img, user_num_answers, user_num_questions, user_num_reached, user_joined_date, user_profile_views, user_reputation, base_url + user_url)))

                                    user_id += 1

                            elif post_id == 1:
                                for users in users_list:
                                    if user not in users:
                                        checklist.append('false')
                                    else:
                                        checklist.append('true')
                                        break
                                if 'true' in checklist:
                                    print(f'\tSkip Answerer: {user}')
                                    pass
                                elif 'false' in checklist:
                                    user_url = answer_containers[i].find('div', 'user-details').a['href']
                                    print(f'\tAnswerer {user}')
                                    sleep(randint(15,27))
                                    response1 = get(base_url + user_url)
                                    html1 = BeautifulSoup(response1.text, 'html.parser')
                                    # user_data is the whole grid that contains pertinent metrics that we will be using
                                    user_data = html1.find('div', 'fc-medium mb16')
                                    user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')
                                    user_metrics_cont = html1.find_all('div', 'grid gs8 gsx ai-center')

                                    user_num_answers = user_metrics[0].text
                                    user_num_questions = user_metrics[1].text
                                    user_num_reached = user_metrics[2].text
                                    #print('correct4')
                                    arbitrary_tags = html1.find_all('div', 'grid gs8 gsx ai-center')
                                    for arbitrary_tag in arbitrary_tags:
                                        if arbitrary_tag.find(text=re.compile('Member for ')):
                                            user_joined_date = arbitrary_tag.span['title']
                                        if arbitrary_tag.find(text=re.compile(' profile views')):
                                            user_profile_views = arbitrary_tag.find('div', 'grid--cell fl1').text
                                    #print(f'Joined Date: {user_joined_date}')
                                    #print(f'Views: {user_profile_views}')
                                    user_reputation = html1.find('div', 'grid--cell fs-title fc-dark').text
                                    #print(f'Reputation Obtained: {user_reputation}')


                                    users_list.append(tuple((user_id, user, user_img, user_num_answers, user_num_questions, user_num_reached, user_joined_date, user_profile_views, user_reputation, base_url + user_url)))

                                    user_id += 1
                            i += 1
                        k += 1
                except Exception as e:
                    print(f'\nInner skip: {post_id}\n')
                    print(e)
                    continue

                try:
                    # This loop and conditionals checks whether or not the user_question name is in the users_list; if not, it adds the user_question to the users_list.
                    checklist = []
                    print(f'\tChecking Questioner {user_question}')
                    for users in users_list:
                        if user_question not in users:
                            checklist.append('false')
                        else:
                            checklist.append('true')
                    if 'true' in checklist:
                        print(f'\tSkip Questioner: {user_question}')
                        pass
                    elif 'false' in checklist:
                        print(f'\tQuestioner: {user_question}')
                        sleep(randint(15,27))
                        response1 = get(base_url + user_question_url)
                        html1 = BeautifulSoup(response1.text, 'html.parser')
                        # user_data is the whole grid that contains pertinent metrics that we will be using
                        user_data = html1.find('div', 'fc-medium mb16')
                        user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')
                        user_metrics_cont = html1.find_all('div', 'grid gs8 gsx ai-center')

                        user_num_answers = user_metrics[0].text
                        user_num_questions = user_metrics[1].text
                        user_num_reached = user_metrics[2].text
                        #print('correct5')
                        arbitrary_tags = html1.find_all('div', 'grid gs8 gsx ai-center')
                        for arbitrary_tag in arbitrary_tags:
                            if arbitrary_tag.find(text=re.compile('Member for ')):
                                user_joined_date = arbitrary_tag.span['title']
                            if arbitrary_tag.find(text=re.compile(' profile views')):
                                user_profile_views = arbitrary_tag.find('div', 'grid--cell fl1').text
                        #print(f'Joined Date: {user_joined_date}')
                        #print(f'Views: {user_profile_views}')
                        user_reputation = html1.find('div', 'grid--cell fs-title fc-dark').text
                        #print(f'Reputation Obtained: {user_reputation}')


                        users_list.append(tuple((user_id, user_question, user_question_img, user_num_answers, user_num_questions, user_num_reached, user_joined_date, user_profile_views, user_reputation, base_url + user_question_url)))

                        user_id += 1
                    # This loop iterates over the users_list until the user_question (name) matches one of the tuples in users_list. When there is a match it takes the tuple's user_id. The user_id is then used in a tuple that is appended to the full_question_list that gets written to a csv.
                    user_question_id = 0
                    for users in users_list:
                        if user_question in users:
                            user_question_id = users[0]
                        else:
                            pass
                    full_question_list.append(tuple((post_id, header, question, user_question_id, vote_count, answer_count, view_count[3].b.text, question_date, url, base_url + url)))
                    print('Added Question')
                    # iterate over the answer_containers list, add the post_id, and append to full_answer_list
                    i = 0
                    j = 0
                    for answer in answer_containers:
                        answer = answer_containers[j].find('div', 'post-text').text
                        vote_score = answer_containers[j].find('span', 'vote-count-post ').text
                        answer_date = answer_containers[j].find('div', 'user-action-time').span['title']
                        # answer_comment_container = answer_containers[j].find_all('div', 'comment-text js-comment-text-and-form')
                        answer_containers_id = 0
                        length = len(answer_containers[i].find_all('div', 'post-signature grid--cell fl0'))
                        owner_length = len(answer_containers[i].find_all('div', 'post-signature owner grid--cell fl0'))
                        combined_length = length + owner_length
                        for user in answer_containers:
                            if combined_length == 1:
                                user = answer_containers[i].find('div', 'user-details').a.text
                            elif combined_length != 1:
                                user = answer_containers[i].find('div','post-signature grid--cell fl0')
                                user.decompose()
                                user = answer_containers[i].find('div','user-details').a.text
                            else:
                                pass
                            for users in users_list:
                                if user in users:
                                    answer_containers_id = users[0]
                                else:
                                    pass
                        i += 1
                        full_answer_list.append(tuple((post_id, answer, vote_score, answer_date, answer_containers_id)))
                        print('Added Answer')
                        j += 1
                    post_id += 1
                except Exception as e:
                    print(f'\nSecond Inner skip: {post_id}\n')
                    print(e)
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


# def add_user_question(answer_container):
#     user_url = answer_container.find('div', 'user-details').a['href']
#     print(f'\tStepping into {user_url}')
#     sleep(randint(15,27))
#     response1 = get(base_url + user_url)
#     html1 = BeautifulSoup(response1.text, 'html.parser')
#     # user_data is the whole grid that contains pertinent metrics that we will be using
#     user_data = html1.find('div', 'fc-medium mb16')
#     user_metrics = user_data.find_all('div', 'grid--cell fs-body3 fc-dark fw-bold')
#     #user_metrics_cont = html1.find_all('div', 'grid gs8 gsx ai-center')
#
#     user_num_answers = user_metrics[0].text
#     user_num_questions = user_metrics[1].text
#     user_num_reached = user_metrics[2].text
#     print('correct2')
#     arbitrary_tags = html1.find_all('div', 'grid gs8 gsx ai-center')
#     for arbitrary_tag in arbitrary_tags:
#         if arbitrary_tag.find(text=re.compile('Member for ')):
#             user_joined_date = arbitrary_tag.span['title']
#         if arbitrary_tag.find(text=re.compile(' profile views')):
#             user_profile_views = arbitrary_tag.find('div', 'grid--cell fl1').text
#     print(f'Joined Date: {user_joined_date}')
#     print(f'Views: {user_profile_views}')
#     user_reputation = html1.find('div', 'grid--cell fs-title fc-dark').text
#     print(f'Reputation Obtained: {user_reputation}')
#
#     return user_num_answers


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
        csv_out.writerow(['User ID', 'Username', 'Image', 'Answers', 'Questions', 'Reached', 'Joined Date', 'Profile Views', 'Reputation', 'URL'])
        for row in users_list:
            csv_out.writerow(row)
        print("Users successfully written to csv.")
