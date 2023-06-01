import logging
from config import CONFIG

import serial
import serial.threaded
import time

RX = bytearray(CONFIG['rx_command'])
TX = bytearray(CONFIG['tx_command'])


class CIVProxyFactory:
    def __init__(self, proxy_handler=None):
        self.logger = logging.getLogger('CIVProxyFactory')
        self.proxy_handler = proxy_handler

    def create_civ_proxy(self):
        return CIVProxy(self.proxy_handler)


class CIVProxy(serial.threaded.Packetizer):
    def __init__(self, proxy_handler=None):
        super().__init__()
        self.TERMINATOR = b'\xFD'

        self.logger = logging.getLogger('CIVProxy')
        self.proxy_handler = proxy_handler

    def handle_packet(self, data):
        data = bytearray(data)
        data.extend(b'\xFD')
        self.proxy_handler(data)


class CIVWorker:
    def __init__(self):
        self.rig_thread = None
        self.omni_thread = None

        self.logger = logging.getLogger('CIVWorker')

        self.rig_serial = serial.Serial(
            port=CONFIG['rig_port'],
            baudrate=CONFIG['rig_baudrate'],
            parity=CONFIG['rig_parity'],
            stopbits=CONFIG['rig_stopbits'],
            bytesize=CONFIG['rig_bytesize'],
            timeout=CONFIG['rig_timeout']
        )
        self.rig_serial.dts = CONFIG['rig_dts']
        self.rig_serial.rts = CONFIG['rig_rts']

        self.omni_serial = serial.Serial(
            port=CONFIG['omni_port'],
            baudrate=CONFIG['omni_baudrate'],
            parity=CONFIG['omni_parity'],
            stopbits=CONFIG['omni_stopbits'],
            bytesize=CONFIG['omni_bytesize'],
            timeout=CONFIG['omni_timeout']
        )
        self.omni_serial.dts = CONFIG['omni_dts']
        self.omni_serial.rts = CONFIG['omni_rts']

        self.rig_serial.flushInput()
        self.omni_serial.flushInput()

    def start(self):
        self.rig_thread = serial.threaded.ReaderThread(
            self.rig_serial,
            CIVProxyFactory(proxy_handler=self.rig2omni_data_handler).create_civ_proxy)

        self.rig_thread.start()
        self.rig_thread.connect()
        self.logger.info(f"rig thread started")

        self.omni_thread = serial.threaded.ReaderThread(
            self.omni_serial,
            CIVProxyFactory(proxy_handler=self.omni2rig_data_handler).create_civ_proxy)

        self.omni_thread.start()
        self.omni_thread.connect()
        self.logger.info(f"omni thread started")

    def stop(self):
        self.rig_thread.stop()
        self.rig_thread.close()
        self.omni_thread.stop()
        self.omni_thread.close()

        self.logger.info(f"rig & omni thread stoped and connection closed")

    def rig2omni_data_handler(self, data):
        self.logger.debug(f"rig->omni: len={len(data)}, data={data}")
        self.omni_thread.write(data)

    def omni2rig_data_handler(self, data):
        self.logger.debug(f"omni->rig: len={len(data)}, data={data}")
        if data == RX:
            self.rig_serial.rts = False
        elif data == TX:
            self.rig_serial.rts = True
        else:
            self.rig_thread.write(data)


if __name__ == "__main__":
    worker = None

    logging.basicConfig(level=CONFIG['log_level'])

    logger = logging.getLogger('Main')

    while True:
        try:
            worker = CIVWorker()
            worker.start()

            input("\n\nEnter to exit...\n")
            break

        except Exception as e:
            logger.exception("CIVWorker error : " + str(e), stack_info=False)
            if worker:
                worker.stop()

        logger.info("CIVWorker try to stop........")
        if worker:
            worker.stop()

        logger.warning("CIVWorker sleep........")
        time.sleep(3)

    logging.shutdown()
