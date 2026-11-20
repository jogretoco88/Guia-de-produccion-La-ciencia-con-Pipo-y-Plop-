# Guion de narración del Ep. 1 (¿Por qué explotan las palomitas de maíz?) en 5 idiomas, una frase por toma.
# Base: la narración en español de la guía (shots.json), revisada toma por toma contra el video:
#  - C34: en pantalla se despide Pipo, así que la próxima pregunta la deja Pipo (no Plop).
#  - C26: el grano revienta a los 2,75 s de la toma; la frase empieza con «¡Pum!» justo ahí (ancla START).
#  - L1, L3 y CANAL_FINAL se acortan para caber en sus 6 s / 4 s.
# Las etiquetas [..] son dirección de voz para Eleven v4 (no se pronuncian).
import json, re

SHOTS = json.load(open('../shots.json'))['shots']

def ts(x):
    m, s = x.split(':'); return int(m) * 60 + int(s)

L = {}
def line(sid, es, en, fr, pt, hi, anchors=None):
    L[sid] = dict(es=es, en=en, fr=fr, pt=pt, hi=hi, anchors=anchors or [])

line('E01_C01',
 "[curious] Un grano de maíz es duro como una piedra. Pero con calor… [surprised] ¡se convierte en una nube!",
 "[curious] A corn kernel is as hard as a rock. But with heat… [surprised] it turns into a cloud!",
 "[curious] Un grain de maïs est dur comme une pierre. Mais avec la chaleur… [surprised] il devient un nuage !",
 "[curious] Um grão de milho é duro como pedra. Mas com calor… [surprised] ele vira uma nuvem!",
 "[curious] मक्के का दाना पत्थर जैसा सख़्त है। पर गरमी से… [surprised] वह बादल बन जाता है!")
line('E01_C02',
 "¿Cómo cabe algo tan grande y esponjoso dentro de algo tan pequeño y tan duro?",
 "How can something so big and fluffy fit inside something so small and hard?",
 "Comment une chose si grande et si moelleuse tient-elle dans une chose si petite et si dure ?",
 "Como algo tão grande e fofinho cabe dentro de algo tão pequeno e tão duro?",
 "इतनी बड़ी और फूली चीज़ इतने छोटे और सख़्त दाने में कैसे समाती है?")
line('E01_C03',
 "Plop también quiere saberlo. Hoy vamos a descubrir el secreto que esconde cada palomita.",
 "Plop wants to know too. Today we'll discover the secret hiding in every piece of popcorn.",
 "Plop veut le savoir aussi. Aujourd'hui, on découvre le secret caché dans chaque pop-corn.",
 "O Plop também quer saber. Hoje vamos descobrir o segredo que cada pipoca esconde.",
 "प्लॉप भी जानना चाहता है। आज हम हर पॉपकॉर्न का छिपा राज़ खोजेंगे।")
line('CANAL_INICIO',
 "[excited] ¡La ciencia con Pipo y Plop!",
 "[excited] Science with Pipo and Plop!",
 "[excited] La science avec Pipo et Plop !",
 "[excited] A ciência com Pipo e Plop!",
 "[excited] पीपो और प्लॉप के साथ विज्ञान!")
line('E01_C04',
 "[mischievously] Pipo tiene una idea loca: ¿y si adentro vive un duende que infla globos?",
 "[mischievously] Pipo has a wild idea: what if a little elf lives inside, blowing up balloons?",
 "[mischievously] Pipo a une idée folle : et si un lutin vivait dedans pour gonfler des ballons ?",
 "[mischievously] O Pipo tem uma ideia maluca: e se lá dentro morar um duende que enche balões?",
 "[mischievously] पीपो का अजीब ख़याल: क्या अंदर कोई बौना गुब्बारे फुलाता है?")
line('E01_C05',
 "Si fuera así, al acercar la oreja lo oiríamos soplar. Pero no se oye nada.",
 "If so, with an ear up close, we'd hear him blowing. But there's not a sound.",
 "Si c'était vrai, en approchant l'oreille, on l'entendrait souffler. Mais on n'entend rien.",
 "Se fosse assim, encostando a orelha, a gente ouviria ele soprar. Mas não se ouve nada.",
 "अगर ऐसा होता, तो कान लगाने पर फूँकने की आवाज़ आती। पर कुछ सुनाई नहीं देता।")
