# Guion de narración del Ep. 2 (¿Por qué el jabón quita la grasa y el agua no?) en 5 idiomas, una frase por toma.
# Base: la narración en español de la guía (shots.json), revisada toma por toma contra el video:
#  - C34: en pantalla se despide Plop, así que la próxima pregunta la deja Plop (no Pipo).
#  - C27: «el agua ya no resbala… ¡se lleva la grasa!» (antes decía que la grasa no resbalaba).
#  - L1, L2 y L3 siguen los rótulos de cada lámina; L1, L3, CANAL_FINAL y las frases largas se acortan para caber.
# Las etiquetas [..] son dirección de voz para Eleven v4 (no se pronuncian).
import json, re

SHOTS = json.load(open('../shots.json'))['shots']

def ts(x):
    m, s = x.split(':'); return int(m) * 60 + int(s)

L = {}
def line(sid, es, en, fr, pt, hi):
    L[sid] = dict(es=es, en=en, fr=fr, pt=pt, hi=hi, anchors=[])

line('E02_C01',
 "[gasps] ¡Ups! Plop tiene una mancha de grasa. Y el agua sola… no le hace ni cosquillas.",
 "[gasps] Oops! Plop has a grease stain. And water alone… doesn't even tickle it.",
 "[gasps] Oups ! Plop a une tache de gras. Et l'eau toute seule… ne la chatouille même pas.",
 "[gasps] Opa! O Plop tem uma mancha de gordura. E a água sozinha… nem faz cócegas nela.",
 "[gasps] उफ़! प्लॉप पर चिकनाई का दाग है। और अकेला पानी… उसे गुदगुदी तक नहीं करता।")
line('E02_C02',
 "[curious] Pero con jabón, la grasa se rinde enseguida. ¿Qué tiene el jabón que no tenga el agua?",
 "[curious] But with soap, the grease gives up right away. What does soap have that water doesn't?",
 "[curious] Mais avec du savon, le gras abandonne tout de suite. Qu'a le savon que l'eau n'a pas ?",
 "[curious] Mas com sabão, a gordura desiste na hora. O que o sabão tem que a água não tem?",
 "[curious] पर साबुन से चिकनाई फ़ौरन हार जाती है। साबुन में क्या है जो पानी में नहीं?")
line('E02_C03',
 "[playful] Pipo ya tiene una teoría. Y es bastante loca. ¿Listos para investigar?",
 "[playful] Pipo already has a theory. And it's pretty wild. Ready to investigate?",
 "[playful] Pipo a déjà une théorie. Et elle est plutôt folle. Prêts à enquêter ?",
 "[playful] O Pipo já tem uma teoria. E é bem maluca. Prontos para investigar?",
 "[playful] पीपो के पास पहले से एक थ्योरी है। और वह काफ़ी अजीब है। जाँच के लिए तैयार?")
line('CANAL_INICIO',
 "[excited] ¡La ciencia con Pipo y Plop!",
 "[excited] Science with Pipo and Plop!",
 "[excited] La science avec Pipo et Plop !",
 "[excited] A ciência com Pipo e Plop!",
 "[excited] पीपो और प्लॉप के साथ विज्ञान!")
line('E02_C04',
 "[mischievously] La idea loca de Pipo: el jabón gana porque huele rico, ¡y la grasa huye del perfume!",
 "[mischievously] Pipo's wild idea: soap wins because it smells nice, and grease runs from perfume!",
 "[mischievously] L'idée folle de Pipo : le savon gagne parce qu'il sent bon, et le gras fuit le parfum !",
 "[mischievously] A ideia maluca do Pipo: o sabão ganha porque é cheiroso, e a gordura foge do perfume!",
 "[mischievously] पीपो का ख़याल: साबुन की ख़ुशबू से चिकनाई डरकर भाग जाती है!")
