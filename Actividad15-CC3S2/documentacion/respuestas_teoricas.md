# Respuestas Teóricas - Actividad 15

## 1. Idempotencia y Mediador
**Pregunta:** Define idempotencia y por qué es fundamental para el mediador.
**Respuesta:** La idempotencia garantiza que ejecutar una operación múltiples veces produzca el mismo resultado que ejecutarla una sola vez. En nuestro Mediador (), esto es crucial porque el script regenera el archivo `main.tf.json` completo en cada ejecución. Si el Mediador no fuera determinista (idempotente), Terraform detectaría cambios falsos (drifts) constantemente, destruyendo y recreando infraestructura innecesariamente. Delegamos la gestión del estado a Terraform, pero la generación del JSON debe ser siempre consistente para los mismos inputs.

## 2. Comparativa: Mediador vs Graph-Driven nativo
**Ventajas del Mediador (Python):**
1. **Lógica condicional compleja:** Permite usar estructuras de control de Python (, , recursividad) que en HCL (HashiCorp Configuration Language) son limitadas o verbosas. Ejemplo: Nuestro `_create` decide dinámicamente si inyectar un Load Balancer o un Firewall.
2. **Abstracción:** Oculta la complejidad de las dependencias () al usuario final. El usuario solo pide "LoadBalancer" y el mediador resuelve que necesita "Server" y "Network".

**Desventajas:**
1. **Opacidad:** Terraform pierde visibilidad del grafo real hasta que el JSON es generado. El comando `terraform graph` solo ve el resultado final, no la lógica de construcción.
2. **Mantenimiento:** Requiere mantener dos bases de código: los scripts de Python y los recursos de Terraform.

## 3. Extensibilidad (Caso Load Balancer)
Para el ejercicio práctico, extendimos el mediador agregando `LoadBalancerFactoryModule`.
- **Patrón:** Se utilizó el mismo patrón de inyección.
- **Dependencia:** Se definió que el balanceador depende estrictamente del `null_resource.server`.
- **Implementación:** Se modificó `main.py` para detectar la instancia de `LoadBalancerFactoryModule`, forzar la creación previa del servidor (y su red), y enlazar la dependencia mediante triggers.

## REspuestas:

## 1. Idempotencia y Mediador
**Pregunta:** Define idempotencia y por qué es fundamental para el mediador.
**Respuesta:** La idempotencia garantiza que ejecutar una operación múltiples veces produzca el mismo resultado que ejecutarla una sola vez. En nuestro Mediador (`main.py`), esto es crucial porque el script regenera el archivo \`main.tf.json\` completo en cada ejecución. Si el Mediador no fuera determinista (idempotente), Terraform detectaría cambios falsos (drifts) constantemente, destruyendo y recreando infraestructura innecesariamente. Delegamos la gestión del estado a Terraform, pero la generación del JSON debe ser siempre consistente para los mismos inputs.

## 2. Comparativa: Mediador vs Graph-Driven nativo
**Ventajas del Mediador (Python):**
1. **Lógica condicional compleja:** Permite usar estructuras de control de Python (`if`, `for`, recursividad) que en HCL (HashiCorp Configuration Language) son limitadas o verbosas. Ejemplo: Nuestro \`_create\` decide dinámicamente si inyectar un Load Balancer o un Firewall.
2. **Abstracción:** Oculta la complejidad de las dependencias (`depends_on`) al usuario final. El usuario solo pide "LoadBalancer" y el mediador resuelve que necesita "Server" y "Network".

**Desventajas:**
1. **Opacidad:** Terraform pierde visibilidad del grafo real hasta que el JSON es generado. El comando \`terraform graph\` solo ve el resultado final, no la lógica de construcción.
2. **Mantenimiento:** Requiere mantener dos bases de código: los scripts de Python y los recursos de Terraform.

## 3. Extensibilidad (Caso Load Balancer)
Para el ejercicio práctico, extendimos el mediador agregando \`LoadBalancerFactoryModule\`.
- **Patrón:** Se utilizó el mismo patrón de inyección.
- **Dependencia:** Se definió que el balanceador depende estrictamente del \`null_resource.server\`.
- **Implementación:** Se modificó \`main.py\` para detectar la instancia de \`LoadBalancerFactoryModule\`, forzar la creación previa del servidor (y su red), y enlazar la dependencia mediante triggers.
