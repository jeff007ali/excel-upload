import pandas as pd
import json
from bson.json_util import dumps
import logging

from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from testApp.settings import MONGO_DB

logger = logging.getLogger("app")

@method_decorator(csrf_exempt, name='dispatch')
class InsertData(View):
    def post(self, request):
        logger.info("Request Body File: {}".format(request.FILES['file']))
        try:
            filepath = request.FILES['file']

            db = MONGO_DB["excel_data"]

            df = pd.read_excel(filepath, sheet_name=None)
            logger.info("Excel sheets name: {}".format(df.keys()))
            
            final_json = {}
            for key, value in df.items():
                data_json = json.loads(value.to_json(orient='records'))
                final_json[key] = data_json

            db.remove()
            res = db.insert(final_json)
            logger.debug("Data is inserted into MongoDB under Id: {}".format(res))
            
        except Exception as e:
            logger.exception("Exception while inserting data: {}".format(e))

        return JsonResponse({"status": "Excel data is inserted successfully!!!"})


@method_decorator(csrf_exempt, name='dispatch')
class GetData(View):
    def get(self, request):
        db_records = MONGO_DB["excel_data"].find()
        logger.info("Retrived records count is {}".format(db_records.count()))
        return JsonResponse({"status": json.loads(dumps(db_records))})


@method_decorator(csrf_exempt, name='dispatch')
class DeleteData(View):
    def get(self, request):
        MONGO_DB["excel_data"].delete_many({})
        db_records = MONGO_DB["weather"].find()
        logger.info("All records are deleted!!!")
        return JsonResponse({"status": json.loads(dumps(db_records))})

