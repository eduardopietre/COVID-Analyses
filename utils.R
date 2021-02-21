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
