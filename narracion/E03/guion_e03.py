# Guion de narración del Ep. 3 (¿Por qué pica el ají si no está caliente?) en 5 idiomas, una frase por toma.
# Base: la narración corregida en español (E03_guion_narracion.txt), que ya coincide con el video.
# Las etiquetas [..] son dirección de voz para Eleven v4 (no se pronuncian).
import json, re

SHOTS = json.load(open('../shots.json'))['shots']

def ts(x):
    m, s = x.split(':'); return int(m) * 60 + int(s)

L = {}
def line(sid, es, en, fr, pt, hi, anchors=None):
    L[sid] = dict(es=es, en=en, fr=fr, pt=pt, hi=hi, anchors=anchors or [])

line('E03_C01',
 "[gasps] Un mordisquito a este ají y… ¡fuego en la boca! Pero espera: el ají no está caliente.",
 "[gasps] One little bite of this chili and… fire in your mouth! But wait: the chili isn't hot.",
 "[gasps] Une petite bouchée de ce piment et… le feu dans la bouche ! Mais attends : le piment n'est pas chaud.",
 "[gasps] Uma mordidinha nesta pimenta e… fogo na boca! Mas espera: a pimenta não está quente.",
 "[gasps] इस मिर्च का एक छोटा सा टुकड़ा और… मुँह में आग! पर रुको: मिर्च गरम नहीं है।")
line('E03_C02',
 "[curious] Tócalo: está frío. No hay llamas ni humo. Entonces, ¿por qué sentimos que la boca arde?",
 "[curious] Touch it: it's cold. No flames, no smoke. So why does it feel like your mouth is burning?",
 "[curious] Touche-le : il est froid. Ni flammes ni fumée. Alors, pourquoi la bouche semble brûler ?",
 "[curious] Toque nela: está fria. Sem chamas, sem fumaça. Então, por que a boca parece arder?",
 "[curious] छूकर देखो: यह ठंडी है। न आग, न धुआँ। तो फिर मुँह क्यों जलता हुआ लगता है?")
line('E03_C03',
 "[mischievously] Plop sospecha que aquí hay un truco. Y tiene razón: el ají es un gran mentiroso.",
 "[mischievously] Plop suspects there's a trick here. And he's right: the chili is a big fibber.",
 "[mischievously] Plop soupçonne un tour de passe-passe. Et il a raison : le piment est un grand menteur.",
 "[mischievously] O Plop desconfia que tem truque aqui. E ele tem razão: a pimenta é uma grande mentirosa.",
 "[mischievously] प्लॉप को लगता है कि यहाँ कोई चाल है। और वह सही है: मिर्च बड़ी झूठी है।")
line('CANAL_INICIO',
 "[excited] ¡La ciencia con Pipo y Plop!",
 "[excited] Science with Pipo and Plop!",
 "[excited] La science avec Pipo et Plop !",
 "[excited] A ciência com Pipo e Plop!",
 "[excited] पीपो और प्लॉप के साथ विज्ञान!")
line('E03_C04',
 "[mischievously] La idea loca de Pipo: ¡dentro del ají vive un dragón chiquito que escupe fuego!",
 "[mischievously] Pipo's wild idea: inside the chili lives a tiny dragon that breathes fire!",
 "[mischievously] L'idée folle de Pipo : dans le piment vit un minuscule dragon qui crache du feu !",
 "[mischievously] A ideia maluca do Pipo: dentro da pimenta mora um dragãozinho que cospe fogo!",
 "[mischievously] पीपो का मज़ेदार ख़याल: मिर्च के अंदर एक नन्हा ड्रैगन रहता है जो आग उगलता है!")
line('E03_C05',
 "[playful] Si hubiera fuego de verdad, el ají echaría humo y quemaría el plato. Y está fresquito.",
 "[playful] If there were real fire, the chili would smoke and burn the plate. And it's nice and cool.",
 "[playful] S'il y avait du vrai feu, le piment fumerait et brûlerait l'assiette. Et il est tout frais.",
 "[playful] Se fosse fogo de verdade, a pimenta faria fumaça e queimaria o prato. E está fresquinha.",
 "[playful] अगर सच में आग होती, तो मिर्च से धुआँ निकलता और प्लेट जल जाती। पर यह तो ठंडी है।")
