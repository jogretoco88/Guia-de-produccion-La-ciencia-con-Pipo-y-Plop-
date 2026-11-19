# Guion de narración del Ep. 4 en 5 idiomas, una frase por toma.
# Las etiquetas [..] son dirección de voz para Eleven v4 (no se pronuncian).
# anchor: (segundo dentro de la toma, nº de ocurrencia de la palabra ancla)
import json, re

SHOTS = json.load(open('../shots.json'))['shots']

def ts(x):
    m, s = x.split(':'); return int(m) * 60 + int(s)

L = {}
def line(sid, es, en, fr, pt, hi, anchors=None):
    L[sid] = dict(es=es, en=en, fr=fr, pt=pt, hi=hi, anchors=anchors or [])

# palabra ancla (el hipo / la onomatopeya) por idioma
HIC = dict(es='hip', en='hic', fr='hic', pt='hic', hi='हिच')

line('E04_C01',
 "[surprised] ¡Hip! [curious] ¿Qué fue eso? Todo estaba en calma… y tu cuerpo saltó sin pedirte permiso.",
 "[surprised] Hic! [curious] What was that? Everything was calm… and your body jumped all by itself.",
 "[surprised] Hic ! [curious] C'était quoi, ça ? Tout était calme… et ton corps a sauté tout seul.",
 "[surprised] Hic! [curious] O que foi isso? Estava tudo calmo… e o seu corpo pulou sem pedir licença.",
 "[surprised] हिच! [curious] यह क्या था? सब कुछ शांत था… और तुम्हारा शरीर अपने आप उछल पड़ा।",
 anchors=[('START', 1.05)])
line('E04_C02',
 "[playful] Y otra vez: ¡hip! [curious] No lo decides tú. Entonces… ¿quién está dando la orden?",
 "[playful] And again: hic! [curious] You didn't decide that. So… who's giving the order?",
 "[playful] Et encore : hic ! [curious] Ce n'est pas toi qui décides. Alors… qui donne l'ordre ?",
 "[playful] E de novo: hic! [curious] Não é você que decide. Então… quem está dando a ordem?",
 "[playful] और फिर से: हिच! [curious] यह तुम तय नहीं करते। तो फिर… आदेश कौन दे रहा है?",
 anchors=[('HIC1', 1.18)])
line('E04_C03',
 "[curious] Pipo también quiere saberlo. [mischievously] Hoy vamos a buscar al culpable… debajo de tus costillas.",
 "[curious] Pipo wants to know too. [mischievously] Today we're hunting for the culprit… right under your ribs.",
 "[curious] Pipo aussi veut savoir. [mischievously] Aujourd'hui, on cherche le coupable… sous tes côtes.",
 "[curious] O Pipo também quer saber. [mischievously] Hoje vamos procurar o culpado… debaixo das suas costelas.",
 "[curious] पीपो भी जानना चाहता है। [mischievously] आज हम असली कसूरवार को ढूँढेंगे… तुम्हारी पसलियों के नीचे।")
line('CANAL_INICIO',
 "[excited] ¡La ciencia con Pipo y Plop!",
 "[excited] Science with Pipo and Plop!",
 "[excited] La science avec Pipo et Plop !",
 "[excited] A ciência com Pipo e Plop!",
 "[excited] पीपो और प्लॉप के साथ विज्ञान!")
line('E04_C04',
 "[mischievously] La idea loca de Pipo: ¡Plop se tragó una ranita, y la ranita salta en su panza!",
 "[mischievously] Pipo's wild idea: Plop swallowed a little frog, and it's hopping in his tummy!",
 "[mischievously] L'idée folle de Pipo : Plop a avalé une grenouille qui saute dans son ventre !",
 "[mischievously] A ideia maluca do Pipo: o Plop engoliu um sapinho, e ele pula na barriga dele!",
 "[mischievously] पीपो का मज़ेदार ख़याल: प्लॉप ने एक छोटा मेंढक निगल लिया, और वह उसके पेट में उछल रहा है!")