line('E02_C05',
 "[playful] Probemos: una flor también huele rico… y la grasa ni se mueve. No es el olor.",
 "[playful] Let's test it: a flower smells nice too… and the grease doesn't budge. It's not the smell.",
 "[playful] Testons : une fleur sent bon aussi… et le gras ne bouge pas. Ce n'est pas l'odeur.",
 "[playful] Vamos testar: uma flor também é cheirosa… e a gordura nem se mexe. Não é o cheiro.",
 "[playful] चलो परखें: फूल भी ख़ुशबूदार है… पर चिकनाई हिलती तक नहीं। तो ख़ुशबू नहीं है।")
line('E02_C06',
 "¿Y frotar con más fuerza? [sighs] Tampoco: la grasa solo se embarra más.",
 "And scrubbing harder? [sighs] No luck: the grease just smears even more.",
 "Et frotter plus fort ? [sighs] Non plus : le gras s'étale encore plus.",
 "E esfregar com mais força? [sighs] Também não: a gordura só se espalha mais.",
 "और ज़ोर से रगड़ें? [sighs] नहीं: चिकनाई बस और फैल जाती है।")
line('E02_C07',
 "[thoughtful] Plop se pregunta: ¿por qué el agua ni siquiera se queda sobre la grasa? ¡Se resbala!",
 "[thoughtful] Plop wonders: why won't water even stay on the grease? It just slides off!",
 "[thoughtful] Plop se demande : pourquoi l'eau ne reste même pas sur le gras ? Elle glisse !",
 "[thoughtful] O Plop se pergunta: por que a água nem fica em cima da gordura? Ela escorrega!",
 "[thoughtful] प्लॉप सोचता है: पानी चिकनाई पर टिकता क्यों नहीं? वह फिसल जाता है!")
line('E02_C08',
 "[warmly] Buena observación. El agua y la grasa son como dos equipos que jamás se dan la mano.",
 "[warmly] Good observation. Water and grease are like two teams that never shake hands.",
 "[warmly] Bien observé. L'eau et le gras sont comme deux équipes qui ne se serrent jamais la main.",
 "[warmly] Boa observação. A água e a gordura são como dois times que nunca se dão as mãos.",
 "[warmly] बढ़िया बात पकड़ी। पानी और चिकनाई दो ऐसी टीमें हैं जो कभी हाथ नहीं मिलातीं।")
line('E02_C09',
 "[curious] ¿Cómo logra el jabón juntarlos? ¿Tú qué crees? Piénsalo… [excited] ¡Vamos a mirarlo de cerca!",
 "[curious] How does soap join them? What do you think? Think… [excited] Let's look up close!",
 "[curious] Comment le savon les réunit-il ? À ton avis ? Réfléchis… [excited] Regardons de plus près !",
 "[curious] Como o sabão junta os dois? O que você acha? Pensa… [excited] Vamos olhar de perto!",
 "[curious] साबुन इन्हें कैसे मिलाता है? तुम्हें क्या लगता है? सोचो… [excited] चलो पास से देखें!")
line('E02_C10',
 "[excited] ¡Hagamos zoom! Esto es un pedacito de jabón, tan pequeño que ningún ojo puede verlo.",
 "[excited] Let's zoom in! This is a tiny piece of soap, so small no eye can see it.",
 "[excited] Zoomons ! Voici un minuscule morceau de savon, si petit qu'aucun œil ne peut le voir.",
 "[excited] Vamos dar zoom! Este é um pedacinho de sabão, tão pequeno que nenhum olho consegue ver.",
 "[excited] चलो ज़ूम करें! यह साबुन का इतना छोटा टुकड़ा है कि कोई आँख इसे नहीं देख सकती।")
line('E02_C11',
 "Parece un renacuajo: cabeza redonda y una cola. Y cada parte quiere algo distinto.",
 "It looks like a tadpole: a round head and a tail. And each part wants something different.",
 "On dirait un têtard : une tête ronde et une queue. Et chaque partie veut autre chose.",
 "Parece um girino: cabeça redonda e uma cauda. E cada parte quer uma coisa diferente.",
 "यह मेंढक के बच्चे जैसा है: गोल सिर और एक पूँछ। और हर हिस्सा कुछ अलग चाहता है।")
