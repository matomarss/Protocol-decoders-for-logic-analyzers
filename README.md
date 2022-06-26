---1. semester

Návod na inštaláciu dekodérov:
1. Jednotlivé priečinky s dekódermi skopírujte na miesto inštalácie PulseView. Presnejšie do miesto_instalacie\sigrok\PulseView\share\libsigrokdecode\decoders.
2. Teraz by sa už mali dať tieto dekódery používať v PulseView.

Návod na použitie paketovača:
1. Nad dekódery, ktorých výstupom je UART/SPI/I2C nasadte stack-dekódery UART/SPI/I2C bytes extractor.
2. Nad ne nasadte dekóder Packeter.
3. Paketovač má niekoľko modifikátorov. Prvé 3 sú zjavné. 
4. Do Sequence of characters to separate packets on (hexadecimal values without 0x separated by ,) je možné zadať hexa hodnoty znakov, ktoré budú tvoriť sekvenciu, po ktorej prečítaní sa packet ukončí a začne sa nový. 
Hodnoty zadávate bez 0x a oddelujete ich čiarkou bez medzier. (napr. by ste tu napisali d,a pre oddelovanie paketov po sekvencii znakov s hodnotami 0xd a 0xa)
5. Separate packets on sequence of characters zapína/vypína, či sa horeuvedený modifikátor bude brať do úvahy alebo nie.
6. Display separation sequence characters zapína/vypína, či sa na konci paketov budú zobrazovať aj znaky sekvencie, ktorou bol paket ukončený.

Návod na použitie fixed DS1307 dekodéra:
1. Dekodér nasaďte nad dekodér komunikácie i2c, ktorá predstavuje komunikáciu DS1307 RTC hodín.



---2. semester

Návod na inštaláciu a spustenie PulseView s mnou pridaným kódom (len na Linux-e):
1. Nainštalujte si všetky požiadavky a naklonujte zdrojový kód PulseView podľa návodu (odporúčaná distribúcia a verzia Linuxu Ubuntu 20.04 LTS): https://sigrok.org/wiki/Linux#PulseView 
2. Po naklonovaní vložte súbor flag.cpp z priečinka frequency_visualization do pulseview/pv/views/trace
3. Ďalej vložte súbory view.cpp, view.hpp, tracetreeitem.cpp, tracetreeitem.hpp, ruler.cpp, ruler.hpp z priečinka zoom_and_view_reset do pulseview/pv/views/trace
3. Pokračujte podľa návodu od príkazu cmake .
4. Spustite skompilovaný program pulseview v priečinku pulseview príkazom ./pulseview

Návod na otestovanie fungovania takto upraveného programu:
1. Po spustení PulseView môžete pridávať zelené markery (flagy) na časovú os dvojklikom a zobrazovať kurzory pomocou tlačidla "Show Cursors".
2. Pri podržaní myši nad flagom alebo kurzorom sa vo zvyšných flagoch zobrazí ich vzdialenosť od flagu/kurzora, nad ktorým sa práve nachádza myš, spolu s frekvenciou.

3. Po kliknutí pravým tlačítkom myši na pravítko alebo oblasť záznamu sa zobrazí kontextové okno, z ktorého je možné možnosťami "Reset view" a "Reset zoom" resetovať pohľad na časovej osi na 0 a resetovať priblíženie na predvolenú hodnotu.