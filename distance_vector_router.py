import sys
from collections import defaultdict
from router import Router
from packet import Packet
from json import dumps, loads


class DVrouter(Router):
    """Distance vector routing protocol implementation."""

    def __init__(self, addr, heartbeatTime):
        Router.__init__(self, addr)
        self.heartbeatTime = heartbeatTime
        self.last_time = 0
        self.dv = {}  # {destination: (cost, port)}
        self.neighbor_dvs = {}  # {neighbor: {destination: cost}}
        self.port_to_neighbor = {}  # {port: neighbor}
        self.neighbor_to_port = {}  # {neighbor: port}
        self.forward = {}  # {destination: port}
        self.cost_to_neighbor = {}  # {neighbor: cost}
        self.addr = addr

    def handlePacket(self, port, packet):
        if packet.isTraceroute():
            # Forward data packet if possible
            dst = packet.dstAddr
            if dst in self.forward:
                out_port = self.forward[dst]
                self.send(out_port, packet)
        else:
            # Routing packet: update neighbor's DV and recalculate
            neighbor = self.port_to_neighbor.get(port)
            if neighbor is None:
                return
            try:
                neighbor_dv = loads(packet.content)
            except Exception:
                return
            changed = False
            # Update neighbor's DV
            self.neighbor_dvs[neighbor] = neighbor_dv
            changed = self.update_distance_vector()
            if changed:
                self.broadcast_dv()


    def handleNewLink(self, port, endpoint, cost):
        neighbor = endpoint
        self.port_to_neighbor[port] = neighbor
        self.neighbor_to_port[neighbor] = port
        self.cost_to_neighbor[neighbor] = cost
        # Initialize neighbor's DV as empty
        if neighbor not in self.neighbor_dvs:
            self.neighbor_dvs[neighbor] = {}
        # Set direct cost to neighbor
        if neighbor not in self.dv or cost < self.dv.get(neighbor, (float('inf'), None))[0]:
            self.dv[neighbor] = (cost, port)
        self.update_distance_vector()
        self.broadcast_dv()


    def handleRemoveLink(self, port):
        neighbor = self.port_to_neighbor.get(port)
        if neighbor:
            del self.port_to_neighbor[port]
            del self.neighbor_to_port[neighbor]
            if neighbor in self.neighbor_dvs:
                del self.neighbor_dvs[neighbor]
            if neighbor in self.cost_to_neighbor:
                del self.cost_to_neighbor[neighbor]
        # Remove all routes that used this port
        to_remove = [dst for dst, (cost, p) in self.dv.items() if p == port]
        for dst in to_remove:
            del self.dv[dst]
        self.update_distance_vector()
        self.broadcast_dv()


    def handleTime(self, timeMillisecs):
        if timeMillisecs - self.last_time >= self.heartbeatTime:
            self.last_time = timeMillisecs
            self.broadcast_dv()


    def debugString(self):
        return f"DV: {self.dv}\nForward: {self.forward}\nNeighbors: {self.port_to_neighbor}"

    def update_distance_vector(self):
        changed = False
        # Start with direct neighbors
        new_dv = {dst: (cost, port) for dst, (cost, port) in self.dv.items()}
        # Add self route
        new_dv[self.addr] = (0, None)
        # Bellman-Ford update
        for neighbor, neighbor_dv in self.neighbor_dvs.items():
            cost_to_neighbor = self.cost_to_neighbor.get(neighbor, float('inf'))
            for dst, neighbor_cost in neighbor_dv.items():
                if dst == self.addr:
                    continue
                total_cost = cost_to_neighbor + neighbor_cost
                if dst not in new_dv or total_cost < new_dv[dst][0]:
                    port = self.neighbor_to_port[neighbor]
                    new_dv[dst] = (total_cost, port)
        # Check for changes
        if set(new_dv.keys()) != set(self.dv.keys()) or any(new_dv[k][0] != self.dv.get(k, (float('inf'), None))[0] or new_dv[k][1] != self.dv.get(k, (float('inf'), None))[1] for k in new_dv):
            changed = True
        self.dv = new_dv
        # Update forwarding table
        self.forward = {dst: port for dst, (cost, port) in self.dv.items() if port is not None}
        return changed

    def broadcast_dv(self):
        # Send our DV to all neighbors
        dv_to_send = {dst: cost for dst, (cost, port) in self.dv.items()}
        for port, neighbor in self.port_to_neighbor.items():
            # Poison reverse: set cost to inf for routes learned from that neighbor
            poisoned_dv = dv_to_send.copy()
            for dst in list(poisoned_dv.keys()):
                if dst in self.neighbor_dvs.get(neighbor, {}) and self.dv[dst][1] == port and dst != neighbor:
                    poisoned_dv[dst] = float('inf')
            pkt = Packet(Packet.ROUTING, self.addr, neighbor, dumps(poisoned_dv))
            self.send(port, pkt)
