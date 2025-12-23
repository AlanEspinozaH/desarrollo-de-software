"""Patrón Prototype

Permite clonar objetos (estructuras Terraform JSON) y modificarlos de forma controlada,
sin alterar el original.

Este módulo ofrece dos formas de aplicar Prototype:

1) OO: ResourcePrototype (encapsula un dict y permite clone(mutator)).
2) Funcional: clone_config(base, mutator) y mutator_add_local_file(cfg, ...).
"""

from __future__ import annotations

import copy
from typing import Any, Callable, Dict, Optional

TerraformJSON = Dict[str, Any]
Mutator = Callable[[TerraformJSON], None]


class ResourcePrototype:
    """
    Prototipo de recurso Terraform (dict) que puede clonarse y modificarse
    de forma independiente (deep copy), siguiendo el patrón Prototype.
    """

    def __init__(self, resource_dict: TerraformJSON) -> None:
        """
        Inicializa el prototipo con un diccionario base.

        Args:
            resource_dict: Estructura dict que representa una configuración o recurso Terraform JSON.
        """
        self._resource_dict: TerraformJSON = resource_dict

    def clone(self, mutator: Optional[Mutator] = None) -> "ResourcePrototype":
        """
        Clona el objeto aplicando una mutación opcional sobre el clon.

        Args:
            mutator: Función opcional que recibe el clon (dict) y puede modificarlo.

        Returns:
            Nuevo ResourcePrototype con el contenido clonado (y mutado si se indicó).
        """
        new_dict = copy.deepcopy(self._resource_dict)
        if mutator is not None:
            mutator(new_dict)
        return ResourcePrototype(new_dict)

    @property
    def data(self) -> TerraformJSON:
        """
        Acceso al dict almacenado.
        Nota: No es "solo lectura" a nivel Python (porque dict es mutable),
        pero se mantiene el principio de Prototype al clonar antes de mutar.
        """
        return self._resource_dict


def clone_config(base: TerraformJSON, mutator: Optional[Mutator] = None) -> TerraformJSON:
    """
    Clona (deep copy) una configuración Terraform JSON y aplica un mutator opcional.

    Args:
        base: Config Terraform JSON base.
        mutator: Función opcional para modificar el clon.

    Returns:
        Una nueva configuración (dict) clonada y posiblemente mutada.
    """
    cfg = copy.deepcopy(base)
    if mutator is not None:
        mutator(cfg)
    return cfg


def mutator_add_local_file(
    cfg: TerraformJSON,
    *,
    name: str = "welcome",
    filename: str = "${path.module}/welcome.txt",
    content: str = "Welcome from Prototype mutator\n",
) -> None:
    """
    Mutator de Prototype: agrega un recurso local_file al JSON de Terraform.
    """

    # Asegura bloque terraform[0]
    tf_blocks = cfg.setdefault("terraform", [])
    if not tf_blocks:
        tf_blocks.append({})

    # required_providers DEBE ser un objeto/dict (no lista)
    req = tf_blocks[0].setdefault("required_providers", {})

    # Cada provider entry debe ser un objeto (no lista)
    req.setdefault("null", {"source": "hashicorp/null"})
    req.setdefault("local", {"source": "hashicorp/local"})

    # Asegura estructura resource
    res_blocks = cfg.setdefault("resource", [])
    if not res_blocks:
        res_blocks.append({})

    res0 = res_blocks[0]
    local_list = res0.setdefault("local_file", [])
    if not local_list:
        local_list.append({})

    local_list[0][name] = [{"filename": filename, "content": content}]

