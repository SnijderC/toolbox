BOF Toolbox Markdown Documenatie
================================
De basis is zoals gebruikelijk volgens de documentatie op: [Daring Fireball](http://daringfireball.net/projects/markdown/syntax)

Naast de basis zijn er een aantal plugins geïnstalleerd, deze plugins geven je veel meer mogelijkheden voor opmaak van artikelen.

Hieronder de [Cheatsheet](#cheatsheet) en onder het kopje [Geavanceerd (plugins)](#geavanceerd-plugins) meer mogelijkheden d.m.v. van de geïnstalleerde plugins. Voor de duidelijkheid, deze functies zijn al geïmplementeerd, je kunt ze dus meteen gaan gebruiken.


# Inhoud

[TOC]

## Cheatsheet ##





### Font stijl ###

##### Voorbeeld:
    **dik gedrukt**
    *schuin gedrukt*
    ***dik & schuin gedrukt***

##### Resultaat:
>**dik gedrukt**

>*schuin gedrukt*

>***dik & schuin gedrukt***





### Titels ###

- H1 : `#`
- H2 : `##`
- H3 : `###`
- H4 : `####`
- H5 : `#####`
- H6 : `######`

##### Voorbeeld

    ###### H3 titel
    ###### H3 titel ######

##### Resultaat:

>###### H6 titel
>###### H6 titel ######





### URL / Links ###

##### Voorbeeld:
Een donatie doen? `[Klik hier!](http://www.bof.nl "BOF Website")`
##### Resultaat: 
Een donatie doen? [Klik hier!](http://www.bof.nl "BOF Website")




### Afbeeldingen ###
##### Syntax:

`![Alternatieve tekst](url "Mouseover")`

##### Voorbeeld:
`![Ik ben een kat!](http://lorempixel.com/400/300/cats/ "Meow!, haal je muis weg!")`
##### Resultaat:
![Ik ben een kat!](http://lorempixel.com/400/300/cats/ "Meow!, haal je muis weg!")




### Quotes ###
##### Voorbeeld:
    > &ldquo;*I do not want to live in a world where everything I do and say is recorded. That is not something I am willing to support or live under.*&rdquo; &ndash; Edward Snowden
##### Resultaat:
>&ldquo;*I do not want to live in a world where everything I do and say is recorded. That is not something I am willing to support or live under.*&rdquo; &ndash; Edward Snowden










### Horizontale lijnen ###

##### Voorbeeld:
    * * *
    
    ***
    
    *****
    
    - - -
    
    ---------------------------------------
    

##### Resultaat:

* * *

***

*****

- - -

---------------------------------------





### Lijstjes ###

##### Voorbeeld:

    * Banaan
    * Citrusvruchten
        - Citroen
        - Sinaasappel    
    
    ---
    
    - Koekjes
        - Oreo
    - Snoepgoed
        + Kauwgombal
    
    ---
    
    + Auto's
    + Fietsen
        1. Gazelle
        2. Batavus
    
    ---
    
    1. All bits are equal
        - Don't treat them differently
        - You cannot prioritise them
    2. Private bits are private

    
##### Resultaat:

* Banaan
* Citrusvruchten
    - Citroen
    - Sinaasappel    

---

- Koekjes
    - Oreo
- Snoepgoed
    + Kauwgombal

---

+ Auto's
+ Fietsen
    1. Gazelle
    2. Batavus

---

1. All bits are equal
    - Don't treat them differently
    - You cannot prioritise them
2. Private bits are private




### Vast formaat (pre formatted) ###

Code, uit te voeren commando's, exact text (wachtwoorden bijvoorbeeld) kun je als `<code>` or `<pre>` block weergeven.
Code blokken maak je door middel van de "*backtick*": `` ` `` : `` `commando pinkelen` ``. Het `<pre>` block maak je door voor elke regel 4 spaties te zetten.


##### Voorbeeld:

**backtick**:

\`$ sudo rm -rfv /metadata/*\`

**pre block**

        #!/usr/bin/python
        def Bits(freedom):
            if freedom:
                print "All bits are treated equal."
            else:
                print "All your bits are belong to us"

^^^^ Let op 4 de spaties hier!

##### Resultaat:

`$ sudo rm -rfv /metadata/*`

    #!/usr/bin/python
    def Bits(freedom):
        if freedom:
            print "All bits are treated equal and private."
        else:
            print "All your bits are belong to us!"



## Geavanceerd (plugins) ##

### Smartypants ###

Er zijn een aantal plugins geïnstalleerd. Zo worden `'` en `"` vanzelf `&ldquo;` en `&rdquo;` die er zo: &ldquo;quote!&rdquo; uitzien. Dit zijn de zogenaamde &ldquo;*smart quotes*&rdquo;. Ze zijn onderdeel van de plugin *Smarty*.

Verder worden `--` en `---` respectievelijk: `&ndash;` en `&mdash;`, deze zien er uit als: &ndash; en &mdash; en worden bijvoorbeeld gebruikt om de naam van de persoon te vermelden bij een quote:
##### Voorbeeld:
***All together now.. &#9835;***

    >*&ldquo;Those who surrender freedom for security will not have, nor do they deserve, either one.&rdquo;* &mdash; Benjamin Franklin

##### Resultaat:
>*&ldquo;Those who surrender freedom for security will not have, nor do they deserve, either one.&rdquo;* &mdash; Benjamin Franklin


## Afkortingen (Abbrev) ##

Abbrev is een html tag die aangeeft dat er een woord een afkorting is, als je je muis er boven houdt verschijnt de betekenis.

Normaal gesproken werkt het in HTML als volgt: 

`<abbrev title="Global Positioning System">GPS<abbrev>`

Met deze plugin kun je ook afkortingen aangeven, het enorme voordeel is dat elke afkorting steeds opnieuw een verklaring krijgt.

#### Voorbeeld:
    GPS is een systeem waarmee je je locatie kunt bepalen. Het GPS systeem wordt mogelijk gemaakt door 4 of meer satellieten die in een MEO baan om de aarde draaien. De satellieten zenden een BPSK gemoduleerd signaal uit in de UFH band.
    *[GPS]: Global Positioning System
    *[UHF]: Ultra High Frequency
    *[BPSK]: Binary Phase-Shift Keying
    
#### Resultaat:
>GPS is een systeem waarmee je je locatie kunt bepalen. Het GPS systeem wordt mogelijk gemaakt door 4 of meer satellieten die in een MEO baan om de aarde draaien. De satellieten zenden een BPSK gemoduleerd signaal uit in de UHF band.
*[GPS]: Global Positioning System
*[UHF]: Ultra High Frequency
*[BPSK]: Binary Phase-Shift Keying
*[MEO]: Medium Earth Orbit

### Tabellen ###

Je kunt eenvoudig tabellen maken m.b.v. de Tables plugin.

Je moet wel een beetje spelen met `|` en `-`.
De bovenste regel wordt een "*table header*" (`<th>`).

Je kunt de inhoud van kolommen uitlijnen, links, rechts of in het midden.
Dit doe je door een `:` in de lijn tussen de header en de inhoud te plaatsen, links (`|:---|`), rechts (`|---:|`) of beide voor in het midden (`|:---:|`).

#### Voorbeeld:
    Medewerker    | Functie        | Drinkt koffie? 
    --------------|----------------|:--------------:
    Hans de Zwart | Directeur      | Ja             
    Ton Siedsma   | Legal Wizard   | Nee            
    Rejo Zenger   | Privacy Legend | Een beetje     

#### Resultaat:
Medewerker    | Functie        | Drinkt koffie? 
--------------|---------------:|:--------------:
Hans de Zwart | Directeur      | Ja             
Ton Siedsma   | Legal Wizard   | Nee            
Rejo Zenger   | Privacy Legend | Een beetje     


### Voetnoot ###

Deze plugin maakt het mogelijk een voetnoot te plaatsen. 
Je kunt bijvoorbeeld iets uitsluiten of aangeven dat je niet verantwoordelijk bent voor de acties van een bezoeker. Of dat je geen bananen fabriceert.

### Voorbeeld
    - iOS houdt een lijst van bezochte locaties bij[^1].
    - Apple does not produce banana's.[^banana]
    
    [^1]: iPad 2+, iPhone 4S+ only..
    [^banana]: Although Apple does not make banana's right now, we keep our options open.

### Resultaat

- iOS houdt een lijst van bezochte locaties bij[^1].
- Apple does not produce banana's.[^banana]

[^1]: iPad 2+, iPhone 4S+ only..
[^banana]: Although Apple does not make banana's right now, we keep our options open.

### &ldquo;Fenced code&rdquo; ###

Als je niet steeds 4 spaties wilt zetten voor een `<pre>` blok, kun je gebruik maken van &ldquo;fenced code&rdquo;.
Je kunt eventueel een programmeertaal aangeven, hoewel dat natuurlijk niet hoeft, het hoeft immers niet eens programma code te zijn. Je kunt ook specifieke instructies uitlijnen. Een taal toevoegen als het wél code is, is een goed idee. Voor nu doet het namelijk niets maar wie weet wordt er op een later tijdstip "sytax highlighting" toegevoegd. De Toolbox weet dan welke kleuren er voor welke functies, variabelen etc. gebruikt moeten worden.

#### Voorbeeld

    ~~~~~~~~~~~~~~~~~~~~.python
    #!/usr/bin/python
        def Bits(freedom):
            if freedom:
                print "All bits are treated equal and private."
            else:
                print "All your bits are belong to us!"
    ~~~~~~~~~~~~~~~~~~~~

Alternatieve syntax (Github)
     
    ```python
    # Dit mag ook
    ```
#### Resultaat

~~~~~~~~~~~~~~~~~~~~.python
#!/usr/bin/python
    def Bits(freedom):
        if freedom:
            print "All bits are treated equal and private."
        else:
            print "All your bits are belong to us!"
~~~~~~~~~~~~~~~~~~~~

```python
# Dit mag ook
```

### Definitie blokken

In HTML bestaat het defintie blokken lijst:

    <dl>
        <dt>Bit</dt>
        <dd>Een basis eenheid voor digitale informatie, kort voor *binary digit*.<br /> 
            Hoewel de bit een beschermde informatiesoort is wordt hun gelijkheid vaak bedreigd door commerciële entiteiten en overheden.
        </dd>
    </dl>


Je kunt een definitie blok maken met de definitie plugin.

#### Voorbeeld

    Bit
    :   Een basis eenheid voor digitale informatie, kort voor *binary digit*. 
        Hoewel de bit een beschermde informatiesoort is wordt hun gelijkheid vaak bedreigd door commerciële entiteiten en overheden.
    
    Byte
    :   Een eenheid voor digitale informatie bestaande uit 8 bits.

#### Resultaat

Bit
:   Een basis eenheid voor digitale informatie, kort voor *binary digit*. 
    Hoewel de bit een beschermde informatiesoort is wordt hun gelijkheid vaak bedreigd door commerciële entiteiten en overheden.

Byte
:   Een eenheid voor digitale informatie bestaande uit 8 bits.



### Attribuut lijst

Deze plugin maakt het mogelijk om CSS klassen en ID's toe te voegen aan elementen. Je kunt ook andere attributen toevoegen.

#### Voorbeeld

    Rode tekst rechts.. 
    {: .pull-right style=color:#cc0000; }
    
    ![Ik ben een kat!](http://lorempixel.com/400/300/cats/ "Meow!, haal je muis weg!"){: style=border-width:4px;border-color:#cc0000;border-style:solid;border-style:dashed; }
    {: .col-xs-3 .col-xs-offset-4 .clearfix }


#### Resultaat

--->
{: .center-block style=color:#cc0000; }

Rode tekst.. 
{: style=color:#cc0000; }

![Ik ben een kat!](http://lorempixel.com/400/300/cats/ "Meow!, haal je muis weg!"){: style=border-width:4px;border-color:#cc0000;border-style:solid;border-style:dashed; }
{: .col-xs-8 .col-xs-offset-4 }

#### Andere voorbeelden ####

Op deze website wordt gebruik gemaakt van boostrap. Dat betekent dat je in combinatie met de "*attribute lists*" allerlei boostrap onderdelen op het scherm kunt toveren. 

#### Voorbeeld
~~~~~~~~~~
DOWNLOAD NU!
{: .btn .btn-success }
  
Delete
{: .btn .btn-danger .btn-primary .btn-lg }

Dit is een intro tekst met Boostraps "*Lead*" stijl.
{: .lead }

![Ik ben een kat!](http://lorempixel.com/400/300/cats/ "Meow!, haal je muis weg!"){: .img-circle }

Whoa, this is bad..
{: .label .label-warning }

42
{: .badge }

Waarschuwing, hoewel iMessage end-to-end encryptie toepast heb je geen controle over de gebruikte sleutels!
{: .alert .alert-warning }
~~~~~~~~~~
#### Resultaat

DOWNLOAD NU!
{: .btn .btn-success }
  
Delete
{: .btn .btn-danger .btn-primary .btn-lg }

Dit is een intro tekst met Boostraps "*Lead*" stijl.
{: .lead }

![Ik ben een kat!](http://lorempixel.com/400/300/cats/ "Meow!, haal je muis weg!"){: .img-circle }

Whoa, this is bad..
{: .label .label-warning }

42
{: .badge }

Waarschuwing, hoewel iMessage end-to-end encryptie toepast heb je geen controle over de gebruikte sleutels!
{: .alert .alert-warning }

