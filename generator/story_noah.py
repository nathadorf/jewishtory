# Story script. Markup [[hebrew|translit|tts]] : shown as translit (+ Hebrew), spoken as tts.
# Speakers: N narrator, NOAH, EYDEL, ARIE, HILLEL. "~" = scene break (chime).

TITLE = "Eydel, Arié et Hillel sur la tévah de Noé"

W = {
    "tevah": "[[תֵּבָה|tévah|téva]]",
    "mayim": "[[מַיִם|mayim|maillime]]",
    "yona": "[[יוֹנָה|yona|yona]]",
    "keshet": "[[קֶשֶׁת|késhet|kéchète]]",
    "geshem": "[[גֶּשֶׁם|guéshem|guéchème]]",
    "shalom": "[[שָׁלוֹם|shalom|chalom]]",
    "layla": "[[לַיְלָה טוֹב|layla tov|laïla tov]]",
    "boker": "[[בֹּקֶר טוֹב|boker tov|bôkèr tov]]",
    "toda": "[[תּוֹדָה|toda|toda]]",
    "yeladim": "[[יְלָדִים|yéladim|yéladimme]]",
    "noah": "[[נֹחַ|Noa'h|No-ar]]",
    "eydel": "[[|Eydel|Èïdèl]]",
    "hillel": "[[|Hillel|Ilèl]]",
    "hachem": "[[|Hachem|Achème]]",
}

def f(s):
    return s.format(**W)

