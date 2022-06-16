import os
from datetime import datetime
import sys
filename = "times.txt"

if not os.path.exists(filename):
	file = open(filename, 'w')
	file.write("approach, method, start_time, end_time\n")
else:
	file = open(filename,"a")

# datetime object containing current date and time
start = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
for i in range(6):
	os.system("java -classpath /Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/charsets.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/ext/cldrdata.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/ext/dnsns.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/ext/jaccess.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/ext/jfxrt.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/ext/localedata.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/ext/nashorn.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/ext/sunec.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/ext/zipfs.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/jce.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/jfr.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/jfxswt.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/jsse.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/management-agent.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/resources.jar:/Users/kallejanssen/Library/Java/JavaVirtualMachines/corretto-1.8.0_332/Contents/Home/jre/lib/rt.jar:/Users/kallejanssen/Desktop/Kalle_MSc_Thesis/topic_modeling/TopicModel4J-master/target/classes:/Users/kallejanssen/.m2/repository/edu/stanford/nlp/stanford-corenlp/3.6.0/stanford-corenlp-3.6.0.jar:/Users/kallejanssen/.m2/repository/com/io7m/xom/xom/1.2.10/xom-1.2.10.jar:/Users/kallejanssen/.m2/repository/xml-apis/xml-apis/1.3.03/xml-apis-1.3.03.jar:/Users/kallejanssen/.m2/repository/xerces/xercesImpl/2.8.0/xercesImpl-2.8.0.jar:/Users/kallejanssen/.m2/repository/xalan/xalan/2.7.0/xalan-2.7.0.jar:/Users/kallejanssen/.m2/repository/joda-time/joda-time/2.9/joda-time-2.9.jar:/Users/kallejanssen/.m2/repository/de/jollyday/jollyday/0.4.7/jollyday-0.4.7.jar:/Users/kallejanssen/.m2/repository/javax/xml/bind/jaxb-api/2.2.7/jaxb-api-2.2.7.jar:/Users/kallejanssen/.m2/repository/com/googlecode/efficient-java-matrix-library/ejml/0.23/ejml-0.23.jar:/Users/kallejanssen/.m2/repository/javax/json/javax.json-api/1.0/javax.json-api-1.0.jar:/Users/kallejanssen/.m2/repository/org/slf4j/slf4j-api/1.7.12/slf4j-api-1.7.12.jar:/Users/kallejanssen/.m2/repository/edu/stanford/nlp/stanford-corenlp/3.6.0/stanford-corenlp-3.6.0-models.jar:/Users/kallejanssen/.m2/repository/org/apache/commons/commons-math3/3.6/commons-math3-3.6.jar com.topic.model.BTM")

end = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
file.write("topic_modeling, BTM, " + start[:-3] + ", " + end[:-3] + "\n")
file.close()
