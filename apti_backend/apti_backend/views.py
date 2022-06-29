import json
from re import sub
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
    user_responses = get_user_responses(email)

    if user_responses == None:
        return -1

    # DB Fields
    scores = {}
    level_wise_distribution = {}
    topic_wise_distribution = {}
    total_score = 0


    # evaluating first 100 ques ... that is except language ques
    for question_no in correct_answers:
        question = correct_answers[question_no]['question'].strip().lower()
        correct_ans = correct_answers[question_no]['answer'].strip().lower()
        subject = correct_answers[question_no]['subject'].strip().lower()
        topic = correct_answers[question_no]['topic'].strip().lower()
        difficulty = correct_answers[question_no]['level'].strip().lower()

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

        if not topic in topic_wise_distribution[subject]:
            topic_wise_distribution[subject][topic] = [0, 0, 0, 0]

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
        user_ans = user_responses[question_no + 2].strip().lower()
        print(question_no, ":", correct_ans, ":", user_ans, ":", correct_ans == user_ans)

        # correct then -> +2 bcoz first 3 columns are timestamp, email, score
        if (user_ans == correct_ans):
            # increment no. of correct ans
            level_wise_distribution[subject][difficulty][1] += 1
            topic_wise_distribution[subject][topic][1] += 1
            # increment score
            topic_wise_distribution[subject][topic][3] += points
            total_score += points
            scores[subject] += points
        else:
            # increment no. of incorrect ans
            level_wise_distribution[subject][difficulty][2] += 1
            topic_wise_distribution[subject][topic][2] += 1

        # increment no. of total ques
        level_wise_distribution[subject][difficulty][0] += 1
        topic_wise_distribution[subject][topic][0] += 1


    # evaluate language questions
    language_mapping = {
        "c": 1,
        "c++": 11,
        "java": 21,
        "python": 31
    }

    lang1 = user_responses[103].strip().lower()
    lang2 = user_responses[144].strip().lower()

    for lang in [[lang1, 103], [lang2, 144]]:
        print(lang)
        lang_answers = get_language_answers(lang[0])
        lang_user_responses = user_responses[lang[1] + language_mapping[lang[0]] : lang[1] + 10 + language_mapping[lang[0]]]

        for question_no in lang_answers:
            question = lang_answers[question_no]['question'].strip().lower()
            correct_ans = lang_answers[question_no]['answer'].strip().lower()
            subject = lang_answers[question_no]['subject'].strip().lower()
            topic = lang_answers[question_no]['topic'].strip().lower()
            difficulty = lang_answers[question_no]['level'].strip().lower()

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

            if not topic in topic_wise_distribution[subject]:
                topic_wise_distribution[subject][topic] = [0, 0, 0, 0]

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
            user_ans = lang_user_responses.pop(0).strip().lower()
            print(question_no, ":", correct_ans, ":", user_ans, ":", correct_ans == user_ans)

            # correct then -> +2 bcoz first 3 columns are timestamp, email, score
            if (user_ans == correct_ans):
                # increment no. of correct ans
                level_wise_distribution[subject][difficulty][1] += 1
                topic_wise_distribution[subject][topic][1] += 1
                # increment score
                topic_wise_distribution[subject][topic][3] += points
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
        print("Total Score:", total_score, "\n")
        print("Scores:", scores, "\n")
        print("level_wise_distribution:", level_wise_distribution, "\n")
        print("topic_wise_distribution:", topic_wise_distribution, "\n")
        print("uid:", uid, "\n")
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
        hard = medium = easy = achieved_score = 0

        true_subject = ""
        if (subject == 'overall'):
            true_subject = subject
        elif subject == 'cn':
            true_subject = "Computer Networks"
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
            achieved_score = data['total_score']
            for sub in data['level_wise_distribution']:
                subject_labels.append(sub)
                subject_scores.append(data['scores'][sub])

                innerdata = data['level_wise_distribution'][sub]
                hard += innerdata['hard'][1]
                medium += innerdata['medium'][1]
                easy += innerdata['easy'][1]

                correct.append(innerdata['hard'][1] + innerdata['medium'][1] + innerdata['easy'][1])
                incorrect.append(innerdata['hard'][2] + innerdata['medium'][2] + innerdata['easy'][2])
        else:
            # can't calculate topic scores individually
            hard = data['level_wise_distribution'][subject]['hard'][1]
            medium = data['level_wise_distribution'][subject]['medium'][1]
            easy = data['level_wise_distribution'][subject]['easy'][1]
            achieved_score = data['scores'][subject]

            for topic in data['topic_wise_distribution'][subject]:
                subject_labels.append(topic)
                innerdata = data['topic_wise_distribution'][subject][topic]
                subject_scores.append(innerdata[3])
                correct.append(innerdata[1])
                incorrect.append(innerdata[2])

        Negative_Incorrects = []
        for i in incorrect:
            Negative_Incorrects.append(-1 * i)

        returndata = {
            'name': name,
            'total': achieved_score,
            'subject': true_subject,
            'leetcode': {
                'series': [hard, medium, easy ],
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
        "email":  "demouser7@gmail.com"
        "subject" : "dbms"
    }
    """
    data = {}
    serializer = AnalysisSerializer(data = request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        subject = serializer.data['subject']
        user_id = email.split("@")[0] 
        data = get_user_data(email)
        college = data['college']
        if subject == "overall":
            lst = get_global_ranklist()
            lst1 = get_college_ranklist(college)
        else:
            lst = get_subject_ranklist(subject)
        
        data = {}
        if subject == "overall":
            data["globalRanklist"] = lst
            data["collegeRanklist"] = lst1
        else:
            data["globalRanklist"] = lst
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
