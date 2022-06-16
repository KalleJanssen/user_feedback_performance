import os
from datetime import datetime
import sys
import time
filename = "times.txt"

if not os.path.exists(filename):
	file = open(filename, 'w')
	file.write("approach, method, start_time, end_time\n")
else:
	file = open(filename,"a")

# datetime object containing current date and time
start = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
for i in range(6):
	os.system("java -jar ../topic_modeling/STTM-master.nosync/jar/STTM.jar -model GPU_PDMM -corpus ../topic_modeling/STTM-master.nosync/dataset/pre_topic_modeling_all.txt -vectors ../topic_modeling/STTM-master.nosync/glove/glove.6B.50d.txt -name allGPUPDMM -ntopics 15 -twords 8")

end = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
file.write("topic_modeling, GPUPDMM, " + start[:-3] + ", " + end[:-3] + "\n")
file.close()
