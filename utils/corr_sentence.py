import argparse
import itertools
import xml.etree.ElementTree as ET


def make_h_mtx(human_score, targets, del_targets):
    h_mtx = {}
    N = len(targets)
    sys2id = {targets[i]: i for i in range(N)}

    tree = ET.parse(human_score)
    root = tree.getroot()
    for child in root.find('error-correction-ranking-result'):
        src_id = str(int(child.attrib['src-id']) - 1)

        judg_set = {}
        for trans in child:
            targets = trans.attrib['system'].split()
            rank = int(trans.attrib['rank'])
            for target in targets:
                if target in del_targets:
                    continue
                target = [sys2id[target]]
                if rank not in judg_set.keys():
                    judg_set[rank] = target
                else:
                    judg_set[rank].extend(target)

        sub_mtx = [[None for _ in range(N)] for _ in range(N)]
        comb = itertools.combinations(sorted(judg_set.keys()), 2)
        for c in comb:
            rank1 = c[0]
            rank2 = c[1]
            target1 = judg_set[rank1]
            target2 = judg_set[rank2]
            for t1 in target1:
                for t2 in target2:
                    if t1 < t2:
                        if int(rank1) < int(rank2):
                            sub_mtx[t1][t2] = 1
                        else:
                            sub_mtx[t1][t2] = -1 
                    else:
                        if rank1 < rank2:
                            sub_mtx[t2][t1] = -1
                        else:
                            sub_mtx[t2][t1] = 1 

        while(1):
            if src_id not in h_mtx.keys():
                break
            src_id = src_id + 'rep'
        h_mtx[src_id] = sub_mtx
    
    h_mtx = {k: h_mtx[k] for k in sorted(h_mtx.keys())}
    return h_mtx


def make_m_mtx(metric_score, targets):
    m_mtx = {}
    N = len(targets)
    src_ids = [11, 12, 28, 35, 36, 45, 46, 52, 54, 58, 62, 64, 65, 68, 70, 73, 75, 76, 85, 87, 93, 96, 98, 105, 111, 115, 116, 118, 125, 130, 131, 132, 133, 136, 138, 143, 145, 155, 157, 160, 162, 163, 168, 170, 173, 176, 178, 179, 180, 197, 198, 200, 201, 202, 205, 206, 207, 209, 212, 213, 219, 226, 228, 229, 231, 233, 236, 240, 243, 247, 252, 254, 258, 260, 261, 266, 268, 270, 272, 274, 282, 284, 288, 295, 300, 302, 304, 310, 312, 313, 315, 316, 318, 319, 321, 327, 329, 336, 339, 349, 351, 355, 363, 371, 373, 380, 383, 389, 392, 395, 396, 398, 400, 401, 402, 407, 415, 424, 426, 428, 431, 436, 441, 446, 447, 449, 450, 451, 452, 454, 455, 458, 461, 471, 474, 476, 485, 488, 490, 494, 501, 502, 504, 505, 506, 507, 510, 511, 521, 525, 528, 536, 537, 538, 539, 552, 553, 558, 579, 590, 592, 595, 597, 603, 606, 609, 610, 614, 615, 620, 623, 625, 627, 631, 636, 639, 645, 646, 647, 648, 649, 651, 654, 658, 664, 665, 668, 673, 674, 675, 678, 681, 682, 683, 686, 697, 700, 701, 702, 705, 707, 710, 711, 715, 717, 719, 720, 724, 725, 726, 727, 730, 731, 734, 743, 744, 745, 749, 754, 756, 759, 765, 766, 769, 771, 772, 777, 778, 779, 780, 781, 782, 783, 784, 787, 788, 791, 792, 796, 797, 799, 806, 808, 810, 811, 812, 817, 818, 823, 824, 825, 827, 828, 830, 835, 837, 838, 842, 844, 846, 849, 851, 853, 856, 857, 859, 867, 872, 873, 875, 881, 886, 887, 888, 889, 891, 895, 901, 902, 905, 910, 911, 912, 913, 916, 918, 923, 924, 930, 933, 936, 938, 942, 943, 950, 961, 962, 963, 968, 973, 974, 977, 979, 982, 998, 999, 1001, 1003, 1012, 1016, 1017, 1024, 1031, 1038, 1040, 1051, 1052, 1055, 1056, 1057, 1063, 1064, 1065, 1069, 1070, 1075, 1081, 1083, 1084, 1085, 1088, 1089, 1090, 1091, 1099, 1100, 1104, 1106, 1109, 1110, 1111, 1112, 1119, 1128, 1140, 1142, 1143, 1145, 1146, 1151, 1152, 1154, 1160, 1162, 1168, 1170, 1176, 1184, 1195, 1196, 1202, 1205, 1206, 1207, 1209, 1211, 1212, 1213, 1222, 1224, 1229, 1231, 1234, 1245, 1247, 1249, 1260, 1261, 1263, 1264, 1265, 1275, 1288, 1290, 1294, 1297, 1298, 1300, 1303, 1306, 1310]
    
    score_path = [metric_score + '/' + t + '.txt' for t in targets]
    set = []
    for path in score_path:
        with open(path, 'r') as f:
            sub_set = list(map(float, f.readlines()))
        set.append(sub_set)
    
    scores = []
    for i in range(len(src_ids)):
        score = []
        for j in range(N):
            score.append(set[j][i])
        scores.append(score)

    i = 0
    for src_id, score in zip(src_ids, scores):
        sub_mtx = [[None for _ in range(N)] for _ in range(N)]
        comb = itertools.combinations(range(N), 2)
        for c in comb:
            t1 = c[0]
            t2 = c[1]
            score1 = scores[i][t1]
            score2 = scores[i][t2]
            if score1 > score2:
                if args.order == 'higher':
                    sub_mtx[t1][t2] = 1
                else:
                    sub_mtx[t1][t2] = -1
            else:
                if args.order == 'higher':
                    sub_mtx[t1][t2] = -1
                else:
                    sub_mtx[t1][t2] = 1
        m_mtx[str(src_id)] = sub_mtx
        i += 1

    m_mtx = {k: m_mtx[k] for k in sorted(m_mtx.keys())}
    return m_mtx


