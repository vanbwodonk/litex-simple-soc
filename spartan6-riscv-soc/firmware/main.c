#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libbase/uart.h>
#include <generated/csr.h>

#define LM75_I2C_ADDR  0x48
#define LM75_TEMP_REG  0x00
#define TEMP_SCALE     500

void uart_write_word(const char *word);
uint32_t lm75_read_temperature(void);
void i2c_scan(void);

void uart_write_word(const char *word) {
    while (*word) {
        uart_write(*word);
        word++;
    }
    uart_write('\n');
}

uint32_t lm75_read_temperature(void) {
    uint32_t temp_raw;
    uint32_t temp_milli_celsius;
    char msg[32];

    i2c_master_addr_write(LM75_I2C_ADDR);
    
    i2c_master_rxtx_write(LM75_TEMP_REG);
    
    i2c_master_settings_write(0x00000101);
        
    while (!(i2c_master_status_read() & 0x01));

    i2c_master_addr_write(LM75_I2C_ADDR | 0x01);
    
    i2c_master_settings_write(0x00000200);
        
    while (!(i2c_master_status_read() & 0x02));

    temp_raw = i2c_master_rxtx_read();  // Langsung baca seluruh 16-bit data

    // snprintf(msg, sizeof(msg), "Temp: %04x", temp_raw);
    // uart_write_word(msg);
    
    temp_raw = temp_raw / 128;  // Geser bit sesuai format LM75
    // temp_raw | 0b0000000000000000;
    // uint8_t data2 = ((temp_raw & 0b100000000) >> 8) & 0b11111111;
    // if (temp_raw & (1 << 8)) {  // Jika negatif (bit 10 = 1), lakukan sign extension
    // if(data2 == 0b00000001){
        // temp_raw -= (1 << 9);
    // }
    
    return temp_milli_celsius = temp_raw * TEMP_SCALE;
    
}

void i2c_scan(void) {
    char msg[32];

    for (uint8_t addr = 0x00; addr < 0x80; addr++) {
        i2c_master_addr_write(addr);
        i2c_master_settings_write(0x00000100);
        while (!(i2c_master_status_read() & 0x01));

        if (!(i2c_master_status_read() & 0x04)) {
            snprintf(msg, sizeof(msg), "Found I2C device at 0x%02X", addr);
            uart_write_word(msg);
        }
    }
}

int main(void) {
    char buffer[32];
    uint32_t temp_mC;  // MEnggunakan mili-Celsius untuk menghindari float
    uint8_t temp_int, temp_frac;

    uart_init();
    printf("mulai");

    i2c_master_active_write(1);

    while (1) {
        temp_mC = lm75_read_temperature();

        temp_int = temp_mC / 1000;         // Bagian depan (misalnya 25 dari 25125)
        temp_frac = (temp_mC % 1000) / 10; // Dua angka desimal (misalnya 12 dari 25125)

        snprintf(buffer, sizeof(buffer), "Temp: %d.%02d C", temp_int, temp_frac);
        uart_write_word(buffer);

        busy_wait(1000);
    }

    return 0;
}
