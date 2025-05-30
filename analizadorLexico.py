import pandas as pd

class AutomataProgramado:
    def __init__(self, file_path):
        self.estado_actual = 0
        self.buffer = ""
        self.palabras_reservadas = {
            'if', 'else', 'while', 'for', 'do', 'break', 'continue', 'return', 
            'switch', 'case', 'try', 'int', 'float', 'char', 'bool', 'string',
            'and', 'or'
        }
        self.tokens = []  # Lista para almacenar los resultados
        self.cargar_archivo(file_path)
        
    def cargar_archivo(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.lineas = file.readlines()
            print("Archivo cargado exitosamente.")
        except FileNotFoundError:
            print("Error: Archivo no encontrado.")
            self.lineas = []

    def analizar(self):
        if not self.lineas:
            print("No hay contenido para analizar.")
            return

        for numero_linea, linea in enumerate(self.lineas, start=1):
            self.estado_actual = 0
            self.buffer = ""
            i = 0
            n = len(linea)

            while i < n:
                char = linea[i]

                if self.estado_actual == 0:
                    if char.isalpha() or char == '_':
                        self.estado_actual = 1
                        self.buffer += char
                    elif char in '()[]{}':
                        self.agregar_token('AGRUPADOR', char, numero_linea)
                    elif char.isdigit():
                        self.estado_actual = 3
                        self.buffer += char
                    elif char == '.':
                        self.estado_actual = 4
                        self.buffer += char
                    elif char in '><=!':
                        self.estado_actual = 7
                        self.buffer += char
                    elif char in '.,;"':
                        self.agregar_token('SEPARADOR', char, numero_linea)
                    elif char in '+-*/':
                        self.agregar_token('OPERADOR', char, numero_linea)
                    elif char == '&':
                        self.estado_actual = 12
                        self.buffer += char
                    elif char == '|':
                        self.estado_actual = 14
                        self.buffer += char
                    elif char == '$':
                        self.estado_actual = 20
                        i += 1
                    elif char.isspace():
                        pass
                    else:
                        self.agregar_token('DESCONOCIDO', char, numero_linea)
                    i += 1

                elif self.estado_actual == 1:
                    if char.isalnum() or char == '_':
                        self.buffer += char
                        i += 1
                    else:
                        if self.buffer.lower() in self.palabras_reservadas:
                            categoria = self.obtener_categoria_palabra_reservada(self.buffer)
                            self.agregar_token(categoria, self.buffer, numero_linea)
                        else:
                            self.agregar_token('IDENTIFICADOR', self.buffer, numero_linea)
                        self.reset_automata()

                elif self.estado_actual == 3:
                    if char.isdigit():
                        self.buffer += char
                        i += 1
                    elif char == '.':
                        self.buffer += char
                        self.estado_actual = 5
                        i += 1
                    else:
                        self.agregar_token('NUMERO_ENTERO', self.buffer, numero_linea)
                        self.reset_automata()

                elif self.estado_actual == 4:
                    if char.isdigit():
                        self.buffer += char
                        self.estado_actual = 5
                        i += 1
                    else:
                        self.agregar_token('DESCONOCIDO', self.buffer, numero_linea)
                        self.reset_automata()

                elif self.estado_actual == 5:
                    if char.isdigit():
                        self.buffer += char
                        i += 1
                    else:
                        self.agregar_token('NUMERO_DECIMAL', self.buffer, numero_linea)
                        self.reset_automata()

                elif self.estado_actual == 7:
                    if char == '=':
                        self.buffer += char
                        self.agregar_token('COMPARADOR', self.buffer, numero_linea)
                        self.reset_automata()
                        i += 1
                    else:
                        self.agregar_token('COMPARADOR', self.buffer, numero_linea)
                        self.reset_automata()

                elif self.estado_actual == 12:
                    if char == '&':
                        self.buffer += char
                        self.agregar_token('OPERADOR_LOGICO', self.buffer, numero_linea)
                        self.reset_automata()
                        i += 1
                    else:
                        self.agregar_token('DESCONOCIDO', self.buffer, numero_linea)
                        self.reset_automata()

                elif self.estado_actual == 14:
                    if char == '|':
                        self.buffer += char
                        self.agregar_token('OPERADOR_LOGICO', self.buffer, numero_linea)
                        self.reset_automata()
                        i += 1
                    else:
                        self.agregar_token('DESCONOCIDO', self.buffer, numero_linea)
                        self.reset_automata()

                elif self.estado_actual == 20:  # Comentario hasta salto de línea
                    self.buffer += char
                    i += 1

            # Fin de línea
            if self.estado_actual == 1:
                if self.buffer.lower() in self.palabras_reservadas:
                    categoria = self.obtener_categoria_palabra_reservada(self.buffer)
                    self.agregar_token(categoria, self.buffer, numero_linea)
                else:
                    self.agregar_token('IDENTIFICADOR', self.buffer, numero_linea)
            elif self.estado_actual == 3:
                self.agregar_token('NUMERO_ENTERO', self.buffer, numero_linea)
            elif self.estado_actual == 5:
                self.agregar_token('NUMERO_DECIMAL', self.buffer, numero_linea)
            elif self.estado_actual == 20 and self.buffer:
                self.agregar_token('COMENTARIO', self.buffer.strip(), numero_linea)
            elif self.estado_actual in (7, 12, 14):
                self.agregar_token('DESCONOCIDO', self.buffer, numero_linea)

            self.reset_automata()
        
        # Mostrar tabla completa sin truncar
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.width', None)


        # Mostrar tabla
        df = pd.DataFrame(self.tokens, columns=["TIPO", "LEXEMA", "LINEA"])
        # Nueva columna VALIDACION
        df["VALIDO"] = df["TIPO"].apply(lambda tipo: "✅" if tipo != "DESCONOCIDO" else "❌")

        print("\nTabla de tokens reconocidos:\n")
        print(df)

    def reset_automata(self):
        self.estado_actual = 0
        self.buffer = ""

    def agregar_token(self, tipo, lexema, linea):
        self.tokens.append({"TIPO": tipo, "LEXEMA": lexema, "LINEA": linea })

    def obtener_categoria_palabra_reservada(self, palabra):
        palabra_lower = palabra.lower()
        if palabra_lower in {'if', 'else', 'while', 'for', 'do', 'break', 'continue', 
                             'return', 'switch', 'case', 'try'}:
            return 'CONTROL_FLUJO'
        elif palabra_lower in {'int', 'float', 'char', 'bool', 'string'}:
            return 'TIPO_DATO'
        elif palabra_lower in {'and', 'or'}:
            return 'OPERADOR_LOGICO'
        else:
            return 'PALABRA_RESERVADA'

# Ejecutar
if __name__ == "__main__":
    ruta_archivo = "/Users/oliversaraguro/Downloads/archivoPrueba.txt"
    automata = AutomataProgramado(ruta_archivo)
    automata.analizar()
