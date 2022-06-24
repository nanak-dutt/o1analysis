import json
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .handleDB import *
from .serializers import *


@api_view(['POST'])
def register(request):
    """
    {
        "name": "Demo User8",
        "email": "demouser8@gmail.com",
        "college": "Yeshwantrao Chavan College of Engineering",
        "key": "YCCE",
        "mobile": 8888888888
    }
    """
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data
        college = data['college']
        key = data['key']

        user_data = {
            'name': data['name'],
            'email': data['email'],
            'college': data['college'],
            'mobile': data['mobile'],
        }

        user_id = data["email"].split("@")[0]

        if check_id_exist(user_id) != 0:
            print("EMAIL ALREADY EXIST")
            return Response("EMAIL ALREADY EXIST", status=status.HTTP_400_BAD_REQUEST)

        if check_college_exist(college) != 1:
            print("COLLEGE DOES NOT EXIST")
            return Response("COLLEGE DOES NOT EXIST", status=status.HTTP_400_BAD_REQUEST)

        collegekey = get_college_key(college)

        if (collegekey == -1):
            print("KEY FINDING ERROR")
            return Response("KEY FINDING ERROR", status=status.HTTP_401_UNAUTHORIZED)

        if (key == collegekey):
            print("MATCHED")
            res = create_user(user_data, user_id)

            if res != 1:
                print("ERROR IN PUSHING USER DATA TO DB")
                return Response("ERROR IN PUSHING USER DATA TO DB", status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response("REGISTERED SUCCESSFULLY", status=status.HTTP_201_CREATED)
        else:
            print("NOT MATCHED")
            return Response("WRONG KEY", status=status.HTTP_401_UNAUTHORIZED)

    else:
        return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """
    {
        "email": "demouser8@gmail.com",
        "college": "Yeshwantrao Chavan College of Engineering",
        "key": "YCCE"
    }
    """
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data

        email = data['email']
        college = data['college']
        key = data['key']

        user_id = email.split("@")[0]
        if (check_id_exist(user_id) != 1):
            print("EMAIL DOES NOT EXIST")
            return Response("EMAIL DOES NOT EXIST", status=status.HTTP_401_UNAUTHORIZED)

        clg = get_college_name(user_id)
        if (clg != college):
            print("WRONG COLLEGE NAME")
            return Response("WRONG COLLEGE NAME", status=status.HTTP_401_UNAUTHORIZED)

        collegekey = get_college_key(college)
        if (collegekey == -1):
            print("KEY FINDING ERROR")
            return Response("KEY FINDING ERROR", status=status.HTTP_401_UNAUTHORIZED)
        elif (key == collegekey):
            print("LOGGED IN SUCCESFULLY")
            return Response("LOGGED IN SUCCESSFULLY", status=status.HTTP_200_OK)
        else:
            print("NOT MATCHED")
            return Response("WRONG key", status=status.HTTP_401_UNAUTHORIZED)

    else:
        return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)