line('E02_C12',
 "[warmly] A la cabeza le encanta el agua. Siempre quiere estar pegada a ella.",
 "[warmly] The head loves water. It always wants to stay stuck to it.",
 "[warmly] La tête adore l'eau. Elle veut toujours rester collée à elle.",
 "[warmly] A cabeça adora água. Ela sempre quer ficar grudada nela.",
 "[warmly] सिर को पानी बहुत पसंद है। वह हमेशा उससे चिपका रहना चाहता है।")
line('E02_C13',
 "La cola es al revés: huye del agua y adora la grasa. [excited] ¡Corre a esconderse en ella!",
 "The tail is the opposite: it runs from water and loves grease. [excited] It dives in to hide!",
 "La queue, c'est l'inverse : elle fuit l'eau et adore le gras. [excited] Elle court s'y cacher !",
 "A cauda é o contrário: foge da água e adora gordura. [excited] Corre para se esconder nela!",
 "पूँछ उल्टी है: पानी से भागती है, चिकनाई से प्यार करती है। [excited] उसमें छिप जाती है!")
line('E02_L1',
 "[warmly] La cabeza ama el agua; la cola ama la grasa. ¡Ese es el secreto!",
 "[warmly] The head loves water; the tail loves grease. That's the secret!",
 "[warmly] La tête aime l'eau, la queue aime le gras. Voilà le secret !",
 "[warmly] A cabeça ama a água; a cauda ama a gordura. Esse é o segredo!",
 "[warmly] सिर को पानी पसंद, पूँछ को चिकनाई। यही है राज़!")
line('E02_C14',
 "[laughs] Pipo lo resume a su manera: ¡el jabón es amigo de los dos equipos!",
 "[laughs] Pipo sums it up his way: soap is friends with both teams!",
 "[laughs] Pipo résume à sa façon : le savon est ami des deux équipes !",
 "[laughs] O Pipo resume do jeito dele: o sabão é amigo dos dois times!",
 "[laughs] पीपो अपने अंदाज़ में कहता है: साबुन दोनों टीमों का दोस्त है!")
line('E02_C15',
 "[excited] ¡Exacto! Con una mano agarra la grasa y con la otra agarra el agua. Es un puente.",
 "[excited] Exactly! With one hand it grabs the grease, and with the other, the water. It's a bridge.",
 "[excited] Exactement ! D'une main il attrape le gras, de l'autre, l'eau. C'est un pont.",
 "[excited] Isso! Com uma mão agarra a gordura e com a outra agarra a água. É uma ponte.",
 "[excited] बिल्कुल! एक हाथ से चिकनाई पकड़ता है, दूसरे से पानी। यह एक पुल है।")
line('E02_C16',
 "[curious] Plop quiere saber: un solo jabón es chiquito. ¿Cómo mueve una mancha tan grande?",
 "[curious] Plop wants to know: one soap is so tiny. How can it move such a big stain?",
 "[curious] Plop veut savoir : un seul savon est minuscule. Comment bouge-t-il une si grosse tache ?",
 "[curious] O Plop quer saber: um sabão sozinho é tão pequeno. Como move uma mancha tão grande?",
 "[curious] प्लॉप जानना चाहता है: एक साबुन तो बहुत छोटा है। इतना बड़ा दाग कैसे हटाएगा?")
line('E02_C17',
 "Respuesta: nunca viene uno solo. [excited] ¡En una gota de jabón hay millones y millones!",
 "The answer: it never comes alone. [excited] One drop of soap has millions and millions!",
 "Réponse : il ne vient jamais seul. [excited] Une goutte de savon en contient des millions !",
 "Resposta: ele nunca vem sozinho. [excited] Numa gota de sabão há milhões e milhões!",
 "जवाब: वह कभी अकेला नहीं आता। [excited] साबुन की एक बूँद में लाखों-करोड़ों होते हैं!")
