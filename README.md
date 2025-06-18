# 🎮 GameLeaderboard: DynamoDB Features Demo

Welcome to the GameLeaderboard DynamoDB demo! In this hands-on lab, you'll learn how to use Amazon DynamoDB by building a game leaderboard system for "Cosmic Defenders," a fictional multiplayer space battle game.

## 🚀 Scenario

You're a backend developer for "Cosmic Defenders," a popular online game where players battle in space arenas. The game needs a robust leaderboard system that can:

- Track player scores, achievements, and battle history
- Handle millions of concurrent players during peak hours
- Provide fast access to leaderboard data for different game modes
- Support time-limited seasonal competitions with automatic data expiration
- Process transactions for in-game rewards and achievements
- Scale automatically during major game events

This scenario is perfect for demonstrating DynamoDB's capabilities as it requires high performance, scalability, and various access patterns.

## 📋 Lab Features

This hands-on lab will guide you through implementing the following DynamoDB features:

1. **Table Creation** - Create a table with composite primary key, Local Secondary Index (LSI), and Global Secondary Index (GSI)
2. **Data Loading** - Generate and load game data into the table
3. **Basic CRUD Operations** - Perform put-item, update-item, get-item, delete-item operations
4. **Query Performance Testing** - Compare query performance using partition key vs. GSI
5. **Scan Operations** - Explore various scan techniques and pagination
6. **Exponential Backoff** - Handle throttling with retry mechanisms
7. **Parallel Scan** - Improve scan performance with parallel processing
8. **Auto-scaling** - Observe DynamoDB adapting to changing workloads
9. **Time to Live (TTL)** - Automatically expire seasonal game data
10. **Transactions** - Ensure data consistency for critical game operations
11. **Conditional Operations** - Implement optimistic locking for game state updates
12. **Batch Operations** - Process multiple items efficiently
13. **CloudWatch Metrics** - Monitor and analyze DynamoDB performance

## 🛠️ Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Python 3.11+ with boto3 library
- Basic understanding of AWS services and DynamoDB concepts

## 🏁 Getting Started

Clone this repository and follow the step-by-step instructions in each lab section:

```bash
git clone https://github.com/yourusername/aws-dynamodb-features-demo.git
cd aws-dynamodb-features-demo
```

Each lab section is contained in its own directory with detailed instructions and code samples.

## 📚 Lab Structure

1. [Lab 1: Table Creation](./01-table-creation/)
2. [Lab 2: Data Loading](./02-data-loading/)
3. [Lab 3: CRUD Operations](./03-crud-operations/)
4. [Lab 4: Query Performance](./04-query-performance/)
5. [Lab 5: Scan Operations](./05-scan-operations/)
6. [Lab 6: Exponential Backoff](./06-exponential-backoff/)
7. [Lab 7: Parallel Scan](./07-parallel-scan/)
8. [Lab 8: Auto-scaling](./08-auto-scaling/)
9. [Lab 9: Time to Live](./09-ttl/)
10. [Lab 10: Transactions](./10-transactions/)
11. [Lab 11: Conditional Operations](./11-conditional-operations/)
12. [Lab 12: Batch Operations](./12-batch-operations/)
13. [Lab 13: CloudWatch Metrics](./13-cloudwatch-metrics/)

## 🧹 Cleanup

Don't forget to delete all resources created during this lab to avoid unnecessary AWS charges:

```bash
python cleanup.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.