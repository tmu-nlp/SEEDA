import argparse
import numpy as np
import scipy.stats as st


def open_file(score_path):
    with open(score_path, 'r') as f:
        score = list(map(float, f.readlines()))
    return score


def calc_corr(human_score, metric_score):
    pea, pea_p = st.pearsonr(human_score, metric_score)
    spe, spe_p = st.spearmanr(human_score, metric_score)
    return pea, spe


def main(args):
    human_score = open_file(args.human_score)
    metric_score = open_file(args.metric_score)

    del_list = lambda human_score, del_id: [h for i, h in enumerate(human_score) if i not in del_id]
    if args.systems == 'base':
        del_id = [4, 5, 8]
    elif args.systems == '+INPUT':
        del_id = [4, 8]
    elif args.systems == '+REF-F_GPT-3.5':
        del_id = [5]
    else:
        del_id = []

    human_score = del_list(human_score, del_id)
    metric_score = del_list(metric_score, del_id)

    pea, spe = calc_corr(human_score, metric_score)
    print(f'Pearson: {pea}')
    print(f'Spearman: {spe}')


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--human_score',
                        help='Path to the score file for human evaluations.')
    parser.add_argument('--metric_score',
                        help='Path to the score file for evaluation metrics.')
    parser.add_argument('--systems',
                        choices=['base', '+INPUT', '+REF-F_GPT-3.5', 'all'],
                        help='Set of systems used for meta-evaluation.',
                        default='base')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_arguments()
    main(args)