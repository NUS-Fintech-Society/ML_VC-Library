library(arules)
library(magrittr)
library(dplyr)
library(lubridate)
library(readr)
library(reshape2)
library(tidyr)
library(arulesViz)

library(zoo)
library(stringr)
library(ggplot2)

raw.data <- read_csv('/Users/kexin/Downloads/archive/crunchbase-investments.csv')

tidy.data <- raw.data

#standardizing round codes
tidy.data$funding_round_type[tidy.data$funding_round_type %in% c('series-a')] <- 'A'
tidy.data$funding_round_type[tidy.data$funding_round_type %in% c('series-b')] <- 'B'
tidy.data$funding_round_type[tidy.data$funding_round_type %in% c('series-c')] <- 'C'
tidy.data$funding_round_type[tidy.data$funding_round_type %in% c('series-d')] <- 'D'
tidy.data$funding_round_type[tidy.data$funding_round_type %in% c('series-e')] <- 'E'
tidy.data$funding_round_type[tidy.data$funding_round_type %in% c('series-f')] <- 'F'
tidy.data$funding_round_type[tidy.data$funding_round_type %in% c('series-g')] <- 'G'
tidy.data$funding_round_type[tidy.data$funding_round_type %in% c('series-h')] <- 'H'

#correcting company name
tidy.data$company_name <- as.character(tidy.data$company_name)
tidy.data$company_name[tidy.data$company_name %in% c('#NAME?')] = 'PlusN'
tidy.data$company_name <- as.factor(tidy.data$company_name)

#making undisclosed round type as NA
tidy.data$funding_round_type[tidy.data$funding_round_type == 'undisclosed'] <- NA

#creating variable of coinvestors
aux <- tidy.data %>%
  count(investor_permalink)
tidy.data %<>% 
  left_join(aux, by = 'investor_permalink')
names(tidy.data)[ncol(tidy.data)] <- 'number_coinvestors'
tidy.data %<>%
  mutate(class_coinvestors = ifelse(number_coinvestors == 1, 'Lone Investor',
                                    ifelse(number_coinvestors <= 4, 'Few Co-investors',
                                           ifelse(number_coinvestors <= 10, 'Intermediary Co-investors', 'Large Co-investors'))))
rm(aux, raw.data)


#Preparing data
inv <- tidy.data %>%
  filter(!is.na(investor_name), !is.na(company_category_code), !is.na(company_name), !is.na(funding_round_type), !is.na(investor_country_code), !is.na(class_coinvestors), !is.na(company_country_code),  funding_round_type %in% c('venture'))
inv <- inv[,c("investor_name", "class_coinvestors", "company_category_code", "funding_round_type")]

#select investors with above 15 investments
top.inv <- inv %>%
  group_by(investor_name) %>%
  count(investor_name, class_coinvestors, funding_round_type, company_category_code) %>%
  ungroup %>%
  group_by(investor_name) %>%
  summarise(frequency = sum(n)) %>%
  filter(frequency >= 15) %>%
  ungroup

inv %<>%
  filter(investor_name %in% top.inv$investor_name) %>%
  mutate(id = row_number())

#Create matrix of transactions
inv.mat <- acast(inv, id~company_category_code, idfill=0, fun.aggregate = mean)
#inv.mat <- cbind(inv.mat, acast(inv, id~crossBorders, fill=0, fun.aggregate = length)) #cast(top.inv, investor_name~company_market)     #transforming into a matrix of investor x amount invested in each mkt
inv.mat <- cbind(inv.mat, acast(inv, id~class_coinvestors, fill=0, fun.aggregate = length)) #cast(top.inv, investor_name~company_market)     #transforming into a matrix of investor x amount invested in each mkt
inv.mat <- cbind(inv.mat, acast(inv, id~funding_round_type, fill=0, fun.aggregate = mean)) #cast(top.inv, investor_name~company_market)     #transforming into a matrix of investor x amount invested in each mkt

