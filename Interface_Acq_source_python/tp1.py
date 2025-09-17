import serial
import time

class FPGA:
    def __init__(self, port, baud_rate, timeout):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None

    def open_instrument(self):
        self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
        if self.ser.is_open:
            print(f"Connection ok")

    def set_memory_addr(self, address):
        command = f"A{address}\n"
        self.ser.write(command.encode())
        response = self.ser.readline().decode().strip()
        return response

    def write_val_mem(self, value):
        value_byte = bytes.fromhex(value)
        command = f"W{value_byte.hex().upper()}\n"  
        self.ser.write(command.encode())
        response = self.ser.readline().decode().strip()
        return response

    def display_mem_vals_leds(self):
        command = "G\n"
        self.ser.write(command.encode())
        response = self.ser.readline().decode().strip()
        return response

    def read_mem_val(self):
        command = "R\n"
        self.ser.write(command.encode())
        response = self.ser.readline().decode().strip()
        return response

    def close_instrument(self):
        if self.ser:
            self.ser.close()

if __name__ == '__main__':
    fpga = FPGA(port="COM10", baud_rate=115200, timeout=1)

    fpga.open_instrument()

    print(" memory address  0x00...")
    print(fpga.set_memory_addr("00"))  

    print("écris 0xF5 sur memory")
    print(fpga.write_val_mem("F5")) 

    print(fpga.display_mem_vals_leds())  

    print(fpga.read_mem_val()) 

    fpga.close_instrument()