S = [
 ("N", "Il était une fois, dans une petite maison toute douce, trois enfants qui n'arrivaient pas à dormir : {eydel}, Arié… et le petit {hillel}."),
 ("N", "Ce soir-là, il pleuvait. Tic, tic, tic, faisait la pluie sur la fenêtre. Et la pluie, en hébreu, ça se dit… {geshem}."),
 ("HILLEL", "{geshem}… J'aime bien ce mot. On dirait le bruit des gouttes !"),
 ("EYDEL", "Chut, {hillel}. Écoute… On dirait qu'il y a des animaux dehors !"),
 ("N", "Les trois enfants collèrent leur nez contre la vitre. Et là, devant la maison, au milieu de l'eau, il y avait un énorme bateau en bois. Un bateau grand comme une montagne !"),
 ("ARIE", "Waouh ! C'est quoi, ce bateau géant ?"),
 ("N", "Une petite porte s'ouvrit, et un vieil homme avec une longue barbe blanche leur fit un grand sourire."),
 ("NOAH", "{shalom}, {yeladim} ! {shalom}, les enfants ! Je m'appelle {noah}. Vous voulez monter dans ma {tevah} ?"),
 ("EYDEL", "Ta {tevah} ? C'est quoi, une {tevah} ?"),
 ("NOAH", "Une {tevah}, c'est une arche. Un grand bateau tout rond, comme une maison qui flotte. {hachem} m'a demandé de la construire, planche après planche, pour protéger toutes les familles d'animaux."),
 ("N", "Et hop ! {eydel} prit la main d'Arié, Arié prit la main de {hillel}, et les trois enfants montèrent sur la {tevah}."),
 ("~", ""),
 ("N", "À l'intérieur, quel spectacle ! Il y avait des animaux partout. Deux lions qui bâillaient. Deux girafes qui baissaient la tête pour passer sous le plafond. Deux petits lapins, et même deux tortues, toutes lentes, toutes lentes."),
 ("ARIE", "Je vais les compter ! Un, deux… deux éléphants. Un, deux… deux zèbres. Ils arrivent toujours deux par deux !"),
 ("NOAH", "Bravo, Arié ! Deux par deux, comme des amis qui se tiennent la main. Comme ça, personne n'est jamais tout seul."),
 ("HILLEL", "Moi, je veux donner à manger aux lapins !"),
 ("N", "{noah} donna à {hillel} un panier de carottes, et à {eydel} un grand seau rempli de {mayim}… de l'eau toute fraîche, pour faire boire les animaux."),
 ("EYDEL", "{mayim} pour les chameaux, {mayim} pour les moutons, et un peu de {mayim} pour le petit chat !"),
 ("NOAH", "{toda}, {eydel}. {toda rabbah} ! Merci beaucoup. Tu as le cœur aussi grand que ma {tevah}."),
 ("ARIE", "Dis, {noah}… pourquoi tu as construit une si grande {tevah} ?"),
 ("NOAH", "Parce qu'à cette époque, les gens avaient oublié d'être gentils. Ils se disputaient, ils prenaient les jouets des autres, ils ne disaient jamais merci. Alors {hachem} a voulu tout recommencer, avec une famille qui prend soin des autres… et avec tous les animaux."),
 ("HILLEL", "Moi, je dis toujours {toda} ! Enfin… presque toujours."),
 ("N", "{noah} éclata de rire, d'un grand rire tout doux qui faisait trembler sa barbe blanche. Même l'éléphant leva sa trompe, comme pour rire avec lui."),
 ("N", "Le soir, les enfants aidèrent {noah} à installer les animaux pour la nuit. Arié tapota la tête du gros éléphant, {hillel} borda les petits lapins dans la paille, et {eydel} chanta une berceuse, tout bas, tout bas, pour les oiseaux."),
 ("EYDEL", "Dodo, petits oiseaux, la {tevah} vous berce sur l'eau… {layla tov}, {layla tov}…"),
 ("~", ""),
 ("N", "Soudain, le ciel devint tout gris. Boum ! fit le tonnerre. Et le {geshem}, la pluie, se mit à tomber, tomber, tomber… Beaucoup plus fort que tout à l'heure."),
 ("HILLEL", "J'ai un peu peur… Il y a trop de {geshem} !"),
 ("N", "Alors {eydel} serra son petit frère dans ses bras, et Arié lui prit la main."),
 ("EYDEL", "Ne t'inquiète pas, {hillel}. Ici, dans la {tevah}, on est à l'abri. Écoute… la pluie fait une chanson."),
 ("NOAH", "Elle a raison. Le {geshem} tombe dehors, mais nous, nous sommes tous ensemble, bien au chaud. Et quand on est ensemble, on est plus fort que l'orage."),
 ("N", "Il plut pendant quarante jours et quarante nuits. Il y avait du {mayim} partout, partout, partout. Plus de maisons, plus d'arbres, plus de montagnes… seulement la {tevah}, qui flottait doucement, comme un berceau sur la mer."),
 ("N", "Le soir, les animaux s'endormaient. Les lions ronronnaient comme de gros chats, et {noah} chuchotait à chacun :"),
 ("NOAH", "{layla tov}, les girafes. {layla tov}, les lapins. {layla tov}, les petites tortues."),
 ("~", ""),
 ("N", "Un matin, plus un bruit. Plus de tic, tic, tic. Le {geshem} s'était arrêté !"),
 ("NOAH", "{boker tov}, {yeladim} ! Bonjour, les enfants ! Venez vite, j'ai besoin de vous."),
 ("N", "{noah} ouvrit une petite fenêtre. Dans ses mains, il tenait un bel oiseau tout blanc."),
 ("ARIE", "C'est une colombe !"),
 ("NOAH", "Oui, Arié. En hébreu, la colombe, c'est la {yona}. Ma {yona} va voler très loin, et nous dire si la terre est sèche."),
 ("N", "La {yona} ouvrit ses ailes et s'envola au-dessus du {mayim}. Les enfants attendirent… attendirent… et attendirent encore."),
 ("HILLEL", "Elle revient ! La {yona} revient ! Elle a quelque chose dans son bec !"),
 ("EYDEL", "C'est une petite feuille verte ! Une feuille d'olivier !"),
 ("NOAH", "Merveilleux ! Si la {yona} a trouvé un arbre, c'est que l'eau s'en va. Bientôt, nous pourrons tous sortir de la {tevah}."),
 ("~", ""),
 ("N", "Quelques jours plus tard, la {tevah} se posa tout doucement sur une montagne. La grande porte s'ouvrit, et tous les animaux sortirent, deux par deux, en sautant de joie dans l'herbe mouillée."),
 ("N", "Et là, dans le ciel, apparut quelque chose de magnifique. Une grande arche de couleurs : rouge, orange, jaune, vert, bleu et violet."),
 ("ARIE", "Un arc-en-ciel !"),
 ("NOAH", "Oui. En hébreu, on dit {keshet}. La {keshet}, c'est une promesse de {hachem} : plus jamais de grand déluge. Chaque fois que vous verrez une {keshet}, souvenez-vous de cette promesse."),
 ("HILLEL", "{keshet}… J'aime bien les couleurs de la {keshet}."),
 ("EYDEL", "Monsieur {noah}… Est-ce qu'on pourra revenir vous voir ?"),
 ("NOAH", "Bien sûr, ma grande. Chaque fois que vous serez gentils avec les animaux, et gentils les uns avec les autres, je serai un peu avec vous. {toda}, les enfants. Vous avez été de très bons marins."),
 ("~", ""),
 ("N", "La {yona} se posa sur l'épaule de {hillel}, battit des ailes… et, pfiou ! les trois enfants se retrouvèrent dans leurs lits, sous leurs couvertures toutes chaudes."),
 ("N", "Dehors, le {geshem} s'était arrêté. Et dans le ciel de la nuit, on devinait encore, tout petit, un morceau de {keshet}."),
 ("ARIE", "{eydel}… tu crois que c'était un rêve ?"),
 ("EYDEL", "Je ne sais pas, Arié. Mais moi, je me souviens de tous les mots : {tevah}, {mayim}, {yona}, {keshet}, {geshem}."),
 ("HILLEL", "{tevah}, {mayim}, {yona}, {keshet}, {geshem}… {layla tov}, {eydel}. {layla tov}, Arié."),
 ("N", "Et les trois enfants fermèrent les yeux, en rêvant de girafes, de colombes et d'arcs-en-ciel. {layla tov}, {eydel}. {layla tov}, Arié. {layla tov}, {hillel}. Fais de beaux rêves."),
]

W["layla tov"] = W["layla"]
W["boker tov"] = W["boker"]
W["toda rabbah"] = "[[תּוֹדָה רַבָּה|toda rabbah|toda raba]]"

SEGMENTS = [(sp, f(t)) for sp, t in S]

# rain at the window at the start, then the storm
AMBIENCE = [(None, "collèrent", 0.035, "rain"), ("Boum", "Plus de tic", 0.11, "rain")]
