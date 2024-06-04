# Step 1
N = 3  # Number of server containers
num_slots = 512  # Total number of slots in the consistent hash map
K = 9  # Number of virtual servers for each server container


# Hash function for request mapping
def hash_request(i):
    return (i + 2*i**2 + 17) % num_slots


# Hash function for virtual server mapping
def hash_virtual_server(i, h):
    return (i + h + 2*h**2 + 25) % num_slots


# Step 2
consistent_hash_map = {}

# Initialize the consistent hash map
for server_id in range(N):
    for j in range(K):
        the_virtual_server_id = hash_virtual_server(server_id, j)
        consistent_hash_map[the_virtual_server_id] = server_id


# Step 3
def map_request(requested_id):
    hashed_request = hash_request(requested_id)
    
    # Find the next virtual server ID in the consistent hash map
    next_virtual_server_id = None
    for virtual_server_id in sorted(consistent_hash_map.keys()):
        if virtual_server_id >= hashed_request:
            next_virtual_server_id = virtual_server_id
            break
    
    # If no suitable virtual server is found, wrap around to the beginning
    if next_virtual_server_id is None:
        next_virtual_server_id = sorted(consistent_hash_map.keys())[0]
    
    # Get the server container ID corresponding to the virtual server ID
    the_server_id = consistent_hash_map[next_virtual_server_id]
    
    return the_server_id


# Step 4
request_id = 123
server_id = map_request(request_id)
print(f"Request {request_id} is mapped to Server: {server_id}")
