"""Kavşak Sistemi"""

"""4 Yollu kavşak"""

# import RPi.GPIO as GPIO
import time
import threading
import psycopg2
import numpy as np
import RPi.GPIO as GPIO
import spidev
import time
from enum import Enum, auto
from Pi_MCP23S17 import MCP23S17

radar = np.zeros(16)  # 16 birimlik boş vektör tanımlama input
ledTime = np.zeros(16)  # 16 birimlik boş vektör tanımlama output
__author__ = "pe2a"
__license__ = "GPL"

radar[0] = 0
radar[1] = 1
radar[2] = 2
radar[3] = 3
radar[4] = 4
radar[5] = 5
radar[6] = 6
radar[7] = 7
radar[8] = 8
radar[9] = 9
radar[10] = 10
radar[11] = 11
radar[12] = 12
radar[13] = 13
radar[14] = 14
radar[15] = 15

ledTime[0] = 0
ledTime[1] = 0
ledTime[2] = 0
ledTime[3] = 0
ledTime[4] = 0
ledTime[5] = 0
ledTime[6] = 0
ledTime[7] = 0
ledTime[8] = 0
ledTime[9] = 0
ledTime[10] = 0
ledTime[11] = 0
ledTime[12] = 0
ledTime[13] = 0
ledTime[14] = 0
ledTime[15] = 0

# ANALOG INPUT
AI_1 = 0
AI_2 = 1
AI_3 = 2
AI_4 = 3

AI_5 = 4
AI_6 = 5
AI_7 = 6
AI_8 = 7

# GLOBAL VARIABLES DIGITAL INPUT

DI_1 = 18  # pin1
DI_2 = 23
DI_3 = 24
DI_4 = 12

DI_5 = 16
DI_6 = 20
DI_7 = 21
DI_8 = 26

DI_9 = 19
DI_10 = 13
DI_11 = 6
DI_12 = 5

DI_13 = 22
DI_14 = 27
DI_15 = 17
DI_16 = 4


def __myGPIOInit__():
    # init function
    GPIO.setmode(GPIO.BCM)  # bcm library
    # for digital inputs

    # DIGITAL INPUT
    GPIO.setup(DI_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(DI_5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(DI_9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(DI_13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setwarnings(False)


__myGPIOInit__()


# Digital Input Query
def getDIVal(ch):
    if GPIO.input(ch):
        return True
    else:
        return False


def rpi_dig_vol_converter(val):
    return val * 33.0 / 4095.0


def rpi_readAI(ch):
    try:

        if 7 <= ch <= 0:
            raise Exception('MCP3208 channel must be 0-7: ' + str(ch))

        cmd = 128  # 1000 0000
        cmd += 64  # 1100 0000
        cmd += ((ch & 0x07) << 3)
        ret = spi.xfer2([cmd, 0x0, 0x0])

        # get the 12b out of the return
        val = (ret[0] & 0x01) << 11  # only B11 is here
        val |= ret[1] << 3  # B10:B3
        val |= ret[2] >> 5  # MSB has B2:B0 ... need to move down to LSB

        return (val & 0x0FFF)  # ensure we are only sending 12b


    except:
        pass


# GPIO tanimlari cagiriliyor
def init():
    global mcp1
    global spi

    mcp1 = MCP23S17(ce=0)
    mcp1.open()

    # DO tanimlanmasi
    for x in range(0, 16):
        mcp1.setDirection(x, mcp1.DIR_OUTPUT)

    time.sleep(1)

    spi = spidev.SpiDev()
    spi.open(0, 1)
    spi.max_speed_hz = 7629


def DO_Set_High(ch):
    try:

        mcp1.digitalWrite(ch, MCP23S17.LEVEL_HIGH)
    except:
        pass


def DO_Set_Low(ch):
    try:

        mcp1.digitalWrite(ch, MCP23S17.LEVEL_LOW)
    except:
        pass


init()


def inputDeger(pin):
    while 1:
        x = int(radar[0])
        x1 = int(radar[1])
        x2 = int(radar[2])
        x3 = int(radar[3])
        x4 = int(radar[4])
        x5 = int(radar[5])
        x6 = int(radar[6])
        x7 = int(radar[7])
        x8 = int(radar[8])
        x9 = int(radar[9])
        x10 = int(radar[10])
        x11 = int(radar[11])
        x12 = int(radar[12])
        x13 = int(radar[13])
        x14 = int(radar[14])
        x15 = int(radar[15])

        if getDIVal(DI_16):

            DO_Set_High(x)
            time.sleep(int(ledTime[0]))

        else:

            DO_Set_Low(x)

            if getDIVal(DI_15):

                DO_Set_High(x1)
                time.sleep(int(ledTime[1]))

            else:

                DO_Set_Low(x1)

        if getDIVal(DI_14):

            DO_Set_High(x2)

        else:
            DO_Set_Low(x2)

        if getDIVal(DI_13):

            DO_Set_High(x3)

        else:
            DO_Set_Low(x3)

        if getDIVal(DI_12):

            DO_Set_High(x4)

        else:
            DO_Set_Low(x4)

        if getDIVal(DI_11):

            DO_Set_High(x5)

        else:
            DO_Set_Low(x5)

        if getDIVal(DI_10):

            DO_Set_High(x6)

        else:
            DO_Set_Low(x6)

        if getDIVal(DI_9):

            DO_Set_High(x7)

        else:
            DO_Set_Low(x7)

        if getDIVal(DI_8):

            DO_Set_High(x8)

        else:
            DO_Set_Low(x8)

        if getDIVal(DI_7):

            DO_Set_High(x9)

        else:
            DO_Set_Low(x9)

        if getDIVal(DI_6):

            DO_Set_High(x10)

        else:
            DO_Set_Low(x10)

        if getDIVal(DI_5):

            DO_Set_High(x11)

        else:
            DO_Set_Low(x11)

        if getDIVal(DI_4):

            DO_Set_High(x12)

        else:
            DO_Set_Low(x12)

        if getDIVal(DI_3):

            DO_Set_High(x13)

        else:
            DO_Set_Low(x13)

        if getDIVal(DI_2):

            DO_Set_High(x14)

        else:
            DO_Set_Low(x14)

        if getDIVal(DI_1):

            DO_Set_High(x15)

        else:
            DO_Set_Low(x15)


def db(pin):
    while 1:
        try:
            con = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1",
                                   port="5432")
            print("Database opened successfully")
        except:
            print("Bağlantı sağlanmadı.")

        try:
            cur = con.cursor()
            cur.execute("select i.socket, o.socket, time from rule r , flasher o, input_signal i  where r.output_signal_id = o.id and r.input_signal_id = i.id and r.output_status='ON'")
            rows = cur.fetchall()
            print(rows)
        except:
            print("Veri okunamadı.")

        """Radar PINS"""
        i=0
        for row in rows:
            #radar[row[0] - 1] = row[1] - 1
            radar[i] = row[1]
            i=i+1

        """x[0] 1.Radar pini
           x[1] 2.Radar pini
           ...              """
        j=0
        for row in rows:
            ledTime[j] = row[0]
            j=j+1

        print(radar)

        print("Operation done successfully")
        con.close()
        for i in range(17):
            DO_Set_Low(i)

        time.sleep(30)

t2 = threading.Thread(target=db, args=(1,))
t2.start()
t1 = threading.Thread(target=inputDeger, args=(1,))
t1.start()