#inv.mat <- matrix(c(1, NaN, 2, NaN), ncol=2, nrow=2)
inv.mat[is.nan(inv.mat)] <- 0

transactions <-  as(as.matrix(inv.mat), "transactions")
rm(inv.mat)

#Plot most frequent items
itemFrequencyPlot(transactions,topN=30,type="relative")

#Run apriori
rules <- apriori(transactions, parameter = list(supp = 0.001, conf = 0.01, minlen=2, maxlen = 5))
subrules <- rules[!is.redundant(rules, measure = 'improvement')] 

#Format rules output, removing {} and joining LHS and RHS in one string
rules.df <- DATAFRAME(subrules)
rules.df[1:2] <- lapply(rules.df[1:2], as.character)
rules.df[1:2] <- apply(rules.df[1:2], 2, function(y) (gsub("\\{", "", y)))
rules.df[1:2] <- apply(rules.df[1:2], 2, function(y) (gsub("\\}", "", y)))
rules.df$aux <- paste(rules.df$LHS, rules.df$RHS, sep = '')

#Make sure we are not pasting duplicates
comb = vector()
for (i in 1:nrow(rules.df)) {
  if (paste(rules.df$RHS[i], rules.df$LHS[i], sep = '') %in% comb) {
    next
  } else comb[length(comb)+1] = paste(rules.df$LHS[i], rules.df$RHS[i], sep = '')
}

rules.df %<>% filter(aux %in% comb)
rm(i, comb)
rules.df <- rules.df[-ncol(rules.df)]

#Vector with rules. Necessary to test what if investment followed all the rule features
rules.vec <- str_split(paste(rules.df$LHS,rules.df$RHS,sep =','), ',')

#Rules validation
#retrieve number of investments per category
inv <- tidy.data %>%
  filter(!is.na(investor_name), !is.na(funding_round_type), !is.na(investor_country_code), !is.na(class_coinvestors), !is.na(company_country_code), funded_year >= 2008, funding_round_type %in% c('venture'))
inv <- inv[,c("investor_name", "funded_year", "company_category_code", "class_coinvestors", "funding_round_type")]

#select investors with above 15 investments
top.inv <- inv %>%
  group_by(investor_name) %>%
  summarise(frequency = sum(n())) %>%
  filter(frequency >= 15) %>%
  ungroup

inv %<>%
  filter(investor_name %in% top.inv$investor_name) 

rm(top.inv)

#Create vector of investment features
invest.vec <- str_split(paste(inv$company_category_code, inv$class_coinvestors, inv$funding_round_type,sep =','), ',')

#Check if rule was fully used in each investment.
for(r in 1:length(rules.vec)) {
  aux = vector()
  for (i in 1:nrow(inv)) {
    aux[i] <- ifelse(sum(rules.vec[[r]] %in% invest.vec[[i]]) == length(rules.vec[[r]]), 1, 0)
  }
  print(paste('r:',r))
  inv[[paste('R',r)]] <- aux
}

#Create df with average rule usage per investor
inv.melt <- inv[c(1, 6:ncol(inv))]
inv.count <- inv %>%
  count(investor_name)
inv.melt %<>%
  melt(id = c("investor_name")) %>%
  filter(value > 0) %>%
  left_join(inv.count, by = c('investor_name' = 'investor_name')) %>%
  group_by(investor_name, variable) %>%
  mutate(perc = sum(value)/n) %>%
  group_by(investor_name, variable, perc) %>%
  summarise %>%
  ungroup

#Bubble visualization of rule usage
inv.melt %>%
  filter(perc > .20) %>%
  ggplot(aes(investor_name, variable))+
  geom_jitter(aes(size = perc, alpha = perc), colour = 'blue')+
  theme(
    axis.text.x = element_blank(),
    axis.text.y = element_blank(),
    axis.ticks = element_blank(),
    panel.border = element_rect(colour = 'black', fill = NA))+
  labs(size = 'Size: % of Investments\nthat follow rule', alpha = 'Size: % of Investments\nthat follow rule')+
  xlab('VC Company')+
  ylab('Rule')