line('E01_C06',
 "Otra idea: apretarlo con fuerza. Pero ni con todo el peso de Pipo se abre.",
 "Another idea: squeeze it hard. But even with all of Pipo's weight, it won't open.",
 "Autre idée : l'écraser très fort. Mais même avec tout le poids de Pipo, il ne s'ouvre pas.",
 "Outra ideia: apertar com força. Mas nem com todo o peso do Pipo ele abre.",
 "दूसरा ख़याल: ज़ोर से दबाओ। पर पीपो के पूरे वज़न से भी दाना नहीं खुलता।")
line('E01_C07',
 "[thoughtful] Plop se pregunta algo importante: si la fuerza no lo abre, ¿por qué el calor sí?",
 "[thoughtful] Plop wonders something important: if force can't open it, why can heat?",
 "[thoughtful] Plop se pose une grande question : si la force ne l'ouvre pas, pourquoi la chaleur, oui ?",
 "[thoughtful] O Plop se pergunta algo importante: se a força não abre, por que o calor abre?",
 "[thoughtful] प्लॉप सोचता है: अगर ज़ोर से नहीं खुलता, तो गरमी से क्यों खुलता है?")
line('E01_C08',
 "[warmly] ¡Buena pregunta! Eso significa que el secreto no está afuera. Está escondido adentro.",
 "[warmly] Great question! It means the secret isn't on the outside. It's hidden inside.",
 "[warmly] Bonne question ! Ça veut dire que le secret n'est pas dehors. Il est caché dedans.",
 "[warmly] Boa pergunta! Quer dizer que o segredo não está do lado de fora. Está escondido dentro.",
 "[warmly] बढ़िया सवाल! मतलब राज़ बाहर नहीं है। वह अंदर छिपा है।")
line('E01_C09',
 "[curious] ¿Y tú qué crees que hay dentro? Piénsalo… ¿Ya? [excited] ¡Vamos a abrirlo!",
 "[curious] What do you think is inside? Think about it… Ready? [excited] Let's open it!",
 "[curious] Et toi, qu'y a-t-il dedans, à ton avis ? Réfléchis… Prêt ? [excited] On l'ouvre !",
 "[curious] E você, o que acha que tem dentro? Pense… Pronto? [excited] Vamos abrir!",
 "[curious] तुम्हें क्या लगता है, अंदर क्या है? सोचो… हो गया? [excited] चलो इसे खोलें!")
line('E01_C10',
 "[excited] ¡Hagamos zoom! Al partir el grano por la mitad, aparecen tres partes secretas.",
 "[excited] Let's zoom in! Cut the kernel in half, and three secret parts appear.",
 "[excited] Zoomons ! En coupant le grain en deux, trois parties secrètes apparaissent.",
 "[excited] Vamos dar zoom! Partindo o grão ao meio, aparecem três partes secretas.",
 "[excited] ज़ूम करते हैं! दाने को बीच से काटो, तो तीन छिपे हिस्से दिखते हैं।")
line('E01_C11',
 "Primera: una cáscara amarilla durísima. Se llama pericarpio y funciona como un casco.",
 "First: a super-hard yellow shell. It's called the pericarp, and it works like a helmet.",
 "Un : une coque jaune très dure. On l'appelle le péricarpe, et elle sert de casque.",
 "Primeira: uma casca amarela duríssima. Ela se chama pericarpo e funciona como um capacete.",
 "पहला: पीला, बहुत सख़्त छिलका। इसे पेरीकार्प कहते हैं, यह हेलमेट जैसा है।")
line('E01_C12',
 "Segunda: un relleno blanco y apretado, el almidón. Es la comida que guarda la semilla.",
 "Second: a packed white filling called starch. It's the food the seed keeps in store.",
 "Deux : un remplissage blanc et serré, l'amidon. C'est la nourriture que garde la graine.",
 "Segunda: um recheio branco e apertado chamado amido. É a comida que a semente guarda.",
 "दूसरा: सफ़ेद, ठसाठस भरा स्टार्च। यह बीज का जमा किया खाना है।")
line('E01_C13',
 "[whispers] Y tercera, bien escondida entre el almidón… ¡agua! Solo un poquito, pero es la clave.",
 "[whispers] And third, hidden deep in the starch… water! Just a tiny bit, but it's the key.",
 "[whispers] Et trois, bien cachée dans l'amidon… de l'eau ! Juste un peu, mais c'est la clé.",
 "[whispers] E terceira, bem escondida no amido… água! Só um pouquinho, mas é a chave.",
 "[whispers] और तीसरा, स्टार्च में छिपा… पानी! बस थोड़ा-सा, पर यही असली राज़ है।")