line('E04_C05',
 "[amused] Si fuera una rana, la oiríamos croar. Y además… Plop no ha comido ranas. [playful] Creo.",
 "[amused] If it were a frog, we'd hear it croak. And besides… Plop hasn't eaten any frogs. [playful] I think.",
 "[amused] Une grenouille, on l'entendrait coasser. Et puis… Plop n'a pas mangé de grenouille. [playful] Je crois.",
 "[amused] Se fosse um sapo, a gente ia ouvir ele coaxar. E além disso… o Plop não comeu sapo. [playful] Eu acho.",
 "[amused] अगर मेंढक होता, तो हमें टर्र-टर्र सुनाई देती। और वैसे भी… प्लॉप ने मेंढक नहीं खाया। [playful] शायद।")
line('E04_C06',
 "[thoughtful] Segunda idea: aguantar la respiración hasta que se vaya. A veces sirve… ¿pero por qué?",
 "[thoughtful] Idea number two: hold your breath until it goes away. Sometimes it works… but why?",
 "[thoughtful] Deuxième idée : retenir son souffle jusqu'à ce que ça passe. Ça marche parfois… mais pourquoi ?",
 "[thoughtful] Segunda ideia: prender a respiração até passar. Às vezes funciona… mas por quê?",
 "[thoughtful] दूसरा ख़याल: हिचकी जाने तक साँस रोककर रखना। कभी-कभी यह काम करता है… पर क्यों?")
line('E04_C07',
 "[thoughtful] Plop se pregunta: si yo no quiero saltar, ¿qué parte de mí está saltando sola?",
 "[thoughtful] Plop wonders: if I don't want to jump, what part of me is jumping on its own?",
 "[thoughtful] Plop se demande : si je ne veux pas sauter, quelle partie de moi saute toute seule ?",
 "[thoughtful] O Plop se pergunta: se eu não quero pular, que parte de mim está pulando sozinha?",
 "[thoughtful] प्लॉप सोचता है: अगर मैं उछलना नहीं चाहता, तो मेरा कौन सा हिस्सा अपने आप उछल रहा है?")
line('E04_C08',
 "[excited] ¡Esa es la pregunta correcta! El salto viene de adentro, de un músculo que casi nadie conoce.",
 "[excited] That's the right question! The jump comes from inside, from a muscle almost nobody knows.",
 "[excited] C'est la bonne question ! Le saut vient de l'intérieur, d'un muscle presque inconnu.",
 "[excited] Essa é a pergunta certa! O pulo vem de dentro, de um músculo que quase ninguém conhece.",
 "[excited] यही सही सवाल है! यह उछाल अंदर से आता है, एक ऐसी मांसपेशी से जिसे लगभग कोई नहीं जानता।")
line('E04_C09',
 "[curious] ¿Sabes cuál es? ¿Tú qué crees? Piénsalo… [excited] ¡Vamos a mirar dentro del pecho!",
 "[curious] Do you know which one? What do you think? Think about it… [excited] Let's look inside the chest!",
 "[curious] Tu sais lequel ? Qu'en penses-tu ? Réfléchis… [excited] Allons voir dans la poitrine !",
 "[curious] Sabe qual é? O que você acha? Pense um pouco… [excited] Vamos olhar dentro do peito!",
 "[curious] क्या तुम जानते हो वह कौन सी है? तुम्हें क्या लगता है? सोचो… [excited] चलो सीने के अंदर देखते हैं!")
line('E04_C10',
 "[excited] ¡Hagamos zoom! Estos son tus pulmones: dos bolsas esponjosas que se llenan de aire.",
 "[excited] Let's zoom in! These are your lungs: two spongy bags that fill up with air.",
 "[excited] Zoomons ! Voici tes poumons : deux sacs spongieux qui se remplissent d'air.",
 "[excited] Vamos dar um zoom! Estes são os seus pulmões: duas bolsas fofinhas que se enchem de ar.",
 "[excited] चलो ज़ूम करें! ये हैं तुम्हारे फेफड़े: दो स्पंज जैसी थैलियाँ, जो हवा से भर जाती हैं।")
line('E04_C11',
 "[warmly] Pero los pulmones no se mueven solos. Debajo tienen un músculo en forma de cúpula.",
 "[warmly] But lungs can't move by themselves. Underneath, there's a dome-shaped muscle.",
 "[warmly] Mais les poumons ne bougent pas tout seuls. En dessous, il y a un muscle en forme de dôme.",
 "[warmly] Mas os pulmões não se mexem sozinhos. Embaixo deles tem um músculo em forma de cúpula.",
 "[warmly] लेकिन फेफड़े अपने आप नहीं हिलते। उनके नीचे गुंबद जैसी एक मांसपेशी है।")
