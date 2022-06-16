setwd("~/Desktop/Computer_Science/Master_Thesis/Kalle_MSc_Thesis")

rm(list=ls())

library(glue)
library(plyr)
library(pastecs)
library(ggplot2)
library(tidyverse)
library(gridExtra)
library(cowplot)
library(pracma)
library(hash)

# loads data from result files
load_data <- function() {
  times = read.table("alternatives/Simba_Energy/times.txt", header = TRUE, sep = ",", dec = ".", fill =TRUE)
  energy = read.table("alternatives/Simba_Energy/default_energy.txt", header = TRUE, sep = ",", dec = ".", fill =TRUE)
  accuracy = read.table("alternatives/Simba_Energy/accuracy.txt", header = TRUE, sep = ",", dec = ".", fill =TRUE)
  
  energy = energy[!is.na(energy$watt), ]
  times$start_time = as.POSIXlt(times$start_time,format="%d/%m/%Y %H:%M:%OS",tz=Sys.timezone())
  times$end_time = as.POSIXlt(times$end_time,format="%d/%m/%Y %H:%M:%OS",tz=Sys.timezone())
  energy$Datetime = as.POSIXlt(energy$Datetime,format="%d/%m/%Y %H:%M:%OS",tz=Sys.timezone())
  return(list(times=times, energy=energy, accuracy=accuracy))
}

# calculates the time an algorithm took
calculate_seconds <- function(method, times, approach1) {
  new_times = times[which(times$method == method & times$approach == approach1),]
  return(as.numeric(difftime(new_times$end_time, new_times$start_time,units="secs")))
}

average_watts <- function(new_energy) {
  milliseconds_times_list = as.numeric(as.POSIXct(new_energy$Datetime)) *1000
  return(trapz(milliseconds_times_list, new_energy$watt)/1000)
}

# calculates the amount of joules an algorithm consumed to produce a result
calculate_joules <- function(method, times, energy, approach1) {
  new_times = times[which(times$method == method & times$approach == approach1),]
  x = 5
  seconds = calculate_seconds(method, times, approach1)
  l = 1:nrow(new_times)
  for (i in 1:nrow(new_times)) {
    new_energy = energy[energy$Datetime >= new_times$start_time[i] & energy$Datetime <= new_times$end_time[i], ]
    power = average_watts(new_energy)
    # Some algorithms are so fast that the energy can't be measured as the sampling rate is around 0.2 seconds
    if (is.na(power) || power == 0) {
      power = average_power * seconds[i]
    }
    l[i] = as.numeric(power)
  }
  return(l)
}

addline_format <- function(x,...){
  gsub('\\s','\n',x)
}

all_data = load_data()
energy = all_data$energy
times = all_data$times
accuracy = all_data$accuracy

dict = hash()
# dict[["classification"]] = c(" bert", " forest", " LR", " multinomial", " sequential", " SVM")
dict[["classification_three"]] = c(" bert", " forest", " LR", " multinomial", " sequential", " SVM")
dict[["topic_modeling"]] = c(" BTM", " DMM", " GPUPDMM", " LDA", " LFDMM", " GPUDMM")
dict[["similarity"]] = c(" bert", " jaccard", " MPNet", " WMD", " thefuzz", " simba")
dict[["sentiment"]] = c(" flair", " sentistrength", " textblob", " RoBERTa", " VADER", " senti4SD")

df <- data.frame(method=character(),
                 joules=numeric(),
                 seconds=numeric(),
                 approach=character())

average_power = mean(energy$watt)

# creates a dataframe with: method, joules, seconds, and approach
for (approach1 in keys(dict)) {
  print(approach1)
  for (method in dict[[approach1]]) {
    joules = calculate_joules(method, times, energy, approach1)
    seconds = calculate_seconds(method, times, approach1)
    
    for (j in 1:length(joules)) {
      df[nrow(df) + 1, ] = c(method, joules[j], seconds[j], approach1)
    }
  }
}

# transforms joules and seconds to numeric values
df$joules <- as.numeric(df$joules)
df$seconds <- as.numeric(df$seconds)
accuracy$accuracy <- as.numeric(accuracy$accuracy)

