Návod na inštaláciu:
1. Jednotlivé priečinky s dekódermi skopírujte na miesto inštalácie PulseView. Presnejšie do miesto_instalacie\sigrok\PulseView\share\libsigrokdecode\decoders.
2. Teraz by sa už mali dať tieto dekódery používať v PulseView.

Návod na použitie paketovača:
1. Nad dekódery, ktorých výstupom je UART/SPI/I2C nasadte stack-dekódery UART/SPI/I2C bytes extractor.
2. Nad ne nasadte dekóder Packeter.
2. Paketovač má niekoľko modifikátorov. Prvé 3 sú zjavné. 
3. Do Sequence of characters to separate packets on (hexadecimal values without 0x separated by ,) je možné zadať hexa hodnoty znakov, ktoré budú tvoriť sekvenciu, po ktorej prečítaní sa packet ukončí a začne sa nový. 
Hodnoty zadávate bez 0x a oddelujete ich čiarkou bez medzier. (napr. by ste tu napisali d,a pre oddelovanie paketov po sekvencii znakov s hodnotami 0xd a 0xa)
4. Separate packets on sequence of characters zapína/vypína, či sa horeuvedený modifikátor bude brať do úvahy alebo nie.
5. Display separation sequence characters zapína/vypína, či sa na konci paketov budú zobrazovať aj znaky sekvencie, ktorou bol paket ukončený.

Návod na použitie fixed DS1307 dekodéra:
1. Dekodér nasaďte nad dekodér komunikácie i2c, ktorá predstavuje komunikáciu DS1307 RTC hodín.