library(coronabr)


# Do not change 'file_name' or 'file_extension' without knowing what you are doing.
WrapperGetCoronaBrMinSaude <- function(dir="coronabr_data", file_name="minsaude_", file_extension=".csv", reuse_cache=TRUE) {
    today_date = Sys.Date()
    file_path <- paste0(dir, "/", file_name, today_date, file_extension)
    
    if (file.exists(file_path) & reuse_cache) {
        # Read from existent data.
        return(read.csv(file_path))
    } else {
        # Clean folder to prevent errors.
        file.remove(list.files(dir, include.dirs=FALSE, full.names=TRUE))
        # Download data.
        return(get_corona_minsaude(dir=dir))
    }
    
}


GetCovidTimeSeriesCountry <- function(country, date_str, dir="data", cumulative=TRUE) {
    confirmed = read.csv(paste0(dir, "/time_series_covid19_confirmed_global ", date_str, ".csv"))
    death = read.csv(paste0(dir, "/time_series_covid19_deaths_global ", date_str, ".csv"))
    
    # Filter by country
    country_confirmed = data.frame(t(confirmed[confirmed$Country.Region == country,]))
    country_death = data.frame(t(death[death$Country.Region == country,]))
    
    # dates are now rownames, assign to a column.
    country_confirmed$Date = rownames(country_confirmed)
    country_death$Date = rownames(country_death)
    
    # Reasign rows numbers.
    rownames(country_confirmed) <- NULL
    rownames(country_death) <- NULL
    
    # Drop the first four rows, metadata.
    country_confirmed <- country_confirmed[-c(1,2,3,4),]
    country_death <- country_death[-c(1,2,3,4),]
    
    # Change colnames.
    colnames(country_confirmed)[1] <- "Cases"
    colnames(country_death)[1] <- "Deaths"
    
    # Combine by date and convert date to a date object.
    country_df <- merge(country_confirmed, country_death, by="Date")
    country_df$Date <- as.Date(country_df$Date, format="X%m.%d.%y")
    
    # Order by date, reset index.
    country_df <- country_df[order(country_df$Date),]
    rownames(country_df) <- NULL
    
    # Convert to numbers.
    country_df$Cases <- as.numeric(country_df$Cases)
    country_df$Deaths <- as.numeric(country_df$Deaths)
    
    # Convert from cum sum to daily cases / death.
    if (isFALSE(cumulative)) {
        country_df$Cases <- c(0, diff(country_df$Cases))
        country_df$Deaths <- c(0, diff(country_df$Deaths))
    }
    return(country_df)
}