line('E03_C06',
 "Segunda idea: apagarlo con agua, como una fogata. Pero… [surprised] ¡el picor se riega por toda la boca!",
 "Second idea: put it out with water, like a campfire. But… [surprised] the burn spreads all over his mouth!",
 "Deuxième idée : l'éteindre avec de l'eau, comme un feu de camp. Mais… [surprised] ça pique dans toute la bouche !",
 "Segunda ideia: apagar com água, como uma fogueira. Mas… [surprised] a ardência se espalha pela boca toda!",
 "दूसरा ख़याल: पानी से बुझाओ, अलाव की तरह। लेकिन… [surprised] तीखापन पूरे मुँह में फैल गया!")
line('E03_C07',
 "[thoughtful] Plop se pregunta: si el agua apaga el fuego de verdad, ¿por qué no apaga este?",
 "[thoughtful] Plop wonders: if water puts out real fire, why doesn't it put out this one?",
 "[thoughtful] Plop se demande : si l'eau éteint le vrai feu, pourquoi n'éteint-elle pas celui-ci ?",
 "[thoughtful] O Plop se pergunta: se a água apaga o fogo de verdade, por que não apaga este?",
 "[thoughtful] प्लॉप सोचता है: अगर पानी असली आग बुझा देता है, तो यह वाली क्यों नहीं बुझती?")
line('E03_C08',
 "[excited] ¡Gran pista, Plop! Si el agua no lo apaga, quizá no es fuego. Quizá es otra cosa.",
 "[excited] Great clue, Plop! If water can't put it out, maybe it isn't fire. Maybe it's something else.",
 "[excited] Super indice, Plop ! Si l'eau ne l'éteint pas, ce n'est peut-être pas du feu. C'est autre chose.",
 "[excited] Ótima pista, Plop! Se a água não apaga, talvez não seja fogo. Talvez seja outra coisa.",
 "[excited] बढ़िया सुराग, प्लॉप! अगर पानी से नहीं बुझती, तो शायद यह आग है ही नहीं। कुछ और है।")
line('E03_C09',
 "[curious] ¿Qué será lo que nos engaña? ¿Tú qué crees? Piénsalo… [excited] ¡Vamos a abrir el ají!",
 "[curious] What could be tricking us? What do you think? Think about it… [excited] Let's open the chili!",
 "[curious] Qu'est-ce qui nous trompe ? À ton avis ? Réfléchis… [excited] Ouvrons le piment !",
 "[curious] O que será que nos engana? O que você acha? Pensa… [excited] Vamos abrir a pimenta!",
 "[curious] हमें क्या धोखा दे रहा है? तुम्हें क्या लगता है? सोचो… [excited] चलो मिर्च खोलते हैं!")
line('E03_C10',
 "[excited] ¡Hagamos zoom! Dentro del ají hay semillas y venitas blancas. Ahí se esconde el culpable.",
 "[excited] Let's zoom in! Inside the chili are seeds and little white veins. The culprit hides there.",
 "[excited] Zoomons ! Dans le piment, il y a des graines et de petites veines blanches. Le coupable s'y cache.",
 "[excited] Vamos dar zoom! Dentro da pimenta tem sementes e veinhas brancas. O culpado se esconde ali.",
 "[excited] चलो ज़ूम करें! मिर्च के अंदर बीज और सफ़ेद नसें हैं। असली कसूरवार वहीं छिपा है।")
