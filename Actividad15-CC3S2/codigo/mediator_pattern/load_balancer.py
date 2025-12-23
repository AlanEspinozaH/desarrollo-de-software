from dependency import DependsOn

class LoadBalancerFactoryModule:
    def __init__(self, depends=None):
        self.depends = depends

    def build(self):
        triggers = {"name": "hello-world-lb"}
        # Si se le pasa una dependencia (ej. server), la registramos en Terraform
        if self.depends:
            triggers["depends_on"] = f"{self.depends.resource_type}.{self.depends.resource_id}"
        
        return {
            "resource": {
                "null_resource": {
                    "load_balancer": {"triggers": triggers}
                }
            }
        }

    def outputs(self):
        return DependsOn("null_resource", "load_balancer", {"name": "hello-world-lb"})