# ggtitle('Rule usage by Investor')


#Clustering
#generate matrix
rules.mat <- inv.melt %>%
  acast(investor_name~variable, fill = 0, fun.aggregate = sum)

# PCA
pc.a.props = prcomp(rules.mat)

#293 components express 99% of the variability
cumsum(pc.a.props$sdev^2)/sum(pc.a.props$sdev^2)
x <- data.frame(var = cumsum(pc.a.props$sdev^2)/sum(pc.a.props$sdev^2))
x %<>% mutate(ncomp = row_number())

x %>%
  ggplot(aes(ncomp, var))+
  geom_line()+
  theme_bw()+
  xlab('Number of Components')+
  ylab('Cumulative Percentage of \nVariation Explained (PVE)')


#Gower Clustering
library(analogue)
gower_dist <- as.dist(distance(pc.a.props$x[,1:49], method = "alt.gower"))
fit <- hclust(d = gower_dist, method = "ward.D2")
plot(fit, labels = FALSE, xlab = NA, main = NA)

#Select 3 clusters
groups = cutree(fit, k = 3)

#Take mean and std dev of rules across clusters
ar = aggregate(rules.mat,list(groups),mean)
ar.sd = aggregate(rules.mat,list(groups),sd)

#Select top clusters for all rules
top.rules <- ar %>%
  melt(id = "Group.1") %>%
  group_by(variable) %>%
  arrange(desc(value)) %>%
  mutate(ranking = row_number()) %>%
  ungroup %>%
  filter(ranking == 1)

#Include df column with what the rule code means
for (i in 1:nrow(top.rules)) {
  top.rules$rule[i] <- paste(rules.vec[[as.numeric(gsub('R ','',top.rules$variable[i]))]], collapse = ", ")
}

#Top rules per cluster
graph <- top.rules %>% 
  group_by(Group.1) %>%
  top_n(20, wt = value) %>%
  slice(1:20) %>%
  ungroup() %>%
  arrange(Group.1, value) %>%
  mutate(order = row_number())
graph %>%
  ggplot(aes(order, value*100, fill = factor(Group.1)))+
  geom_bar(stat='identity', show.legend = FALSE)+
  scale_x_continuous(
    breaks = graph$order,
    labels = graph$rule,
    expand = c(0,0)
  )+
  coord_flip()+
  facet_wrap(~Group.1, scales = 'free_y', ncol = 1)+
  ylab('Average Percentage (%) of Investments \naccording to rule')+
  xlab('Association Rule')+
  theme_bw()

#Number of rules per cluster
top.rules %>%
  count(Group.1) %>%
  ungroup %>%
  ggplot(aes(Group.1, n))+
  geom_bar(stat = 'identity')+
  theme_bw()+
  xlab('Cluster')+
  ylab('Number of Predominant Rules')

#plot number of rules used vs number of investments per company
inv.count <- inv %>%
  count(investor_name)
inv.count <- inv.melt %>%
  count(investor_name) %>%
  left_join(inv.count, by = c('investor_name' = 'investor_name')) %>%
  left_join(data.frame(investor_name = names(groups), Cluster = groups), by = c('investor_name' = 'investor_name')) %>%
  left_join(data.frame(investor_name = fit$labels, ord = fit$order), by = c('investor_name' = 'investor_name'))

inv.count %>%
  ggplot(aes(n.x, n.y))+
  geom_point(aes(colour = factor(Cluster), shape = factor(Cluster)),alpha = 0.7)+
  geom_smooth(se = F)+
  theme_bw()+
  ylab('Number of Investments')+
  xlab('Number of Rules')+
  # ggtitle('Number of Investments per Investor vs. Number of Rules used per Investor')+
  labs(colour = 'Cluster', shape = 'Cluster')

