# SEEDA

This repository contains the code for our TACL paper:

[Revisiting Meta-evaluation for Grammatical Error Correction]([https://aclanthology.org/2024.tacl-1.47/]).

If you use this code, please cite our paper:

```
@misc{kobayashi2024revisiting,
      title={Revisiting Meta-evaluation for Grammatical Error Correction}, 
      author={Masamune Kobayashi and Masato Mita and Mamoru Komachi},
      year={2024},
      eprint={2403.02674},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```


## Meta-evaluate evaluation metrics using SEEDA
### System-level meta-evaluation

First, evaluate the sentences in `outputs/subset` at the system level with the evaluation metric you want to meta-evaluate. Then, calculate the correlation using the system scores provided by humans (Table 2).[^1]

To conduct system-level meta-evaluation, simply run:
```
python corr_system.py --human_score HUMAN_SCORE --metric_score METRIC_SCORE --systems SYSTEMS
```
- `HUMAN_SCORE` The file of human evaluation scores for each system in `scores/human` directory. The system scores are arranged alphabetically as follows:
1: BART, 2: BERT-fuse, 3: GECToR_BERT, 4: GECToR_ens, 5: GPT-3.5, 6: INPUT, 7: LM-Critic, 8: PIE, 9: REF-F, 10: REF-M, 11: Riken-Tohoku, 12: T5, 13: TemplateGEC, 14: TransGEC, 15: UEDIN-MS.
- `METRIC_SCORE` The file of evaluation metric scores for each system in `scores/metric` directory. Please create system-level evaluation score files for the target metrics. All scores should be sorted alphabetically.
- `SYSTEMS` Set of systems to consider for meta-evaluation. The default is set to `base`. To consider fluently corrected sentences, use `+REF-F_GPT-3.5`. To consider uncorrected sentences, use `INPUT`. Specify `all` to use all 15 systems.

To conduct system-level window analysis, simply run:
```
python window_analysis_system.py --human_score HUMAN_SCORE --metric_score METRIC_SCORE --window_size WINDOW_SIZE
```
- `WINDOW_SIZE` The number of systems to use for window analysis.


### Sentece-level meta-evaluation
First, evaluate the sentences in `outputs/subset` at the sentence level with the evaluation metric you want to meta-evaluate. Then, calculate the correlation using the sentence scores provided by humans.

To conduct sentence-level meta-evaluation, simply run:
```
python corr_sentence.py --human_score HUMAN_SCORE --metric_score METRIC_SCORE --order ORDER --systems SYSTEMS
```
- `HUMAN_SCORE` The xml file of human evaluation scores for each sentence in `data` directory. Consider the evaluation granularity of the metric (edit or sentence) when making your selection.
- `METRIC_SCORE` The file of evaluation metric scores for each sentence in `scores/metric/sentence_score` directory. Please create evaluation score files for the target metrics.
- `ORDER` If a higher metric score indicates better system performance, choose `higher`; otherwise, choose `lower`.
- `SYSTEMS` Set of systems to consider for meta-evaluation. The default is set to `base`. To consider fluently corrected sentences, use `+REF-F_GPT-3.5`. To consider uncorrected sentences, use `INPUT`. Specify `all` to use all 15 systems.


## Evaluation scores for each system
We provide the evaluation scores for each system to promote the use of existing evaluation metrics[^2].

| | M<sup>2</sup> | SentM<sup>2</sup> | PT-M<sup>2</sup> | ERRANT | SentERRANT | PT-ERRANT | GoToScorer | GLEU | Scribendi Score | SOME | IMPARA |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| BART | 50.3 | 51.29 | 50.41 | 46.66 | 50.31 | 48.89 | 15.86 | 63.46 | 527 | 0.7933 | 5.31 |
| BERT-fuse | 62.77 | 63.21 | 62.99 | 58.99 | 61.81 | 61.18 | 21.1 | 68.5 | 739 | 0.8151 | 5.816 |
| GECToR-BERT | 61.83 | 61.23 | 60.76 | 58.05 | 59.76 | 59.17 | 18.98 | 66.56 | 640 | 0.8016 | 5.644 |
| GECToR-ens | 63.53 | 60.37 | 59.21 | 61.43 | 59.64 | 58.57 | 16.58 | 65.08 | 529 | 0.786 | 5.17 |
| GPT-3.5 | 53.5 | 53.28 | 53.41 | 44.12 | 49.23 | 48.93 | 22.85 | 65.93 | 835 | 0.8379 | 6.376 |
| INPUT | 0.0 | 31.33 | 31.33 | 0.0 | 31.4 | 31.33 | 0.0 | 56.6 | 0.0 | 0.7506 | 4.089 |
| LM-Critic | 55.5 | 58.0 | 57.16 | 52.38 | 56.41 | 55.86 | 16.23 | 64.39 | 683 | 0.8028 | 5.543 |
| PIE | 59.93 | 60.7 | 60.69 | 55.89 | 59.35 | 58.65 | 21.07 | 67.83 | 601 | 0.8066 | 5.659 |
| REF-F | 47.48 | 48.99 | 46.54 | 33.24 | 41.41 | 39.69 | 21.7 | 60.34 | 711 | 0.8463 | 6.569 |
| REF-M | 60.12 | 62.3 | 62.91 | 54.77 | 60.11 | 60.6 | 23.92 | 67.27 | 754 | 0.8155 | 5.908 |
| Riken-Tohoku | 64.74 | 64.22 | 64.31 | 61.88 | 63.13 | 62.73 | 20.94 | 68.37 | 678 | 0.8123 | 5.757 |
| T5 | 65.07 | 65.2 | 66.13 | 60.65 | 63.24 | 63.77 | 20.46 | 68.81 | 668 | 0.8202 | 6.045 |
| TemplateGEC | 56.29 | 57.59 | 57.47 | 51.34 | 56.08 | 55.96 | 14.7 | 65.07 | 448 | 0.7972 | 5.52 |
| TransGEC | 68.08 | 68.33 | 68.37 | 64.43 | 66.76 | 66.37 | 21.93 | 70.2 | 779 | 0.82 | 6.035 |
| UEDIN-MS | 64.55 | 62.68 | 62.67 | 61.33 | 61.38 | 61.19 | 18.94 | 67.41 | 666 | 0.808 | 5.591 |

[^1]: Human rankings can be created by replacing the judgments.xml file in [Grundkiewicz et al. (2015)’s repository](https://github.com/grammatical/evaluation).
[^2]: All scores are based on the entire text of the CoNLL-2014 test set and differ from the scores obtained using the subset used for our meta-evaluation.
