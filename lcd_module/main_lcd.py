# coding: utf-8
# Module to write messages in display LCD 16x2 or 20x4
# coding: utf-8
import time

# Raspberry Pi pin configuration:
lcd_rs = 26
lcd_en = 19
lcd_d4 = 13
lcd_d5 = 6
lcd_d6 = 5
lcd_d7 = 11

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2


# Write message in LCD
def escreve_lcd(msg):
    # TODO docstring

    # Initialize the LCD using the pins above.
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

    lcd.clear()
    lcd.message(msg)
    time.sleep(1)  # Delay de 200ms


def limpa_lcd():
    # TODO docstring

    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
    lcd.clear()


if __name__ == '__main__':
    import Adafruit_CharLCD as LCD

    escreve_lcd('teste')
else:
    import sys

    # Relative import: adding module to the path
    sys.path.insert(0, 'lcd_module')
    import Adafruit_CharLCD as LCD