line('E01_L1',
 "Casco duro, almidón y un poquito de agua. ¡Recuerda estas tres!",
 "Hard shell, starch, and a little water. Remember these three!",
 "Coque dure, amidon et un peu d'eau. Retiens bien ces trois-là !",
 "Casca dura, amido e um pouquinho de água. Lembre dessas três!",
 "सख़्त छिलका, स्टार्च और थोड़ा पानी। ये तीनों याद रखो!")
line('E01_C14',
 "[surprised] Pipo no lo puede creer: ¿agua? ¡Si el grano está sequísimo por fuera!",
 "[surprised] Pipo can't believe it: water? But the kernel is bone-dry on the outside!",
 "[surprised] Pipo n'y croit pas : de l'eau ? Mais le grain est tout sec dehors !",
 "[surprised] O Pipo não acredita: água? Mas o grão está sequinho por fora!",
 "[surprised] पीपो को यक़ीन नहीं: पानी? दाना तो बाहर से बिल्कुल सूखा है!")
line('E01_C15',
 "Justo por eso. El casco es tan cerrado que el agua no puede escapar.",
 "That's exactly why. The shell is sealed so tight that the water can't escape.",
 "Justement. La coque est si fermée que l'eau ne peut pas s'échapper.",
 "É justamente por isso. A casca é tão fechada que a água não consegue escapar.",
 "इसीलिए तो। छिलका इतना बंद है कि पानी बाहर नहीं निकल पाता।")
line('E01_C16',
 "Y Plop ya lo sospecha: agua encerrada, más calor… ¡aquí va a pasar algo!",
 "And Plop already suspects it: trapped water, plus heat… something's about to happen!",
 "Et Plop s'en doute déjà : de l'eau enfermée, plus la chaleur… il va se passer quelque chose !",
 "E o Plop já desconfia: água presa, mais calor… alguma coisa vai acontecer!",
 "प्लॉप को शक है: बंद पानी, ऊपर से गरमी… कुछ तो होने वाला है!")
line('E01_C17',
 "Ahora encendemos el calor. El grano se calienta más y más por dentro.",
 "Now we turn up the heat. The kernel gets hotter and hotter inside.",
 "Maintenant, on allume le feu. Le grain chauffe de plus en plus à l'intérieur.",
 "Agora ligamos o calor. O grão esquenta cada vez mais por dentro.",
 "अब गरमी चालू। दाना अंदर से और गरम, और गरम होता जाता है।")
line('E01_C18',
 "Con el calor, el agua hace su truco: deja de ser líquida y se convierte en vapor.",
 "With the heat, water does its trick: it stops being liquid and turns into steam.",
 "Avec la chaleur, l'eau fait son tour : elle n'est plus liquide, elle devient vapeur.",
 "Com o calor, a água faz seu truque: deixa de ser líquida e vira vapor.",
 "गरमी से पानी अपना जादू दिखाता है: वह तरल नहीं रहता, भाप बन जाता है।")
line('E01_C19',
 "Y el vapor es un grandulón: necesita muchísimo más espacio que el agua.",
 "And steam is a real giant: it needs much, much more space than water.",
 "Et la vapeur est une géante : il lui faut beaucoup plus de place que l'eau.",
 "E o vapor é um grandalhão: precisa de muito mais espaço que a água.",
 "और भाप तो बहुत फैलती है: उसे पानी से कहीं ज़्यादा जगह चाहिए।")
line('E01_C20',
 "Pipo lo entiende así: es como inflar un globo dentro de una caja cerrada.",
 "Pipo sees it like this: it's like blowing up a balloon inside a closed box.",
 "Pipo le voit comme ça : c'est comme gonfler un ballon dans une boîte fermée.",
 "O Pipo entende assim: é como encher um balão dentro de uma caixa fechada.",
 "पीपो ऐसे समझता है: जैसे बंद डिब्बे में गुब्बारा फुलाना।")
line('E01_C21',
 "El vapor empuja el casco desde adentro, buscando una salida. Pero el casco aguanta.",
 "The steam pushes the shell from inside, looking for a way out. But the shell holds.",
 "La vapeur pousse la coque de l'intérieur, elle cherche une sortie. Mais la coque tient bon.",
 "O vapor empurra a casca por dentro, procurando uma saída. Mas a casca aguenta.",
 "भाप अंदर से छिलके को धकेलती है, बाहर निकलना चाहती है। पर छिलका टिका रहता है।")