df <- na.omit(df)

df$kj = df$joules/1000
# best to worst:
#1bc2e0 Light blue
#1b1ee0 Dark blue
#e0e01b Yellow
#e0871b Orange
#e0281b Red
#FFC0CB pink

# Performance
for (approach1 in keys(dict)) {
  print(approach1)
  for (method in dict[[approach1]]) {
    print(method)
    print(mean(accuracy[which(accuracy$approach==approach1 & accuracy$method==method), ]$accuracy))
    print(mean(accuracy[which(accuracy$approach==approach1 & accuracy$method==method), ]$precision))
    print(mean(accuracy[which(accuracy$approach==approach1 & accuracy$method==method), ]$recall))
    print(mean(accuracy[which(accuracy$approach==approach1 & accuracy$method==method), ]$F1))
    print(mean(accuracy[which(accuracy$approach==approach1 & accuracy$method==method), ]$MAE))
  }
}


# correct size: 12x13
p1 <- ggplot(df[df$approach=="classification_three", ], aes(x = method, y=kj, group=method, color=method)) + 
  geom_boxplot() + ggtitle("Classification") + ylab("Energy (kJ)") + xlab("Method") +
  scale_color_manual(labels = c(0.811, 0.628, 0.669, 0.524, 0.770, 0.747), values = c("#1bc2e0", "#1b1ee0", "#e0e01b", "#e0871b", "#e0281b", "#FFC0CB")) +
  theme_bw() +
  guides(color=guide_legend("F1 trinary"))
p1 = p1 + stat_summary(fun=mean, geom="point", shape=23, size=4) + theme(text = element_text(size = 17), legend.key.size = unit(0.9, 'cm')) +
  scale_y_continuous(limits = c(0, 6000)) + scale_x_discrete(labels=c(" bert" = "BERT", " forest" = "RF", " LR" = "LR", " multinomial" = "MNB", " sequential" = "SEQ", " SVM" = "SVM"))

p2 <- ggplot(df[df$approach=="topic_modeling", ], aes(x = method, y=kj, group=method, color=method)) + 
  geom_boxplot() + ggtitle("Topic Modeling") + ylab("Energy (kJ)") + xlab("Method") +
  scale_color_manual(labels = c("0.23", "0.10", "0.00", "0.07", "0.10", "0.30"), values = c("#1bc2e0", "#1b1ee0", "#e0e01b", "#e0871b", "#e0281b", "#FFC0CB")) +
  theme_bw() +
  guides(color=guide_legend("Accuracy"))
p2 = p2 + stat_summary(fun=mean, geom="point", shape=23, size=4) + theme(text = element_text(size = 17), legend.key.size = unit(0.9, 'cm')) +
  scale_y_continuous(limits = c(0, 550))

p3 <- ggplot(df[df$approach=="sentiment", ], aes(x = method, y=kj, group=method, color=method)) + 
  geom_boxplot() + ggtitle("Sentiment") + ylab("Energy (kJ)") + xlab("Method") +
  scale_color_manual(labels = c(0.487, 0.617, 0.626, 0.511, 0.503, 0.647), values = c("#1bc2e0", "#1b1ee0", "#e0e01b", "#e0871b", "#e0281b", "#FFC0CB")) +
  theme_bw() +
  guides(color=guide_legend("F1"))
p3 = p3 + stat_summary(fun=mean, geom="point", shape=23, size=4) + theme(text = element_text(size = 17), legend.key.size = unit(0.9, 'cm')) +
  scale_y_continuous(limits = c(0, 850)) + scale_x_discrete(labels=c(" flair" = "Flair", " RoBERTa" = "RoBERTa", " senti4SD" = "S4SD", " sentistrength" = "SS", " textblob" = "TB", " VADER" = "VADER"))

p4 <- ggplot(df[df$approach=="similarity", ], aes(x = method, y=kj, group=method, color=method)) + 
  geom_boxplot() + ggtitle("Similarity") + ylab("Energy (kJ)") + xlab("Method") +
  scale_color_manual(labels = c(0.609, "0.720", 0.791, "0.770", 0.774, 0.661), values = c("#1bc2e0", "#1b1ee0", "#e0e01b", "#e0871b", "#e0281b", "#FFC0CB")) +
  theme_bw() +
  guides(color=guide_legend("F1"))
