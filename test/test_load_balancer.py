import requests
import threading
import time
import json

# Constants
LOAD_BALANCER_URL = "http://localhost:5000"
NUM_REQUESTS = 10000


def send_request(endpoint):
    try:
        response = requests.get(f"{LOAD_BALANCER_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json().get("message")
    except Exception as e:
        print(f"Error: {e}")
    return None


def simulate_load(num_requests, endpoint):
    results = []
    for _ in range(num_requests):
        result = send_request(endpoint)
        if result:
            results.append(result)
    return results


def test_load_distribution():
    # Start the load test
    print("Starting load test...")
    results = simulate_load(NUM_REQUESTS, "home")

    # Count the requests handled by each server
    server_counts = {}
    for result in results:
        if isinstance(result, str):
            server_id = result.split(": ")[-1]
            if server_id not in server_counts:
                server_counts[server_id] = 0
            server_counts[server_id] += 1

    # Print the results
    print("Request Distribution Across Servers:")
    for server_id, count in server_counts.items():
        print(f"Server {server_id}: {count} requests")


def test_scalability():
    average_loads = []
    server_counts = [2, 3, 4, 5, 6]

    for count in server_counts:
        print(f"Testing with {count} servers...")
        # Adjust the number of servers
        requests.post(f"{LOAD_BALANCER_URL}/add", json={"new_instances": count,
                                                        "hostnames": [f"server_{i+1}" for i in range(count)]})

        # Wait for the servers to be added
        time.sleep(5)

        # Run the load test
        results = simulate_load(NUM_REQUESTS, "home")

        # Count the requests handled by each server
        server_counts = {}
        for result in results:
            if isinstance(result, str):
                server_id = result.split(": ")[-1]
                if server_id not in server_counts:
                    server_counts[server_id] = 0
                server_counts[server_id] += 1

        # Calculate the average load
        average_load = sum(server_counts.values()) / len(server_counts)
        average_loads.append(average_load)

        # Remove the added servers
        requests.delete(f"{LOAD_BALANCER_URL}/rm", json={"remove_instances": count,
                                                         "hostnames": [f"server_{i+1}" for i in range(count)]})

    # Print the results
    print("Scalability Analysis:")
    for count, avg_load in zip(server_counts, average_loads):
        print(f"{count} servers: Average load = {avg_load}")


if __name__ == "__main__":
    test_load_distribution()
    test_scalability()
