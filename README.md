# distinctai-invoice

#This is a RESTful serverless microservice app built on AWS Lambda and API Gateway, and mangaed + deployed with [Serverless Framework](https://www.serverless.com/). Standard HTTP status codes are in use. This is meant to support agile development by allowing micro ownership of the service.

**Deploy**
- To deploy and run this app on AWS, [setup](https://www.serverless.com/framework/docs/getting-started) Serverless Framework and add your AWS keys
- Clone this repo
- Run _sls deploy_ to deploy on AWS and get the associated endpoint url.
- For test purposes, an active endpoint is at: https://cz7pgk7yz9.execute-api.eu-west-1.amazonaws.com/prod/invoice

**Calling the endpoint + Testing**
- This is a POST endpoint accepting form-data bearing a file input with a single key *data* which is a csv file.
- See sample input data as *sample_input*. See also two sample bad input data for testing

**Response**
- The endpoint responds with a *message* key specifying the result of the call and an extra *data* key if successful.
- CORS is enabled for prelight calls.

**Error Hanlding**
- The service will detect bad calls and malformed csv files that thus:
  - Missing payload
  - CSV data Lacking expected the total count of columns: 5
  - Missing data in unit price
  - Wrong data in date and time columns
