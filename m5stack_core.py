
import machine
import ili934xnew

BUTTON_A_PIN = const(39)
BUTTON_B_PIN = const(38)
BUTTON_C_PIN = const(37)
SPEAKER_PIN  = const(25)

SPI_A_MISO_PIN = const(19)
SPI_A_MOSI_PIN = const(23)
SPI_A_CLK_PIN = const(18)
SPI_A_TFT_CS_PIN = const(14)
TFT_DC_PIN = const(27)
TFT_RST_PIN = const(33)
TFT_BACKLIGHT_PIN = const(32)

spiA_miso_pin = machine.Pin(SPI_A_MISO_PIN)
spiA_mosi_pin = machine.Pin(SPI_A_MOSI_PIN)
spiA_clk_pin = machine.Pin(SPI_A_CLK_PIN)
spiA = machine.SPI(
     2,
     baudrate=40000000,
     miso=spiA_miso_pin,
     mosi=spiA_mosi_pin,
     sck=spiA_clk_pin)

display_cs_pin = machine.Pin(SPI_A_TFT_CS_PIN)
display_dc_pin = machine.Pin(TFT_DC_PIN)
display_rst_pin = machine.Pin(TFT_RST_PIN)
display = ili934xnew.ILI9341(
     320,
     240,
     spiA,
     cs=display_cs_pin,
     dc=display_dc_pin,
     rst=display_rst_pin)

display_bl_pin = machine.Pin(TFT_BACKLIGHT_PIN)
display_bl = machine.PWM(display_bl_pin, freq=500, duty=512) #, duty=0, timer=1)

buttonA = machine.Pin(BUTTON_A_PIN, mode=machine.Pin.IN, pull=None)
buttonB = machine.Pin(BUTTON_B_PIN, mode=machine.Pin.IN, pull=None)
buttonC = machine.Pin(BUTTON_C_PIN, mode=machine.Pin.IN, pull=None)

#lcd.init(lcd.M5STACK, width=240, height=320, speed=40000000, rst_pin=33, 
#         miso=19, mosi=23, clk=18, cs=14, dc=27, bgr=True,invrot=3, 
#         expwm=machine.PWM(32, duty=0, timer=1))
