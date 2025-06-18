# Lab 8: DynamoDB Auto-scaling

In this lab, you'll learn how to configure and observe DynamoDB auto-scaling in action.

## What is DynamoDB Auto-scaling?

DynamoDB auto-scaling automatically adjusts provisioned throughput capacity in response to actual traffic patterns. This helps you:

1. Maintain performance during traffic spikes
2. Reduce costs during periods of low activity
3. Eliminate the need for manual capacity planning

## Lab Overview

In this lab, you'll:

1. Configure auto-scaling for your DynamoDB table
2. Generate traffic to trigger scaling events
3. Observe scaling activities in real-time
4. Analyze CloudWatch metrics to understand scaling behavior

## Instructions

### Step 1: Configure Auto-scaling

Run the provided script to configure auto-scaling for your table:

```bash
python configure_autoscaling.py
```

This will:
- Set target utilization to 70%
- Configure min capacity to 5 RCUs/WCUs
- Configure max capacity to 100 RCUs/WCUs

### Step 2: Generate Traffic

Run the provided script to generate traffic that will trigger auto-scaling:

```bash
python generate_traffic.py
```

This script will gradually increase the read and write operations to trigger scaling events.

### Step 3: Observe Auto-scaling in Action

While the traffic generator is running, monitor the auto-scaling activities:

```bash
python monitor_autoscaling.py
```

This will show you:
- Current provisioned capacity
- Consumed capacity
- Scaling activities
- CloudWatch metrics

## Next Steps

Once you've completed this lab, proceed to [Lab 9: Time to Live](../09-ttl/) to learn how to automatically expire items in DynamoDB.