## Kinesis Data Stream
---
#### Create Kinesis Data Stream - OnDeamd
```
aws kinesis create-stream <KDS Name> --region <Region>
```

#### Create Kinesis Data Stream - Provisioned
```
aws kinesis create-stream --stream-name <KDS Name> --shard-count <Number>
```