line('E04_C12',
 "[warmly] Se llama diafragma. Cuando baja, hace espacio y el aire entra a los pulmones.",
 "[warmly] It's called the diaphragm. When it moves down, it makes room and air flows into the lungs.",
 "[warmly] C'est le diaphragme. Quand il descend, il fait de la place et l'air entre dans les poumons.",
 "[warmly] Ele se chama diafragma. Quando desce, abre espaço e o ar entra nos pulmões.",
 "[warmly] इसका नाम है डायाफ्राम। जब यह नीचे जाता है, तो जगह बनती है और हवा फेफड़ों में आती है।")
line('E04_C13',
 "[calmly] Cuando sube, empuja el aire hacia afuera. Baja y sube, baja y sube, todo el día.",
 "[calmly] When it moves up, it pushes the air out. Down and up, down and up, all day long.",
 "[calmly] Quand il remonte, il pousse l'air dehors. Il descend, il monte, toute la journée.",
 "[calmly] Quando sobe, empurra o ar para fora. Desce e sobe, desce e sobe, o dia todo.",
 "[calmly] जब यह ऊपर जाता है, तो हवा को बाहर धकेलता है। नीचे और ऊपर, नीचे और ऊपर, पूरे दिन।")
line('E04_L1',
 "[warmly] Pulmones arriba, diafragma abajo: el jefe de tu respiración.",
 "[warmly] Lungs on top, diaphragm below: the boss of your breathing.",
 "[warmly] Les poumons en haut, le diaphragme en bas : le chef de ta respiration.",
 "[warmly] Pulmões em cima, diafragma embaixo: o chefe da sua respiração.",
 "[warmly] ऊपर फेफड़े, नीचे डायाफ्राम: तुम्हारी साँसों का असली बॉस।")
line('E04_C14',
 "[curious] Pipo pregunta: ¿y quién le dice al diafragma cuándo moverse? [playful] ¡Yo no le digo nada!",
 "[curious] Pipo asks: who tells the diaphragm when to move? [playful] I don't tell it anything!",
 "[curious] Pipo demande : qui dit au diaphragme quand bouger ? [playful] Moi, je ne lui dis rien !",
 "[curious] O Pipo pergunta: e quem avisa o diafragma quando se mexer? [playful] Eu não falo nada!",
 "[curious] पीपो पूछता है: डायाफ्राम को कौन बताता है कि कब हिलना है? [playful] मैं तो कुछ नहीं कहता!")
line('E04_C15',
 "[warmly] Se lo dice tu cerebro, por unos cables llamados nervios. Manda la orden sin que lo notes.",
 "[warmly] Your brain does, through little cables called nerves. It sends the order without you noticing.",
 "[warmly] C'est ton cerveau, par de petits câbles appelés nerfs. Il envoie l'ordre sans que tu le saches.",
 "[warmly] Quem avisa é o seu cérebro, por uns cabinhos chamados nervos. Ele manda a ordem sem você perceber.",
 "[warmly] यह काम तुम्हारा दिमाग़ करता है, नसों नाम की छोटी तारों से। वह चुपचाप आदेश भेजता है।")
line('E04_C16',
 "[curious] Plop ya sospecha algo: ¿y si a veces esa orden llega… con un error?",
 "[curious] Plop suspects something: what if sometimes that order arrives… with a mistake?",
 "[curious] Plop se doute de quelque chose : et si parfois cet ordre arrivait… avec une erreur ?",
 "[curious] O Plop já desconfia: e se às vezes essa ordem chega… com um erro?",
 "[curious] प्लॉप को कुछ शक है: अगर कभी वह आदेश… किसी गलती के साथ पहुँचे तो?")
line('E04_C17',
 "[playful] Así es. Si comes muy rápido, tragas aire o te da un ataque de risa…",
 "[playful] That's right. If you eat too fast, swallow air, or get a giggle attack…",
 "[playful] Exactement. Si tu manges trop vite, si tu avales de l'air ou si tu as un fou rire…",
 "[playful] Isso mesmo. Se você come muito rápido, engole ar ou tem uma crise de riso…",
 "[playful] बिल्कुल। अगर तुम बहुत जल्दी खाते हो, हवा निगल लेते हो, या ज़ोर-ज़ोर से हँसते हो…")
