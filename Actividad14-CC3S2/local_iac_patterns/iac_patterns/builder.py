"""Patrón Builder
Construye de manera fluida configuraciones Terraform locales combinando los patrones
Factory, Prototype y Composite.

Ejercicio 2.5: build_group(prefix, size)
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict

from .composite import CompositeModule
from .factory import NullResourceFactory
from .prototype import ResourcePrototype

TerraformJSON = Dict[str, Any]


class InfrastructureBuilder:
    """Builder fluido que combina Factory, Prototype y Composite para crear módulos Terraform."""

    def __init__(self, env_name: str) -> None:
        self.env_name = env_name
        self._module = CompositeModule()

    def build_null_fleet(self, count: int = 5) -> "InfrastructureBuilder":
        """
        Construye una flota de null_resource clonados desde un prototipo base.
        Cada recurso recibe un trigger "index".
        """
        if count <= 0:
            raise ValueError("count debe ser > 0")

        base_proto = ResourcePrototype(NullResourceFactory.create("placeholder"))

        for i in range(count):
            def mutator(d: Dict[str, Any], idx: int = i) -> None:
                res_block = d["resource"][0]["null_resource"][0]
                original_name = next(iter(res_block.keys()))
                new_name = f"{original_name}_{idx}"
                res_block[new_name] = res_block.pop(original_name)

                # Asegura que triggers exista
                res_block[new_name][0].setdefault("triggers", {})
                res_block[new_name][0]["triggers"]["index"] = idx

            clone = base_proto.clone(mutator).data
            self._module.add(clone)

        return self

    def add_custom_resource(self, name: str, triggers: Dict[str, Any]) -> "InfrastructureBuilder":
        """Agrega un null_resource personalizado al módulo compuesto."""
        self._module.add(NullResourceFactory.create(name, triggers))
        return self

    def export(self, path: str) -> None:
        """Exporta el módulo compuesto a un archivo JSON compatible con Terraform."""
        data = self._module.export()

        dirpath = os.path.dirname(path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"[Builder] Terraform JSON escrito en: {path}")


def build_group(prefix: str, size: int) -> TerraformJSON:
    """
    Ejercicio 2.5 (Builder):
    Construye un grupo de `size` null_resource con nombres: prefix1..prefixN
    y retorna un Terraform JSON listo para serializar.
    """
    if size <= 0:
        raise ValueError("size debe ser > 0")

    cfg: TerraformJSON = {"resource": []}

    for i in range(1, size + 1):
        name = f"{prefix}{i}"
        cfg["resource"].extend(NullResourceFactory.create(name).get("resource", []))

    return cfg
