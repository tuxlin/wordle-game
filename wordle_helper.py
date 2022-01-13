#!/usr/bin/env python3

import sys
import json
import pandas as pd

def get_all_words():
    with open('words.txt') as f:
        lines = f.readlines()
    words = []
    for line in lines:
        line = line.strip()
        if len(line):
            words.append(line)
    return words


def get_reqd_letters(letters_w_pos):
    letters = []
    for i in letters_w_pos.keys():
        value = letters_w_pos[i]
        if value.get('n', False):
            if len(value['n']) < 5:
                letters.append(i)
        if value.get('y', False):
            letters.append(i)
    return letters


def get_reqd_positions(letters_w_pos):
    positions = {}
    for i in letters_w_pos.keys():
        value = letters_w_pos[i]
        position = value.get('y', False)
        if position is not False:
            positions[i] = position
    return positions


def fit_word(letters_w_pos, word):
    reqd_letters = get_reqd_letters(letters_w_pos)
    reqd_pos = get_reqd_positions(letters_w_pos)
    if len(reqd_letters):
        if not all([l in word for l in reqd_letters]):
            return False
    for i,letter in enumerate(list(word)):
        if i in list(reqd_pos.values()):
            if reqd_pos.get(letter, False) is not i:
                return False
        if letter in letters_w_pos.keys():
            pos = letters_w_pos[letter]
            if i is pos['y']:
                continue
            elif pos['n']:
                if i in pos['n']:
                    return False
    return True


def get_possible_words(letters_w_pos, five_letter_words):
    if not len(letters_w_pos.keys()):
        return five_letter_words
    possible_words = []
    for w in five_letter_words:
        if fit_word(letters_w_pos, w):
            possible_words.append(w)
    return possible_words


def update_letters_w_pos(letter, pos, correct, lwps):
    correct = correct.lower()
    ypos = npos = False
    if correct == 'y':
        ypos = pos
    elif correct == 'a':
        if letter in lwps.keys():
            if len(lwps[letter]['n']):
                npos = list(set(lwps[letter]['n'] + [pos]))
        else:
            npos = [pos]
    elif correct == 'n':
        npos = [0,1,2,3,4]

    lwps[letter] = {'y': ypos, 'n': npos}
    return lwps


def column_list(x):
    columns_list_df = []
    for col in x.columns:
        columns_list_df.append(x[col].value_counts().rank())
    return pd.DataFrame(columns_list_df).T


def get_score(x, cols_df, four_letter_words):
    word_as_list = x[:5].to_list()
    word = ''.join(word_as_list)
    rank = 0
    for i,letter in enumerate(word_as_list):
        rank += cols_df.loc[letter, i]
    if word[4] in ['s', 'd'] and ''.join(word[0:4]) in four_letter_words:
        if rank > 20:
            rank -= rank * 0.5
    if ''.join(word[2:5]) in ['ied', 'ies']:
        if rank > 20:
            rank -= rank * 0.25
    return rank


def rank_possible_words(possible_words, four_letter_words):
    words = [list(i) for i in possible_words]
    if not len(words):
        raise('no words no rank')

    words_df = pd.DataFrame(words)
    cols_df = column_list(words_df)
    words_df['word'] = words_df.iloc[:,:5].apply(''.join, axis=1)
    words_df['rank'] = words_df.T.apply(get_score, cols_df=cols_df, four_letter_words=four_letter_words)
    words_df['uniq'] = words_df.T.apply(lambda x: len(x[:5].unique()))
    return words_df.sort_values(['uniq','rank'], ascending=False)[['word']].head(10).to_csv(header=None,index=False)


def get_four_letter_words():
    four_letter_words = set([])
    with open('./4-letter.txt') as f:
        for i in f.read().split():
            if len(i):
                four_letter_words.add(i)
    return four_letter_words


def auto_check(guess, answer, turn, letters_w_pos):
    print(f'guessing: {guess}')
    if guess == answer:
        print(f'I win on turn {turn}')
        sys.exit()
    else:
        for pos,letter in enumerate(guess):
            correct = 'n'
            if letter in answer:
                if answer[pos] == letter:
                    correct = 'y'
                else:
                    correct = 'a'
            letters_w_pos = update_letters_w_pos(letter, pos, correct, letters_w_pos)
    return letters_w_pos


if __name__ == "__main__":

    answer_provided = sys.argv[1] if len(sys.argv) > 1 else False

    five_letter_words = get_all_words()
    four_letter_words = get_four_letter_words()
    letters_w_pos = {}
    possible_words = get_possible_words(letters_w_pos, five_letter_words)
    possible_words_ranked = rank_possible_words(possible_words, four_letter_words)

    turns = 0
    while turns < 20:
        turns += 1
        possible_words = get_possible_words(letters_w_pos, five_letter_words)
        possible_words_ranked = rank_possible_words(possible_words, four_letter_words)

        if answer_provided:
            guess = possible_words_ranked.split('\n')[0]
            print(f'guess provided: {guess}')
            letters_w_pos = auto_check(guess, answer_provided, turns, letters_w_pos)
        else:
            print(f'\n{possible_words_ranked}')
            if len(possible_words_ranked.split()) <= 1:
                print('only one word left -- exiting...')
                sys.exit()
            guess = input('guess: ')
            for pos, letter in enumerate(list(guess)):
                correct = input(f'({letter.upper()})[y/a/N]: ') or 'n'
                letters_w_pos = update_letters_w_pos(letter, pos, correct, letters_w_pos)
