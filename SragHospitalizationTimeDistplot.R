library(ggplot2)

# "data/SRAG 2020_cleaned.csv" must exist for this script to work.
# Check "SragCleanData.py" for more information.

srag_data = read.csv2("data/SRAG 2020_cleaned.csv")

srag_data$DT_INTERNA = as.Date(srag_data$DT_INTERNA, format="%d/%m/%Y")
srag_data$DT_EVOLUCA = as.Date(srag_data$DT_EVOLUCA, format="%d/%m/%Y")
srag_data$HOSP_TIME = srag_data$DT_EVOLUCA - srag_data$DT_INTERNA
class(srag_data$HOSP_TIME) = "difftime"
attr(srag_data$HOSP_TIME, "units") = "days"

srag_data$EVOLUCAO = factor(
    srag_data$EVOLUCAO,
    levels = c(1, 2),
    labels = c("Cure", "Death")
)

data = na.omit(srag_data, cols="HOSP_TIME")

g <- ggplot(data, aes(x = HOSP_TIME)) +
    geom_density(aes(color = EVOLUCAO, fill = EVOLUCAO), alpha=0.5) +
    scale_color_manual("Evolution", values = c("#00cc00", "#B20000")) +
    scale_fill_manual("Evolution", values = c("#00cc00", "#B20000")) +
    theme(legend.position = c(0.85, 0.85)) + 
    xlim(0, 60) +
    ylim(0.0, 0.1) +
    labs(x="Duration (days)", y="Density") +
    ggtitle("SRAG 2020 Hospitalization Duration Density Plot by Evolution")

ggsave(file="images/SragHospitalizationTimeDistplot.png", g, height=6, width=6, dpi=400)
