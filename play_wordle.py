#!/usr/bin/env python3

import sys


def get_words():
    with open('./words_ranked.txt') as f:
        words = f.read().rstrip().split()
    results = [tuple(i.split(',')) for i in words if len(i)]
    return results


def find_guess(words, words_guessed, elim, lpos):
    if len(lpos):
        reqd_letters = lpos.keys() 
    else: 
        reqd_letters = []
    high_rank = 0
    guess = ''
    skip = False
    for word,rank in words:
        if word in words_guessed:
            continue
        if any([i in word for i in elim]):
            continue
        for pos,letter in enumerate(word):
            positions = lpos.get(letter, False)
            if positions:
                if str(pos) in positions['n']:
                    skip = True
                if any([str(pos) in lpos[k]['y'] for k in lpos.keys() if k != letter]):
                    skip = True
        if skip:
            continue
        if all([i in word for i in reqd_letters]):
            rank = float(rank)
            if rank > high_rank:
                high_rank = rank
                guess = word
    return guess, high_rank


def eval_guess(word, guess, lpos):
    elim = []
    for i,letter in enumerate(guess):
        if not letter in word:
            elim.append(letter)
            continue
        else:
            if not letter in lpos.keys():
                lpos[letter] = {}
                lpos[letter]['y'] = set()
                lpos[letter]['n'] = set()
            if letter == word[i]:
                lpos[letter]['y'].add(i)
            else:
                lpos[letter]['n'].add(i)
    return elim, lpos


def create_view(lpos):
    view_list = []
    for i in range(0,5):
        blank = True
        for k in lpos.keys():
            if i in lpos[k]['y']:
                view_list.append(k)
                blank = False
        if blank:
            view_list.append('_')
    print(''.join(view_list))




try:
    WORD = sys.argv[1]
except:
    print('provide the word')

words = get_words()

turns = 20
words_guessed = []
letters_elim = []
letters_pos = {}
for turn in range(0,turns):
    create_view(letters_pos)
    print(f'\nturn: {turn + 1}')
    guess, rank = find_guess(words, words_guessed, letters_elim, letters_pos)
    print(f'guess: {guess} with rank: {rank}')
    words_guessed.append(guess)
    if WORD == guess:
        print(f"won with guess: {guess}!!!")
        break
    elim, lpos = eval_guess(WORD, guess, letters_pos)
    letters_pos.update(lpos)
    for e in elim:
        letters_elim.append(e)
