# Actividad 4 – CLI Unix para DevSecOps

> Curso: CC3S2 – Desarrollo de Software
> Entorno principal: Ubuntu en WSL (Windows)

## Objetivo

Laboratorio práctico de CLI en Unix-like con enfoque DevSecOps: navegación, pipes/redirecciones/globbing, utilidades de texto y tratamiento seguro de evidencias (redacción de secretos).

---

## Estructura del repo (parcial)

Ruta de trabajo:
`~/CC3S2-desarrollo-software/desarrollo-de-software/Actividad4-CC3S2/lab-cli`

Contenido actual (confirmado):

```
lab-cli/
├─ etc_lista.txt
└─ evidencias/
   └─ sesion_redactada.txt
```

> Nota: El archivo `evidencias/sesion.txt` (sesión sin redactar) **no se incluye** en el repo para evitar exponer datos.

---

## Sección 1 – Manejo sólido de CLI (realizado)

### Comandos clave ejecutados

* **Navegación y listados**

  ```bash
  pwd
  ls -l
  ls -a
  cd /etc; ls -a > ~/CC3S2-desarrollo-software/desarrollo-de-software/Actividad4-CC3S2/lab-cli/etc_lista.txt
  ```

* **Globbing / conteos (enunciado)**

  ```bash
  # Ejemplo robusto (referencia del enunciado)
  find /tmp -maxdepth 1 -type f \( -name '*.txt' -o -name '*.doc' \) | wc -l
  ```

* **Pipes y redirecciones (enunciado)**

  ```bash
  ls | wc -l
  ls > lista.txt     # (no se guardó en el dir actual finalmente; ver Nota)
  printf "Hola\n" >> lista.txt
  ls noexiste 2> errores.txt
  ```

  **Nota**: Hubo intentos fuera de la carpeta correcta (`~/lab-cli` vs `.../Actividad4-CC3S2/lab-cli`), por eso algunos archivos (p. ej. `lista.txt`, `errores.txt`) no quedaron en el directorio final. Se mantuvo únicamente lo confirmado.

* **Buenas prácticas de seguridad (referenciadas)**

  * `--` para fin de argumentos.
  * `-print0 | xargs -0` para nombres con espacios.
  * “dry-run” anteponiendo `echo`.

**Archivo generado (confirmado):** `etc_lista.txt`.

---

## Sección 2 – Administración básica (**PENDIENTE**)

> Esta sección (usuarios/grupos/permisos, procesos/señales, systemd y journalctl) queda pendiente a propósito.
> Se agregará evidencia y comandos una vez completada.

---

## Sección 3 – Utilidades de texto (parcial)

> Se siguió el marco teórico y se dejaron listos los comandos de referencia del enunciado. La evidencia concreta de esta sección se agregará al finalizar (p. ej. `mayus.txt`, `usuarios.txt`, `lista_conf.txt`).

Comandos de referencia:

```bash
# grep / sed / awk / cut / sort / uniq / tr / tee / find
grep root /etc/passwd
sed 's/viejo/nuevo/' archivo
awk -F: '{print $1}' /etc/passwd | sort | uniq
cut -d: -f1 /etc/passwd
printf "hola\n" | tr 'a-z' 'A-Z' | tee mayus.txt
find /tmp -mtime -5 -type f
ls /etc | grep conf | sort | tee lista_conf.txt | wc -l
```

---

## Redacción de evidencias (hecho) ✅

Para proteger secretos en `evidencias/sesion.txt`, se aplicó un pipeline de **redacción**.
Se generó `evidencias/sesion_redactada.txt` y se verificó que **no queden** credenciales.

**Ruta de ejecución:** `~/CC3S2-desarrollo-software/desarrollo-de-software/Actividad4-CC3S2/lab-cli`

### 1) Redactar palabras sensibles y pares `clave=valor` / `clave: valor`

