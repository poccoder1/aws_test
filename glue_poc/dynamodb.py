# Import the necessary libraries
import boto3
import json

# Define the name of the DynamoDB table and the region
dynamodb_table_name = 'your-dynamodb-table-name'
region_name = 'your-region-name'

# Create a connection to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=region_name)

# Get the table object for the specified table name
table = dynamodb.Table(dynamodb_table_name)

# Scan the table and get all the items
response = table.scan()

# Extract the items from the response
dynamodb_data = response['Items']

# Keep scanning until all the items have been extracted
while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    dynamodb_data.extend(response['Items'])

# Print the extracted items for debugging purposes
print('DynamoDB data: {}'.format(json.dumps(dynamodb_data)))

# Convert the DynamoDB data to a PySpark data frame
dynamodb_data_frame = spark.read.json(sc.parallelize(dynamodb_data))




#####============== Filter condition ===============


# Import the necessary libraries
import boto3
import json

# Define the name of the DynamoDB table and the region
dynamodb_table_name = 'your-dynamodb-table-name'
region_name = 'your-region-name'

# Create a connection to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=region_name)

# Define the filter expression
filter_expression = 'attribute_not_exists(some_attribute)'

# Define the expression attribute values for the filter expression
expression_attribute_values = {}

# Define the expression attribute names for the filter expression
expression_attribute_names = {}

# Get the table object for the specified table name
table = dynamodb.Table(dynamodb_table_name)

# Scan the table and get all the items that match the filter expression
response = table.scan(
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values,
    ExpressionAttributeNames=expression_attribute_names
)

# Extract the items from the response
dynamodb_data = response['Items']

# Keep scanning until all the items have been extracted
while 'LastEvaluatedKey' in response:
    response = table.scan(
        FilterExpression=filter_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=expression_attribute_names,
        ExclusiveStartKey=response['LastEvaluatedKey']
    )
    dynamodb_data.extend(response['Items'])

# Print the extracted items for debugging purposes
print('DynamoDB data: {}'.format(json.dumps(dynamodb_data)))

# Convert the DynamoDB data to a PySpark data frame
dynamodb_data_frame = spark.read.json(sc.parallelize(dynamodb_data))

#
#
# filter_expression = 'attribute_not_exists(some_attribute)': Define the filter expression to fetch only the items that do not have the some_attribute attribute.
#
# expression_attribute_values = {}: Define an empty dictionary for the expression attribute values, as we don't need to pass any values for this filter expression.
#
# expression_attribute_names = {}: Define an empty dictionary for the expression attribute names, as we don't need to use any aliases for this filter expression.
#
# response = table.scan(: Update the scan() method call to include the FilterExpression, ExpressionAttributeValues, and ExpressionAttributeNames parameters.
#
# ExclusiveStartKey=response['LastEvaluatedKey']: Include the ExclusiveStartKey parameter in the subsequent scan() method calls to continue scanning from where the previous scan left off.
#
# You can update the filter_expression, expression_attribute_values, and expression_attribute_names variables to apply other filters as needed. The FilterExpression parameter supports various comparison operators, such as =, >, <, >=, <=, <>, BETWEEN, IN, and attribute_exists, among others. The ExpressionAttributeValues and ExpressionAttributeNames parameters can be used to pass any variable values or aliases used in the FilterExpression.

#############=========

#Example:::

employee_id	name	department	salary
1	John	IT	5000
2	Jane	Sales	7000
3	Bob	Finance	6000
4	Alice	Marketing	9000
5	Michael	IT	5500
6	Jennifer	Marketing	8500


filter_expression = 'department = :dept'
expression_attribute_values = {':dept': 'IT'}



filter_expression = 'salary BETWEEN :start AND :end'
expression_attribute_values = {':start': 6000, ':end': 9000}



filter_expression = 'department = :dept AND salary > :salary'
expression_attribute_values = {':dept': 'Marketing', ':salary': 8000}



filter_expression = 'attribute_not_exists(email)'


filter_expression = 'attribute_exists(name)'


##====================

id	name	age	city
1	Alice	25	New York
2	Bob	30	Los Angeles
3	Charlie	35	San Francisco
4	Dave	40	New York
5	Emma	45	Chicago
6	Frank	50	Los Angeles
7	Grace	55	Miami

#IN filter: Fetch all items with a city in a given list of cities

from boto3.dynamodb.conditions import Key, Attr

filter_expression = Attr('city').is_in(['New York', 'Miami'])
response = table.scan(FilterExpression=filter_expression)


##OR filter: Fetch all items that satisfy at least one of the specified conditions:

from boto3.dynamodb.conditions import Key, Attr

filter_expression = Attr('age').lt(30) | Attr('age').gt(50)
response = table.scan(FilterExpression=filter_expression)


#AND filter: Fetch all items that satisfy all of the specified conditions:
from boto3.dynamodb.conditions import Key, Attr

filter_expression = Attr('age').gt(30) & Attr('city').begins_with('Los')
response = table.scan(FilterExpression=filter_expression)

#NOT filter: Fetch all items that do not satisfy the specified condition:
from boto3.dynamodb.conditions import Key, Attr

filter_expression = ~Attr('city').contains('o')
response = table.scan(FilterExpression=filter_expression)

#begins_with filter: Fetch all items that have an attribute that begins with the specified value:
from boto3.dynamodb.conditions import Key, Attr

filter_expression = Key('name').begins_with('C')
response = table.scan(FilterExpression=filter_expression)


#contains filter: Fetch all items that have an attribute that contains the specified value:
from boto3.dynamodb.conditions import Key, Attr

filter_expression = Attr('name').contains('i')
response = table.scan(FilterExpression=filter_expression)

#size filter: Fetch all items that have a list or set attribute with a specified size:
from boto3.dynamodb.conditions import Key, Attr

filter_expression = Attr('city').size().eq(9)
response = table.scan(FilterExpression=filter_expression)


