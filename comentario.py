import boto3
import uuid
import json
import os

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    s3_name = os.environ["S3_NAME"]
    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')
    table = dynamodb.Table(nombre_tabla)

    s3.put_object(
        Bucket=s3_name,
        Key=f"{tenant_id}/{uuidv1}.json",
        Body=json.dumps(comentario),
        ContentType="application/json"
    )
    response = table.put_item(Item=comentario)
    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response
    }