line('E04_C18',
 "[curious] tu estómago se infla y le hace cosquillas al nervio que pasa justo al lado.",
 "[curious] your stomach puffs up and tickles the nerve that runs right next to it.",
 "[curious] ton estomac gonfle et chatouille le nerf qui passe juste à côté.",
 "[curious] o seu estômago incha e faz cócegas no nervo que passa bem do lado.",
 "[curious] तो तुम्हारा पेट फूल जाता है और पास से गुज़रने वाली नस को गुदगुदी करता है।")
line('E04_C19',
 "[dramatically] El nervio se confunde y manda una orden equivocada: [excited] ¡aprieta ya, con todas tus fuerzas!",
 "[dramatically] The nerve gets confused and sends the wrong order: [excited] squeeze now, as hard as you can!",
 "[dramatically] Le nerf s'embrouille et envoie un mauvais ordre : [excited] serre, de toutes tes forces !",
 "[dramatically] O nervo se confunde e manda uma ordem errada: [excited] aperta já, com toda a força!",
 "[dramatically] नस उलझ जाती है और गलत आदेश भेज देती है: [excited] अभी कसो, पूरी ताक़त से!")
line('E04_C20',
 "[surprised] ¡Zas! [dramatically] El diafragma obedece y da un tirón hacia abajo… y el aire entra de golpe.",
 "[surprised] Whoosh! [dramatically] The diaphragm obeys and gives a sudden tug down… and air rushes in.",
 "[surprised] Hop ! [dramatically] Le diaphragme obéit et tire brusquement vers le bas… et l'air entre d'un coup.",
 "[surprised] Zás! [dramatically] O diafragma obedece e dá um puxão para baixo… e o ar entra de uma vez.",
 "[surprised] झटका! [dramatically] डायाफ्राम बात मानता है और तेज़ी से नीचे खिंचता है… और हवा एकदम अंदर आती है।",
 anchors=[('START', 0.50)])
line('E04_C21',
 "[warmly] Ese chorro de aire sorprende a tu garganta, donde están las cuerdas vocales.",
 "[warmly] That rush of air surprises your throat, where your vocal cords are.",
 "[warmly] Ce jet d'air surprend ta gorge, là où se trouvent les cordes vocales.",
 "[warmly] Esse jato de ar surpreende a sua garganta, onde ficam as cordas vocais.",
 "[warmly] हवा का यह झोंका तुम्हारे गले को चौंका देता है, जहाँ स्वर-तंतु होते हैं।")
line('E04_C22',
 "[surprised] ¡Clac! [dramatically] Las cuerdas vocales se cierran de golpe, como una puerta con el viento.",
 "[surprised] Clack! [dramatically] The vocal cords slam shut, like a door in the wind.",
 "[surprised] Clac ! [dramatically] Les cordes vocales se ferment d'un coup, comme une porte qui claque au vent.",
 "[surprised] Clac! [dramatically] As cordas vocais se fecham de repente, como uma porta batendo com o vento.",
 "[surprised] खट! [dramatically] स्वर-तंतु झट से बंद हो जाते हैं, जैसे हवा में कोई दरवाज़ा बंद होता है।",
 anchors=[('START', 0.80)])
line('E04_C23',
 "[playful] Ese portazo es el sonido del hipo. ¡Hip! No es tu voz: es una puerta cerrándose.",
 "[playful] That slam is the sound of a hiccup. Hic! It's not your voice: it's a door closing.",
 "[playful] Ce claquement, c'est le bruit du hoquet. Hic ! Ce n'est pas ta voix : c'est une porte qui se ferme.",
 "[playful] Essa batida é o som do soluço. Hic! Não é a sua voz: é uma porta se fechando.",
 "[playful] दरवाज़े की वह धड़ाम ही हिचकी की आवाज़ है। हिच! यह तुम्हारी आवाज़ नहीं, बंद होता दरवाज़ा है।",
 anchors=[('HIC1', 2.95)])
