import pandas as pd
import random
import collections
random.seed(1)
pd.set_option("display.max_colwidth", None)

filename = "topic_manual_annotated.csv"

# load topic assignments
with open("Topic_modeling_results/allGPUPDMM.topicAssignments") as file:
    gpupdmm_ass = file.readlines()

with open("Topic_modeling_results/allGPUDMM.topicAssignments") as file:
    gpudmm_ass = file.readlines()

with open("Topic_modeling_results/allLDA.topicAssignments") as file:
    lda_ass = file.readlines()

with open("Topic_modeling_results/allLFDMM.topicAssignments") as file:
    lfdmm_ass = file.readlines()

with open("Topic_modeling_results/allDMM.topicAssignments") as file:
    dmm_ass = file.readlines()

btm_ass = pd.read_table('Topic_modeling_results/resultsBTM_doc_topic_15.txt', sep='\s+')

data = pd.read_csv(filename)

btm_predicted = [list(btm_ass.iloc[i]).index(max(btm_ass.iloc[i])) for i in range(len(btm_ass))]
gpupdmm_predicted = [collections.Counter([int(j) for j in i.split() if j != ' ' and j != '\n']).most_common(1)[0] for i in gpupdmm_ass]
gpudmm_predicted = [collections.Counter([int(j) for j in i.split() if j != ' ' and j != '\n']).most_common(1)[0][0] for i in gpudmm_ass]
lda_predicted = [collections.Counter([int(j) for j in i.split() if j != ' ' and j != '\n']).most_common(1)[0][0] for i in lda_ass]
lfdmm_predicted = [collections.Counter([int(j) for j in i.split() if j != ' ' and j != '\n']).most_common(1)[0][0] for i in lfdmm_ass]
dmm_predicted = [collections.Counter([int(j) for j in i.split() if j != ' ' and j != '\n']).most_common(1)[0][0] for i in dmm_ass]

methods = [['kalle_BTM1', 'kirsten_BTM1', 'kalle_BTM2'], ['kalle_GPUDMM1', 'kirsten_GPUDMM1', 'kalle_GPUDMM2'], ['kalle_GPUPDMM1', 'kirsten_GPUPDMM1', 'kalle_GPUPDMM2'], ['kalle_LDA1', 'kirsten_LDA1', 'kalle_LDA2'], ['kalle_LFDMM1', 'kirsten_LFDMM1', 'kalle_LFDMM2'], ['kalle_DMM1', 'kirsten_DMM1', 'kalle_DMM2']]
predicted = [btm_predicted, gpupdmm_predicted, gpudmm_predicted, lda_predicted, lfdmm_predicted, dmm_predicted]
for method in range(len(methods)):
    correct = 0
    incorrect = 0
    for annotator in methods[method]:
        for i in range(len(data[annotator])):
            index = int(data[annotator][i][1:-1].split()[0][:-1])
            correct_label = int(data[annotator][i][1:-1].split()[1])
            if predicted[method][index] == correct_label:
                correct += 1
            else:
                incorrect += 1
    print(['BTM', 'GPUDMM', 'GPUPDMM', 'LDA', 'LFDMM', 'DMM'][method])
    print(correct/(correct+incorrect))