line('E03_C11',
 "Se llama capsaicina: una sustancia aceitosa e invisible. La pintamos de amarillo para verla.",
 "It's called capsaicin: an oily, invisible substance. We painted it yellow so we can see it.",
 "Elle s'appelle la capsaïcine : une substance huileuse et invisible. On l'a peinte en jaune pour la voir.",
 "Ela se chama capsaicina: uma substância oleosa e invisível. Pintamos de amarelo para ver.",
 "इसका नाम है कैप्सेसिन: एक तैलीय और अदृश्य पदार्थ। देखने के लिए हमने इसे पीला रंग दिया है।")
line('E03_C12',
 "Plop también probó un poquito y saca la lengua: mira, está llena de botones de alarma diminutos.",
 "Plop tried a little bit too, and sticks out his tongue: look, it's full of tiny alarm buttons.",
 "Plop a goûté aussi et tire la langue : regarde, elle est pleine de minuscules boutons d'alarme.",
 "O Plop também provou um pouquinho e mostra a língua: olha, ela está cheia de botõezinhos de alarme.",
 "प्लॉप ने भी थोड़ा चखा और जीभ निकाली: देखो, इस पर अलार्म के नन्हे-नन्हे बटन हैं।")
line('E03_C13',
 "Su trabajo es avisar del calor. Si la sopa quema, se encienden y gritan: [dramatically] ¡cuidado!",
 "Their job is to warn about heat. If soup is too hot, they light up and shout: [dramatically] careful!",
 "Leur travail : prévenir de la chaleur. Si la soupe brûle, ils s'allument et crient : [dramatically] attention !",
 "O trabalho deles é avisar do calor. Se a sopa queima, eles acendem e gritam: [dramatically] cuidado!",
 "उनका काम है गर्मी की चेतावनी देना। सूप गरम हो, तो वे जलकर चिल्लाते हैं: [dramatically] सावधान!")
line('E03_L1',
 "Capsaicina en el ají, botones en la lengua de Plop. [curious] ¿Y si se encuentran?",
 "Capsaicin in the chili, buttons on Plop's tongue. [curious] What if they meet?",
 "Capsaïcine dans le piment, boutons sur la langue de Plop. [curious] Et s'ils se rencontrent ?",
 "Capsaicina na pimenta, botões na língua do Plop. [curious] E se eles se encontrarem?",
 "मिर्च में कैप्सेसिन, प्लॉप की जीभ पर बटन। [curious] अगर दोनों मिल जाएँ तो?")
line('E03_C14',
 "Pipo pregunta cómo se llaman esos botones. [playful] Tienen nombre de robot: te erre pe uve uno.",
 "Pipo asks what those buttons are called. [playful] They have a robot name: T-R-P-V-one.",
 "Pipo demande comment s'appellent ces boutons. [playful] Ils ont un nom de robot : T-R-P-V-un.",
 "O Pipo pergunta como se chamam esses botões. [playful] Eles têm nome de robô: tê-erre-pê-vê-um.",
 "पीपो पूछता है कि इन बटनों का नाम क्या है। [playful] इनका नाम रोबोट जैसा है: टी-आर-पी-वी-वन।")
line('E03_C15',
 "Y aquí está el truco: [mischievously] la capsaicina tiene justo la forma de la llave de esos botones.",
 "And here's the trick: [mischievously] capsaicin has exactly the shape of the key to those buttons.",
 "Et voici l'astuce : [mischievously] la capsaïcine a exactement la forme de la clé de ces boutons.",
 "E aqui está o truque: [mischievously] a capsaicina tem exatamente o formato da chave desses botões.",
 "और यही है चाल: [mischievously] कैप्सेसिन का आकार ठीक उन बटनों की चाबी जैसा है।")
line('E03_C16',
 "Plop ya lo ve venir: una llave falsa… [dramatically] ¡va a encender la alarma sin que haya calor!",
 "Plop sees it coming: a fake key… [dramatically] it's going to set off the alarm with no heat at all!",
 "Plop le voit venir : une fausse clé… [dramatically] elle va déclencher l'alarme sans aucune chaleur !",
 "O Plop já sacou: uma chave falsa… [dramatically] vai disparar o alarme sem ter calor nenhum!",
 "प्लॉप समझ गया: एक नकली चाबी… [dramatically] बिना गर्मी के ही अलार्म बजा देगी!")
