date: 2013-08-18
slug: jekyll-pelican
title: Lo strano caso del dr. Jekyll e mr. <strike>Hyde</strike> Pelican
tags: python, pelican, github

*Ferie*. Queste ferie hanno portato in dote la possibilità di fare quello che da tempo avrei voluto fare:
tenere un blog personale dove poter parlare di tutto quello che durante le mie giornate lavorative (*effettivamente
anche non lavorative.. con amore-odio*) mi ha appassionato con qualche tip e insight, più o meno smart.

**OK**, *facciamo il blog!*

Pipeline dei lavori:

1. Scegliere se:
    1. utilizzare uno tra gli innumerevoli servizi di blogging:
        * [wordpress.com](http://wordpress.com/)
        * [tumblr.com](https://www.tumblr.com/)
        * [blogger.com](http://www.blogger.com/‎)
        * [...](https://www.google.it/search?q=blog+platform&oq=blog+platform)
    2. hostare un'installazione più o meno standard di un CMS
    3. buttare giu un blog-engine in *django*
    4. **trovare un modo _alternativo_ **
2. Sviluppare il frontend
    * qualcosa di **semplice**, **leggibile** e sviluppabile in **poco tempo**
3. Bootstrap*-are* iniziando a scrivere qualche articolo

Tralasciando i punti 2 e 3, parliamo del punto 1:

sicuramente utilizzare qualcosa di già pronto come servizio stra-collaudato ha i suoi indubbi vantaggi:
poter iniziare a bloggare a distanza di un'iscrizione profilo, postare un articolo da qualunque parte del
globo e con qualsiasi device che abbia un browser js-capable e non preoccuparsi minimamente di problemi host-related,
sono tutti elementi che il web 2.0 ci ha generosamente regalato e a cui ormai siamo troppo affezionati.

> scommetto che c'è un ma..

No bhè, in realtà il 'ma' neanche c'è. Il punto è che *no pain, no gain*,
manca il fattore soddisfazione, il divertimento e la gioia di scrivere qualcosa, più o meno from scratch, che faccia
quello che deve fare e anche **bene**, o comunque meglio rispetto a qualcosa pensata per essere
utilizzata da milioni di persone da tutto il mondo.
Il punto 1.2 sebbene abbia qualche vantaggio rispetto all'1.1 (la libertà di poter installare
qualsiasi tipo di plugin, ad esempio) pone il problema di dover, potenzialmente, gestire una istanza e il relativo
stack ```WebServer-MySql-PHP``` con, da non sottovalutare per non inginocchiare la macchina (o VM che sia),
politiche di caching (chi ha detto [varnish](https://www.varnish-cache.org/)? Devo ricordarmi fare un articolo
a riguardo..).

> quindi?

Ipotizziamo di voler utilizzare un'installazione di un qualsiasi blog-engine/CMS hostato su di una nostra macchina o
di sviluppare from-scratch un blog-engine con un qualsiasi linguaggio di backend.
Ad ogni nuova richiesta, come d'uopo, il web-server interrogherà il backend, che a sua volta per computare la richiesta
interrogherà il DB; ma, **siamo sicuri che nel caso di un blog tutti questi giri abbiano senso**?
![](/static/images/cache_proxy.png "Cache proxy chart")
ed è qui che ci vengono in soccorso - *emergente soccorso* - tutti quei meccanismi di caching più o meno avanzati.
I vari ```memcached```, ```varnish``` o, rimanendo in ambito WP, ```WP-SuperCache```.

La  ratio naturalmente è: dato che i contenuti di un blog sono praticamente statici, fatta eccezione per:

* inserimento/modifica di un post
* commenti relativi ad un post

perchè non cache-*are* tali contenuti e invalidarli al trascorrere di una data quantità di tempo (medio-grande) o
al trigger di un evento (```nuovo-post```, ```nuovo-commento```, ```...```) ?

**Non fa una piega.**

Ma perchè, invece, non generare questi contenuti one-time e servire *semplici pagine HTML?*

## Static site generators

La meravigliosa maestà dell'opensource sull'onda del web 2.0 è qualcosa da lasciare senza fiato.
Qualsiasi cosa di cui si possa aver bisogno per costruire qualcosa, per lavoro o per diletto è qui per noi, ben
documentato, free, supportato da intere comunità.. basta solo saper scegliere, bene!

Io, qualche giorno fa, ho scelto Jekyll.

### Jekyll

![](/static/images/jekyll.png 'Jekyll logo')

Jekyll è un generatore di siti statici scritto in ruby, che,
cito testualmente dal suo [sito ufficiale](http://jekyllrb.com/):

* **simple**
No more databases, comment moderation, or pesky updates to install—just your content.
* **static**
Markdown (or Textile), Liquid, HTML & CSS go in. Static sites come out ready for deployment.
* **blog-aware**
Permalinks, categories, pages, posts, and custom layouts are all first-class citizens here.
* **free hosting with GitHub-Pages**
Sick of dealing with hosting companies? *GitHub Pages are powered by Jekyll*,
so you can easily deploy your site using GitHub for free—custom domain name and all.

**_bam!_**

in poco più di un paio d'ore il blog che state leggendo adesso era ```up & running``` jekyll-powered, hostato
su GitHub-Pages.

Mi si è aperto un mondo, niente backend, niente DB, nulla da sottoporre al renderer di turno..

Cosa ho riscontrato, oggettivamente:

* **+** perfettamente integrato con GitHub: è necessario solo pushare un progetto jekyll nel master branch
di un qualsiasi repository per far generare al sistema i contenuti statici
* **+** semplice
* **-** scarsamente documentato
* **-** installazioni su macchine windows abbastanza macchinose *(ruby)*

Soggettivamente non mi è piaciuto troppo il fatto che utilizzi *liquid* come template-engine e il fatto che sia
in ruby con il vincolo per questo linguaggio anche sui plugin: non ho mai scritto una riga di ruby e
l'idea di utilizzare qualcosa senza avere troppe possibilità di personalizzazione, devo ammettere,
mi è stata da subito un po' stretta.

> quindi hai buttato il lavoro di un pomeriggio?

.. *coff* sì *coff* ..

### Pelican

Pelican, è un generatore di siti statici ma, a differenza della sua *controparte*, **scritto in python**.
E già mi è simpatico! No, scherzi e (stupide) guerre di religione a parte..

![](/static/images/pelican.png 'Pelican logo')

Gli scopi sono gli stessi di Jekyll, forse Pelican è più blog-oriented (è ciò non può che essere un bene per i miei
bisogni naturalmente) e, passato un altro pomeriggio a convertire il frontend sviluppato da *liquid* a *jinja2*
(il template-engine di [flask](http://flask.pocoo.org/)!) incapsulandolo in un tema (a partire dal tema di default
*notmyidea*) ecco ciò che, oggettivamente, posso dire di aver riscontrato:

* **+** documentazione molto più ampia sebbene anche essa abbastanza incompleta
* **+** semplice
* **+** scritto in python, con la conseguente semplicità che ne consegue
* **+** template-engine jinja2, sintassi praticamente standard de-facto per i dev django/flask
* **+** migliore gestione delle categorie e tag
* **-** **deploy/integrazione su Github-Pages non immediata** (naturalmente è una limitazione imposta di GitHub, vale
solo se si vuol utilizzare GitHub-Pages)

L'ultimo punto merita un intero articolo che spero di poter scrivere, tempo permettendo, al più presto.