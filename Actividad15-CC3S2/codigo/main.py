# main.py (Versión Mediator Pattern)
import json
from dependency import DependsOn
from network import NetworkFactoryModule
from server import ServerFactoryModule
from firewall import FirewallFactoryModule
# Importamos el nuevo módulo que creaste
from load_balancer import LoadBalancerFactoryModule

class Mediator:
    def __init__(self, module):
        self.module = module
        self.order = []

    def _create(self, module):
        # 1. Crear red si es necesario
        if isinstance(module, NetworkFactoryModule):
            self.order.append(module.build())
            return module.outputs()

        # 2. Crear servidor si es necesario (depende de Network)
        if isinstance(module, ServerFactoryModule):
            net_out = self._create(NetworkFactoryModule())
            module.depends = net_out
            self.order.append(module.build())
            return module.outputs()

        # 3. Crear firewall si es necesario (depende de Server)
        if isinstance(module, FirewallFactoryModule):
            srv_out = self._create(ServerFactoryModule(self._create(NetworkFactoryModule())))
            module.depends = srv_out
            self.order.append(module.build())
            return module.outputs()

        # 4. (NUEVO) Crear Load Balancer si es necesario
        # Lógica: El LB depende del Servidor (Server -> LB)
        if isinstance(module, LoadBalancerFactoryModule):
            # Para crear un LB, necesitamos un Server primero.
            # Llamamos recursivamente a _create(Server...)
            srv_out = self._create(ServerFactoryModule(self._create(NetworkFactoryModule())))
            
            # Asignamos la dependencia y construimos
            module.depends = srv_out
            self.order.append(module.build())
            return module.outputs()

        # Módulo desconocido (fallback)
        self.order.append(module.build())
        return module.outputs()

    def build(self):
        # Inicia la creación recursiva empezando por el módulo inyectado
        self._create(self.module)
        
        # Estructura base de Terraform
        merged = {"terraform": {"required_providers": {}}, "resource": {}}
        
        # Unir todos los bloques generados en self.order
        for block in self.order:
            for res_type, res_defs in block["resource"].items():
                merged_resources = merged["resource"].setdefault(res_type, {})
                merged_resources.update(res_defs)
        return merged

if __name__ == "__main__":
    # INICIO DEL PROCESO:
    # Solicitamos un LoadBalancer. El mediador se encargará de crear
    # primero la Red, luego el Server y finalmente el LoadBalancer.
    mediator = Mediator(LoadBalancerFactoryModule())
    
    cfg = mediator.build()
    
    with open("main.tf.json", "w") as f:
        json.dump(cfg, f, indent=2)
        print("Archivo 'main.tf.json' generado correctamente con el patrón Mediator.")