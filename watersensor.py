import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import time

lcd = CharLCD('PCF8574',0x27)

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

photo_ch = 0

def init():
         GPIO.setwarnings(False)
         GPIO.cleanup()	
         GPIO.setmode(GPIO.BCM)
         GPIO.setup(SPIMOSI, GPIO.OUT)
         GPIO.setup(SPIMISO, GPIO.IN)
         GPIO.setup(SPICLK, GPIO.OUT)
         GPIO.setup(SPICS, GPIO.OUT)
         
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)	

        GPIO.output(clockpin, False)
        GPIO.output(cspin, False)

        commandout = adcnum
        commandout |= 0x18
        commandout <<= 3
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1
        return adcout

def main():
         init()
         time.sleep(2)
         print("will start detec water level\n")
         while True:
                  adc_value=readadc(photo_ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
                  if adc_value < 15:
                           print("HELP! I'm dying :(\n" + str(adc_value) + "\n")
                           lcd.clear()
                           lcd.cursor_pos = (1, 0)
                           lcd.write_string("HELP! I'm dying :(")
                           lcd.cursor_pos = (2, 0)
                           lcd.write_string("Water level: " + str(round(adc_value / 700 * 100, 2)) + "%")
                  elif adc_value>=15 and adc_value<50 :
                           print("I need water soon \n" + str(adc_value) + "\n")
                           lcd.clear()
                           lcd.cursor_pos = (1, 0)
                           lcd.write_string("I need water soon...")
                           lcd.cursor_pos = (2, 0)
                           lcd.write_string("Water level: " + str(round(adc_value / 700 * 100, 2)) + "%")
                  elif adc_value>=50 and adc_value<430 :
                           print("Feeling goooood\n" + str(adc_value) + "\n")
                           lcd.clear()
                           lcd.cursor_pos = (1, 0)
                           lcd.write_string("Feeling gooood :)")
                           lcd.cursor_pos = (2, 0)
                           lcd.write_string("Water level: " + str(round(adc_value / 700 * 100, 2)) + "%")
                  elif adc_value>=430 :
                          print("feeling in a glass of water" + str(adc_value) + "\n")
                          lcd.clear()
                          lcd.cursor_pos = (1, 0)
                          lcd.write_string("Flooded o.O")
                          lcd.cursor_pos = (2, 0)
                          lcd.write_string("Water level: " + str(round(adc_value / 700 * 100, 2)) + "%")
                  time.sleep(3)
        

if __name__ == '__main__':
         try:
                  main()
                 
         except KeyboardInterrupt:
                  lcd.clear()
                  pass
GPIO.cleanup()