line('E04_C24',
 "[curious] Pipo quiere saber por qué se repite. [warmly] Porque el nervio sigue confundido y repite la orden.",
 "[curious] Pipo wants to know why it keeps coming back. [warmly] Because the nerve is still confused and repeats the order.",
 "[curious] Pipo veut savoir pourquoi ça recommence. [warmly] Le nerf, encore embrouillé, répète l'ordre.",
 "[curious] O Pipo quer saber por que ele se repete. [warmly] Porque o nervo continua confuso e repete a ordem.",
 "[curious] पीपो जानना चाहता है कि यह बार-बार क्यों होती है। [warmly] क्योंकि नस अब भी उलझी है और वही आदेश दोहराती है।")
line('E04_C25',
 "[playful] Tirón, portazo, ¡hip! [pause] Tirón, portazo, ¡hip! [curious] ¿Cómo se apaga esta máquina, Plop?",
 "[playful] Tug, slam, hic! [pause] Tug, slam, hic! [curious] How do we switch off this machine, Plop?",
 "[playful] Ça tire, ça claque, hic ! [pause] Ça tire, ça claque, hic ! [curious] Comment on arrête cette machine, Plop ?",
 "[playful] Puxão, batida, hic! [pause] Puxão, batida, hic! [curious] Como se desliga essa máquina, Plop?",
 "[playful] झटका, धड़ाम, हिच! [pause] झटका, धड़ाम, हिच! [curious] प्लॉप, यह मशीन बंद कैसे होगी?",
 anchors=[('HIC1', 2.05), ('HIC2', 4.10)])
line('E04_C26',
 "[calmly] Probemos lo de antes: respirar muy lento… y aguantar el aire un momento.",
 "[calmly] Let's try that idea again: breathe in very slowly… and hold the air for a moment.",
 "[calmly] Essayons l'idée de tout à l'heure : respirer très lentement… et retenir l'air un moment.",
 "[calmly] Vamos tentar aquela ideia: respirar bem devagar… e segurar o ar por um momento.",
 "[calmly] चलो पहले वाला तरीका आज़माएँ: बहुत धीरे साँस लो… और थोड़ी देर हवा रोककर रखो।")
line('E04_C27',
 "[warmly] Al aguantar el aire, en tu cuerpo se junta un gas llamado dióxido de carbono.",
 "[warmly] When you hold your breath, a gas called carbon dioxide builds up in your body.",
 "[warmly] Quand tu retiens ton souffle, un gaz appelé dioxyde de carbone s'accumule dans ton corps.",
 "[warmly] Quando você segura o ar, junta no seu corpo um gás chamado dióxido de carbono.",
 "[warmly] जब तुम साँस रोकते हो, तो शरीर में कार्बन डाइऑक्साइड नाम की गैस जमा होती है।")
line('E04_C28',
 "[calmly] El cerebro lo nota y se concentra en respirar bien. Las órdenes vuelven a salir en calma.",
 "[calmly] Your brain notices and focuses on breathing well. The orders come out calm again.",
 "[calmly] Le cerveau le remarque et se concentre sur la respiration. Les ordres redeviennent calmes.",
 "[calmly] O cérebro percebe e se concentra em respirar bem. As ordens voltam a sair com calma.",
 "[calmly] दिमाग़ इसे महसूस करता है और ठीक से साँस लेने पर ध्यान देता है। आदेश फिर शांत हो जाते हैं।")
line('E04_C29',
 "[softly] El diafragma recupera su ritmo: baja y sube suavecito. Y la puerta deja de dar portazos.",
 "[softly] The diaphragm finds its rhythm: down and up, nice and gentle. And the door stops slamming.",
 "[softly] Le diaphragme retrouve son rythme : il descend et monte tout doucement. Et la porte ne claque plus.",
 "[softly] O diafragma recupera o ritmo: desce e sobe bem devagarinho. E a porta para de bater.",
 "[softly] डायाफ्राम अपनी लय वापस पा लेता है: धीरे-धीरे नीचे और ऊपर। और दरवाज़ा धड़ाम करना बंद कर देता है।")
line('E04_C30',
 "[laughs] ¡Se fue! [happy] No era una rana, Pipo: era un músculo confundido. ¡Misterio resuelto, Plop!",
 "[laughs] It's gone! [happy] It wasn't a frog, Pipo: it was a confused muscle. Mystery solved, Plop!",
 "[laughs] Il est parti ! [happy] Pas une grenouille, Pipo : un muscle embrouillé. Mystère résolu, Plop !",
 "[laughs] Passou! [happy] Não era um sapinho, Pipo: era um músculo confuso. Mistério resolvido, Plop!",
 "[laughs] चली गई! [happy] वह मेंढक नहीं था, पीपो: वह एक उलझी हुई मांसपेशी थी। रहस्य सुलझ गया, प्लॉप!")
