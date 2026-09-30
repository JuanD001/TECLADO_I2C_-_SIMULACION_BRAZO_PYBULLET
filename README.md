# Brazo Robótico en PyBullet Controlado por ESP32 🤖🖊️

Este proyecto integra hardware (ESP32) y software de simulación (PyBullet) para controlar un brazo robótico capaz de escribir números en una pizarra virtual. Mediante un teclado matricial 4x4 y una pantalla OLED SH1106, el usuario ingresa un número, la ESP32 lo procesa y lo envía por puerto Serial a un script en Python. 

El script utiliza OpenCV para extraer los contornos del texto y cinemática inversa para que el modelo URDF del brazo dibuje el trayecto exacto en la simulación.

## 🎥 Demostración
<!-- Reemplaza TU_ENLACE_DE_YOUTUBE por el ID de tu video -->
[![Demostración del Proyecto](https://img.youtube.com/vi/TU_ENLACE_DE_YOUTUBE/0.jpg)](https://www.youtube.com/watch?v=TU_ENLACE_DE_YOUTUBE)

## 📸 Montaje Físico
![Montaje del Circuito](ruta_de_tu_imagen.jpg)

---

## 🛠️ Requisitos de Hardware

* **Microcontrolador:** ESP32 (ej. DOIT DevKit V1).
* **Pantalla:** OLED I2C de 1.3" (Controlador SH1106, 4 pines: VCC, GND, SDA, SCK).
* **Teclado:** Matricial 4x4 de membrana.
* Cables jumper y protoboard.

### Esquema de Conexiones

| Componente | Pin Físico | Pin ESP32 | Notas |
| :--- | :--- | :--- | :--- |
| **OLED SH1106** | VCC | 3.3V | Alimentación |
| **OLED SH1106** | GND | GND | Tierra |
| **OLED SH1106** | SDA | GPIO 21 | Bus I2C de datos |
| **OLED SH1106** | SCK / SCL | GPIO 22 | Bus I2C de reloj |
| **Teclado 4x4** | Filas (F1-F4)| GPIO 13, 14, 27, 26 | Salidas digitales |
| **Teclado 4x4** | Colum (C1-C4)| GPIO 25, 33, 32, 23 | Entradas con Pull-up |

---

## 💻 Códigos y Configuración (Software)

### 1. Entorno de la ESP32 (C++ / PlatformIO)
Para configurar la ESP32, crea un proyecto en **PlatformIO** (VS Code) y utiliza los siguientes archivos:

**`platformio.ini`** (Configuración de dependencias)
```ini
[env:esp32doit-devkit-v1]
platform = espressif32
board = esp32doit-devkit-v1
framework = arduino
monitor_speed = 115200
lib_deps = 
    adafruit/Adafruit SH110X @ ^2.1.8
    adafruit/Adafruit GFX Library @ ^1.11.5
    chris--a/Keypad @ ^3.1.1
