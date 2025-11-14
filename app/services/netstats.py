import subprocess
from collections import defaultdict
from typing import Dict, List

from app.data.agents import BOT_UA_KEYWORDS

WEB_PORTS = [80, 443]


request_log: Dict[str, List[Dict]] = defaultdict(list)


def get_tcp_connections() -> List[Dict]:
    """
    Returns a list of TCP connections:
    { local_ip, local_port, remote_ip, remote_port, state }
    """
    result = subprocess.run(["ss", "-tn"], capture_output=True, text=True)
    lines: list = result.stdout.strip().split("\n")[1:]  # skip header
    connections: List[Dict] = []

    for line in lines:
        parts = line.split()
        if len(parts) < 5:
            continue
        state = parts[0]
        local = parts[3]
        remote = parts[4]
        try:
            l_ip, l_port = local.rsplit(":", 1)
            r_ip, r_port = remote.rsplit(":", 1)
            connections.append(
                {
                    "local_ip": l_ip,
                    "local_port": int(l_port),
                    "remote_ip": r_ip,
                    "remote_port": int(r_port),
                    "state": state,
                }
            )
        except ValueError:
            continue
    return connections


def get_web_connections(connections=None) -> List[Dict]:
    if connections is None:
        connections = get_tcp_connections()
    return [c for c in connections if c["local_port"] in WEB_PORTS]


def log_bot_request(ip: str, user_agent: str, path: str):
    """
    Call this in FastAPI middleware for bot requests
    """
    print("Logging bot request:", ip, user_agent, path)
    request_log[ip].append({"user_agent": user_agent, "path": path})
    # Optional: limit history per IP
    if len(request_log[ip]) > 1000:
        request_log[ip] = request_log[ip][-1000:]


def log_request(ip: str, user_agent: str, path: str):
    """
    Call this in FastAPI middleware
    """
    request_log[ip].append({"user_agent": user_agent, "path": path})
    # Optional: limit history per IP
    if len(request_log[ip]) > 1000:
        request_log[ip] = request_log[ip][-1000:]


def get_bot_stats() -> Dict[str, int]:
    """
    Returns a dict: {ip: bot_request_count}
    """
    bot_counts = {}
    for ip, entries in request_log.items():
        bot_counts[ip] = sum(
            1
            for e in entries
            if any(k in str(e.get("user_agent", "")).lower() for k in BOT_UA_KEYWORDS)
        )
    return bot_counts


def get_total_web_requests() -> int:
    """
    Total number of web requests logged
    """
    return sum(len(entries) for entries in request_log.values())
