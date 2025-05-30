# Analizador Léxico en Python

**Universidad Técnica Particular de Loja**  
**Teoría de autómatas y compiladores**  
**Por:** Oliver Roberto Saraguro Remache  
**Fecha:** 16 de mayo del 2025  
**Docente:** Ing. Torres Diaz Juan Carlos

---

## 1. Analizador léxico en Python

Este proyecto consiste en la construcción de un analizador léxico programado en Python. Su función es leer un archivo de texto con código fuente en un lenguaje definido, identificar los distintos tokens válidos e inválidos, clasificarlos según su tipo, y generar una tabla de resultados que incluye:

- Tipo de token  
- Lexema identificado  
- Línea del archivo  
- Validez léxica (✅ válido / ❌ inválido)

Además, el programa reporta si el archivo fue cargado correctamente y genera una tabla final con todos los tokens reconocidos.

### 1.1 Programa funcional con lectura de archivo fuente

El analizador incluye las siguientes características:

- Lectura de un archivo `.txt` fuente.
- Identificación de tokens como: palabras reservadas, identificadores, números, operadores, agrupadores, separadores, comentarios, etc.
- Detección de errores léxicos.
- Clasificación automática con estados de un autómata finito.
- Tabla final con los resultados organizados.

🔗 Enlace al repositorio de GitHub: (coloca aquí el link al repositorio)

---

## 2. Documentación

### 2.1 Definición del lenguaje

El lenguaje procesado por el analizador léxico ha sido diseñado de forma propia para este proyecto. Su propósito es simular una estructura lógica y sintáctica básica similar a los lenguajes de programación tradicionales, pero con características particulares definidas por el desarrollador. Este lenguaje es utilizado para fines académicos y experimentales en el análisis léxico y compilación.

#### 2.1.1 Estructura de los programas que acepta

- Comentarios de línea (que inician con `$`)
- Declaraciones de variables
- Condiciones con operadores lógicos y relacionales
- Bloques de control como `if` y `else`
- Operaciones aritméticas
- Invocaciones a funciones como `print()`
- Manejo básico de errores léxicos

#### 2.1.2 Instrucciones que reconoce

| Categoría             | Elementos reconocidos                                    |
|-----------------------|----------------------------------------------------------|
| Tipos de datos        | `int`, `float`, `bool`, `char`, `string`, `double`, `long` |
| Palabras reservadas   | `if`, `else`, `while`, `print`, `not`, `and`, `or`, `true`, `false` |
| Operadores aritméticos | `+`, `-`, `*`, `/`                                       |
| Operadores relacionales | `==`, `!=`, `>`, `<`, `>=`, `<=`                         |
| Operadores lógicos    | `and`, `or`, `not`, `&&`, `||`                            |
| Separadores           | `,`, `;`, `"`                                             |
| Agrupadores           | `(`, `)`, `{`, `}`, `[`, `]`                              |
| Identificadores       | Comienzan con letra, seguidos por letras, números, `_` o `.`. (No inician con números) |
| Literales numéricos   | Enteros y decimales (ej: `.99`, `123.`, `10.5`)           |
| Literales string      | Texto entre comillas dobles `"texto"`                    |
| Comentarios           | Inician con `$` y terminan al final de la línea          |

#### 2.1.3 Sintaxis de cada instrucción

**Declaración de variables:**

### Sintaxis
```
    tipo nombre_variable = valor

    # Ejemplo
    int numero = 10
```

### Condiciónales
```
if condición
    instrucción
else
    instrucción
```
### Operaciones aritméticas y lógicas
```
resultado = (numero * 2 + 5 - 3) / 2
```
### Ciclos
```
while condición
    instrucción
```
### Comentarios
```
$ Esto es un comentario
```

## Automata grafico
<img width="442" alt="image" src="https://github.com/user-attachments/assets/361ae1d7-e65e-45f4-821a-a4bef3da6e24" />

## Tabla de transiciones del autómata

| ORIGEN | SÍMBOLO              | DESTINO | TOKEN FINAL                       |
|--------|----------------------|---------|-----------------------------------|
| 0      | L                    | 1       |                                   |
| 1      | L                    | 1       |                                   |
| 1      | N                    | 1       |                                   |
| 1      | ESPACIO              | 0       | IDENTIFICADORES                   |
| 0      | (,),[,],{,}          | 2       |                                   |
| 2      | ESPACIO              | 0       |                                   |
| 0      | N                    | 3       |                                   |
| 3      | N                    | 3       |                                   |
| 3      | ESPACIO              | 0       | AGRUPADORES                       |
| 3      | .                    | 6       |                                   |
| 6      | N                    | 5       |                                   |
| 5      | N                    | 5       |                                   |
| 5      | ESPACIO              | 0       |                                   |
| 0      | .                    | 4       |                                   |
| 4      | N                    | 5       |                                   |
| 5      | N                    | 5       |                                   |
| 5      | ESPACIO              | 0       | NÚMEROS ENTEROS Y DECIMALES      |
| 0      | >, <, =, !           | 7       |                                   |
| 7      | ESPACIO              | 0       |                                   |
| 7      | =                    | 8       |                                   |
| 8      | ESPACIO              | 0       | COMPARADORES                      |
| 0      | ., ,, "              | 9       |                                   |
| 9      | ESPACIO              | 0       | SEPARADORES                       |
| 0      | +, -, *, /           | 10      |                                   |
| 10     | ESPACIO              | 0       |                                   |
| 10     | =                    | 11      |                                   |
| 11     | ESPACIO              | 0       | OPERADORES                        |
| 0      | &                    | 12      |                                   |
| 12     | &                    | 13      |                                   |
| 13     | ESPACIO              | 0       | OPERADORES LÓGICOS                |
| 0      | \|                   | 14      |                                   |
| 14     | \|                   | 15      |                                   |
| 15     | ESPACIO              | 0       | OPERADORES LÓGICOS                |
| 0      | $                    | 16      |                                   |
| 16     | /n                   | 0       | COMENTARIO                        |

## Palabras reservadas del lenguaje

| Palabra     | Uso principal                                     | Categoría             |
|-------------|---------------------------------------------------|------------------------|
| if          | Condición                                         | Control de flujo       |
| else        | Alternativa a if                                  | Control de flujo       |
| while       | Bucle con condición al inicio                     | Control de flujo       |
| for         | Bucle con contador                                | Control de flujo       |
| do          | Bucle do-while                                    | Control de flujo       |
| break       | Salir de un bucle                                 | Control de flujo       |
| continue    | Saltar a la siguiente iteración del bucle         | Control de flujo       |
| return      | Salida de una función                             | Control de flujo       |
| switch      | Selección múltiple                                | Control de flujo       |
| case        | Opción en switch                                  | Control de flujo       |
| try         | Bloque para excepciones                           | Manejo de errores      |
| int         | Tipo de dato entero                               | Tipos de datos         |
| float       | Tipo de dato decimal                              | Tipos de datos         |
| char        | Tipo de dato carácter                             | Tipos de datos         |
| bool        | Tipo de dato booleano                             | Tipos de datos         |
| string      | Tipo de dato texto                                | Tipos de datos         |
| AND / OR    | Operadores lógicos                                | Operadores lógicos     |
| \|\| / \&\& | Operadores lógicos                                | Operadores lógicos     |



