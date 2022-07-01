import json
from re import sub
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .handleMongoDB import *
from .serializers import *


@api_view(['POST'])
def register(request):
    """
    {
        "name": "Demo User8",
        "email": "rr@gmail.com",
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
        collegekey = get_college_key(college)

        if (collegekey == -1):
            print("COLLEGE DOES NOT EXIST")
            return Response("COLLEGE DOES NOT EXIST", status=status.HTTP_400_BAD_REQUEST)

        if (key == collegekey):
            print("MATCHED")
            res = create_user(user_data)

            if res != 1:
                print("EMAIL ALREADY EXIST")
                return Response("EMAIL ALREADY EXIST", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("REGISTERED SUCCESSFULLY", status=status.HTTP_201_CREATED)
        else:
            print("NOT MATCHED")
            return Response("WRONG KEY", status=status.HTTP_401_UNAUTHORIZED)

    else:
        return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)

"""
@api_view(['POST'])
def login(request):
    ""
    {
        "email": "rr@gmail.com",
        "college": "Yeshwantrao Chavan College of Engineering",
        "key": "YCCE"
    }
    ""
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
"""

# helper function to generate analytics
def generate_test_analysis(email):
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

    res = update_scored_db(email, total_score, scores)
    if res == -1:
        print("Email:", email, "\n")
        print("Total Score:", total_score, "\n")
        print("Scores:", scores, "\n")
        print("level_wise_distribution:", level_wise_distribution, "\n")
        print("topic_wise_distribution:", topic_wise_distribution, "\n")
        return -1

    return [total_score, scores, level_wise_distribution, topic_wise_distribution]


@api_view(['POST'])
def analytics(request):
    """
    {
        "email": "rr@gmail.com",
        "subject" : "overall"
    }
    """
    serializer = AnalysisSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        subject = serializer.data['subject']

        user = get_user_data(email)

        # user does not exist
        if user is None:
            return Response("NO USER FOUND", status=status.HTTP_404_NOT_FOUND)

        print("GENERATING ANALYTICS")
        result = generate_test_analysis(email)

        if result == -1:
            return Response("USER NOT SUBMITTED THE TEST", status=status.HTTP_404_NOT_FOUND)
        else:
            print("ANALYTICS GENERATED SUCCESSFULLY")

        ############# RETURNING JSON RESPONSE ///// ANALYSIS DATA
        total_score, scores, level_wise_distribution, topic_wise_distribution = result
        name = user.get("name")
        subject_scores = []
        subject_labels = []
        correct = []
        incorrect = []
        hard = medium = easy = achieved_score = 0
        total_easy = total_medium = total_hard = 0

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
            achieved_score = total_score
            for sub in level_wise_distribution:
                subject_labels.append(sub)
                subject_scores.append(scores[sub])

                hard += level_wise_distribution[sub]['hard'][1]
                medium += level_wise_distribution[sub]['medium'][1]
                easy += level_wise_distribution[sub]['easy'][1]

                ### counting total easy, medium, hard questions
                total_hard += level_wise_distribution[sub]['hard'][0]
                total_medium += level_wise_distribution[sub]['medium'][0]
                total_easy += level_wise_distribution[sub]['easy'][0]

                correct.append(level_wise_distribution[sub]['hard'][1] + level_wise_distribution[sub]['medium'][1] + level_wise_distribution[sub]['easy'][1])
                incorrect.append(level_wise_distribution[sub]['hard'][2] + level_wise_distribution[sub]['medium'][2] + level_wise_distribution[sub]['easy'][2])
        else:
            # can't calculate topic scores individually
            hard = level_wise_distribution[subject]['hard'][1]
            medium = level_wise_distribution[subject]['medium'][1]
            easy = level_wise_distribution[subject]['easy'][1]

            total_hard = level_wise_distribution[subject]['hard'][0]
            total_medium = level_wise_distribution[subject]['medium'][0]
            total_easy = level_wise_distribution[subject]['easy'][0]

            achieved_score = scores[subject]

            for topic in topic_wise_distribution[subject]:
                subject_labels.append(topic)
                subject_scores.append(topic_wise_distribution[subject][topic][3])
                correct.append(topic_wise_distribution[subject][topic][1])
                incorrect.append(topic_wise_distribution[subject][topic][2])

        Negative_Incorrects = []
        for i in incorrect:
            Negative_Incorrects.append(-1 * i)

        returndata = {
            'name': name,
            'total': achieved_score,
            'subject': true_subject,
            'leetcode': {
                'series': [[hard, total_hard], [medium, total_medium], [easy, total_easy]],
                'labels': ["Hard", "Medium", "Easy"]
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

        return Response(returndata, status = status.HTTP_200_OK)
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
        "email":  "rr@gmail.com",
        "subject" : "overall"
    }
    """
    serializer = AnalysisSerializer(data = request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        subject = serializer.data['subject']

        data = get_user_data(email)
        college = data['college']

        data = {
            "globalRanklist" : get_global_ranklist(subject),
            "collegeRanklist" : get_college_ranklist(college, subject)
        }

        return Response(data, status=status.HTTP_200_OK)

    return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)


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
        "email" : "rr@gmail.com"
    }
    """
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        ser_data = serializer.data
        email = ser_data['email']

        max_scores = {
            'dsa': 36,
            'oops': 38,
            'os': 60,
            'cn': 60,
            'dbms': 78,
            'quantitative': 36,
            'logical': 48,
            'verbal': 36,
            'c': 38,
            'c++': 38,
            'java': 38,
            'python': 38
        }

        user_data = get_user_data(email)
        scores = user_data["scores"]

        weak_subjects = []
        for subject in scores.keys():
            if(subject in max_scores.keys()):
                user_score = scores[subject]
                max_score = max_scores[subject]
                score_85 = 0.85*max_score
                if(user_score < score_85):
                    weak_subjects.append(subject)

        core_subject = sde_bootcamp_subject = apti_subject = ""
        for subject in weak_subjects:
            if(subject=='oops' or subject=='os' or subject=='cn' or subject=='dbms' ):
                core_subject = subject
            elif(subject=='dsa' or subject=='c' or subject=='c++' or subject=='java' or subject=='python'):
                sde_bootcamp_subject = subject
            elif(subject=='verbal' or subject=='quantitative' or subject=='logical'):
                apti_subject = subject

        data = {}
        if(core_subject!=""):
            data['core'] = core_subject
        if(sde_bootcamp_subject!=""):
            data['sde_bootcamp'] = sde_bootcamp_subject
        if(apti_subject!=""):
            data['apti'] = apti_subject

        return Response(data, status=status.HTTP_200_OK)

    return Response("INVALID DATA (ISSUE IN SERIALIZATION)", status=status.HTTP_400_BAD_REQUEST)