line('E03_C17',
 "Eso es justo lo que pasa. La capsaicina toca el botón de Plop, y se enciende por error.",
 "That's exactly what happens. Capsaicin touches Plop's button, and it switches on by mistake.",
 "C'est exactement ça. La capsaïcine touche le bouton de Plop, et il s'allume par erreur.",
 "É exatamente isso que acontece. A capsaicina toca o botão do Plop, e ele acende por engano.",
 "ठीक यही होता है। कैप्सेसिन प्लॉप के बटन को छूता है, और बटन ग़लती से जल उठता है।")
line('E03_C18',
 "El botón manda un aviso urgente por los nervios, como por un cable, hasta la cabeza de Plop.",
 "The button sends an urgent message along the nerves, like down a wire, all the way to Plop's head.",
 "Le bouton envoie un message urgent par les nerfs, comme par un fil, jusqu'à la tête de Plop.",
 "O botão manda um aviso urgente pelos nervos, como por um fio, até a cabeça do Plop.",
 "बटन नसों से होकर, जैसे किसी तार से, प्लॉप के सिर तक एक ज़रूरी संदेश भेजता है।")
line('E03_C19',
 "Su cerebro recibe el aviso: [dramatically] ¡alarma, aquí hay algo muy caliente! [playful] Aunque no sea verdad.",
 "His brain gets the message: [dramatically] alarm, something very hot is here! [playful] Even though it isn't true.",
 "Son cerveau reçoit le message : [dramatically] alerte, il y a quelque chose de très chaud ! [playful] Même si c'est faux.",
 "O cérebro dele recebe o aviso: [dramatically] alarme, tem algo muito quente aqui! [playful] Mesmo que não seja verdade.",
 "उसका दिमाग़ संदेश पाता है: [dramatically] ख़तरा, यहाँ कुछ बहुत गरम है! [playful] भले ही यह सच न हो।")
line('E03_C20',
 "A Pipo le pasa lo mismo: su cerebro se lo cree todo y siente fuego donde no hay.",
 "The same thing happens to Pipo: his brain believes it all and feels fire where there is none.",
 "Pareil pour Pipo : son cerveau y croit complètement et sent du feu là où il n'y en a pas.",
 "Com o Pipo acontece o mesmo: o cérebro dele acredita em tudo e sente fogo onde não tem.",
 "पीपो के साथ भी यही होता है: उसका दिमाग़ सब मान लेता है और बिना आग के आग महसूस करता है।")
line('E03_C21',
 "Y como su cerebro cree que se quema, intenta enfriarlo: [laughs] ¡mira cómo suda Pipo!",
 "And since his brain thinks he's burning, it tries to cool him down: [laughs] look at Pipo sweat!",
 "Et comme son cerveau croit qu'il brûle, il essaie de le refroidir : [laughs] regarde Pipo transpirer !",
 "E como o cérebro acha que ele está queimando, tenta esfriar: [laughs] olha como o Pipo sua!",
 "और दिमाग़ को लगता है कि वह जल रहा है, तो उसे ठंडा करने लगता है: [laughs] देखो पीपो को पसीना!")
line('E03_C22',
 "[worried] Plop pregunta lo que todos pensamos: entonces… ¿mi lengua se está quemando o no?",
 "[worried] Plop asks what we're all thinking: so… is my tongue burning or not?",
 "[worried] Plop pose la question que tout le monde se pose : alors… ma langue brûle ou pas ?",
 "[worried] O Plop pergunta o que todos pensamos: então… minha língua está queimando ou não?",
 "[worried] प्लॉप वही पूछता है जो हम सब सोच रहे हैं: तो… मेरी जीभ जल रही है या नहीं?")
