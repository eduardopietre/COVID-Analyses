library(ggplot2)
library(gridExtra)

source("utils.R")


df <- GetCovidTimeSeriesCountry("Brazil", "13-02-21", cumulative=FALSE)
df$Day <- weekdays(df$Date)

# Reorder weekdays.
df$Day <- factor(df$Day, levels=c(
    "segunda-feira", "terça-feira", "quarta-feira",
    "quinta-feira", "sexta-feira", "sábado", "domingo"
))


plot_cases <- ggplot(df, aes(x=Cases, y=Day, fill=Day)) + 
    stat_boxplot(geom="errorbar", width=0.3, lwd=1.2) +
    geom_boxplot(lwd=1.2) +
    coord_flip() +
    theme(legend.position="none") +
    ylab("Weekday") +
    ggtitle("Boxplot of Cases by Weekday")

plot_deaths <- ggplot(df, aes(x=Deaths, y=Day, fill=Day)) + 
    stat_boxplot(geom="errorbar", width=0.3, lwd=1.2) +
    geom_boxplot(lwd=1.2) +
    coord_flip() +
    theme(legend.position="none") +
    ylab("Weekday") +
    ggtitle("Boxplot of Deaths by Weekday")

g <- arrangeGrob(plot_cases, plot_deaths, nrow=2)
ggsave(file="images/DayOfTheWeekBoxplot.png", g, height=8, width=8, dpi=400)