line('E02_C18',
 "Todas las colas hacen lo mismo: se clavan en la grasa para esconderse del agua.",
 "All the tails do the same thing: they dig into the grease to hide from the water.",
 "Toutes les queues font pareil : elles s'enfoncent dans le gras pour fuir l'eau.",
 "Todas as caudas fazem o mesmo: se enfiam na gordura para se esconder da água.",
 "सारी पूँछें यही करती हैं: पानी से छिपने के लिए चिकनाई में धँस जाती हैं।")
line('E02_C19',
 "Poco a poco la rodean por completo, como un equipo abrazando un balón.",
 "Little by little they surround it completely, like a team hugging a ball.",
 "Petit à petit, elles l'entourent complètement, comme une équipe qui serre un ballon.",
 "Pouco a pouco elas cercam tudo, como um time abraçando uma bola.",
 "धीरे-धीरे वे उसे पूरा घेर लेती हैं, जैसे कोई टीम गेंद को गले लगा रही हो।")
line('E02_C20',
 "Mira cómo quedó: la grasa atrapada en el centro y las cabezas mirando hacia afuera.",
 "Look how it turned out: the grease trapped in the middle, and the heads facing out.",
 "Regarde : le gras est piégé au centre, et les têtes regardent vers l'extérieur.",
 "Olha só: a gordura presa no meio e as cabeças viradas para fora.",
 "देखो: चिकनाई बीच में फँसी है, और सारे सिर बाहर की ओर हैं।")
line('E02_C21',
 "[laughs] Para Pipo es una pelota con peinado de bolitas. Los científicos la llaman micela.",
 "[laughs] To Pipo, it's a ball with a bobbly hairdo. Scientists call it a micelle.",
 "[laughs] Pour Pipo, c'est une balle coiffée de petites boules. Les scientifiques l'appellent micelle.",
 "[laughs] Para o Pipo, é uma bola com penteado de bolinhas. Os cientistas chamam de micela.",
 "[laughs] पीपो को यह गोलियों वाले बालों की गेंद लगती है। वैज्ञानिक इसे मिसेल कहते हैं।")
line('E02_C22',
 "Y la micela tiene un superpoder: por fuera ya no parece grasa. [excited] ¡Parece amiga del agua!",
 "And the micelle has a superpower: outside, it's not greasy anymore. [excited] Water likes it!",
 "Et la micelle a un super-pouvoir : dehors, elle n'a plus l'air grasse. [excited] L'eau l'adore !",
 "E a micela tem um superpoder: por fora não parece mais gordura. [excited] Parece amiga da água!",
 "मिसेल का सुपरपावर: बाहर से वह चिकनी नहीं लगती। [excited] पानी की दोस्त लगती है!")
line('E02_C23',
 "Así que cuando llega el agua, se agarra de todas esas cabezas…",
 "So when the water arrives, it grabs on to all those heads…",
 "Alors, quand l'eau arrive, elle s'accroche à toutes ces têtes…",
 "Então, quando a água chega, ela se agarra em todas essas cabeças…",
 "तो जब पानी आता है, वह उन सारे सिरों को पकड़ लेता है…")
line('E02_C24',
 "…y se lleva la micela rodando, con la grasa encerrada adentro. [excited] ¡Adiós, mancha!",
 "…and rolls the micelle away, with the grease locked inside. [excited] Bye-bye, stain!",
 "…et emporte la micelle en roulant, avec le gras enfermé dedans. [excited] Adieu, la tache !",
 "…e leva a micela rolando, com a gordura presa lá dentro. [excited] Tchau, mancha!",
 "…और मिसेल को लुढ़काकर ले जाता है, चिकनाई अंदर बंद है। [excited] अलविदा, दाग!")