line('E03_C23',
 "[warmly] ¡No, Plop! Tu lengua está perfecta. Es una falsa alarma: el ají engaña a tus sensores.",
 "[warmly] No, Plop! Your tongue is perfectly fine. It's a false alarm: the chili tricks your sensors.",
 "[warmly] Non, Plop ! Ta langue va très bien. C'est une fausse alerte : le piment trompe tes capteurs.",
 "[warmly] Não, Plop! Sua língua está perfeita. É um alarme falso: a pimenta engana seus sensores.",
 "[warmly] नहीं, प्लॉप! तुम्हारी जीभ ठीक है। यह झूठा अलार्म है: मिर्च सेंसरों को धोखा देती है।")
line('E03_C24',
 "[curious] ¿Y el agua? La capsaicina es aceitosa, y el agua resbala sobre el aceite. Solo la pasea.",
 "[curious] And the water? Capsaicin is oily, and water slides right over oil. It just moves it around.",
 "[curious] Et l'eau ? La capsaïcine est huileuse, et l'eau glisse sur l'huile. Elle la promène, c'est tout.",
 "[curious] E a água? A capsaicina é oleosa, e a água escorrega no óleo. Ela só espalha.",
 "[curious] और पानी? कैप्सेसिन तैलीय है, और पानी तेल पर फिसल जाता है। बस उसे इधर-उधर ले जाता है।")
line('E03_C25',
 "Por eso, después del agua, [surprised] ¡pica en más lugares! Pipo necesita otro plan… y rápido.",
 "That's why, after water, [surprised] it burns in even more places! Pipo needs a new plan… and fast.",
 "Voilà pourquoi, après l'eau, [surprised] ça pique à plus d'endroits ! Pipo a besoin d'un autre plan… et vite.",
 "Por isso, depois da água, [surprised] arde em mais lugares! O Pipo precisa de outro plano… e rápido.",
 "इसीलिए पानी के बाद [surprised] और ज़्यादा जगह तीखा लगता है! पीपो को नई तरकीब चाहिए… और जल्दी।")
line('E03_C26',
 "[excited] Plop tiene la solución: leche. [curious] ¿Qué tendrá la leche que no tiene el agua?",
 "[excited] Plop has the answer: milk. [curious] What does milk have that water doesn't?",
 "[excited] Plop a la solution : le lait. [curious] Qu'est-ce que le lait a de plus que l'eau ?",
 "[excited] O Plop tem a solução: leite. [curious] O que será que o leite tem que a água não tem?",
 "[excited] प्लॉप के पास हल है: दूध। [curious] दूध में ऐसा क्या है जो पानी में नहीं?")
line('E03_C27',
 "Tiene caseína: una proteína que adora las grasas y atrapa a la capsaicina como un imán.",
 "It has casein: a protein that loves fats and grabs capsaicin like a magnet.",
 "Il contient de la caséine : une protéine qui adore les graisses et attrape la capsaïcine comme un aimant.",
 "Ele tem caseína: uma proteína que adora gordura e prende a capsaicina como um ímã.",
 "इसमें केसीन है: चिकनाई पसंद करने वाला प्रोटीन, जो कैप्सेसिन को चुंबक की तरह पकड़ता है।")
line('E03_C28',
 "La despega de los botones de Plop y se la lleva. [relieved] Se apagan… y la alarma termina.",
 "It pulls it off Plop's buttons and carries it away. [relieved] They switch off… and the alarm stops.",
 "Elle la décolle des boutons de Plop et l'emporte. [relieved] Ils s'éteignent… et l'alarme s'arrête.",
 "Ela solta a capsaicina dos botões do Plop e leva embora. [relieved] Eles apagam… e o alarme para.",
 "यह उसे प्लॉप के बटनों से छुड़ाकर ले जाता है। [relieved] बटन बुझ जाते हैं… और अलार्म बंद।")
line('E03_C29',
 "[sighs] ¡Qué alivio! No había dragón, Pipo: era una llave falsa encendiendo tus sensores.",
 "[sighs] What a relief! There was no dragon, Pipo: just a fake key switching on your heat sensors.",
 "[sighs] Quel soulagement ! Pas de dragon, Pipo : juste une fausse clé qui allumait tes capteurs.",
 "[sighs] Que alívio! Não tinha dragão, Pipo: era uma chave falsa acendendo seus sensores.",
 "[sighs] कितनी राहत! कोई ड्रैगन नहीं था, पीपो: बस एक नकली चाबी तुम्हारे सेंसर जला रही थी।")
