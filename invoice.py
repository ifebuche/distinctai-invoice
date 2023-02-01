import json
import io
import cgi
from datetime import datetime as dt
from utils import cors_headers

def handler(event, context):
    """
    Process csv content.

    - Validate contents of the csv to match expected input: unit price, year and time.
    - Dispatch headers with response to cater to preflight calls from browsers.
    """

    content = event.get('body')
    if not content:
        body = {"message": "Empty payload"}
        response = {"statusCode": 400, "body":json.dumps(body), "headers":cors_headers}
        return response
    
    #Parse multi-part/form into a dict for use
    byte_data = io.BytesIO(event['body'].encode('utf-8'))
    param_dict = cgi.parse_header(event['headers']['Content-Type'])[1]
    
    if 'boundary' in param_dict:
        param_dict['boundary'] = param_dict['boundary'].encode('utf-8')

    param_dict['CONTENT-LENGTH'] = len(event['body'])
    form_data = cgi.parse_multipart(byte_data, param_dict)

    raw_input_data = form_data['data']
    data = raw_input_data[0].decode('utf-8').split('\r')
    header = data[0].split(',')

    if len(header) != 5:
        body = {"message": f"We expect a 5 column csv file. {len(header)} uploaded."}
        response = {"statusCode": 400, "body":json.dumps(body, default=str), "headers": cors_headers}

    #extract rows of the file and calculate invoice figures.
    rows = [line.strip() for line in data[1:]] #drop the first row/head

    output = []
    for row in rows:
        if row: #Cater to possible blank row at the end of csv
            result = {}
            row = row.split(',')
            result['Employee ID'] = row[0]
            try:
                unit_price = int(row[1])
            except ValueError as err:
                body = {"message": f"Invalid value in Unit Price - {err}"}
                response = {"statusCode": 400, "body":json.dumps(body, default=str), "headers": cors_headers}
                return response

            result['Unit Price'] = unit_price
            try:
                start = dt.strptime(f"{row[3]} : {row[4]}", "%Y-%m-%d : %H:%M")
                end = dt.strptime(f"{row[3]} : {row[5]}", "%Y-%m-%d : %H:%M")
            except ValueError as err:
                body = {"message": f"Bad time format detected. Expected year and time format: 'YYYY-MM-DD' and 'HH:MM' - {err}"}
                response = {"statusCode": 400, "body":json.dumps(body, default=str), "headers": cors_headers}
                return response

            total_hours = (end - start).total_seconds()/(60*60)
            result["Number of Hours"] = total_hours
            result['Cost'] = round((total_hours * unit_price), 2)
            output.append(result)

    body = {"message": "invoice details", "data":output}
    response = {"statusCode": 200, "body":json.dumps(body, default=str), "headers":cors_headers}
    return response   
