class Instance:
    """
    Represents a hierarchical subcircuit instance.
    """

    def __init__(self, name, model, connections):
        self.name = name
        self.model = model
        self.connections = connections

    def __str__(self):
        connections = ", ".join(self.connections)
        return (
            f"{self.name} ({self.model})\n"
            f"  Connections: {connections}"
        )