from app import enum, time, threading, serial, list_ports


CELL_COUNT = 13
TEMP_COUNT = 6
CODE = 0xDEADBEEF


class State(enum.Enum):
    OFF = 0
    PRECHARGE = 1
    IDLE = 2
    DISCHARGE = 3
    CHARGE = 4
    BALANCE = 5
    FAULT = 6
    SHUTDOWN = 7


class Decoder:
    def __init__(self):
        self.ser = serial.Serial(baudrate=115200, timeout=None)

        self.connected = False
        self.last_connection_check = 0
        self.serial_buffer = b""
        self.serial_buffer_idx = 0

        self.code = 0
        self.capacity = 0
        self.soc = 0
        self.state = State(0)
        self.volt = [ 0 for _ in range(CELL_COUNT) ]
        self.temp = [ 0 for _ in range(TEMP_COUNT) ]
        self.balance = [0 for _ in range(CELL_COUNT) ]
        self.precharge = 0
        self.charge = 0
        self.discharge = 0
        self.pack_voltage = 0
        self.pack_current = 0
        self.fault_ov = 0
        self.fault_uv = 0
        self.fault_oc = 0
        self.fault_sc = 0
        self.fault_bq = 0
        self.fault_ot = 0
        self.fault_cm = 0
        self.cpu = 0

        self.worker_thread = threading.Thread(target=self.worker_task, daemon=True)
        self.worker_thread.start()

    def try_connect(self):
        for port, _, id in list_ports.comports():
            try:
                vid = id.split()[1][8:12]
                pid = id.split()[1][13:17]
            except IndexError:
                continue

            if vid == '0483' and pid == '374B':
                try:
                    self.ser.setPort(port)
                    self.ser.open()
                except:
                    self.ser = serial.Serial(timeout=None)

    def is_connected(self):
        for _1, _2, id in list_ports.comports():
            try:
                vid = id.split()[1][8:12]
                pid = id.split()[1][13:17]
                if vid == '0483' and pid == '374B':
                    return self.ser.isOpen()
            except IndexError:
                continue
        return False

    def read_serial(self, size):
        if len(self.serial_buffer) - self.serial_buffer_idx < 60:
            self.serial_buffer = b''.join([self.serial_buffer[self.serial_buffer_idx:], self.ser.read(256)])
            self.serial_buffer_idx = 0
        self.serial_buffer_idx += size
        return self.serial_buffer[self.serial_buffer_idx - size:self.serial_buffer_idx]
    
    def worker_task(self):
        while True:
            if time.time() - self.last_connection_check > 1:
                self.last_connection_check = time.time()
                self.connected = self.is_connected()

            if self.connected:
                try:
                    self.code = self.code >> 8
                    self.code = self.code | (int.from_bytes(self.read_serial(1), "little") << 24)

                    if self.code != CODE:
                        continue
                    
                    self.capacity = int.from_bytes(self.read_serial(4), "little")
                    self.soc = int.from_bytes(self.read_serial(2), "little")
                    self.state = State(int.from_bytes(self.read_serial(2), "little"))
                    for i in range(CELL_COUNT):
                        self.volt[i] = int.from_bytes(self.read_serial(2), "little")
                    for i in range(TEMP_COUNT):
                        self.temp[i] = int.from_bytes(self.read_serial(2), "little")
                    raw = int.from_bytes(self.read_serial(2), "little")
                    for i in range(CELL_COUNT):
                        self.balance[i] = (raw >> i) & 1
                    self.precharge = (raw >> (CELL_COUNT + 0)) & 1
                    self.charge    = (raw >> (CELL_COUNT + 1)) & 1
                    self.discharge = (raw >> (CELL_COUNT + 2)) & 1
                    self.pack_voltage = int.from_bytes(self.read_serial(2), "little")
                    self.pack_current = int.from_bytes(self.read_serial(2), "little", signed=True)
                    raw = int.from_bytes(self.read_serial(2), "little")
                    self.fault_oc = (raw >> 0) & 1
                    self.fault_sc = (raw >> 1) & 1
                    self.fault_ov = (raw >> 2) & 1
                    self.fault_uv = (raw >> 3) & 1
                    self.fault_bq = (raw >> 4) & 1
                    self.fault_ot = (raw >> 5) & 1
                    self.fault_cm = (raw >> 6) & 1
                    raw = int.from_bytes(self.read_serial(2), "little")
                    self.cpu = int((100 - raw) / 100)
                except:
                    pass
            else:
                time.sleep(1)
                self.try_connect()
                print("attempted to connect")
