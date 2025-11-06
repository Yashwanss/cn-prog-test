# Interactive Network Routing Simulator

## Overview

This project implements and simulates two fundamental network routing algorithms: **Distance Vector Routing** and **Link State Routing**. NetSim provides a comprehensive, event-driven network simulation environment where users can create custom network topologies, inject dynamic events (like link failures and cost changes), and observe how routing protocols adapt in real-time. The simulator includes an interactive GUI visualization tool that displays routing tables, packet transmission, and network state changes, making it an ideal educational and research platform for understanding distributed routing algorithms.

## Novelty

### Key Innovations

- **Event-Driven Dynamic Simulation:**
  - Unlike static routing simulators, NetSim supports **time-based network events** defined in JSON configuration files. You can schedule link failures, cost changes, and topology modifications at specific timestamps, allowing you to test protocol resilience and convergence behavior under realistic network conditions.
  
- **Real-Time Interactive Visualization:**
  - Built-in **Tkinter GUI** provides live visualization of the network topology, routing table updates, and packet flow animations. Users can click on routers to inspect their internal state, debug strings, and forwarding tables in real-time.
  
- **Side-by-Side Protocol Comparison:**
  - Implements both **Distance Vector (Bellman-Ford)** and **Link State (Dijkstra)** protocols from scratch, enabling direct comparison of convergence speed, routing loops, count-to-infinity problems, and scalability characteristics.
  
- **Flexible Topology Configuration:**
  - Network topologies are defined via **JSON files** with support for custom routers, clients, link costs, latencies, and buffer sizes. Multiple pre-configured topologies (small, medium, large) with various failure scenarios are included.
  
- **Traceroute & Packet Simulation:**
  - Simulates actual packet transmission with support for traceroute functionality, allowing users to trace the path packets take through the network and observe how routes change dynamically.

- **Thread-Based Concurrent Execution:**
  - Each router runs in its own thread, simulating distributed and autonomous behavior. Routers exchange routing information via packets, mimicking real-world distributed protocols without centralized coordination.

### Why This Project?

- **Educational Value:** Routing protocols like RIP (Distance Vector) and OSPF (Link State) are the backbone of the Internet. This simulator demystifies their operation and helps students/engineers understand:
  - How routers discover paths without global knowledge
  - Why link state protocols converge faster than distance vector
  - The impact of network failures on routing convergence
  
- **Research Platform:** Serves as a testbed for experimenting with routing algorithm modifications, new convergence techniques, or hybrid protocols.

- **Hands-On Learning:** Instead of just reading about Bellman-Ford or Dijkstra, users can *see* these algorithms in action, modify parameters, and immediately observe the results.

## Features

- **Distance Vector Router** (`distance_vector_router.py`):
  - Implements the Bellman-Ford algorithm with split-horizon and poison reverse optimizations
  - Periodic heartbeat-based routing updates
  - Handles link failures and cost changes dynamically
  
- **Link State Router** (`link_state_router.py`):
  - Implements Dijkstra's shortest path algorithm
  - Sequence number-based flooding to prevent routing loops
  - Uses NetworkX for efficient graph operations
  - Link state advertisements (LSAs) with controlled flooding
  
- **Network Simulation Engine** (`networks.py`):
  - Multi-threaded router execution for true distributed simulation
  - Event scheduler for link failures, additions, and cost changes
  - Support for multiple network topologies from JSON configuration
  - Client traffic generation with configurable send rates
  
- **Packet Handling** (`packet.py`):
  - Models data packets with source/destination addressing
  - Traceroute functionality for path discovery
  - Packet animation support for visualization
  
- **Interactive Visualization** (`visualize_networks.py`):
  - Real-time GUI using Tkinter
  - Network topology visualization with animated packet flow
  - Live routing table display
  - Router debug information on-click
  - Configurable animation speed
  
- **Client Interface** (`client.py`):
  - Traffic generation for testing routing protocols
  - Simulates end hosts sending packets through the network

## Achievements

- **Full Protocol Implementation:** Both Distance Vector and Link State protocols implemented from scratch with proper convergence guarantees
- **Dynamic Event Handling:** Successfully handles link failures, recoveries, and cost changes with automatic route recalculation
- **Real-Time Visualization:** Interactive GUI that displays routing tables, packet animations, and network state changes
- **Scalability Testing:** Tested with small, medium, and large network topologies (up to dozens of routers)
- **Convergence Analysis:** Demonstrated faster convergence of Link State vs. Distance Vector protocols
- **Educational Impact:** Clear visualizations make complex routing concepts accessible and understandable

## Screenshots / Implementation

<!-- Add your screenshots below by replacing the placeholder paths -->

### Network Topology Visualization
<img alt="Network Topology with Active Links" src="https://github.com/user-attachments/assets/e92acb7b-94cf-4477-b6bb-87b9c516f94a" />
*Real-time visualization of network topology with routers, clients, and active links*

### Distance Vector Routing in Action
<img  alt="image" src="https://github.com/user-attachments/assets/df04ebc2-b4a1-491b-8d5e-947cf0f54390" />
*Distance Vector routing tables showing hop counts and next-hop information*