# helper function to generate analytics
def generate_test_analysis(email, uid):
    correct_answers = get_correct_answers()

    # ORIGINAL CODE Uncomment this

    #user_responses = get_user_responses(email)
    # if user_responses == None:
    #     return -1


    # TEMPORARY CODE TO CHECK API --> Bhushan Wanjari
    language_chosen1='c'
    language_chosen2='python'
    user_responses={}
    i=0
    for question_no in correct_answers:
        i=i+1
        subject = correct_answers[question_no]['subject']
        topic = correct_answers[question_no]['topic']
        # correct_ans = correct_answers[question_no]['answer']
        if(subject=='language' and (topic!=language_chosen1 and topic!=language_chosen2)):
            user_responses[question_no + 2]="" ## Putting Blank answer
        elif(i%7==0 or i%5==0):
            user_responses[question_no + 2]=correct_answers[question_no]['answer']
        else:
            user_responses[question_no + 2]='setting wrong answer'
    ### END

    # DB Fields
    scores = {}
    level_wise_distribution = {}
    topic_wise_distribution = {}
    total_score = 0

    ## language skipped checker
    lang={
        "c":0,
        "c++":0,
        "python":0,
        "java":0
    }
    lang_total={
        "c":0,
        "c++":0,
        "python":0,
        "java":0
    }

    for question_no in correct_answers:
        subject = correct_answers[question_no]['subject']
        topic = correct_answers[question_no]['topic']
        if(subject=='language'):
           # checking blank answers
           lang_total[topic]=lang_total[topic]+1
           if (user_responses[question_no + 2].strip() == ""):
               lang[topic]=lang[topic]+1
    skipped_lang=[]
    if(lang_total['c']==lang['c']):
         skipped_lang.append('c')
    if(lang_total['c++']==lang['c++']):
         skipped_lang.append('c++')
    if(lang_total['python']==lang['python']):
         skipped_lang.append('python')
    if(lang_total['java']==lang['java']):
         skipped_lang.append('java')


    for question_no in correct_answers:
        question = correct_answers[question_no]['question']
        correct_ans = correct_answers[question_no]['answer']
        subject = correct_answers[question_no]['subject']
        topic = correct_answers[question_no]['topic']
        difficulty = correct_answers[question_no]['level']

        # Field check
        if not subject in scores:
            scores[subject] = 0
        if not subject in level_wise_distribution:
                level_wise_distribution[subject] = {
                "hard": [0, 0, 0],
                "medium": [0, 0, 0],
                "easy": [0, 0, 0]
            }
        if not subject in topic_wise_distribution:
                topic_wise_distribution[subject] = {}
        if(subject!='language'):
            if not topic in topic_wise_distribution[subject]:
                topic_wise_distribution[subject][topic] = [0, 0, 0]
        elif(subject=='language' and (topic!=skipped_lang[0] and topic!=skipped_lang[1])):
            if not topic in topic_wise_distribution[subject]:
                topic_wise_distribution[subject][topic] = [0, 0, 0]



        if difficulty == "easy":
            points = 2
        elif difficulty == "medium":
            points = 4
        elif difficulty == "hard":
            points = 6
        else:
            print(difficulty)
            return -1

        # DEBUGGING
        print(question_no, correct_answers[question_no]["id"])
        print(correct_ans.strip())
        print(user_responses[question_no + 2].strip())
        print(correct_ans.strip() == user_responses[question_no + 2].strip())


        # correct then -> +2 bcoz first 3 columns are timestamp, email, score
        if(subject=='language' and (topic==skipped_lang[0] or topic==skipped_lang[1])):
            continue
        elif (user_responses[question_no + 2].strip() == correct_ans.strip()):
            # increment no. of correct ans
            level_wise_distribution[subject][difficulty][1] += 1
            topic_wise_distribution[subject][topic][1] += 1

            total_score += points
            scores[subject] += points
        else:
            # increment no. of incorrect ans
            level_wise_distribution[subject][difficulty][2] += 1
            topic_wise_distribution[subject][topic][2] += 1

        # increment no. of total ques
        level_wise_distribution[subject][difficulty][0] += 1
        topic_wise_distribution[subject][topic][0] += 1


    res = update_scored_db(total_score, scores, level_wise_distribution, topic_wise_distribution, uid)
    if res == -1:
        print("Total Score:", total_score)
        print("Scores:", scores)
        print("level_wise_distribution:", level_wise_distribution)
        print("topic_wise_distribution:", topic_wise_distribution)
        print("uid:", uid)
        return -1

    return 1


