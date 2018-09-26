import numpy as np
import os
from random import *
import matplotlib.pyplot as plt
import json

class Userstudy(object):
    def __init__(self, num_q):
        self.num_q = num_q
        self.num_ns = 60-self.num_q
        self.dataset = ['koba', 'pat']

    def init_userinfo(self):
        self.uname = input ("Enter your name in english")
        self.answer = {
            self.uname: {
                self.dataset[0]: {
                    'user_answer' : [],
                    'correct_answer' : []
                },
                self.dataset[1]: {
                    'user_answer' : [],
                    'correct_answer' : []
                }
            }
        }

    def load_data(self):
        if self.data == 'pat':
            text_src_path = os.path.join('./userstudy_data/PAT_text.npy')
            pal_src_path = os.path.join('./userstudy_data/PAT_palette.npy')
            self.num_color = 5
        elif self.data == 'koba':
            text_src_path = os.path.join('./userstudy_data/kobayashi_names.npy')
            pal_src_path = os.path.join('./userstudy_data/kobayashi_palettes.npy')
            self.num_color = 3
        
        with open(text_src_path, 'rb') as fin:
            self.text_seqs = np.load(fin)
        with open(pal_src_path, 'rb') as fin:
            self.pal_seqs = np.load(fin)

    def run(self):
        for i in range(2):
            self.data = self.dataset[i]
            self.load_data()
            if self.data == 'koba':
                self.init_userinfo()

            q_idx = [60]*self.num_q
            ns_idx = [60]*(self.num_ns)

            i=0
            while i < self.num_q:
                rand = randint(0,59)
                if not rand in q_idx:
                    q_idx[i] = rand
                else:
                    i -= 1
                i += 1

            i=0
            while i < self.num_ns:
                rand = randint(0,59)
                if not rand in q_idx and not rand in ns_idx:
                    ns_idx[i] = rand
                else:
                    i -= 1
                i += 1

            q_text = []
            q_palette = []
            for idx in q_idx:
                q_text += [self.text_seqs[idx]]
                q_palette += [self.pal_seqs[idx]]

            ns_text = []
            ns_palette = []
            for idx in ns_idx:
                ns_text += [self.text_seqs[idx]]
                ns_palette += [self.pal_seqs[idx]]

            for i in range(self.num_q):
                self.show_output(q_text[i], q_palette[i], ns_text[3*i:3*(i+1)], ns_palette[3*i:3*(i+1)])
            
            count=0
            for i, ans in enumerate(self.answer[self.uname][self.data]['user_answer']):    
                count += (int(ans)==self.answer[self.uname][self.data]['correct_answer'][i])

            self.answer[self.uname][self.data]['accuracy'] = '%d%%' % int((count/self.num_q)*100)

            if self.data == 'pat':
                directory = 'answer'
                if not os.path.exists(directory):
                    os.makedirs(directory)

                directory2 = os.path.join(directory,'%s.json' % (self.uname))
                with open(directory2, 'w') as outfile:
                    json.dump(self.answer, outfile)

                print('FINISH!! THANKS ^_^')

    def show_output(self, q_text, q_palette, ns_text, ns_palette):
        show_idx = [5]*4
        show_ns_idx = [4]*3
        i = 0
        while i < 4:
            rand = randint(0,3)
            if not rand in show_idx:
                show_idx[i] = rand
            else:
                i -= 1
            i += 1

        i = 0
        while i < 3:
            rand = randint(0,2)
            if not rand in show_ns_idx:
                show_ns_idx[i] = rand
            else:
                i -= 1
            i += 1


        print('============================================================')
        print('Select correct color palette corresponding to the text below')
        print('============================================================')
        print('color name: %s' % q_text)
        if self.data == 'pat':
            fig1, axs1 = plt.subplots(nrows=4, ncols=self.num_color, figsize=[8,8])
        else:
            fig1, axs1 = plt.subplots(nrows=4, ncols=self.num_color, figsize=[6,6])
            q_palette = q_palette/255
            ns_palette = [ns/255 for ns in ns_palette]

        for j, idx in enumerate(show_idx):
            if j == 0:
                color=q_palette
                axs1[idx][0].set_title('(%d)'%(idx+1))
                for i in range(self.num_color):
                    rgb = color[3*i:3*(i+1)]
                    axs1[idx][i].imshow([[rgb]])
                    axs1[idx][i].axis('off')
            else:
                color=ns_palette[show_ns_idx[j-1]]
                axs1[idx][0].set_title('(%d)'%(idx+1))
                for i in range(self.num_color):
                    rgb = color[3*i:3*(i+1)]
                    axs1[idx][i].imshow([[rgb]])
                    axs1[idx][i].axis('off')
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        plt.show()

        self.answer[self.uname][self.data]['user_answer'] += [input ("whats the answer?")]
        self.answer[self.uname][self.data]['correct_answer'] += [show_idx[0]+1]