line('E04_L2',
 "[warmly] Repasemos: el nervio se confunde, el diafragma da un tirón y las cuerdas vocales hacen ¡hip!",
 "[warmly] Let's review: the nerve gets confused, the diaphragm tugs, and the vocal cords go hic!",
 "[warmly] On révise : le nerf s'embrouille, le diaphragme tire d'un coup et les cordes vocales font hic !",
 "[warmly] Vamos revisar: o nervo se confunde, o diafragma dá um puxão e as cordas vocais fazem hic!",
 "[warmly] चलो दोहराएँ: नस उलझती है, डायाफ्राम झटका देता है, और स्वर-तंतु करते हैं हिच!")
line('E04_C31',
 "[curious] Dato extra: no solo las personas tienen hipo. [happy] ¡Los perritos y los gatitos también!",
 "[curious] Bonus fact: people aren't the only ones who get hiccups. [happy] Puppies and kittens do too!",
 "[curious] Le savais-tu ? On n'est pas les seuls à avoir le hoquet. [happy] Les chiots et les chatons aussi !",
 "[curious] Curiosidade: não são só as pessoas que têm soluço. [happy] Os cachorrinhos e os gatinhos também!",
 "[curious] एक मज़ेदार बात: सिर्फ़ इंसानों को ही हिचकी नहीं आती। [happy] पिल्लों और बिल्ली के बच्चों को भी आती है!")
line('E04_C32',
 "[warmly] Hasta los bebés tienen hipo antes de nacer. Quizás así practican cómo respirar.",
 "[warmly] Even babies get hiccups before they're born. Maybe that's how they practice breathing.",
 "[warmly] Même les bébés ont le hoquet avant de naître : peut-être pour s'entraîner à respirer.",
 "[warmly] Até os bebês têm soluço antes de nascer. Talvez seja assim que eles treinam a respiração.",
 "[warmly] नन्हे शिशुओं को तो जन्म से पहले भी हिचकी आती है। शायद ऐसे ही वे साँस लेना सीखते हैं।")
line('E04_C33',
 "[warmly] Casi siempre el hipo se va solito en unos minutos. [playful] Mientras tanto, Plop tiene un reto.",
 "[warmly] Hiccups usually go away on their own in a few minutes. [playful] Meanwhile, Plop has a challenge.",
 "[warmly] Le hoquet part presque toujours tout seul en quelques minutes. [playful] En attendant, Plop a un défi.",
 "[warmly] Quase sempre o soluço passa sozinho em poucos minutos. [playful] Enquanto isso, o Plop tem um desafio.",
 "[warmly] ज़्यादातर हिचकी कुछ ही मिनटों में अपने आप चली जाती है। [playful] तब तक, प्लॉप के पास एक चुनौती है।")
line('E04_L3',
 "[warmly] Cuando tengas hipo, respira lento y cuenta los ¡hip! hasta que se vaya.",
 "[warmly] When you get hiccups, breathe slowly and count the hics until they're gone.",
 "[warmly] Quand tu as le hoquet, respire lentement et compte les hic jusqu'à ce qu'il parte.",
 "[warmly] Quando tiver soluço, respire devagar e conte os hics até ele passar.",
 "[warmly] जब हिचकी आए, धीरे साँस लो और हिच गिनते रहो, जब तक वह चली न जाए।")
line('E04_C34',
 "[curious] La próxima pregunta es de Pipo: ¿por qué flota el hielo si es sólido?",
 "[curious] The next question is from Pipo: why does ice float if it's solid?",
 "[curious] La prochaine question vient de Pipo : pourquoi la glace flotte-t-elle si elle est solide ?",
 "[curious] A próxima pergunta é do Pipo: por que o gelo flutua se ele é sólido?",
 "[curious] अगला सवाल पीपो का है: बर्फ़ ठोस है, फिर भी पानी पर क्यों तैरती है?")