line('E01_C22',
 "Mientras, el calor ablanda el almidón y lo vuelve una gelatina caliente y elástica.",
 "Meanwhile, the heat softens the starch into a hot, stretchy jelly.",
 "Pendant ce temps, la chaleur ramollit l'amidon : il devient une gelée chaude et élastique.",
 "Enquanto isso, o calor amolece o amido até virar uma gelatina quente e elástica.",
 "इस बीच गरमी स्टार्च को नरम करके गरम, लचीली जेली बना देती है।")
line('E01_C23',
 "Más calor, más vapor, más presión. ¡El grano es ahora una mini olla a presión!",
 "More heat, more steam, more pressure. The kernel is now a mini pressure cooker!",
 "Plus de chaleur, plus de vapeur, plus de pression. Le grain est une mini cocotte-minute !",
 "Mais calor, mais vapor, mais pressão. O grão agora é uma mini panela de pressão!",
 "ज़्यादा गरमी, ज़्यादा भाप, ज़्यादा दबाव। दाना अब छोटा-सा प्रेशर कुकर है!")
line('E01_C24',
 "[whispers] ¿Cuánto más aguantará el casco? Plop casi no quiere mirar… ¿y tú?",
 "[whispers] How much longer can the shell hold? Plop can barely look… can you?",
 "[whispers] Combien de temps la coque va tenir ? Plop n'ose presque plus regarder… et toi ?",
 "[whispers] Quanto mais a casca vai aguentar? O Plop quase não quer olhar… e você?",
 "[whispers] छिलका और कितना सहेगा? प्लॉप तो देख भी नहीं पा रहा… और तुम?")
line('E01_C25',
 "Cuando llega a unos ciento ochenta grados, el casco ya no puede más y…",
 "When it reaches about one hundred eighty degrees, the shell can't take any more and…",
 "Vers cent quatre-vingts degrés, la coque n'en peut plus et…",
 "Quando chega a uns cento e oitenta graus, a casca não aguenta mais e…",
 "लगभग एक सौ अस्सी डिग्री पर, छिलका और नहीं सह पाता और…")
line('E01_C26',
 "[excited] ¡Pum! El casco revienta y el vapor escapa de golpe.",
 "[excited] Pop! The shell bursts and the steam rushes out all at once.",
 "[excited] Pop ! La coque éclate et la vapeur s'échappe d'un coup.",
 "[excited] Pum! A casca estoura e o vapor escapa de uma vez.",
 "[excited] धड़ाम! छिलका फट जाता है और भाप एकदम बाहर निकलती है।",
 anchors=[['START', 2.68]])
line('E01_C27',
 "La gelatina de almidón se infla como espuma, se enfría en el aire y queda tiesa.",
 "The starch jelly puffs up like foam, cools in the air, and goes stiff.",
 "La gelée d'amidon gonfle comme une mousse, refroidit dans l'air et devient toute raide.",
 "A gelatina de amido incha como espuma, esfria no ar e fica durinha.",
 "स्टार्च की जेली झाग की तरह फूलती है, हवा में ठंडी होकर सख़्त हो जाती है।")
line('E01_C28',
 "¡Esa espuma blanca y crujiente es la palomita! El grano se volteó al revés.",
 "That crunchy white foam is the popcorn! The kernel turned itself inside out.",
 "Cette mousse blanche et croustillante, c'est le pop-corn ! Le grain s'est retourné comme un gant.",
 "Essa espuma branca e crocante é a pipoca! O grão virou do avesso.",
 "यही सफ़ेद, कुरकुरा झाग पॉपकॉर्न है! दाना अंदर से बाहर पलट गया।")
line('E01_C29',
 "[laughs] No había duende, Pipo. El que infla la palomita… ¡es el vapor de agua!",
 "[laughs] There was no elf, Pipo. What puffs up the popcorn… is steam!",
 "[laughs] Il n'y avait pas de lutin, Pipo. Ce qui gonfle le pop-corn… c'est la vapeur d'eau !",
 "[laughs] Não tinha duende, Pipo. Quem enche a pipoca… é o vapor de água!",
 "[laughs] कोई बौना नहीं था, पीपो। पॉपकॉर्न को फुलाती है… पानी की भाप!")
