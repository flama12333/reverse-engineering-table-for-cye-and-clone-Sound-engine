the purpose is to create converter python raw to mid 
in the future to compete gamehero midi and the wild west roblox with midi player by creating script distributed by me.
Used in

v1 - less feature
https://youtu.be/5ozLqt-22x0
Lian Huan Pao - ATT II 


v2 standart feature
999
https://youtu.be/Cca1YA-yzcc
Good Luck 2 
https://youtu.be/xdvTqW1Zo0Q

v3 - modified feature
Wu Lin Zhengba 
https://youtu.be/ddU9LWYCs4E





Todo Decompile  For analyzis and meaning
with ym2413

Lian Huan Pao - ATT II  - has sound  cpu z80
 999 and Good luck2 - has cpu 6502 

ym3812
Wu Lin Zhengba - z80 sound cpu


Todo Create python code for converter to midi
V1 - Standart feature
address  0000 
Offset 00 tempo
CH1
Offset 01 Instrument
Offset 02 Volume

CH2
Offset 03 Instrument
Offset 04 Volume

CH3
Offset 05 Instrument
Offset 06 Volume

CH4
Offset 07 Instrument
Offset 08 Volume

CH5
Offset 09 Instrument
Offset 0AVolume

CH6
Offset 0B Instrument
Offset 0C Volume
CH7 - Drums
Offset 0D Volume for Drums 1?
Offset 0E Volume for Drums 2?
Offset 0F Volume for Drums 3?
address  0010 
Offset 10 Volume for Drums 4?
Offset 11 Volume for Drums 5?

Address where notes are located
the address is inverted
Offset 12 Channel 1
Offset 14 Channel 2
Offset 16 Channel 3
Offset 18 Channel 4
Offset 1A Channel 5
Offset 1C Channel 6
Offset 1E Channel 7
Command
61 staccato - idk is correct name

64 - Loop to play per times where notes are located - idk what should car this
Offset 01 - in which time to loop 
Offset 02 - Address where notes are located
65 - No Loop to play where notes are located - idk what should car this
Offset 01 - undocumented behavior. 
Offset 02 - Address where notes are located

66 at address 0020 check if there are 66 to change octave or something similar
Offset 01 - Channel 1
Offset 02 - Channel 2
Offset 03 - Channel 3
Offset 04 - Channel 4
Offset 05 - Channel 5
Offset 06 - Channel 6


70
Offset 01 - Instrument
Offset 02 - Instrument
80  - ??
81  - FF  - legato  play per times similar something called  piano roll bar in midi

Drums - Coming soon
00 - 60 Hex notes
07 - 60 Hex notes






















































