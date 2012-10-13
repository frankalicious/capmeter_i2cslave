#main c source code file  (without file ending)
code = capmeter

SRC = $(code).c
# other c files (with file ending)
SRC += lcd.c
# SRC += rfm12.c
SRC += uart.c
# SRC += twimaster.c

OBJ = $(SRC:.c=.o)

# used avr microcontroller
#MCU=atmega8
#MCU=atmega32
#MCU=atmega16
#MCU=attiny2313
MCU=atmega88
#MCU=atmega328



F_CPU = 14318180
#F_CPU =   8000000
#F_CPU =   12000000
#F_CPU =   16000000
#F_CPU = 4000000

#AVRDUDE_PORT = /dev/ttyS0
AVRDUDE_PORT = usb

#AVRDUDE_PROGRAMMER = ponyser #pollin evalboard
#AVRDUDE_PROGRAMMER = stk500v2 #stk500
#AVRDUDE_PROGRAMMER = jtag2 #mkII jtag
AVRDUDE_PROGRAMMER = jtag2isp #mkII isp
#AVRDUDE_PROGRAMMER = jtag2dw #mkII debugwire

# Optimization level, can be [0, 1, 2, 3, s]. 
#     0 = turn off optimization. s = optimize for size.
#     (Note: 3 is not always the best optimization level. See avr-libc FAQ.)
OPT = s

CDEFS = -DF_CPU=$(F_CPU)UL

WARNOPT = -Wall -Wextra -pedantic -Wundef -Wshadow \
	-Wmissing-prototypes -Wmissing-declarations \
	-Wredundant-decls -Wunreachable-code 

# Makefile for $(code) - AVR $(code) $(code)

# Each rule is in the form:
# target: dependency1 dependency2
# 	command to make target from dependencies

# make looks at all dependencies for a target before making it:
#	1) If there is a rule to make dependency, then do that rule
#	2) If there is no rule, and the dependency file exists, then:
#	   a) if target file exists and is newer than dependency file,
#             then look at next dependency
#          b) if dependency file is newer than target (or target doesn't
#             exist), then run command to make target.

# default target when "make" is run w/o arguments
all: $(code).rom
	@ echo
	@ avr-size -C --mcu=$(MCU) $(code).elf
	@ avr-objdump -h -S $(code).elf > $(code).lss
# compile $(code).c into $(code).o
#$(code).o: $(code).c
#	avr-gcc -c -g -Os -Wall -mmcu=$(MCU) -I. $(code).c -o $(code).o
#	avr-gcc -c    -Os -Wall -mmcu=$(MCU) -I. lib/font.c -o font.o
#	avr-gcc -c    -Os -Wall -mmcu=$(MCU) -I. lib/ledutils.c -o ledutils.o

%.o : %.c
#	avr-gcc -c -g -O$(OPT) -Wall -mmcu=$(MCU) $(CDEFS) -I. $< -o $@
#-save-temps
	avr-gcc -c -g -O$(OPT) $(WARNOPT) -ffunction-sections -fdata-sections -mmcu=$(MCU) $(CDEFS) $(PROJECTDEFS) -I. $< -o $@
#	avr-gcc -c -g -O$(OPT) $(WARNOPT) -mmcu=$(MCU) $(CDEFS) -I. $< -o $@
#http://www.mikrocontroller.net/articles/GCC:_unbenutzte_Funktionen_entfernen

# link up $(code).o and timer.o into $(code).elf
#$(code).elf: $(code).o
#	avr-gcc $(code).o font.o ledutilsNG.o -Wl,-Map=$(code).map,--cref -mmcu=$(MCU) -o $(code).elf
.SECONDARY : $(code).elf
.PRECIOUS : $(OBJ)
%.elf: $(OBJ)
	avr-gcc $(OBJ) --output $@ -Wl,-Map=$(code).map,--cref -mmcu=$(MCU) \
	 -funsigned-char -funsigned-bitfields -fpack-struct -fshort-enums \
	$(WARNOPT) -Wl,--gc-sections -Wl,--print-gc-sections 
#	 -Wall -Wstrict-prototypes
#http://www.mikrocontroller.net/articles/GCC:_unbenutzte_Funktionen_entfernen

# copy ROM (FLASH) object out of $(code).elf into $(code).rom
$(code).rom: $(code).elf
	@ avr-objcopy -O ihex $(code).elf $(code).rom

# command to program chip (optional) (invoked by running "make install")
install:
#-q: disable progressbar for make in emacs
	avrdude -p $(MCU) -P $(AVRDUDE_PORT) -c $(AVRDUDE_PROGRAMMER) -U flash:w:$(code).rom -q

info:
	avrdude -p $(MCU) -P $(AVRDUDE_PORT) -c $(AVRDUDE_PROGRAMMER) -v

server:
#jtag
#	avarice --file $(code).elf --part $(MCU) -j $(AVRDUDE_PORT) :4242 --mkII
#debugwire	
	avarice -w --file $(code).elf --part $(MCU) -j $(AVRDUDE_PORT) :4242 --mkII

ddd: 
	ddd --debugger "avr-gdb -x init.gdb"

gdb:
	avr-gdb --annotate=3 -x init.gdb

fuses:
#	avrdude -p $(MCU) -P $(AVRDUDE_PORT) -c $(AVRDUDE_PROGRAMMER) -U lfuse:w:0xff:m  -U hfuse:w:0xd9:m 
#debugwire
	avrdude -p $(MCU) -P $(AVRDUDE_PORT) -c $(AVRDUDE_PROGRAMMER) -U lfuse:w:0xff:m  -U hfuse:w:0x99:m 
doku:
	doxygen doc/Doxyfile
#	firefox doc/html/index.html

clean:
	rm -f *.o *.lss *.rom *.elf *.map *~ *.s *.i lib/*.o
