// This file is Copyright (c) 2020 Florent Kermarrec <florent@enjoy-digital.fr>
// License: BSD

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <irq.h>
#include <libbase/uart.h>
#include <libbase/console.h>
#include <generated/csr.h>

int main(void)
{
#ifdef CONFIG_CPU_HAS_INTERRUPT
  irq_setmask(0);
  irq_setie(1);
#endif
  uart_init();

  while (1)
  {
    gpio_out_write(0xFFFF); // Turn all LEDs ON
    busy_wait(500000);      // Delay
    gpio_out_write(0x0000); // Turn all LEDs OFF
    busy_wait(500000);      // Delay
  }

  return 0;
}
