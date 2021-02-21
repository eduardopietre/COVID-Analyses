library(dplyr)
library(ggplot2)
library(gridExtra)

source("utils.R")

# mortes = deaths
# casos = cases
# novas = new
# meses = months
# mes_ano = month_and_year
# data = date in format %Y-%m-%d

CustomBarPlot <- function(summ_data, x_col, y_col, title, y_label, color_low, color_high) {
    plot <- ggplot(summ_data, aes(x=.data[[x_col]], y=.data[[y_col]], fill=.data[[y_col]])) +
        geom_bar(stat = "identity") +
        geom_text(aes(label=.data[[y_col]]), position=position_dodge(width=0.9), vjust=-0.25) +
        scale_fill_gradient(low=color_low, high=color_high) +
        theme(legend.position="none") +
        ggtitle(title) +
        xlab("Meses") +
        ylab(y_label)

    return(plot)
}

# Load dataset using 'coronabr', see 'utils.R'.
ministry_dataset <- WrapperGetCoronaBrMinSaude()

city_name = "Petrópolis"  # City name to filter by.

frame <- subset(ministry_dataset, municipio == city_name)
frame <- subset(frame, select=c("municipio", "data", "casosNovos", "obitosNovos"))
frame$data <- as.Date(frame$data, format = "%Y-%m-%d")
frame$mes_ano = format(frame$data, "%B\n%Y")

group = group_by(frame, mes_ano)
summ = summarise(
    group,
    casosNovos = sum(casosNovos),
    obitosNovos = sum(obitosNovos),
)

# Reorder months.
summ$mes_ano = factor(summ$mes_ano, levels=c(
    "março\n2020",
    "abril\n2020",
    "maio\n2020",
    "junho\n2020",
    "julho\n2020",
    "agosto\n2020",
    "setembro\n2020",
    "outubro\n2020",
    "novembro\n2020",
    "dezembro\n2020",
    "janeiro\n2021",
    "fevereiro\n2021"
))

plot_cases <- CustomBarPlot(
    summ, "mes_ano", "casosNovos",
    paste("Novos casos de COVID-19 por mês em", city_name, "-", Sys.Date()),
    "Novos Casos", "grey", "black"
)

plot_deaths <- CustomBarPlot(
    summ, "mes_ano", "obitosNovos",
    paste("Novas mortes por COVID-19 por mês em", city_name, "-", Sys.Date()),
    "Novas Mortes", "yellow", "red"
)

g <- arrangeGrob(plot_cases, plot_deaths, nrow=2)
ggsave(file="images/CompareMonthsBarplot.png", g, height=8, width=8, dpi=400)