line('E03_C30',
 "[warmly] Tu pista era buena, Plop: no era fuego, era un aceite. Y a ese lo atrapa la leche.",
 "[warmly] Your clue was good, Plop: it wasn't fire, it was an oil. And milk catches that.",
 "[warmly] Ton indice était bon, Plop : ce n'était pas du feu, c'était une huile. Et le lait l'attrape.",
 "[warmly] Sua pista era boa, Plop: não era fogo, era um óleo. E o leite pega ele.",
 "[warmly] तुम्हारा सुराग सही था, प्लॉप: वह आग नहीं, तेल था। और उसे दूध पकड़ लेता है।")
line('E03_L2',
 "[warmly] Repasemos: la capsaicina engaña a tus sensores, el agua la pasea y la leche la atrapa.",
 "[warmly] Let's review: capsaicin tricks your sensors, water moves it around, and milk catches it.",
 "[warmly] Résumons : la capsaïcine trompe tes capteurs, l'eau la promène et le lait l'attrape.",
 "[warmly] Vamos revisar: a capsaicina engana seus sensores, a água espalha e o leite prende.",
 "[warmly] चलो दोहराएँ: कैप्सेसिन सेंसरों को धोखा देता है, पानी उसे फैलाता है, और दूध उसे पकड़ता है।")
line('E03_C31',
 "[curious] Dato extra: a los pájaros el ají no les pica nada. Sus sensores no reconocen esa llave.",
 "[curious] Bonus fact: chili isn't spicy at all for birds. Their sensors don't recognize that key.",
 "[curious] Petit bonus : le piment ne pique pas du tout les oiseaux. Leurs capteurs ne reconnaissent pas cette clé.",
 "[curious] Curiosidade: pimenta não arde nada para os passarinhos. Os sensores deles ignoram essa chave.",
 "[curious] मज़ेदार बात: पक्षियों को मिर्च बिल्कुल तीखी नहीं लगती। उनके सेंसर वह चाबी नहीं पहचानते।")
line('E03_C32',
 "[warmly] Y eso le conviene a la planta: los pájaros se llevan sus semillas volando a otros lugares.",
 "[warmly] And that helps the plant: birds carry its seeds away, flying to new places.",
 "[warmly] Et ça arrange la plante : les oiseaux emportent ses graines en volant vers d'autres endroits.",
 "[warmly] E isso é bom para a planta: os passarinhos levam as sementes voando para outros lugares.",
 "[warmly] और इससे पौधे का फ़ायदा है: पक्षी उसके बीज उड़कर दूसरी जगहों पर ले जाते हैं।")
line('E03_C33',
 "El picante es el truco del ají para elegir quién se lo come. [excited] Y ahora, un reto.",
 "Spiciness is the chili's trick for choosing who eats it. [excited] And now, a challenge.",
 "Le piquant, c'est l'astuce du piment pour choisir qui le mange. [excited] Et maintenant, un défi.",
 "A ardência é o truque da pimenta para escolher quem come ela. [excited] E agora, um desafio.",
 "तीखापन मिर्च की चाल है, यह चुनने की कि उसे कौन खाए। [excited] और अब, एक चुनौती।")
line('E03_L3',
 "[playful] ¿Quién aguanta más picante en casa? Cuéntales el secreto de la leche.",
 "[playful] Who at home can handle the most spice? Tell them the milk secret.",
 "[playful] Qui supporte le mieux le piquant chez toi ? Raconte-leur le secret du lait.",
 "[playful] Quem em casa aguenta mais pimenta? Conte o segredo do leite.",
 "[playful] घर में कौन ज़्यादा तीखा सह सकता है? उन्हें दूध का राज़ बताओ।")
