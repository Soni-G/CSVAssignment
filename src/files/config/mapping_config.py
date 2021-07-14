"""This config file is meant for keeping the column name mapping for\
   differnt file types from different banks."""


#specify date format for final unified csv file
date_format = "%m-%d-%Y"

#specifying desired column order in final unified csv file
column_order = ["date", "transaction_type", "amount", "from", "to"]

# Below mapping dict has been prepared considering these column names for the unified csv:
# ["date", "transaction_type", "amount", "from", "to"]
column_name_mapping = {
    # first file column name mapping
    "timestamp": "date",
    "type": "transaction_type",
    "amount": "amount",
    "from": "from",
    "to": "to",
    #  second file unique column name mapping
    "date": "date",
    "transaction": "transaction_type",
    "amounts": "amount",
    #  third file unique column name mapping
    "date_readable": "date",
    "euro": "amount_integer",
    "cents": "amount_decimal"
}