p4 = p4 + stat_summary(fun=mean, geom="point", shape=23, size=4) + theme(text = element_text(size = 17), legend.key.size = unit(0.9, 'cm')) +
  scale_y_continuous(limits = c(0, 9500)) + scale_x_discrete(labels=c(" bert" = "BERT", " jaccard" = "Jaccard", " MPNet" = "MPNet", " simba" = "SIMBA", " thefuzz" = "TF", " WMD" = "WMD"))

grid.arrange(p1, p2, p3, p4, ncol=1)

# Descriptive statistics
options(digits=9)
by(df[df$approach=="classification_three", ]$kj, df[df$approach=="classification_three", ]$method, summary)
by(df[df$approach=="topic_modeling", ]$kj, df[df$approach=="topic_modeling", ]$method, summary)
by(df[df$approach=="sentiment", ]$kj, df[df$approach=="sentiment", ]$method, summary)
by(df[df$approach=="similarity", ]$kj, df[df$approach=="similarity", ]$method, summary)

for (approach1 in keys(dict)) {
  print(approach1)
  for (method in dict[[approach1]]) {
    print(method)
    print(sd(df[which(df$method == method & df$approach == approach1),]$kj))
  }
}

first_column <- c("value_1", "value_2", "value_1", "value_2", "value_1", "value_2", "value_1", "value_2", "value_3", "value_3", "value_3", "value_3", "value_1", "value_2", "value_3")
second_column <- c(2, 5, 3, 8, 1, 7, 3, 9, 15, 17, 14, 15, 15, 3, 2)
third_column <- 2 * second_column

joule_classification = df[which(df$approach== "classification_three"), ]
joule_classification = joule_classification[order(joule_classification$method),]$joules
accuracy_classification = accuracy[which(accuracy$approach== "classification_three"), ]
accuracy_classification = accuracy_classification[order(accuracy_classification$method), ]
cor.test(joule_classification, accuracy_classification$precision, method="spearman")
cor.test(joule_classification, accuracy_classification$recall, method="spearman")
cor.test(joule_classification, accuracy_classification$F1, method="spearman")
cor.test(joule_classification, accuracy_classification$accuracy, method="spearman")

joule_topic = df[which(df$approach== "topic_modeling"), ]
joule_topic = joule_topic[order(joule_topic$method),]$joules
accuracy_topic = accuracy[which(accuracy$approach== "topic_modeling"), ]
accuracy_topic = accuracy_topic[order(accuracy_topic$method), ]
cor.test(joule_topic, accuracy_topic$accuracy, method="spearman")

joule_sentiment = df[which(df$approach== "sentiment"), ]
joule_sentiment = joule_sentiment[order(joule_sentiment$method),]$joules
accuracy_sentiment = accuracy[which(accuracy$approach== "sentiment"), ]
accuracy_sentiment = accuracy_sentiment[order(accuracy_sentiment$method), ]
cor.test(joule_sentiment, accuracy_sentiment$precision, method="spearman")
cor.test(joule_sentiment, accuracy_sentiment$recall, method="spearman")
cor.test(joule_sentiment, accuracy_sentiment$F1, method="spearman")
cor.test(joule_sentiment, accuracy_sentiment$accuracy, method="spearman")
cor.test(joule_sentiment, accuracy_sentiment$MAE, method="spearman")

joule_similarity = df[which(df$approach== "similarity"), ]
joule_similarity = joule_similarity[order(joule_similarity$method),]$joules
accuracy_similarity = accuracy[which(accuracy$approach== "similarity"), ]
accuracy_similarity = accuracy_similarity[order(accuracy_similarity$method), ]
cor.test(joule_similarity, accuracy_similarity$precision, method="spearman")
cor.test(joule_similarity, accuracy_similarity$recall, method="spearman")
cor.test(joule_similarity, accuracy_similarity$F1, method="spearman")
cor.test(joule_similarity, accuracy_similarity$accuracy, method="spearman")
cor.test(joule_similarity, accuracy_similarity$MAE, method="spearman")

