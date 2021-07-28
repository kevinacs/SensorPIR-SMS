import network
import time
import urequests
from machine import Pin
from time import sleep


# FUNCIÓN PARA ESTABLECER LA CONEXIÓN WIFI (STATION)
def conectaWifi(red, password):
    global miRed
    miRed = network.WLAN(network.STA_IF)
    if not miRed.isconnected():  # Si no está conectado…
        miRed.active(True)  # activa la interface
        miRed.connect("Kevin", "Ytre456.")  # Intenta conectar con la red
        print('Conectando a la red', red + "…")
        timeout = time.time()
        while not miRed.isconnected():  # Mientras no se conecte..
            if (time.ticks_diff(time.time(), timeout) > 10):
                return False
    return True


if conectaWifi("Kevin", "Ytre456."):
    print("Conexión exitosa")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    url = "https://maker.ifttt.com/trigger/sendEmail1/with/key/57SSaU7yns8F3zlTfAZ9Q"

    motion = False


    def handle_interrupt(pin):
        global motion
        motion = True
        global interrupt_pin
        interrupt_pin = pin


    led = Pin(15, Pin.OUT)
    pir = Pin(16, Pin.IN)

    pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

    while True:
        if motion:
            print('Movimiento detectado desde:', interrupt_pin)
            led.value(1)
            sleep(3)
            led.value(0)
            print('Movimiento detenido!')
            motion = False
            respuesta = urequests.get(url)
            print(respuesta.text)
            print(respuesta.status_code)
            respuesta.close()
            time.sleep(5)

else:
    print("Imposible conectar")
    miRed.active(False)