@api_view(['POST'])
def analytics(request):
    """
    {
        "email": "demouser6@gmail.com",
        "subject" : "overall"
    }
    """
    serializer = AnalysisSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        subject = serializer.data['subject']
        user_id = email.split("@")[0]

        # check if email exist
        if check_id_exist(user_id) != 1:
            return Response("NO USER FOUND", status=status.HTTP_404_NOT_FOUND)

        res = check_analytics_exist(user_id)

        # analytics not generated
        if res != 1:
            print("GENERATING ANALYTICS")
            result = generate_test_analysis(email, user_id)
            print(result)
            if result == -1:
                return Response("USER NOT SUBMITTED THE TEST", status=status.HTTP_404_NOT_FOUND)
            else:
                print("ANALYTICS GENERATED SUCCESSFULLY")

        ############# RETURNING JSON RESPONSE ///// ANALYSIS DATA
        data = get_user_data(email)
        name = data['name']
        subject_scores = []
        subject_labels = []
        correct = []
        incorrect = []
        hard = medium = easy = total = 0

        true_subject = ""
        if (subject == 'overall'):
            true_subject = subject
        elif subject == 'cn':
            true_subject = "Computer NetWorks"
        elif subject == 'os':
            true_subject = "Operating Systems"
        elif subject == 'dbms':
            true_subject = "Database Management System"
        elif subject == 'dsa':
            true_subject = "Data Structures and Algorithms"
        elif subject == 'oops':
            true_subject = "Object Oriented Programming"
        else:
            true_subject = subject

        if (subject == 'overall'):
            total = data['total_score']
            for sub in data['level_wise_distribution']:
                subject_labels.append(sub)
                subject_scores.append(data['scores'][sub])

                innerdata = data['level_wise_distribution'][sub]

                hard += innerdata['hard'][0]
                medium += innerdata['medium'][0]
                easy += innerdata['easy'][0]

                correct.append(innerdata['hard'][1] + innerdata['medium'][1] + innerdata['easy'][1])
                incorrect.append(innerdata['hard'][2] + innerdata['medium'][2] + innerdata['easy'][2])
        else:
            hard = data['level_wise_distribution'][subject]['hard'][0]
            medium = data['level_wise_distribution'][subject]['medium'][0]
            easy = data['level_wise_distribution'][subject]['easy'][0]
            total = hard + easy + medium
            for topic in data['topic_wise_distribution'][subject]:
                subject_labels.append(topic)
                innerdata = data['topic_wise_distribution'][subject][topic]
                correct.append(innerdata[1])
                incorrect.append(innerdata[2])
                subject_scores.append(innerdata[0])

        Negative_Incorrects = []
        for i in incorrect:
            Negative_Incorrects.append(-1 * i)

        returndata = {
            'name': name,
            'total': total,
            'subject': true_subject,
            'leetcode': {
                'series': [hard, medium, easy],
                'labels': ["Hard", "Medium", "Easy"],
            },
            'stackgraph': {
                'series': [
                    {
                        'name': "Correct",
                        'data': correct,
                    },
                    {
                        'name': "Incorrect",
                        'data': Negative_Incorrects,
                    },
                ],
                'labels': subject_labels,
            },
            'linegraph': {
                'labels': subject_labels,
                'series': [
                    {
                        'name': "Subjects",
                        'data': subject_scores,
                    },
                ],
            },
            'piechart': {
                'series': subject_scores,
                'labels': subject_labels,
            },
        }

        return Response(returndata)
    else:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def globalranklist(request):
    lst = get_global_ranklist()
    data = {
        "ranklist": lst
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def collegeranklist(request):
    """
    {
        "college" : "Shri Ramdeobaba College of Engineering and Management"
    }
    """
    serializer = CollegeRankListSerializer(data = request.data)
    if serializer.is_valid():
        college = serializer.data['college']
        lst = get_college_ranklist(college)
        data = {
            "ranklist": lst
        }
        return Response(data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def subjectranklist(request):
    """
    {
        "subject" : "dbms"
    }
    """
    data = {}
    serializer = SubjectRanklistSerializer(data = request.data)
    if serializer.is_valid():
        subject = serializer.data['subject']
        if subject == "overall":
            lst = get_global_ranklist()
        else:
            lst = get_subject_ranklist(subject)

        data = {
            "ranklist": lst
        }
        return Response(data, status=status.HTTP_200_OK)

    return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def question_bank(request):
    questions = get_all_questions()
    return Response({"data": questions}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_link(request):
    testlink = get_test_link()
    return Response({"link": testlink}, status=status.HTTP_200_OK)


@api_view(['GET'])
def college_list(request):
    college_names = list(sorted(get_all_colleges()))
    return Response({"clg_names" : college_names}, status=status.HTTP_200_OK)


@api_view(['POST'])
def weakest_topics(request):
    """
    {
        "email" : "demouser6@gmail.com"
    }
    """
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        ser_data = serializer.data
        email = ser_data['email']
        user_id = email.split("@")[0]

        user_data = get_user_data(email)

        subject_list = []
        topic_list = []

        if 'topic_wise_distribution' not in user_data.keys():
            return Response("NO TEST GIVEN YET", status=status.HTTP_400_BAD_REQUEST)

        # calculating 85% score benchmark from any random topic
        questions = db.collection("ques_bank").get()
        question1 = questions[0].to_dict()

        question1_subject = question1['subject']
        question1_topic = question1['topic']

        topic_questions = db.collection("ques_bank").where(u'subject', u'==', question1_subject).where(u'topic', u'==', question1_topic).get()

        score = 0
        for question in topic_questions:
            dict = question.to_dict()

            if(dict['level']=='easy'):
                score += 2
            elif(dict['level']=='medium'):
                score += 4
            elif(dict['level']=='hard'):
                score += 6

        score_85 = score*0.85
        print(score_85)

        subjects = user_data["topic_wise_distribution"]

        for subject in subjects.keys():
            topics = subjects[subject]

            var = score_85
            weak_topic = ""

            for topic in topics.keys():
                mark = topics[topic][0]
                if (mark < var):
                    var = mark
                    weak_topic = topic

            # if there is no weak topic in subject, subject will not be added
            if(weak_topic != ""):
                subject_list.append(subject)
                topic_list.append(weak_topic)

        print(subject_list)
        print(topic_list)

        core_topic=""
        core_subject=""
        sde_bootcamp_topic=""
        sde_bootcamp_subject=""
        apti_topic=""
        apti_subject=""

        sz = len(subject_list)

        for i in range(0, sz):
            subject = subject_list[i]
            topic = topic_list[i]

            if(subject=='oops' or subject=='os' or subject=='cn' or subject=='dbms' ):
                core_topic = topic
                core_subject = subject
            elif(subject=='dsa'):
                sde_bootcamp_topic = topic
                sde_bootcamp_subject = subject
            elif(subject=='verbal' or subject=='quantitative' or subject=='logical'):
                apti_topic = topic
                apti_subject = subject

        data = {}
        if(core_topic != "" and core_subject!=""):
            data['core'] = core_topic + " is weakest topic of " + core_subject

        if(sde_bootcamp_topic != "" and sde_bootcamp_subject!=""):
            data['sde_bootcamp'] = sde_bootcamp_topic + " is weakest topic of " + sde_bootcamp_subject

        if(apti_topic != "" and apti_subject!=""):
            data['apti'] = apti_topic + " is weakest topic of " + apti_subject

        return Response(data, status=status.HTTP_200_OK)

    return Response("INVALID DATA (ISSUE IN SERIALIZATION)", status=status.HTTP_400_BAD_REQUEST)