joule_all = df[order(df$method),]$joules
accuracy_all = accuracy[order(accuracy$method), ]
cor.test(joule_all, accuracy$precision, method="spearman")
cor.test(joule_all, accuracy$recall, method="spearman")
cor.test(joule_all, accuracy$F1, method="spearman")
cor.test(joule_all, accuracy$accuracy, method="spearman")

kruskal.test(df[which(df$approach == "classification_three"),]$kj ~ df[which(df$approach == "classification_three"),]$method)
kruskal.test(df[which(df$approach == "topic_modeling"),]$kj ~ df[which(df$approach == "topic_modeling"),]$method)
kruskal.test(df[which(df$approach == "sentiment"),]$kj ~ df[which(df$approach == "sentiment"),]$method)
kruskal.test(df[which(df$approach == "similarity"),]$kj ~ df[which(df$approach == "similarity"),]$method)

kruskal.test(accuracy[which(accuracy$approach == "classification_three"),]$precision ~ accuracy[which(accuracy$approach == "classification_three"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "topic_modeling"),]$precision ~ accuracy[which(accuracy$approach == "topic_modeling"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "sentiment"),]$precision ~ accuracy[which(accuracy$approach == "sentiment"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "similarity"),]$precision ~ accuracy[which(accuracy$approach == "similarity"),]$method)

kruskal.test(accuracy[which(accuracy$approach == "classification_three"),]$recall ~ accuracy[which(accuracy$approach == "classification_three"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "topic_modeling"),]$recall ~ accuracy[which(accuracy$approach == "topic_modeling"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "sentiment"),]$recall ~ accuracy[which(accuracy$approach == "sentiment"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "similarity"),]$recall ~ accuracy[which(accuracy$approach == "similarity"),]$method)

kruskal.test(accuracy[which(accuracy$approach == "classification_three"),]$F1 ~ accuracy[which(accuracy$approach == "classification_three"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "topic_modeling"),]$F1 ~ accuracy[which(accuracy$approach == "topic_modeling"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "sentiment"),]$F1 ~ accuracy[which(accuracy$approach == "sentiment"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "similarity"),]$F1 ~ accuracy[which(accuracy$approach == "similarity"),]$method)

kruskal.test(accuracy[which(accuracy$approach == "classification_three"),]$accuracy ~ accuracy[which(accuracy$approach == "classification_three"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "topic_modeling"),]$accuracy ~ accuracy[which(accuracy$approach == "topic_modeling"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "sentiment"),]$accuracy ~ accuracy[which(accuracy$approach == "sentiment"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "similarity"),]$accuracy ~ accuracy[which(accuracy$approach == "similarity"),]$method)

kruskal.test(accuracy[which(accuracy$approach == "sentiment"),]$MAE ~ accuracy[which(accuracy$approach == "sentiment"),]$method)
kruskal.test(accuracy[which(accuracy$approach == "similarity"),]$MAE ~ accuracy[which(accuracy$approach == "similarity"),]$method)

pairwise.wilcox.test(second_column, first_column, p.adjust.method = "BH")

for (method in dict[["classification_three"]]) {
  print(method)
  print(wilcox.test(df[which(df$approach == "classification_three" & df$method == " multinomial"),]$kj, df[which(df$approach == "classification_three" & df$method == method),]$kj, paired=FALSE))
}

for (method in dict[["topic_modeling"]]) {
  print(method)
  print(wilcox.test(df[which(df$approach == "topic_modeling" & df$method == " LDA"),]$kj, df[which(df$approach == "topic_modeling" & df$method == method),]$kj, paired=FALSE))
}

for (method in dict[["sentiment"]]) {
  print(method)
  print(wilcox.test(df[which(df$approach == "sentiment" & df$method == " VADER"),]$kj, df[which(df$approach == "sentiment" & df$method == method),]$kj, paired=FALSE))
}

for (method in dict[["similarity"]]) {
  print(method)
  print(wilcox.test(df[which(df$approach == "similarity" & df$method == " jaccard"),]$kj, df[which(df$approach == "similarity" & df$method == method),]$kj, paired=FALSE))
}
