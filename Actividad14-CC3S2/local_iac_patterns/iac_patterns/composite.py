"""Patrón Composite
Permite tratar múltiples recursos Terraform como una única unidad lógica o módulo compuesto.
"""

from __future__ import annotations

from typing import Any, Dict, List

TerraformJSON = Dict[str, Any]


class CompositeModule:
    """
    Agrega múltiples diccionarios Terraform JSON como un módulo lógico único.
    """

    def __init__(self) -> None:
        self._children: List[TerraformJSON] = []

    def add(self, resource_dict: TerraformJSON) -> None:
        """
        Agrega un hijo (Terraform JSON parcial o completo).
        """
        self._children.append(resource_dict)

    def export(self) -> TerraformJSON:
        """
        Compat: exporta recursos combinados bajo "resource".
        """
        aggregated: TerraformJSON = {"resource": []}
        for child in self._children:
            aggregated["resource"].extend(child.get("resource", []))
        return aggregated

    def execute_all(self) -> TerraformJSON:
        """
        Requerido por el ejercicio: combina todos los hijos en un único Terraform JSON.
        - Une "resource" de todos los hijos.
        - Si algún hijo trae bloque "terraform" (p.ej. required_providers), lo mergea.
        """
        aggregated: TerraformJSON = {"resource": []}
        tf0: Dict[str, Any] = {}
        tf_enabled = False

        for child in self._children:
            # merge resources
            aggregated["resource"].extend(child.get("resource", []))

            # merge terraform blocks si existen (opcional)
            tf_blocks = child.get("terraform")
            if isinstance(tf_blocks, list) and tf_blocks:
                tf_enabled = True
                child_tf0 = tf_blocks[0] if isinstance(tf_blocks[0], dict) else {}
                for k, v in child_tf0.items():
                    if k == "required_providers" and isinstance(v, dict):
                        rp = tf0.setdefault("required_providers", {})
                        # child override si hay colisión
                        rp.update(v)
                    else:
                        tf0.setdefault(k, v)

        if tf_enabled:
            aggregated["terraform"] = [tf0]

        return aggregated