line('CANAL_FINAL',
 "[warmly] La ciencia está en todas partes. [excited] ¡Hasta el próximo misterio!",
 "[warmly] Science is everywhere. [excited] See you at the next mystery!",
 "[warmly] La science est partout. [excited] À la prochaine énigme !",
 "[warmly] A ciência está em todo lugar. [excited] Até o próximo mistério!",
 "[warmly] विज्ञान हर जगह है। [excited] अगले रहस्य में मिलते हैं!")


# --- Ajustes tras la calibración (presupuesto de tiempo por idioma) ---
def fix(sid, lg, t): L[sid][lg] = t
fix('E04_C08','es',"[excited] ¡Esa es la pregunta correcta! El salto viene de un músculo que casi nadie conoce.")
fix('E04_L2','es',"[warmly] Repasemos: nervio confundido, tirón del diafragma… y las cuerdas vocales hacen ¡hip!")
fix('E04_L2','en',"[warmly] Let's review: a confused nerve, a diaphragm tug… and the vocal cords go hic!")
fix('E04_L2','fr',"[warmly] On révise : un nerf embrouillé, le diaphragme qui tire… et les cordes vocales font hic !")
fix('E04_L2','pt',"[warmly] Vamos revisar: nervo confuso, puxão do diafragma… e as cordas vocais fazem hic!")
fix('E04_L3','es',"[warmly] Cuando tengas hipo: respira lento y cuenta los ¡hip!")
fix('E04_L3','en',"[warmly] When you get hiccups: breathe slowly and count the hics.")
fix('E04_L3','fr',"[warmly] Quand tu as le hoquet : respire lentement et compte les hic.")
fix('E04_L3','pt',"[warmly] Quando tiver soluço: respire devagar e conte os hics.")
fix('E04_L3','hi',"[warmly] हिचकी आए तो: धीरे साँस लो और हिच गिनो।")
for lg,t in dict(es="¡Hasta el próximo misterio!", en="See you at the next mystery!", fr="À la prochaine énigme !",
                 pt="Até o próximo mistério!", hi="अगले रहस्य में मिलते हैं!").items():
    fix('CANAL_FINAL', lg, "[excited] " + t)
