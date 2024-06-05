#load data

library(cluster)
library(dendextend)
library(ggplot2)
library(DataEditR)

csvs=list.files(path="F:\\drone_footage", pattern="drone.csv", recursive = TRUE, full.names = TRUE)
happy="N"

  
for(csv in csvs){
  while(happy == "N"){
data=read.csv(csv)
total_birds=rowSums(data[,5:7])
simplified_names=as.numeric(gsub(".*?([0-9]+).*", "\\1", data$label))
print(ggplot(data = data, aes(y=longitude, x=latitude, color=as.factor(total_birds)))+geom_point()+
  geom_text(aes(label=ifelse(total_birds >0, label, "")), col="black")+
    ggtitle(unique(data$date))+
    theme(legend.position = "none"))
happy=readline("happy Y/N? ")
}
happy="N"}


ggplot(data = data, aes(x=longitude, y=latitude, color=as.factor(Males)))+geom_point()+
  geom_text(aes(label=ifelse(total_birds >0, label, "")), col="black")





# filter and keep only data with observations 
distance=dist(data[,3:4],method = "euclidean" )
hc=hclust(distance)
clusters=cutree(hc, h=)
plot(hc)
rect.hclust(hc, h = 2, border = 2:4) 
data$cluster=clusters
