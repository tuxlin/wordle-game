#!/usr/bin/env python3

import pandas as pd


def get_words_df():

    data = []
    with open('./words.txt') as f:
        words = f.read().split()
        for word in words:
            word_dict = {}
            if len(word):
                for n in range(0,5):
                    word_dict[f'col{n}'] = word[n]
                data.append(word_dict)

    df = pd.DataFrame(data=data)
    return df


def get_four_letter_words():
    flws = set([])
    with open('./4-letter.txt') as f:
        for i in f.read().split():
            if len(i):
                flws.add(i)

    return flws


def column_list(x):

    column_list_df = []
    for col_name in x.columns:
        column_list_df.append(x[col_name].value_counts().rank())

    return pd.DataFrame(column_list_df)


def get_score(x, cols_df, flws):

    word_as_list = x[:5].to_list()
    word = ''.join(word_as_list)
    rank = 0

    for i,letter in enumerate(word_as_list):
        rank += cols_df.loc[letter, f'col{i}']
    if word[4] in ['s', 'd'] and ''.join(word[0:4]) in flws:
        if rank > 20:
            rank -= rank * 0.5
    if ''.join(word[2:5]) in ['ied', 'ies']:
        if rank > 20:
            rank -= rank * 0.25

    return rank


def get_uniq(x):
    unique = x[:5].unique()
    return len(unique)


flws = get_four_letter_words()
pd.set_option("display.max_rows", None, "display.max_columns", None)
words_df = get_words_df()
letters_df = column_list(words_df)
cols_df = letters_df.T
words_df['word'] = words_df.iloc[:].agg(''.join, axis=1)
words_df['rank'] = words_df.T.apply(get_score, cols_df=cols_df, flws=flws)
words_df['uniq'] = words_df.T.apply(lambda x: len(x[:5].unique()))
print(words_df.sort_values(['uniq', 'rank'], ascending=False)[['word', 'rank']].to_csv(header=None,index=False))
