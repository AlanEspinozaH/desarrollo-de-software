import json
from dependency import DependsOn
from network import NetworkFactoryModule
from server import ServerFactoryModule
from firewall import FirewallFactoryModule
from load_balancer import LoadBalancerFactoryModule

class Mediator:
    def __init__(self, module):
        self.module = module
        self.order = []

    def _create(self, module):
        # 1. Red
        if isinstance(module, NetworkFactoryModule):
            self.order.append(module.build())
            return module.outputs()

        # 2. Servidor
        if isinstance(module, ServerFactoryModule):
            net_out = self._create(NetworkFactoryModule())
            module.depends = net_out
            self.order.append(module.build())
            return module.outputs()

        # 3. Firewall
        if isinstance(module, FirewallFactoryModule):
            srv_out = self._create(ServerFactoryModule(self._create(NetworkFactoryModule())))
            module.depends = srv_out
            self.order.append(module.build())
            return module.outputs()

        # 4. Load Balancer (NUEVO)
        if isinstance(module, LoadBalancerFactoryModule):
            srv_out = self._create(ServerFactoryModule(self._create(NetworkFactoryModule())))
            module.depends = srv_out
            self.order.append(module.build())
            return module.outputs()

        # Fallback
        self.order.append(module.build())
        return module.outputs()

    def build(self):
        self._create(self.module)
        merged = {"terraform": {"required_providers": {}}, "resource": {}}
        for block in self.order:
            for res_type, res_defs in block["resource"].items():
                merged_resources = merged["resource"].setdefault(res_type, {})
                merged_resources.update(res_defs)
        return merged

if __name__ == "__main__":
    # Solicitamos LoadBalancer en lugar de Firewall
    mediator = Mediator(LoadBalancerFactoryModule())
    cfg = mediator.build()
    with open("main.tf.json", "w") as f:
        json.dump(cfg, f, indent=2)
    print("EXITO: main.tf.json generado con LoadBalancer.")
