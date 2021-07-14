import sys
import csv
import json
import os
from os import listdir
from pathlib import Path
import dateutil.parser
from datetime import datetime

#setting current dir & parent dir paths, source & target file paths
path = Path(os.getcwd())
parent_dir = str(path.parent.absolute())
source_dir = parent_dir+"/files/source/"
target_dir = parent_dir+"/files/target/unified.csv"
target_json_dir = parent_dir+"/files/target/unified.json"
target_xml_dir = parent_dir+"/files/target/unified.xml"
temp_file_dir = parent_dir+"/files/target/temp.csv"
#adding src folder path in system path
sys.path.insert(0, parent_dir)

from files.config.mapping_config import column_name_mapping, column_order, date_format

class file_processing():
    """csv file processing class"""
    
    def get_updated_columns(self, old_column_names):
        """method to update column name as per the unified csv format"""
        old_column_names = old_column_names.strip()      
        new_column_names = ""
        old_column_list = old_column_names.split(",")
        for col_name in old_column_list:
            new_column_names += (column_name_mapping.get(col_name, col_name) + ",")
        new_column_names = new_column_names.rstrip(",")
        new_column_names += "\n"
        return new_column_names

    def prepare_temp_source_csv_file(self, csv_file_path):
        """method to prepare a temporary copy of csv file with updated
           column name in temp_file_dir"""
        updated_rows = []
        with open(temp_file_dir, "w") as ftempout:
            column_processed = False
            for line in open(csv_file_path):
                if not column_processed:
                    updated_column_name = self.get_updated_columns(line)
                    ftempout.write(updated_column_name)
                    column_processed = True
                else:
                    ftempout.write(line)
            ftempout.write("\n")
        # below code will run if source file contains amount in integer & decimal columns
        if updated_column_name.find('amount_integer') != -1:
            with open(temp_file_dir, "r") as ftempread:
                reader = csv.DictReader(ftempread) # read rows into a dictionary format
                for row in reader: # read a row as {column1: value1, column2: value2,...}
                    row['amount'] = int(row['amount_integer']) + int(row['amount_decimal'])/100
                    row.pop('amount_integer', None)
                    row.pop('amount_decimal', None)
                    updated_rows.append(row)
        if updated_rows:
            keys = updated_rows[0].keys()
            with open(temp_file_dir, 'w')  as ftempupdated:
                dict_writer = csv.DictWriter(ftempupdated, keys)
                dict_writer.writeheader()
                dict_writer.writerows(updated_rows)

    
    def populate_unified_csv(self, format='csv'):
        """Main method to populate final csv file"""
        #iterate over each csv file in the source directory
        if(os.path.exists(target_dir) and os.path.isfile(target_dir)):
            os.remove(target_dir)
        first_file_processed = False
        for csv_file in listdir(source_dir):
            if csv_file.endswith('.csv'):
                # set source csv file path
                csv_file_path = source_dir + csv_file
                # preparing temporary source file with updated file name
                self.prepare_temp_source_csv_file(csv_file_path)
                # open source & target csv in read & write mode respectively
                with open(temp_file_dir, 'r') as fin, open(target_dir, 'a') as fout:
                    writer = csv.DictWriter(fout, fieldnames=column_order)
                    if not first_file_processed:
                        # reorder the header first
                        writer.writeheader()
                        first_file_processed = True
                    for row in csv.DictReader(fin):
                        # writes the reordered rows to the new file
                        writer.writerow(row)
        # below code runs to update the date column in final unified.csv file
        # it updates the date format as specified in the config file
        final_updated_rows = []
        with open(target_dir, "r") as ffinalread:
            reader = csv.DictReader(ffinalread) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                parsed_date = dateutil.parser.parse(row['date'])
                datetime_object = datetime.strptime(str(parsed_date),'%Y-%m-%d  %H:%M:%S')
                new_date = datetime_object.strftime(date_format)
                row['date'] = new_date
                final_updated_rows.append(row)
        keys = final_updated_rows[0].keys()
        with open(target_dir, 'w')  as ffinalwrite:
            dict_writer = csv.DictWriter(ffinalwrite, keys)
            dict_writer.writeheader()
            dict_writer.writerows(final_updated_rows)
        if format == 'json':
            csv_file_path = target_dir
            json_data = {}
            row_list = []
            with open(csv_file_path) as fscvpath:
                reader = csv.DictReader(fscvpath)
                for rows in reader:
                    row_list.append(row)
                json_data['data'] = row_list
            with open(target_json_dir, 'w') as fjson:
                fjson.write(json.dumps(json_data, indent=4))
        if format == 'xml':
            csvFile = target_dir
            xmlFile = 'myData.xml'
            with open(csvFile) as fcsv, open(target_xml_dir, 'w') as fxml:
                csvreader = csv.reader(fcsv)
                fxml = open(target_xml_dir, 'w')
                fxml.write('<?xml version="1.0"?>' + "\n")
                fxml.write('<csv_data>' + "\n")
                rowNum = 0
                for row in csvreader:
                    if not row:
                        continue
                    if rowNum == 0:
                        tags = row
                        # replace spaces w/ underscores in tag names
                        for i in range(len(tags)):
                            tags[i] = tags[i].replace(' ', '_')
                    else: 
                        fxml.write('<row>' + "\n")
                        for i in range(len(tags)):
                            fxml.write('    ' + '<' + tags[i] + '>'\
                                + row[i] + '</' + tags[i] + '>' + "\n")
                        fxml.write('</row>' + "\n")
                            
                    rowNum +=1
                fxml.write('</csv_data>' + "\n")
        return f"file generated successfully! Check unified.{format} file in location src/files/target"

f_process = file_processing()
print(f_process.populate_unified_csv(format='csv'))
print(f_process.populate_unified_csv(format='json'))
print(f_process.populate_unified_csv(format='xml'))