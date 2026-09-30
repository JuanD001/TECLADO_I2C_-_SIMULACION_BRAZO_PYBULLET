# ================================================================
# Actividad 6 - Punto 1  |  ESP32 + MicroPython (Thonny)
# Teclado matricial 4x4 + OLED I2C -> brazo dibujando en PyBullet
# ================================================================
from machine import Pin, I2C
import sys
import select
import time
import ssd1306

# ---------------- OLED I2C (SSD1306) ----------------
# Resolución estándar de 128x64 píxeles.
ANCHO_OLED = 128
ALTO_OLED = 64

class _SinOLED:
    def fill(self, c): pass
    def text(self, t, x, y): pass
    def show(self): pass

try:
    i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
    print("I2C encontrado en:", [hex(d) for d in i2c.scan()])
    oled = ssd1306.SSD1306_I2C(ANCHO_OLED, ALTO_OLED, i2c)
except Exception as e:
    print("AVISO: OLED no responde (revisa VCC=3.3V, GND, SDA=21, SCL=22):", e)
    oled = _SinOLED()

led = Pin(2, Pin.OUT)

# ---------------- TECLADO 4x4 ----------------
TECLAS = (
    ("1", "2", "3", "A"),
    ("4", "5", "6", "B"),
    ("7", "8", "9", "C"),
    ("*", "0", "#", "D"),
)
FILAS = [Pin(n, Pin.OUT, value=1) for n in (13, 14, 27, 26)]
COLUMNAS = [Pin(n, Pin.IN, Pin.PULL_UP) for n in (25, 33, 32, 23)]

def escanear():
    for f, fila in enumerate(FILAS):
        fila.value(0)
        time.sleep_us(5)
        for c, col in enumerate(COLUMNAS):
            if col.value() == 0:
                fila.value(1)
                return TECLAS[f][c]
        fila.value(1)
    return None

# ---------------- COMUNICACIÓN CON EL PC ----------------
lector = select.poll()
lector.register(sys.stdin, select.POLLIN)
buffer_pc = ""

def leer_pc():
    global buffer_pc
    while lector.poll(0):
        ch = sys.stdin.read(1)
        if ch in ("\n", "\r"):
            if buffer_pc:
                linea, buffer_pc = buffer_pc, ""
                return linea
        else:
            buffer_pc += ch
    return None

# ---------------- PROGRAMA PRINCIPAL ----------------
MAX_CIFRAS = 4
numero = ""
ultima = None
ANTIRREBOTE_MS = 30

txt_numero = ""
txt_estado = ""

def refrescar_pantalla():
    """Limpia el OLED y reescribe las dos líneas de texto actualizadas"""
    oled.fill(0) # Fondo negro
    oled.text(txt_numero, 0, 15)  # Escribe en la parte superior
    oled.text(txt_estado, 0, 35)  # Escribe en la parte inferior
    oled.show()

def mostrar_numero():
    global txt_numero
    txt_numero = "Numero: " + numero + ("_" if len(numero) < MAX_CIFRAS else "")
    refrescar_pantalla()

def estado(texto):
    global txt_estado
    txt_estado = texto[:16] # Limita a 16 caracteres para que quepa en la pantalla
    refrescar_pantalla()

mostrar_numero()
estado("#=Dibujar *=Borr")
print("ESP32 lista: teclado + OLED")

while True:
    tecla = escanear()

    if tecla is not None and tecla != ultima:
        time.sleep_ms(ANTIRREBOTE_MS)
        if escanear() == tecla:
            print("TECLA:" + tecla)
            led.value(1)
            time.sleep_ms(40)
            led.value(0)
            
            if tecla.isdigit():
                if len(numero) < MAX_CIFRAS:
                    numero += tecla
                    mostrar_numero()
                else:
                    estado("Max 4 cifras")
            elif tecla == "*":
                numero = numero[:-1]
                mostrar_numero()
            elif tecla == "#":
                if numero:
                    print("NUM:" + numero)
                    estado("Enviado: " + numero)
                    numero = ""
                    mostrar_numero()
                else:
                    estado("Escribe un num.")
            elif tecla == "A":
                print("CMD:A")
                estado("Repitiendo...")
            elif tecla == "B":
                print("CMD:B")
                estado("Borrando pizarra")
            elif tecla == "C":
                print("CMD:C")
                estado("Brazo a home")
            elif tecla == "D":
                numero = ""
                mostrar_numero()
                estado("#=Dibujar *=Borr")
    ultima = tecla

    msg = leer_pc()
    if msg and msg.startswith("LCD:"):
        estado(msg[4:])

    time.sleep_ms(10)