
setwd("C:/Users/Wes/Documents/GitHub/NHLStats")



year = 2015
filename = paste0("team_game_season_", year, "_", year+1, ".csv")

### Read the raw season data
dat = read.csv(filename, fileEncoding="UTF-8-BOM")

dat = dat[order(dat$Game), ]

### Get team legend
# team_legend maps team names to their 3-letter tags
team_legend = read.csv("team_legend.csv", fileEncoding="UTF-8-BOM", header = F)

rownames(team_legend) = team_legend$V1
team_legend = team_legend[2]



### Fix up data so that there is only Time, Home team, Away team and result
# Rename home teams with their 3-letter tag
dat$Home = team_legend[dat$Team, ]
# Keep only Time, Home, Away and Result columns
dat = dat[c("Home", "Opp.Team", "W")]
dat$Time = 1:nrow(dat)
colnames(dat) = c("Home", "Away", "Result", "Time")
# Reorder columns
dat = dat[c(4, 1, 2, 3)]

dat$Home = as.character(dat$Home)
dat$Away = as.character(dat$Away)


### Try rating systems
library(PlayerRatings)
test = glicko(dat, history=T)

test2 = test$history[,,1]
test2 = data.frame(t(test2))


plot(test2$ARI, type="l", ylim=c(1700, 2800))

for(i in 1:30) {
  lines(test2[names(test2)[i]], col="gray")
}
lines(test2$ANA)