import boto3
import threading
import time
import json
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

class ParallelScanWorker:
    """Worker class for parallel scan segments."""
    
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        self.consumed_capacity = 0
    
    def scan_segment(self, segment, total_segments):
        """Scan a specific segment of the table."""
        
        items = []
        scanned_count = 0
        
        # Start with initial scan
        response = self.table.scan(
            TotalSegments=total_segments,
            Segment=segment,
            ReturnConsumedCapacity='TOTAL'
        )
        
        # Process items from this segment
        items.extend(response['Items'])
        scanned_count += response['ScannedCount']
        self.consumed_capacity += response['ConsumedCapacity']['CapacityUnits']
        
        # Continue scanning if we have more items in this segment
        while 'LastEvaluatedKey' in response:
            response = self.table.scan(
                TotalSegments=total_segments,
                Segment=segment,
                ExclusiveStartKey=response['LastEvaluatedKey'],
                ReturnConsumedCapacity='TOTAL'
            )
            items.extend(response['Items'])
            scanned_count += response['ScannedCount']
            self.consumed_capacity += response['ConsumedCapacity']['CapacityUnits']
        
        print(f"Segment {segment}: Scanned {scanned_count} items, retrieved {len(items)} items")
        return items

def run_parallel_scan(table_name, total_segments):
    """Perform a parallel scan using multiple threads."""
    
    print(f"=== Running Parallel Scan with {total_segments} segments ===")
    
    # Create worker
    worker = ParallelScanWorker(table_name)
    
    # Start timing
    start_time = time.time()
    
    # Use ThreadPoolExecutor to manage threads
    all_items = []
    with ThreadPoolExecutor(max_workers=total_segments) as executor:
        # Submit tasks for each segment
        futures = [
            executor.submit(worker.scan_segment, segment, total_segments)
            for segment in range(total_segments)
        ]
        
        # Collect results as they complete
        for future in futures:
            segment_items = future.result()
            all_items.extend(segment_items)
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    # Print results
    print("\n=== Parallel Scan Results ===")
    print(f"Total items retrieved: {len(all_items)}")
    print(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Items per second: {len(all_items) / execution_time:.2f}")
    print(f"Total consumed capacity: {worker.consumed_capacity:.2f} RCUs")
    
    return {
        'items_count': len(all_items),
        'execution_time': execution_time,
        'items_per_second': len(all_items) / execution_time,
        'consumed_capacity': worker.consumed_capacity
    }

if __name__ == "__main__":
    # Run parallel scan with different numbers of segments
    table_name = 'GameLeaderboard'
    
    # Test with different segment counts to find optimal performance
    segment_counts = [1, 2, 4, 8]
    results = {}
    
    for segments in segment_counts:
        print(f"\nTesting with {segments} segment(s)...")
        results[segments] = run_parallel_scan(table_name, segments)
    
    # Compare results
    print("\n=== Performance Comparison ===")
    print("Segments | Execution Time (s) | Items/Second | Consumed RCUs")
    print("---------|-------------------|-------------|-------------")
    
    for segments, result in results.items():
        print(f"{segments:8} | {result['execution_time']:17.2f} | {result['items_per_second']:11.2f} | {result['consumed_capacity']:13.2f}")
    
    # Find the best performing configuration
    best_segments = max(results.keys(), key=lambda s: results[s]['items_per_second'])
    
    print(f"\nBest performance achieved with {best_segments} segment(s):")
    print(f"- {results[best_segments]['items_per_second']:.2f} items/second")
    print(f"- {results[best_segments]['execution_time']:.2f} seconds total execution time")