### Link State Protocol Visualization
<img alt="image" src="https://github.com/user-attachments/assets/261207e3-f566-4272-9986-a0b198a5e4e8" />
*Link State protocol with Dijkstra's algorithm computing shortest paths*

### Dynamic Link Failure Response
<img alt="image" src="https://github.com/user-attachments/assets/79e5f3fd-d941-49aa-8b15-216aa3ce3cdb" />
<img alt="image" src="https://github.com/user-attachments/assets/50b57dfd-b2b0-4ec0-8f17-dd7caf2f42fe" />
*Network adapting to link failure - observe routing table updates and convergence*
- The screenshots above show:

    At time 12s: Link C-D goes down.

    At time 24s: Link C-D comes back up with a higher cost (9), and link A-D goes down


### Packet Flow Animation
![20251106-1605-46 0200678](https://github.com/user-attachments/assets/e22f3ded-590e-4f79-88ea-a9ebb8a17d78)

*Animated packet flow showing data traversing through the network*

## Getting Started

### Prerequisites

- **Python 3.8+** (tested on Python 3.8-3.11)
- **Required Libraries:**
  - `networkx` - for graph operations in Link State routing
  - `tkinter` - for GUI visualization (usually comes with Python)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/NetSim-Routing-Simulator.git
   cd NetSim-Routing-Simulator
   ```

2. **Install required dependencies:**
   ```bash
   pip install networkx
   ```
   
   *Note: `tkinter` is usually included with Python. If not installed, use:*
   - **Ubuntu/Debian:** `sudo apt-get install python3-tk`
   - **macOS:** `brew install python-tk`
   - **Windows:** Included by default with Python installer

### Running the Project

#### Option 1: Run with Visualization (Recommended)

**Distance Vector Protocol:**
```bash
python networks.py DV main_net_topology_events.json --visualize
```

**Link State Protocol:**
```bash
python networks.py LS main_net_topology_events.json --visualize
```

This will open a GUI window showing the network topology with:
- Real-time routing table updates
- Animated packet transmission
- Interactive router inspection (click on routers for debug info)

#### Option 2: Run Without Visualization (Console Mode)

**Distance Vector:**
```bash
python networks.py DV small_net_topology.json
```

**Link State:**
```bash
python networks.py LS medium_net_topology.json
```

#### Available Topology Files

- `small_net_topology.json` - Simple 3-router network for basic testing
- `medium_net_topology.json` - Medium-sized network with 6 routers
- `medium_net_topology_2.json` - Alternative medium topology
- `main_net_topology_events.json` - Complex topology with scheduled link failures
- `small_net_topology_link_failure.json` - Small topology with failure events

### Understanding the Output

- **Routing Tables:** Displayed in the GUI (right panel) showing destination, next-hop, and cost
- **Console Output:** Shows packet transmissions, routing updates, and convergence events
- **Debug String:** Click on any router in the GUI to see its internal state

### Custom Topologies

You can create your own network scenarios by editing the JSON configuration files:

```json
{
  "routers": ["A", "B", "C"],
  "clients": ["a", "b", "c"],
  "clientSendRate": 10,
  "endTime": 100,
  "links": [
    ["A", "B", 1, 1, 3, 3],  // [node1, node2, port1, port2, cost, latency]
    ["B", "C", 2, 1, 5, 2]
  ],
  "changes": [
    [20, ["A", "B"], "down"],  // At time 20, link A-B goes down
    [40, ["A", "B", 1, 1, 10, 3], "up"]  // At time 40, link comes back with cost 10
  ]
}
```

### Testing Scripts

Run the included test script to validate both protocols:
```bash
bash test_scripts/test_dv_ls.sh
```

## Project Structure

```
NetSim-Routing-Simulator/
├── router.py                           # Base Router class
├── distance_vector_router.py           # Distance Vector (Bellman-Ford) implementation
├── link_state_router.py                # Link State (Dijkstra) implementation
├── networks.py                         # Network simulation engine (main entry point)
├── visualize_networks.py               # GUI visualization tool
├── packet.py                           # Packet class for data transmission
├── link.py                             # Link class modeling network connections
├── client.py                           # Client (end host) implementation
├── test_scripts/                       # Testing scripts
│   └── test_dv_ls.sh                  # Automated test script
└── *.json                             # Network topology configuration files
```

## How It Works

1. **Initialization:** Network topology is loaded from a JSON file defining routers, clients, links, and events
2. **Router Threads:** Each router runs in a separate thread, simulating distributed execution
3. **Routing Protocol:** Routers exchange routing packets according to DV or LS protocol rules
4. **Convergence:** Routers build and update their forwarding tables based on received information
5. **Data Transmission:** Clients send packets through routers using the computed routes
6. **Events:** Scheduled network changes (link failures/recoveries) trigger routing table updates
7. **Visualization:** GUI displays the network state, routing tables, and packet animations in real-time

## Learning Outcomes

By working with this project, you will understand:

- How distributed routing protocols operate without centralized control
- The difference between distance vector and link state algorithms
- Why link state protocols converge faster but require more memory
- How sequence numbers prevent routing loops in link state protocols
- The count-to-infinity problem in distance vector routing
- How split-horizon and poison reverse improve distance vector convergence
- The impact of network failures on routing stability

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.