line('E03_C34',
 "[curious] La próxima pregunta es de Plop: ¿qué es el hipo y por qué no lo puedes parar?",
 "[curious] The next question is Plop's: what are hiccups, and why can't you stop them?",
 "[curious] La prochaine question vient de Plop : c'est quoi le hoquet, et pourquoi on ne peut pas l'arrêter ?",
 "[curious] A próxima pergunta é do Plop: o que é o soluço, e por que você não consegue parar?",
 "[curious] अगला सवाल प्लॉप का है: हिचकी क्या है, और तुम उसे रोक क्यों नहीं पाते?")
line('CANAL_FINAL',
 "[excited] ¡Hasta el próximo misterio!",
 "[excited] See you at the next mystery!",
 "[excited] À la prochaine énigme !",
 "[excited] Até o próximo mistério!",
 "[excited] अगले रहस्य में मिलते हैं!")

def fix(sid, lg, text): L[sid][lg] = text
# (retoques tras escuchar / medir van aquí)
fix('E03_L2','hi',"[warmly] कैप्सेसिन सेंसरों को धोखा देता है, पानी उसे फैलाता है, दूध उसे पकड़ता है।")  # la voz omitió «दोहराएँ»; el guion refleja lo que se oye
fix('E03_C11','fr',"Elle s'appelle la capsaïcine : une substance huileuse et invisible. Ici, on la montre en jaune pour la voir.")
fix('E03_C33','fr',"Le goût piquant, c'est l'astuce du piment pour choisir qui le mange. [excited] Et maintenant, un défi.")
fix('E03_C29','hi',"[sighs] कितनी राहत! ड्रैगन नहीं था, पीपो: बस नकली चाबी सेंसर जला रही थी।")
fix('E03_L1','es',"Capsaicina en el ají, botones en la lengua. [curious] ¿Y si se encuentran?")
fix('E03_C12','es',"Plop también probó y saca la lengua: mira, está llena de botones de alarma diminutos.")
fix('E03_C12','pt',"O Plop também provou e mostra a língua: olha, ela está cheia de botõezinhos de alarme.")
fix('E03_L1','pt',"Capsaicina na pimenta, botões na língua. [curious] E se eles se encontrarem?")
fix('E03_C11','hi',"इसका नाम है कैप्सेसिन: एक तैलीय, अदृश्य पदार्थ। हमने इसे पीला रंग दिया है।")
fix('E03_L1','hi',"मिर्च में कैप्सेसिन, जीभ पर बटन। [curious] अगर दोनों मिलें तो?")
fix('E03_C20','hi',"पीपो का दिमाग़ भी यही मान लेता है, और बिना आग के आग महसूस करता है।")
fix('E03_C24','hi',"[curious] और पानी? कैप्सेसिन तैलीय है, और पानी तेल पर फिसल जाता है। बस उसे फैला देता है।")
fix('E03_C27','hi',"इसमें केसीन है: चिकनाई पसंद प्रोटीन, जो कैप्सेसिन को चुंबक की तरह पकड़ता है।")
fix('E03_C31','hi',"[curious] मज़ेदार बात: पक्षियों को मिर्च तीखी नहीं लगती। उनके सेंसर वह चाबी नहीं पहचानते।")

VIDEO_END = 300.0
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
json.dump(dict(lines=out, hic={}), open('guion.json', 'w'), ensure_ascii=False, indent=1)
RATE = dict(es=12.6, en=13.3, fr=15.3, pt=12.8, hi=10.9)   # caracteres hablados por segundo (medido en el Ep. 4)
if __name__ == '__main__':
    for lg in RATE:
        risk = []
        for o in out:
            est = len(spoken(o[lg])) / RATE[lg]; w = o['win'][1] - o['win'][0]
            if est > w * 1.0: risk.append(f"{o['id']}:{est/w:.2f}")
        print(lg, sum(len(spoken(o[lg])) for o in out), 'chars | en riesgo:', ' '.join(risk) or 'ninguna')
