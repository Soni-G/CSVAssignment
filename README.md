# CSVAssignment

# What this does?
## The purpose of this application is to take multiple csv files as input & prepare a single
## unified file in the desired format of either csv, json or xml.

# How to run
## Keep all the source csv files in src/files/source folder.
## install the packages mentioned in requirements.txt file
## Navigate to src/service folder & run the addcsv.py file
## User can generate files in differnt format by calling the function populate_unified_csv() and
## specifying the desired file type. Eg:
## print(file_processing().populate_unified_csv(format='csv'))
## print(file_processing().populate_unified_csv(format='json'))
## print(file_processing().populate_unified_csv(format='xml'))

# Flexibilities available:
## The application supports multiple flexibilities mentioned below:
## 1). User can update the date format in final file as per his liking by updating the 'date_format'
##     variable available in src/files/config/mapping_config.py file.
## 
## 2). User can add source csv files with different column names and in different order, the 
##     application will support it. ONLY IMPORTANT REQUIREMENT is, user has to update the column mapping
##     in 'column_name_mapping' dictionary available in src/files/config/mapping_config.py file.
## 
## 3). User can also change the order of the columns in final unified file. ONLY IMPORTANT REQUIREMENT
##     is, user has to update the column order in 'column_order' list available in
##    src/files/config/mapping_config.py file.

# Future Scope
## The file generation function can be accessed via a REST Api to generate the final file & the result
## can be sent as a response to the user to be consumed by UI or download & use as report.

# Limitations:
## currently the application supports conversion of only euro & cents to amount.
## other currency support can be generalised & added.
