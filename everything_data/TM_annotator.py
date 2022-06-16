import pandas as pd
import pickle
import os
import random
pd.set_option("display.max_colwidth", None)

filename = "topic_manual_annotated.csv"

with open("Topic_modeling_results/pre_topic_modeling_all", "rb") as fp:   # Unpickling
    b = pickle.load(fp)

if not os.path.exists(filename):
    file = open(filename, 'w')
    file.write("subject1\n")
    file.write("0\n")
    file.write("0\n")
    file.write("0\n")
    file.write("0\n")
    file.write("0\n")
    file.write("0\n")
    file.write("0\n")
    file.write("0\n")
    file.write("0\n")
    file.write("0\n")
else:
	file = open(filename,"a")

data = pd.read_csv(filename)

# load topics
with open("Topic_modeling_results/allGPUPDMM.topWords") as file:
    gpupdmm_topic = file.readlines()
gpupdmm_topic = [i[:-2] for i in gpupdmm_topic]

with open("Topic_modeling_results/allGPUDMM.topWords") as file:
    gpudmm_topic = file.readlines()
gpudmm_topic = [i[:-2] for i in gpudmm_topic]

with open("Topic_modeling_results/allLDA.topWords") as file:
    lda_topic = file.readlines()
lda_topic = [i[:-2] for i in lda_topic]

with open("Topic_modeling_results/allLFDMM.topWords") as file:
    lfdmm_topic = file.readlines()
lfdmm_topic = [i[:-2] for i in lfdmm_topic]

with open("Topic_modeling_results/allDMM.topWords") as file:
    dmm_topic = file.readlines()
dmm_topic = [i[:-2] for i in dmm_topic]

with open("Topic_modeling_results/resultsBTM_topic_word_15.txt") as file:
    btm_topic = file.readlines()
btm_topic = [i[:-2] for i in btm_topic[1::2]]

print(data)
print("Existing names: " + str(data.columns.values.tolist()))
annotator_name = input("Please enter a new name: ")

seed = input("Please enter a seed: ")
random.seed(seed)
random_list = random.sample(range(len(b)), 10)
b_list = [b[i] for i in random_list]
os.system('clear')

label_list = []
print("BTM")
for i in range(len(b_list)):
    print(b_list[i])
    for topic in range(len(btm_topic)):
        print("({}) {}". format(topic, btm_topic[topic]))
    label = int(input('Enter an integer between 0 and 14: '))
    label_list.append((random_list[i], label))
    os.system('clear')
data[annotator_name + "_BTM" + str(seed)] = label_list
data.to_csv(filename, index=False)

label_list = []
print("GPUDMM")
for i in range(len(b_list)):
    print(b_list[i])
    for topic in range(len(gpudmm_topic)):
        print("({}) {}". format(topic, gpudmm_topic[topic]))
    label = int(input('Enter an integer between 0 and 14: '))
    label_list.append((random_list[i], label))
    os.system('clear')
data[annotator_name + "_GPUDMM" + str(seed)] = label_list
data.to_csv(filename, index=False)

label_list = []
print("GPU-PDMM")
for i in range(len(b_list)):
    print(b_list[i])
    for topic in range(len(gpupdmm_topic)):
        print("({}) {}". format(topic, gpupdmm_topic[topic]))
    label = int(input('Enter an integer between 0 and 14: '))
    label_list.append((random_list[i], label))
    os.system('clear')
data[annotator_name + "_GPUPDMM" + str(seed)] = label_list
data.to_csv(filename, index=False)

label_list = []
print("LDA")
for i in range(len(b_list)):
    print(b_list[i])
    for topic in range(len(lda_topic)):
        print("({}) {}". format(topic, lda_topic[topic]))
    label = int(input('Enter an integer between 0 and 14: '))
    label_list.append((random_list[i], label))
    os.system('clear')
data[annotator_name + "_LDA" + str(seed)] = label_list
data.to_csv(filename, index=False)

label_list = []
print("LFDMM")
for i in range(len(b_list)):
    print(b_list[i])
    for topic in range(len(lfdmm_topic)):
        print("({}) {}". format(topic, lfdmm_topic[topic]))
    label = int(input('Enter an integer between 0 and 14: '))
    label_list.append((random_list[i], label))
    os.system('clear')
data[annotator_name + "_LFDMM" + str(seed)] = label_list
data.to_csv(filename, index=False)

label_list = []
print("DMM")
for i in range(len(b_list)):
    print(b_list[i])
    for topic in range(len(dmm_topic)):
        print("({}) {}". format(topic, dmm_topic[topic]))
    label = int(input('Enter an integer between 0 and 14: '))
    label_list.append((random_list[i], label))
    os.system('clear')
data[annotator_name + "_DMM" + str(seed)] = label_list
data.to_csv(filename, index=False)
print(data)