line('E02_C25',
 "[thoughtful] Plop mira su panza… ¿Funcionará de verdad? [excited] ¡Hay que comprobarlo!",
 "[thoughtful] Plop looks at his belly… Will it really work? [excited] We have to test it!",
 "[thoughtful] Plop regarde son ventre… Ça marchera vraiment ? [excited] Il faut vérifier !",
 "[thoughtful] O Plop olha a barriga… Será que funciona mesmo? [excited] Vamos comprovar!",
 "[thoughtful] प्लॉप अपना पेट देखता है… क्या सच में काम करेगा? [excited] परखना होगा!")
line('E02_C26',
 "Primero, jabón. Hay que frotar bien para que las colas encuentren toda la grasa.",
 "First, soap. Scrub well so the tails can find all the grease.",
 "D'abord, le savon. Il faut bien frotter pour que les queues trouvent tout le gras.",
 "Primeiro, sabão. Tem que esfregar bem para as caudas acharem toda a gordura.",
 "पहले साबुन। अच्छे से रगड़ो, ताकि पूँछें सारी चिकनाई ढूँढ लें।")
line('E02_C27',
 "Ahora, agua. Y mira: el agua ya no resbala… [excited] ¡se lleva la grasa!",
 "Now, water. And look: the water doesn't slide off… [excited] it carries the grease away!",
 "Maintenant, l'eau. Et regarde : elle ne glisse plus… [excited] elle emporte le gras !",
 "Agora, água. E olha: a água não escorrega mais… [excited] ela leva a gordura!",
 "अब पानी। और देखो: पानी अब फिसलता नहीं… [excited] चिकनाई को साथ ले जाता है!")
line('E02_C28',
 "[excited] ¡Panza limpia! El jabón no destruyó la grasa: la envolvió y el agua se la llevó.",
 "[excited] Clean belly! Soap didn't destroy the grease: it wrapped it up, and water carried it off.",
 "[excited] Ventre propre ! Le savon n'a pas détruit le gras : il l'a emballé, et l'eau l'a emporté.",
 "[excited] Barriga limpa! O sabão não destruiu a gordura: embrulhou, e a água levou embora.",
 "[excited] पेट साफ़! साबुन ने चिकनाई को मिटाया नहीं: लपेट दिया, और पानी उसे ले गया।")
line('E02_C29',
 "[warmly] No era el perfume, Pipo: eran millones de renacuajos haciendo de puente.",
 "[warmly] It wasn't the perfume, Pipo: it was millions of tadpoles making a bridge.",
 "[warmly] Ce n'était pas le parfum, Pipo : c'étaient des millions de têtards formant un pont.",
 "[warmly] Não era o perfume, Pipo: eram milhões de girinos fazendo uma ponte.",
 "[warmly] ख़ुशबू नहीं थी, पीपो: लाखों मेंढक के बच्चे पुल बना रहे थे।")
line('E02_C30',
 "Y tu pregunta ya tiene respuesta, Plop: sola, el agua resbala; con jabón, agarra.",
 "And your question has an answer, Plop: alone, water slides off; with soap, it grabs on.",
 "Et ta question a sa réponse, Plop : seule, l'eau glisse ; avec du savon, elle accroche.",
 "E sua pergunta já tem resposta, Plop: sozinha, a água escorrega; com sabão, ela agarra.",
 "जवाब मिल गया, प्लॉप: अकेला पानी फिसलता है, साबुन के साथ पकड़ लेता है।")
line('E02_L2',
 "[warmly] Repasemos: la cola se clava, la micela envuelve, y el agua se la lleva.",
 "[warmly] Let's review: the tail digs in, the micelle wraps up, and the water carries it away.",
 "[warmly] Révisons : la queue s'enfonce, la micelle enveloppe, et l'eau l'emporte.",
 "[warmly] Vamos revisar: a cauda se crava, a micela envolve, e a água leva embora.",
 "[warmly] दोहराते हैं: पूँछ धँसती है, मिसेल लपेटती है, और पानी ले जाता है।")
