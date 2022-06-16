import os
import random
import time
import subprocess
subjects = ["classification_three_bert.py", "classification_three_forest.py", "classification_three_LR.py", "classification_three_multinomial.py", "classification_three_sequential.py", "classification_three_SVM.py", 
"topic_modeling_BTM.py", "topic_modeling_DMM.py", "topic_modeling_GPUPDMM.py", "topic_modeling_LDA.py", "topic_modeling_LFDMM.py", "topic_modeling_GPUDMM.py", 
"sentiment_flair.py", "sentiment_senti4SD.py", "sentiment_sentistrength.py", "sentiment_textblob.py", "sentiment_roberta.py", "sentiment_VADER.py",
"similarity_bert.py", "similarity_jaccard.py", "similarity_thefuzz.py", "similarity_mpnet.py", "similarity_WMD.py", "similarity_SIMBA.py"]

for i in range(5):
    for subject in random.sample(subjects, len(subjects)):
        print("Now running {} for run {}".format(subject, i))
        if subject == "similarity_SIMBA.py":
            os.system('source /Users/kallejanssen/opt/anaconda3/etc/profile.d/conda.sh && conda activate /Users/kallejanssen/opt/anaconda3/envs/py27 && python aligner.py && conda deactivate')
        else:
            run_experiment = "python3 " + subject
            os.system(run_experiment)
        time.sleep(60)