```bash
sed -E \
  -e 's/(password|token|secret|api[-_]?key)/[REDACTED]/gI' \
  -e 's/\b(pass(word)?|token|secret|api[-_]?key)\b[[:space:]]*[:=][[:space:]]*[^[:space:];"]+/\1: [REDACTED]/gI' \
  evidencias/sesion.txt > evidencias/sesion_redactada.txt
```

### 2) Ocultar `Authorization: Basic/Bearer`

```bash
sed -E 's/\b(Authorization:)[[:space:]]+(Basic|Bearer)[[:space:]]+[A-Za-z0-9._~+\/=-]+/\1 \2 [REDACTED]/gI' \
  evidencias/sesion_redactada.txt > evidencias/sesion_redactada.tmp && \
  mv evidencias/sesion_redactada.tmp evidencias/sesion_redactada.txt
```

### 3) Extras de protección (preparados)

```bash
# user:pass@host en URLs
sed -E 's#https?://([^:/@]+):([^@]+)@#https://\1:[REDACTED]@#gI' \
  evidencias/sesion_redactada.txt > evidencias/sesion_redactada.tmp && mv evidencias/sesion_redactada.tmp evidencias/sesion_redactada.txt

# ?token= / ?access_token= / ?api_key=
sed -E 's/([?&](access_)?token|[?&]api[-_]?key)=([^&[:space:]]+)/\1=[REDACTED]/gI' \
  evidencias/sesion_redactada.txt > evidencias/sesion_redactada.tmp && mv evidencias/sesion_redactada.tmp evidencias/sesion_redactada.txt

# Cookies
sed -E 's/\b(Set-)?Cookie:[[:space:]]*[^;[:space:]]+=([^;]+)(;?)/Cookie: [REDACTED]\3/gI' \
  evidencias/sesion_redactada.txt > evidencias/sesion_redactada.tmp && mv evidencias/sesion_redactada.tmp evidencias/sesion_redactada.txt

# Bloques de llaves privadas (si existieran)
sed -E '/-----BEGIN (OPENSSH )?PRIVATE KEY-----/,/-----END (OPENSSH )?PRIVATE KEY-----/c\[REDACTED PRIVATE KEY BLOCK\]' \
  evidencias/sesion_redactada.txt > evidencias/sesion_redactada.tmp && mv evidencias/sesion_redactada.tmp evidencias/sesion_redactada.txt
```

### 4) (Opcional) Quitar códigos ANSI

```bash
sed -E 's/\x1B\[[0-9;]*[A-Za-z]//g' \
  evidencias/sesion_redactada.txt > evidencias/sesion_redactada.tmp && \
  mv evidencias/sesion_redactada.tmp evidencias/sesion_redactada.txt
```

### Verificación (resultado: **sin hallazgos**)

```bash
grep -nEi '(pass(word)?|token|secret|api[-_]?key|authorization|cookie)[[:space:]]*[:=]' evidencias/sesion_redactada.txt \
  | grep -vi '\[REDACTED\]' \
  | grep -viE 'sed -E| grep ' \
  | grep -viE '^\s*#' \
  | head
# (no imprime resultados no redactados)
```

> Interpretación: No quedaron entradas sin redactar de `password|pass|token|secret|api[-_]?key|authorization|cookie` seguidas de `:` o `=`.

---

## Entregables (estado actual)

* ✅ `evidencias/sesion_redactada.txt` (versión segura para la entrega)
* ✅ `etc_lista.txt`
* ⏳ **PENDIENTE**: Archivos de Sección 2 (usuarios/procesos/systemd o fallbacks) y mini-pipeline de auditoría.
* ⏳ **PENDIENTE**: Evidencias de Sección 3 (p. ej. `mayus.txt`, `usuarios.txt`, `lista_conf.txt`), cuando se ejecute todo en el directorio correcto.

---

## Notas de seguridad

* Se eliminan/ocultan credenciales en: `Authorization` (Basic/Bearer), tokens/keys en parámetros de URL, cookies y posibles bloques de claves privadas.
* No se publican archivos sin redactar.
* Se incluye solo un fragmento representativo de `sudo -l` cuando corresponda (no aplicado aún).

---



