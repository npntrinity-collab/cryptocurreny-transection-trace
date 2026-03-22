id="svc2"
def build_graph(transactions):

    nodes = {}
    edges = []

    for tx in transactions:
        from_wallet = tx["from"]
        to_wallet = tx["to"]

        # Add nodes
        nodes[from_wallet] = {"data": {"id": from_wallet, "label": from_wallet}}
        nodes[to_wallet] = {"data": {"id": to_wallet, "label": to_wallet}}

        # Add edge
        edges.append({
            "data": {
                "source": from_wallet,
                "target": to_wallet,
                "label": f'{tx["amount"]} BTC'
            }
        })

    return {
        "nodes": list(nodes.values()),
        "edges": edges
    }