line('E02_C31',
 "[curious] Dato extra: muchos microbios tienen un abrigo de grasa. ¿Adivinas qué hace el jabón?",
 "[curious] Bonus fact: many germs wear a coat of grease. Can you guess what soap does?",
 "[curious] Info bonus : beaucoup de microbes ont un manteau de gras. Devine ce que fait le savon ?",
 "[curious] Curiosidade: muitos micróbios usam um casaco de gordura. Adivinha o que o sabão faz?",
 "[curious] एक और बात: कई कीटाणुओं पर चिकनाई का कोट होता है। सोचो, साबुन क्या करता है?")
line('E02_C32',
 "[excited] ¡Les desarma el abrigo! Por eso lavarte las manos con jabón te protege de enfermarte.",
 "[excited] It breaks their coat apart! That's why washing hands with soap keeps you healthy.",
 "[excited] Il défait leur manteau ! C'est pour ça que se laver les mains au savon protège des maladies.",
 "[excited] Ele desmonta o casaco! Por isso lavar as mãos com sabão protege você de ficar doente.",
 "[excited] साबुन उनका कोट तोड़ देता है! इसलिए साबुन से हाथ धोओ, बीमारी से बचो।")
line('E02_C33',
 "Pero el jabón necesita tiempo para rodear toda la grasa. [excited] Plop tiene un reto para ti.",
 "But soap needs time to surround all the grease. [excited] Plop has a challenge for you.",
 "Mais le savon a besoin de temps pour entourer tout le gras. [excited] Plop a un défi pour toi.",
 "Mas o sabão precisa de tempo para cercar toda a gordura. [excited] O Plop tem um desafio para você.",
 "पर साबुन को चिकनाई घेरने में समय लगता है। [excited] प्लॉप की तुम्हें एक चुनौती है!")
line('E02_L3',
 "[playful] Frota las manos con jabón veinte segundos. ¿Qué canción cabe?",
 "[playful] Scrub your hands with soap for twenty seconds. What song fits?",
 "[playful] Frotte tes mains au savon vingt secondes. Quelle chanson tient dedans ?",
 "[playful] Esfregue as mãos com sabão por vinte segundos. Que música cabe?",
 "[playful] बीस सेकंड साबुन से हाथ रगड़ो। कौन-सा गाना पूरा होगा?")
line('E02_C34',
 "[curious] Plop nos deja la próxima pregunta: ¿por qué pica el ají si no está caliente?",
 "[curious] Plop leaves us the next question: why is chili spicy if it isn't hot?",
 "[curious] Plop nous laisse la prochaine question : pourquoi le piment pique s'il n'est pas chaud ?",
 "[curious] O Plop deixa a próxima pergunta: por que a pimenta arde se não está quente?",
 "[curious] प्लॉप का अगला सवाल: मिर्च तीखी क्यों लगती है, जब वह गरम नहीं?")
line('CANAL_FINAL',
 "[excited] ¡Hasta el próximo misterio!",
 "[excited] See you at the next mystery!",
 "[excited] À la prochaine énigme !",
 "[excited] Até o próximo mistério!",
 "[excited] अगले रहस्य में मिलते हैं!")

def fix(sid, lg, text): L[sid][lg] = text
# (retoques tras escuchar / medir van aquí)

VIDEO_END = 300.0
out = []
for s in SHOTS:
    sid = s['id']; t0, t1 = [ts(x) for x in s['t'].replace('–', '-').split('-')]
    t1 = min(t1, VIDEO_END)
    still = 'still' in s['cls']
    lo = 0.2 if sid.startswith('CANAL') else 0.3
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
            if est > w * 0.97: risk.append(f"{o['id']}:{est/w:.2f}")
        print(lg, sum(len(spoken(o[lg])) for o in out), 'chars | en riesgo:', ' '.join(risk) or 'ninguna')
