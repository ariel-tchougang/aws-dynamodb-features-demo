# Lab 13: DynamoDB CloudWatch Metrics

In this lab, you'll learn how to monitor DynamoDB performance using CloudWatch metrics and create alarms for proactive monitoring.

## What are DynamoDB CloudWatch Metrics?

Amazon CloudWatch collects and processes raw data from DynamoDB into readable, near real-time metrics. These metrics help you:

1. Monitor table performance
2. Set up alarms for capacity issues
3. Analyze usage patterns
4. Make data-driven scaling decisions

## Lab Overview

In this lab, you'll:

1. Generate traffic to produce metrics
2. View and analyze DynamoDB metrics in CloudWatch
3. Create CloudWatch alarms for capacity monitoring
4. Create a CloudWatch dashboard for DynamoDB

## Instructions

### Step 1: Generate Traffic

Run the provided script to generate traffic that will produce metrics:

```bash
python generate_traffic.py
```

This will create a mix of read and write operations to generate various metrics.

### Step 2: View DynamoDB Metrics

Run the provided script to view the metrics:

```bash
python view_metrics.py
```

This will show you:
- Consumed capacity metrics
- Throttling events
- Latency metrics
- System errors

### Step 3: Create CloudWatch Alarms

Run the provided script to create CloudWatch alarms:

```bash
python create_alarms.py
```

This will create alarms for:
- High consumed capacity
- Throttling events
- High latency

### Step 4: Create a CloudWatch Dashboard

Run the provided script to create a CloudWatch dashboard:

```bash
python create_dashboard.py
```

This will create a dashboard with:
- Consumed capacity widgets
- Throttling widgets
- Latency widgets
- Error widgets

## Key DynamoDB Metrics

- **ConsumedReadCapacityUnits** - The number of read capacity units consumed
- **ConsumedWriteCapacityUnits** - The number of write capacity units consumed
- **ReadThrottleEvents** - The number of read requests that exceed provisioned capacity
- **WriteThrottleEvents** - The number of write requests that exceed provisioned capacity
- **SuccessfulRequestLatency** - The latency of successful requests
- **SystemErrors** - The number of internal server errors

## Next Steps

Congratulations! You've completed all the labs in this DynamoDB features demo. You now have hands-on experience with a wide range of DynamoDB features and best practices.

To clean up all resources created during these labs, run:

```bash
python ../cleanup.py
```