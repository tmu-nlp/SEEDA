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
    del_id = [4, 5, 8]

    human_score = del_list(human_score, del_id)
    metric_score = del_list(metric_score, del_id)

    sort_ids = np.argsort(human_score)[::-1]
    human_score = np.sort(human_score)[::-1]
    metric_score = [metric_score[i] for i in sort_ids]

    N = int(args.window_size)
    for i in range(len(sort_ids)-N+1):
        pea, spe = calc_corr(human_score[i:i+N], metric_score[i:i+N])
        print(f'--- From ranking {i+1} to {i+N} ---')
        print(f'Pearson: {pea}')
        print(f'Spearman: {spe}')


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--human_score',
                        help='Path to the score file for human evaluations.')
    parser.add_argument('--metric_score',
                        help='Path to the score file for evaluation metrics.')
    parser.add_argument('--window_size',
                        choices=['4', '5', '6', '7', '8'],
                        help='The number of systems to use for window analysis.',
                        default='8')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_arguments()
    main(args)