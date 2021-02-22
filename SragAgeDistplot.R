library(dplyr)
library(ggplot2)

# "data/SRAG 2020_cleaned.csv" must exist for this script to work.
# Check "SragCleanData.py" for more information.

srag_data = read.csv2("data/SRAG 2020_cleaned.csv")

srag_data$EVOLUCAO = factor(
    srag_data$EVOLUCAO,
    levels = c(1, 2),
    labels = c("Cure", "Death")
)

g <- ggplot(srag_data, aes(x = NU_IDADE_N)) +
    geom_density(aes(color = EVOLUCAO, fill = EVOLUCAO), alpha=0.6) +
    scale_color_manual("Evolution", values = c("#00cc00", "#B20000")) +
    scale_fill_manual("Evolution", values = c("#00cc00", "#B20000")) +
    theme(legend.position = c(0.15, 0.85)) + 
    labs(x="Age", y="Density") +
    xlim(0, 105) +
    ylim(0, 0.03) +
    ggtitle("SRAG 2020 Age Density Plot by Evolution")

ggsave(file="images/SragAgeHistogram.png", g, height=6, width=6, dpi=400)