line('E01_C30',
 "Y esa es tu respuesta, Plop: el calor lo abre porque convierte el agua en vapor.",
 "And that's your answer, Plop: heat opens it because it turns the water into steam.",
 "Et voilà ta réponse, Plop : la chaleur l'ouvre parce qu'elle change l'eau en vapeur.",
 "E essa é a sua resposta, Plop: o calor abre porque transforma a água em vapor.",
 "यही तुम्हारा जवाब है, प्लॉप: गरमी पानी को भाप बनाती है, इसलिए दाना खुलता है।")
line('E01_L2',
 "[warmly] Repasemos: agua escondida, calor que la vuelve vapor, un casco que aguanta… ¡y pum!",
 "[warmly] Let's review: hidden water, heat that turns it to steam, and a shell that holds… until pop!",
 "[warmly] Révisons : l'eau cachée, la chaleur qui la change en vapeur, la coque qui tient… jusqu'au pop !",
 "[warmly] Vamos revisar: água escondida, calor que vira vapor e uma casca que aguenta… até que pum!",
 "[warmly] दोहराते हैं: छिपा पानी, गरमी से भाप, और टिका हुआ छिलका… फिर धड़ाम!")
line('E01_C31',
 "[curious] ¿Y los granos que no revientan? Tienen una grieta: el vapor se escapa poquito a poco.",
 "[curious] And the kernels that never pop? They have a crack: the steam leaks out bit by bit.",
 "[curious] Et les grains qui n'éclatent jamais ? Ils ont une fissure : la vapeur s'échappe peu à peu.",
 "[curious] E os grãos que nunca estouram? Eles têm uma rachadura: o vapor escapa aos pouquinhos.",
 "[curious] और जो दाने नहीं फूटते? उनमें दरार होती है: भाप धीरे-धीरे निकल जाती है।")
line('E01_C32',
 "Por eso siempre quedan algunos en el fondo del tazón. No son flojos: ¡tienen una fuga!",
 "That's why a few always stay at the bottom of the bowl. They're not lazy: they leak!",
 "Voilà pourquoi il en reste toujours au fond du bol. Ils ne sont pas paresseux : ils ont une fuite !",
 "Por isso sempre sobram alguns no fundo da tigela. Não são preguiçosos: têm um vazamento!",
 "इसीलिए कटोरे की तली में कुछ दाने बच जाते हैं। वे आलसी नहीं: उनमें रिसाव है!")
line('E01_C33',
 "Plop tiene un reto para ti. Necesitas a un adulto, palomitas… y ojos de detective.",
 "Plop has a challenge for you. You'll need a grown-up, popcorn… and detective eyes.",
 "Plop a un défi pour toi. Il te faut un adulte, du pop-corn… et des yeux de détective.",
 "O Plop tem um desafio para você. Precisa de um adulto, pipoca… e olhos de detetive.",
 "प्लॉप की तुम्हें एक चुनौती है। चाहिए एक बड़ा, पॉपकॉर्न… और जासूस वाली नज़र।")
line('E01_L3',
 "[playful] Cuenten los granos sin reventar. ¿Encuentran su grieta?",
 "[playful] Count the unpopped kernels. Can you find their crack?",
 "[playful] Comptez les grains pas éclatés. Trouvez-vous leur fissure ?",
 "[playful] Contem os grãos que não estouraram. Acham a rachadura?",
 "[playful] बिना फूटे दाने गिनो। क्या उनकी दरार दिखी?")
line('E01_C34',
 "[curious] Pipo nos deja la próxima pregunta: ¿por qué el jabón quita la grasa y el agua no?",
 "[curious] Pipo leaves us the next question: why does soap remove grease, but water doesn't?",
 "[curious] Pipo nous laisse la prochaine question : pourquoi le savon enlève le gras, et pas l'eau ?",
 "[curious] O Pipo deixa a próxima pergunta: por que o sabão tira a gordura e a água não?",
 "[curious] पीपो का अगला सवाल: साबुन चिकनाई हटाता है, पानी क्यों नहीं?")
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
            lo = o['anchors'][0][1] if o['anchors'] else o['win'][0]
            est = len(spoken(o[lg])) / RATE[lg]; w = o['win'][1] - lo
            if est > w * 0.97: risk.append(f"{o['id']}:{est/w:.2f}")
        print(lg, sum(len(spoken(o[lg])) for o in out), 'chars | en riesgo:', ' '.join(risk) or 'ninguna')
