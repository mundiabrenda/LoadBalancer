# Load Balancer Analysis

## A-1: Load Distribution Among Servers

### Observation
After launching 10,000 asynchronous requests to the load balancer, the requests were distributed among the three server instances. The results are printed as follows:

### Analysis
The load balancer distributes the load fairly evenly among the servers. Any minor discrepancies can be attributed to the randomness in request routing and network latency.

## A-2: Scalability Analysis

### Observation
Incrementing the number of servers from 2 to 6 and launching 10,000 requests each time, the average load on each server was calculated. The results are printed as follows:

### Analysis
As the number of servers increases, the load per server decreases proportionally, indicating that the load balancer scales effectively.

## A-3: Server Failure Recovery

### Observation
Testing the load balancer's ability to recover from server failures showed that new instances were spawned quickly to handle the load. The '/rep' endpoint was used to verify the status of replicas.

### Analysis
The load balancer effectively maintains the specified number of replicas, ensuring high availability and fault tolerance.

# A-4: Hash Function Modification

### Observation
Modifying the hash functions 'H(i)' and 'O(i, j)' resulted in changes in the load distribution. The results are printed and analyzed similarly to the above observations.

### Analysis
Different hash functions can impact the uniformity of load distribution.