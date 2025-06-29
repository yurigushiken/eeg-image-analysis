library(dplyr)
library(ggplot2)
library(tidyr)

participant_list <- c("2","3","4","5","8","9","10","11","12","13","14","15","17","21","22","23","25","26","27","28","29","31","32","33")

for (n in 1:length(participant_list)){
  
setwd("/Users/liyuexin/Desktop/Numbers_EEG/Data")
  
trials <- read.csv("HAPPE_Usable_Trials.csv")

current_part <- paste("Subject",participant_list[n],sep="")
current_trials <- trials[which(trials[1]==current_part),]
trial_nums <- current_trials["Kept_Segs_Indxs"][1,1]
new_trials <- as.integer(strsplit(trial_nums,", ")[[1]])

setwd(paste("/Users/liyuexin/Desktop/Numbers_EEG/Data/",current_part,sep=""))

behavioral_data <- read.csv(paste("Subject",participant_list[n],"Behavioral.csv",sep=""))
behavioral_data <- filter(behavioral_data,`Procedure.Block.` != "Practiceproc")
for (i in 1:300){
  if (i <= 60){
    next}
  else if (i <= 120) {
    behavioral_data[i,"Trial"] <- behavioral_data[i,"Trial"] + 60}
  else if (i <= 180) {
    behavioral_data[i,"Trial"] <- behavioral_data[i,"Trial"] + 120}
  else if (i <= 240) {
    behavioral_data[i,"Trial"] <- behavioral_data[i,"Trial"] + 180}
  else if (i <= 300) {
    behavioral_data[i,"Trial"] <- behavioral_data[i,"Trial"] + 240}}
behavioral_data <- filter(behavioral_data,Trial %in% new_trials)

eeg_data <- read.csv(paste("Subject",participant_list[n],".csv",sep=""))

trial_total <- length(eeg_data[,1]) / 175
trial_new <- c(1:trial_total)

behavioral_complete <- cbind(behavioral_data,New.Trials = trial_new)
#behavioral_complete <- behavioral_complete %>%
#  filter(Target.RT == 0 | Target2.RT == 0 | Target3.RT == 0 | Target5.RT == 0 | Target7.RT == 0 | Target9.RT == 0)
behavioral_complete <- behavioral_complete %>%
  filter(Target.ACC == 1 | Target2.ACC == 1 | Target3.ACC == 1 | Target5.ACC == 1 | Target7.ACC == 1 | Target9.ACC == 1) 
         
#condition_list <- c("11","22","33","44","55","66")
condition_list <- c("21","31","32","41","42","43","52","53","54","63","64","65",
                    "12","13","14","23","24","25","34","35","36","45","46","56")

trial_number_condition <- data.frame()
for (j in 1:length(condition_list)){
  behavioral_new <- filter(behavioral_complete,CellNumber == condition_list[j])
  trial_list <- behavioral_new[,"New.Trials"]
  eeg_new <- data.frame()
  
  if (length(trial_list) > 0 ) {
  for (k in 1:length(trial_list)){
    val2 <- 175*trial_list[k]
    val1 <- val2 - 174
    new_data <- eeg_data[c(val1:val2),-c(1)]
    
    if (k <= 1){
      eeg_new <- new_data
      print(eeg_new[1,1])}
    else if (k > 1){
      eeg_current <- eeg_new + new_data
      eeg_new <- eeg_current
      print(eeg_new[1,1])}}
  eeg_new <- eeg_new / length(trial_list)
  eeg_new <- cbind(Time = eeg_data[c(1:175),1],eeg_new)
  write.csv(eeg_new,file = paste("sub", participant_list[n], "_", condition_list[j],".csv",sep="")) }
  
  new_row <- data.frame(Condition = condition_list[j],Number.of.Trials = length(trial_list))
  trial_number_condition <- rbind(trial_number_condition,new_row)
  print(j)}

write.csv(trial_number_condition,file = "Number of Trials per Condition.csv")}
