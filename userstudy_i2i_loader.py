import numpy as np
import pandas as pd
import os
from random import *
import matplotlib.pyplot as plt
import json
import glob
import random
from PIL import Image, ImageDraw

class Userstudy(object):
    def __init__(self, num_q):
        self.num_q = num_q
        self.imgdir = './userstudy_data/'
        self.dataset = ['ours', 'drit', 'munit']
            #['ours', 'drit', 'munit', 'cdgan']
        self.dataset_pick_num = [10, 10, 10]
            #[10, 10, 10, 10]
        self.userstudy_df = pd.read_csv('./userstudy.csv').sample(60)
        self.real_filenames = random.sample(glob.glob(self.imgdir+'real/*.jpg'), 30)

    def init_userinfo(self):
        self.uname = input("Enter your name in english")
        self.answer = {
            self.uname: {
                'Q1': {
                    'user_answer': [],
                    'correct_answer': []
                },
                'Q2': {
                    'user_answer': [],
                    'correct_answer': []
                },
                'Q3': {
                    'user_answer': [],
                    'correct_answer': []
                },
                'Q4': {
                    'user_answer': [],
                    'correct_answer': []
                }
            }
        }

    def make_question_pair(self):
        AB_list = self.userstudy_df.iloc[:30]['ours_AB'].tolist()
        ours_list = map(lambda x:(self.imgdir+'ours/' + x, 'ours'), AB_list[:10])
        drit_list = map(lambda x:(self.imgdir + 'drit/' + x, 'drit'), AB_list[10:20])
        munit_list = map(lambda x:(self.imgdir + 'munit/' + x, 'munit'), AB_list[20:30])
        #cdgan_list = map(lambda x:(self.imgdir + 'cdgan/' + x, 'cdgan'), AB_list[30:40])
        ab_list = []
        ab_list.extend(ours_list)
        ab_list.extend(drit_list)
        ab_list.extend(munit_list)
        #ab_list.extend(cdgan_list)
        random.shuffle(ab_list)

        real_Q = [pair for pair in zip(ab_list, self.real_filenames)]
        ours_Q = self.userstudy_df.iloc[30:]['ours_AB'].tolist()
        return real_Q, ours_Q

    def run(self):
        real_Q, ours_Q = self.make_question_pair()
        self.init_userinfo()
        for q in real_Q[:self.num_q]:
            self.show_question(q, _type='real')

        dataset = self.dataset[1:]
        types = dataset*10
        random.shuffle(types)

        for q, _type in zip(ours_Q[:self.num_q], types[:self.num_q]):
            self.show_question(q, _type=_type)

        directory = 'answer'
        if not os.path.exists(directory):
            os.makedirs(directory)

        directory2 = os.path.join(directory, '%s.json' % (self.uname))
        with open(directory2, 'w') as outfile:
            json.dump(self.answer, outfile)

        print('FINISH!! THANKS ^_^')

    def show_question(self, q, _type='real'):
        if _type=='real':
            q = list(q)
            correct = {}
            random.shuffle(q)

            if type(q[0]) is tuple:
                correct['A'] = q[0][1]
                correct['B'] = 'real'
                A = plt.imread(q[0][0])
                B = plt.imread(q[1])
            else:
                correct['A'] = 'real'
                correct['B'] = q[1][1]
                A = plt.imread(q[0])
                B = plt.imread(q[1][0])

            images = [A, B]

            print('============================================================')
            print('A 와 B 중 하나는 가짜 이미지 입니다. 아래의 질문에 답해주세요')
            print('============================================================')

            plt.figure(figsize=(5, 5))
            columns = 2
            for i, image in enumerate(images):
                if i == 0:
                    text = 'A'
                else:
                    text = 'B'
                axs1 = plt.subplot(len(images) / columns + 1, columns, i + 1)
                plt.imshow(image)
                axs1.axis('off')
                axs1.set_title(str(text))

            plt.show()
            self.answer[self.uname]['Q1']['user_answer'] += [input("어느것이 실제 이미지인가요?(A, B)\t")]
            self.answer[self.uname]['Q1']['correct_answer'] += [correct]

        else:

            print('=================================================================================')
            print('갈색헤어 + 무표정인 이미지를 금색헤어 + 웃는 얼굴로 변환하는 학습모델입니다.')
            print('앞으로 말할 "스타일"의 의미는 style 이미지의 머리 색과 표정입니다.')
            print('=================================================================================')

            correct = {}

            A = self.imgdir + 'brown_nosmile/' + q[:6] + '.jpg'
            B = self.imgdir + 'blond_smile/' + q[6:]
            other_AB = self.imgdir + _type + '/' + q
            ours_AB = self.imgdir + 'ours/' + q

            q = [(other_AB, _type), (ours_AB, 'ours')]
            random.shuffle(q)

            if q[0][0] == 'ours':
                correct['A'] = q[0][1]
                correct['B'] = q[1][1]
                q_A = plt.imread(q[0][0])
                q_B = plt.imread(q[1][0])
            else:
                correct['A'] = q[1][1]
                correct['B'] = q[0][1]
                q_A = plt.imread(q[1][0])
                q_B = plt.imread(q[0][0])

            A = plt.imread(A)
            B = plt.imread(B)

            images = [A, B, q_A, q_B]

            plt.figure(figsize=(8, 8))
            columns = 2
            for i, image in enumerate(images):
                if i == 0:
                    text = 'Content'
                elif i == 1:
                    text = 'Style'
                elif i == 2:
                    text = 'A'
                elif i == 3:
                    text = 'B'

                axs1 = plt.subplot(len(images) / columns + 1, columns, i + 1)
                plt.imshow(image)
                axs1.axis('off')
                axs1.set_title(str(text))

            plt.show()

            self.answer[self.uname]['Q2']['user_answer'] += [input("어느 것이 스타일을 잘 적용했나요(A, B)?\t")]
            self.answer[self.uname]['Q2']['correct_answer'] += [correct]
            self.answer[self.uname]['Q3']['user_answer'] += [input("어느 것이 content 이미지를 잘 유지하고 있나요(A, B)\t")]
            self.answer[self.uname]['Q3']['correct_answer'] += [correct]
            self.answer[self.uname]['Q4']['user_answer'] += [input("어떤 이미지가 content의 배경정보를 잘 유지하고 있나요 (A, B)\t")]
            self.answer[self.uname]['Q4']['correct_answer'] += [correct]