fix('E04_C24','en',"[curious] Pipo wants to know why it repeats. [warmly] The nerve is still confused, so it repeats the order.")
fix('E04_C05','pt',"[amused] Um sapo, a gente ouviria coaxar. E além disso… o Plop não comeu sapo. [playful] Eu acho.")
fix('E04_C15','pt',"[warmly] É o seu cérebro, por cabinhos chamados nervos. Ele manda a ordem sem você perceber.")
fix('E04_C33','pt',"[warmly] O soluço quase sempre passa sozinho em minutos. [playful] Enquanto isso, o Plop tem um desafio.")
fix('E04_C03','hi',"[curious] पीपो भी जानना चाहता है। [mischievously] आज हम कसूरवार ढूँढेंगे… तुम्हारी पसलियों के नीचे।")
fix('E04_C04','hi',"[mischievously] पीपो का मज़ेदार ख़याल: प्लॉप ने मेंढक निगल लिया, जो पेट में उछल रहा है!")
fix('E04_C05','hi',"[amused] मेंढक होता, तो टर्र-टर्र सुनाई देती। और प्लॉप ने मेंढक खाया ही नहीं… [playful] शायद।")
fix('E04_C07','hi',"[thoughtful] प्लॉप सोचता है: मैं उछलना नहीं चाहता, तो मेरा कौन सा हिस्सा उछल रहा है?")
fix('E04_C08','hi',"[excited] यही सही सवाल है! उछाल अंदर की एक मांसपेशी से आता है, जिसे कम लोग जानते हैं।")
fix('E04_C09','hi',"[curious] वह कौन सी है? तुम्हें क्या लगता है? सोचो… [excited] चलो सीने के अंदर देखें!")
fix('E04_C10','hi',"[excited] ज़ूम करो! ये हैं तुम्हारे फेफड़े: हवा से भरने वाली दो स्पंजी थैलियाँ।")
fix('E04_C12','hi',"[warmly] इसका नाम है डायाफ्राम। यह नीचे जाता है, तो जगह बनती है और हवा अंदर आती है।")
fix('E04_C13','hi',"[calmly] ऊपर जाकर यह हवा बाहर धकेलता है। नीचे-ऊपर, नीचे-ऊपर, पूरे दिन।")
fix('E04_C14','hi',"[curious] पीपो पूछता है: डायाफ्राम को हिलने का कौन कहता है? [playful] मैं तो नहीं कहता!")
fix('E04_C15','hi',"[warmly] यह तुम्हारा दिमाग़ करता है, नसों नाम की तारों से। वह चुपचाप आदेश भेजता है।")
fix('E04_C17','hi',"[playful] बिल्कुल। अगर तुम जल्दी-जल्दी खाओ, हवा निगलो, या बहुत ज़्यादा हँसो…")
fix('E04_C20','hi',"[surprised] झटका! [dramatically] डायाफ्राम आदेश मानकर नीचे खिंचता है… और हवा एकदम अंदर आती है।")
fix('E04_C22','hi',"[surprised] खट! [dramatically] स्वर-तंतु झट से बंद हो जाते हैं, जैसे हवा से दरवाज़ा।")
fix('E04_C23','hi',"[playful] यही धड़ाम हिचकी की आवाज़ है। हिच! यह आवाज़ नहीं, बंद होता दरवाज़ा है।")
fix('E04_C24','hi',"[curious] पीपो पूछता है, यह बार-बार क्यों? [warmly] क्योंकि उलझी हुई नस वही आदेश दोहराती है।")
fix('E04_C28','hi',"[calmly] दिमाग़ इसे भाँपकर साँसों पर ध्यान देता है। आदेश फिर शांत हो जाते हैं।")
fix('E04_C29','hi',"[softly] डायाफ्राम फिर लय में आ जाता है: धीरे नीचे, धीरे ऊपर। दरवाज़े की धड़ाम बंद!")
fix('E04_C30','hi',"[laughs] चली गई! [happy] मेंढक नहीं, पीपो: एक उलझी मांसपेशी थी। रहस्य सुलझ गया!")
fix('E04_C31','hi',"[curious] मज़ेदार बात: [happy] पिल्लों और बिल्लियों को भी हिचकी आती है!")
fix('E04_C32','hi',"[warmly] शिशुओं को तो जन्म से पहले भी हिचकी आती है। शायद ऐसे वे साँस लेना सीखते हैं।")
fix('E04_C18','fr',"[warmly] Alors, ton estomac gonfle… et il chatouille le nerf qui passe juste à côté.")
fix('E04_C22','fr',"[surprised] Clac ! [dramatically] Le passage des cordes vocales se ferme d'un coup, comme une porte qui claque au vent.")
fix('E04_C05','pt',"[amused] Se fosse um sapo, ia coaxar. E o Plop não comeu sapo nenhum… [playful] eu acho.")
fix('E04_C18','pt',"[curious] O seu estômago incha e faz cócegas no nervo que passa bem do lado.")
fix('E04_C30','pt',"[laughs] Passou! [happy] Não era sapo, Pipo: era um músculo confuso. Mistério resolvido!")
fix('E04_L2','hi',"[warmly] नस उलझती है, डायाफ्राम झटका देता है, और स्वर-तंतु करते हैं हिच!")
fix('E04_C33','hi',"[warmly] हिचकी अक्सर कुछ मिनट में खुद चली जाती है। [playful] तब तक प्लॉप की एक चुनौती है।")

VIDEO_END = 7199 / 24  # 299.958 s, duración real del video
out = []
for s in SHOTS:
    sid = s['id']; t0, t1 = [ts(x) for x in s['t'].replace('–', '-').split('-')]
    t1 = min(t1, VIDEO_END)
    still = 'still' in s['cls']
    lo = 0.1 if L[sid]['anchors'] else (0.2 if sid.startswith('CANAL') else 0.3)
    hi = (t1 - t0) - (0.12 if sid == 'CANAL_FINAL' else 0.4)
    out.append(dict(id=sid, t0=t0, t1=t1, win=[lo, round(hi, 3)], still=still, **L[sid]))
assert len(out) == 39 and len(L) == 39
spoken = lambda t: re.sub(r'\[[^\]]*\]\s*', '', t)
json.dump(dict(lines=out, hic=HIC), open('guion.json', 'w'), ensure_ascii=False, indent=1)
for lg in 'es en fr pt hi'.split():
    print(lg, sum(len(o[lg]) for o in out), 'chars con etiquetas,', sum(len(spoken(o[lg])) for o in out), 'hablados')
