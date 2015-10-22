var config = module.exports = {
  kinesis : {
    region : 'us-east-1'
  },

  sampleProducer : {
    stream : 'Alpha-TestStream',
    shards : 1,
    waitBetweenDescribeCallsInSeconds : 5,
    PartitionKey: 'TestBuilding'
},

accessKeyId: process.env.AWS_ACCESS_KEY_ID,
secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    

  PartitionKey: 'TestBuilding'
}