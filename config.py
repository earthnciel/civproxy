import logging
import serial

CONFIG = {

    # RX/TX command
    'rx_command': b'\xFE\xFE\x28\xE0\x1C\x00\x00\xFD',
    'tx_command': b'\xFE\xFE\x28\xE0\x1C\x00\x01\xFD',


    # rig
    'rig_port': 'COM10',
    'rig_baudrate': 9600,
    'rig_parity': serial.PARITY_NONE,
    'rig_stopbits': serial.STOPBITS_ONE,
    'rig_bytesize': serial.EIGHTBITS,
    'rig_timeout': 1,
    'rig_dts': True,
    'rig_rts': False,


    # omnirig
    'omni_port': 'COM5',
    'omni_baudrate': 9600,
    'omni_parity': serial.PARITY_NONE,
    'omni_stopbits': serial.STOPBITS_ONE,
    'omni_bytesize': serial.EIGHTBITS,
    'omni_timeout': 1,
    'omni_dts': True,
    'omni_rts': False,

    # logging
    'log_level': logging.DEBUG
}