def calc_corr(h_mtx, m_mtx):
    cnt_mtx = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    N = len(h_mtx['11'][0])

    for src_id, h in h_mtx.items():
        if 'rep' in src_id:
            src_id = src_id.replace('rep', '')
        m = m_mtx[src_id]

        for i in range(N):
            for j in range(N):
                if h[i][j] == -1 and m[i][j] == -1:
                    cnt_mtx[0][0] += 1
                elif h[i][j] == -1 and m[i][j] == 0:
                    cnt_mtx[0][1] += 1
                elif h[i][j] == -1 and m[i][j] == 1:
                    cnt_mtx[0][2] += 1
                elif h[i][j] == 1 and m[i][j] == -1:
                    cnt_mtx[2][0] += 1
                elif h[i][j] == 1 and m[i][j] == 0:
                    cnt_mtx[2][1] += 1
                elif h[i][j] == 1 and m[i][j] == 1:
                    cnt_mtx[2][2] += 1

    denom = cnt_mtx[0][0] + cnt_mtx[0][1] + cnt_mtx[0][2] + cnt_mtx[2][0] + cnt_mtx[2][1] + cnt_mtx[2][2]
    acc_numer = cnt_mtx[0][0] + cnt_mtx[2][2]
    ken_numer = cnt_mtx[0][0] + cnt_mtx[2][2] - cnt_mtx[0][2] - cnt_mtx[2][0]
    acc = acc_numer / denom
    ken = ken_numer / denom
    return acc, ken


def main(args):
    targets = [
        'BART', 'BERT-fuse', 'GECToR-BERT', 'GECToR-ens', 'GPT-3.5', 'INPUT', 'LM-Critic', 'PIE', 
        'REF-F', 'REF-M', 'Riken-Tohoku', 'T5', 'TemplateGEC', 'TransGEC', 'UEDIN-MS'
        ]
    if args.systems == 'base':
        del_id = [4, 5, 8]
    elif args.systems == '+INPUT':
        del_id = [4, 8]
    elif args.systems == '+REF-F_GPT-3.5':
        del_id = [5]
    else:
        del_id = []
    del_targets = [targets[i] for i in del_id]
    targets = [t for i, t in enumerate(targets) if i not in del_id]

    h_mtx = make_h_mtx(args.human_score, targets, del_targets)
    m_mtx = make_m_mtx(args.metric_score, targets)

    acc, ken = calc_corr(h_mtx, m_mtx)
    print(f'Accuracy: {acc}')
    print(f'Kendall: {ken}')


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--human_score',
                        help='Path to the xml file for human evaluations.')
    parser.add_argument('--metric_score',
                        help='Path to the sentence score directory for evaluation metrics.')
    parser.add_argument('--order',
                        choices=['higher', 'lower'],
                        help='If a higher score indicates better system performance, choose "higher"; otherwise, choose "lower".',
                        default='higher')
    parser.add_argument('--systems',
                        choices=['base', '+INPUT', '+REF-F_GPT-3.5', 'all'],
                        help='Set of systems used for meta-evaluation.',
                        default='base')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_arguments()
    main(args)