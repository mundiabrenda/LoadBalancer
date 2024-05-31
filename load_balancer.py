from flask import Flask, request, jsonify
import os
import random
from consistent_hash import map_request
from consistent_hash import consistent_hash_map, num_slots, K, hash_virtual_server

app = Flask(__name__)

# Initial number of server containers (N)
N = 3
# Consistent hash map and virtual server setup from Task 2


# List of current server replicas
servers = [f'server_{i}' for i in range(N)]
virtual_servers = {}

# Initialize the consistent hash map with current servers
for server_id in servers:
    for j in range(K):
        virtual_server_id = hash_virtual_server(int(server_id.split('_')[1]), j)
        virtual_servers[virtual_server_id] = server_id


@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({"replicas": servers}), 200


@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.json
    new_instances = data.get('new_instances', 0)
    hostnames = data.get('hostnames', [])

    if new_instances <= 0:
        return jsonify({"error": "Invalid number of instances"}), 400

    if len(hostnames) > new_instances:
        return jsonify({"error": "Hostnames list is longer than the number of new instances"}), 400

    for i in range(new_instances):
        hostname = hostnames[i] if i < len(hostnames) else f'server_{len(servers)}'
        servers.append(hostname)
        for a in range(K):
            the_virtual_server_id = hash_virtual_server(int(hostname.split('_')[1]), a)
            virtual_servers[the_virtual_server_id] = hostname

    return jsonify({"status": "success", "new_replicas": servers[-new_instances:]}), 201


@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.json
    remove_instances = data.get('remove_instances', 0)
    hostnames = data.get('hostnames', [])

    if remove_instances <= 0:
        return jsonify({"error": "Invalid number of instances"}), 400

    if len(hostnames) > remove_instances:
        return jsonify({"error": "Hostnames list is longer than the number of removable instances"}), 400

    if remove_instances > len(servers):
        return jsonify({"error": "Trying to remove more instances than available"}), 400

    removed = []
    if hostnames:
        for hostname in hostnames:
            if hostname in servers:
                servers.remove(hostname)
                removed.append(hostname)
            else:
                return jsonify({"error": f"Hostname {hostname} not found"}), 400
    else:
        for _ in range(remove_instances):
            hostname = random.choice(servers)
            servers.remove(hostname)
            removed.append(hostname)

    for the_server_id in removed:
        for b in range(K):
            virtual_server_id_3 = hash_virtual_server(int(the_server_id.split('_')[1]), b)
            virtual_servers.pop(virtual_server_id_3, None)

    return jsonify({"status": "success", "removed_replicas": removed}), 200


@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    requested_id = random.randint(0, num_slots - 1)
    server_id_3 = map_request(requested_id)
    return jsonify({"message": f"Request routed to {server_id_3}"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
