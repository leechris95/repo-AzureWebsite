"""
TO DO: print message instead of contents when not inputting api arguments.
"""

from azure.data.tables import UpdateMode 
from azure.data.tables import TableClient

import json
import os

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:

    # input 
    partition_key = req.params.get('Partition_key', 'StaticWebsite')
    row_key = req.params.get('Row_key', 'staticwebsite1315x')

    table_client = TableClient.from_connection_string(os.environ["MyConnectionString"], "Resources")

    got_entity = table_client.get_entity(partition_key, row_key)

    # Add 1 to the VisitorCount
    got_entity['VisitorCount'] += 1 

    table_client.update_entity(mode=UpdateMode.REPLACE, entity=got_entity)

    cow = got_entity['VisitorCount']
    cow2 = {
         "VisitorCount":cow
         }

    return func.HttpResponse(
        json.dumps(cow2),
        mimetype="application/json",
        status_code=200
        )