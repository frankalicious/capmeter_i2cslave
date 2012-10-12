#set source
file capmeter.elf

#set target
target remote localhost:4242

#set address for portb
set $portb=(char *)0x800038

#set address for pind
set $pind=(char *)0x800030

#print portb binary
define p_portb_b
       p/t *$portb
end
define p_portb0
       p (*$portb & 1<<0)>>0
end
define p_portb1
       p (*$portb & 1<<1)>>1
end
define p_portb2
       p (*$portb & 1<<2)>>2
end
define p_portb3
       p (*$portb & 1<<3)>>3
end
define p_portb4
       p (*$portb & 1<<4)>>4
end
define p_portb5
       p (*$portb & 1<<5)>>5
end
define p_portb6
       p (*$portb & 1<<6)>>6
end
define p_portb7
       p (*$portb & 1<<7)>>7
end

#print pind binary
define p_pind_b
       p/t *$pind
end