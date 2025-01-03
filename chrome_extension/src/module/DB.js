import AWS from 'aws-sdk';

AWS.config.update({ region: 'ap-northeast-2' });

const secretsManager = new AWS.SecretsManager();

const getSecretValue = async (secretName) => {
  try {
    const data = await secretsManager.getSecretValue({ SecretId: secretName }).promise();
    if ('SecretString' in data) {
      return JSON.parse(data.SecretString);
    } else {
      const buff = new Buffer(data.SecretBinary, 'base64');
      return JSON.parse(buff.toString('ascii'));
    }
  } catch (error) {
    console.error('Error retrieving secret from Secrets Manager', error);
    throw error;
  }
};

const initDynamoDb = async () => {
  const secrets = await getSecretValue(process.env.REACT_APP_AWS_SECRET_NAME);

  AWS.config.update({
    accessKeyId: secrets.AWS_ACCESS_KEY_ID,
    secretAccessKey: secrets.AWS_SECRET_ACCESS_KEY
  });

  return new AWS.DynamoDB.DocumentClient();
};

const getItemFromDynamoDB = async (tableName, key) => {
  const dynamoDb = await initDynamoDb();
  const params = {
    TableName: tableName,
    Key: key
  };

  try {
    const data = await dynamoDb.get(params).promise();
    return data.Item;
  } catch (error) {
    console.error("Error getting item from DynamoDB", error);
    throw error;
  }
};

export { getItemFromDynamoDB };
