# Episode 37 : Matot-Massé (read together most years). Same markup as story.py: [[hebrew|translit|tts]].
# New words: néder, Yarden, ir, massa'ot, zikaron. Reused: a'him, tson, midbar, anan, man, yona, toda, layla tov.
# Keeping one's word, the tribes of Réouven and Gad who promise to help their brothers first, and Moshé remembering all the stops of the journey.
# The war against Midyan is left out.

TITLE = "Eydel, Arié et Hillel et la promesse des frères"

W = {
    "neder": "[[נֶדֶר|néder|nédèr]]",
    "yarden": "[[יַרְדֵּן|Yarden|Yardène]]",
    "ir": "[[עִיר|ir|ir]]",
    "massaot": "[[מַסָּעוֹת|massa'ot|massaote]]",
    "zikaron": "[[זִכָּרוֹן|zikaron|zikarone]]",
    "ahim": "[[אַחִים|a'him|arime]]",
    "tson": "[[צֹאן|tson|tsone]]",
    "midbar": "[[מִדְבָּר|midbar|midbar]]",
    "anan": "[[עָנָן|anan|anane]]",
    "man": "[[מָן|man|mane]]",
    "yam": "[[יָם|yam|yame]]",
    "yona": "[[יוֹנָה|yona|yona]]",
    "shalom": "[[שָׁלוֹם|shalom|chalom]]",
    "toda": "[[תּוֹדָה|toda|toda]]",
    "layla tov": "[[לַיְלָה טוֹב|layla tov|laïla tov]]",
    "moshe": "[[מֹשֶׁה|Moshé|Moché]]",
    "yehoshoua": "[[יְהוֹשֻׁעַ|Yéhoshoua|Yéochoua]]",
    "reouven": "[[רְאוּבֵן|Réouven|Réouvène]]",
    "israel": "[[יִשְׂרָאֵל|Israël|Israèl]]",
    "eydel": "[[|Eydel|Èïdèl]]",
    "hillel": "[[|Hillel|Ilèl]]",
    "hachem": "[[|Hachem|Achème]]",
}

S = [
 ("N", "Ce soir-là, {hillel} avait promis à Arié de lui prêter son vélo. Et puis il avait oublié. Arié avait attendu toute l'après-midi. Toc, toc, toc. La {yona}."),
 ("HILLEL", "La {yona}… Arié, tu viens quand même avec moi ?"),
 ("EYDEL", "Donnez-moi la main. Un, deux, trois…"),
 ("N", "La {yona} battit des ailes… et pfiou ! Les trois enfants se retrouvèrent au bord d'un fleuve. De l'autre côté, on voyait les collines du pays d'{israel}. C'était le {yarden}, le Jourdain."),
 ("MOSHE", "{shalom}, mes amis. Nous sommes presque arrivés. Quarante ans de {midbar}, et voici le {yarden}. Mais avant de traverser, {hachem} m'a demandé de vous parler des promesses. En hébreu, une promesse, c'est un {neder}."),
 ("MOSHE", "Quand on fait un {neder}, on doit le tenir. Ce qui sort de notre bouche, on le fait. Nos mots sont importants."),
 ("N", "{hillel} baissa la tête. Il pensait au vélo."),
 ("~", ""),
 ("N", "À ce moment-là, des hommes arrivèrent avec d'immenses troupeaux. Des milliers de moutons et de vaches. C'étaient les chefs des tribus de {reouven} et de Gad."),
 ("REOUVEN", "{moshe}, regarde ces prairies, ici, de ce côté du {yarden}. L'herbe est verte et grasse. C'est parfait pour notre {tson}. Laisse-nous rester ici. Pas besoin de traverser."),
 ("MOSHE", "Comment ? Vos {ahim} vont traverser le {yarden}, et affronter toutes les difficultés du pays, et vous, vous resteriez tranquillement ici ?"),
 ("ARIE", "Il a raison ! On ne laisse pas ses {ahim} tout seuls !"),
 ("N", "Les chefs de {reouven} et de Gad se regardèrent. Puis ils s'approchèrent de {moshe}."),
 ("REOUVEN", "Tu as raison, {moshe}. Voici ce qu'on te propose. On construit des enclos pour nos moutons, et une {ir}, une ville, pour nos enfants. Et puis nous, les hommes, on traverse avec tout le monde. On marchera même devant ! Et on ne rentrera chez nous que quand tous nos {ahim} auront leur maison. C'est notre {neder}."),
 ("MOSHE", "Alors c'est d'accord. Si vous tenez votre {neder}, cette terre sera à vous."),
 ("EYDEL", "Ils ont promis d'aider leurs {ahim} d'abord. Avant de penser à eux."),
 ("N", "Et la Torah raconte qu'ils tinrent leur {neder}. Ils traversèrent, ils aidèrent, et ils ne rentrèrent chez eux que quand tout le monde fut installé."),
 ("~", ""),
 ("N", "Le soir, {moshe} s'assit au bord du {yarden}, avec un long rouleau. Les enfants s'assirent à côté de lui."),
 ("MOSHE", "{hachem} m'a demandé d'écrire toutes nos {massaot}. Toutes les étapes du voyage, depuis l'Égypte. Quarante-deux endroits."),
 ("HILLEL", "Pourquoi écrire tout ça ?"),
 ("MOSHE", "Pour le {zikaron}, {hillel}. Le souvenir. Comme un papa qui raconte à son enfant : tu te souviens, là, on a dormi. Là, tu avais froid. Là, tu as eu mal à la tête. Chaque étape compte."),
 ("N", "Et {moshe} lut doucement : Ramsès. La mer. Mara, l'eau amère. Elim, avec ses douze sources et ses soixante-dix palmiers. Le Sinaï. Kadesh…"),
 ("ARIE", "Elim ! C'est là où on a vu les palmiers !"),
 ("EYDEL", "Et le {yam}, et le {man}, et l'{anan}… Toutes les {massaot}, c'est toute notre histoire."),
 ("MOSHE", "Et la prochaine étape, c'est le pays d'{israel}. Vous y entrerez avec {yehoshoua}. Et vous n'oublierez jamais le chemin."),
 ("~", ""),
 ("N", "La {yona} vint se poser sur le rouleau de {moshe}. Il était temps de rentrer."),
 ("MOSHE", "{toda}, mes amis, pour toutes ces {massaot} ensemble. Tenez vos promesses. {layla tov}."),
 ("N", "La {yona} battit des ailes… et pfiou ! Les trois enfants se retrouvèrent dans leurs lits."),
 ("HILLEL", "Arié… Pardon pour le vélo. Demain matin, il est à toi toute la matinée. C'est mon {neder}. Et je le tiendrai."),
 ("ARIE", "Merci, {hillel}. Et après, on fera du vélo ensemble. Comme {reouven} avec ses {ahim}."),
 ("EYDEL", "Qui se souvient des mots ?"),
 ("HILLEL", "{neder}, la promesse. {yarden}, le Jourdain. {ir}, la ville. {massaot}, les étapes du voyage. Et {zikaron}, le souvenir."),
 ("N", "Et les trois enfants s'endormirent, au bout de leur propre petite étape, en attendant celle de demain. {layla tov}, {eydel}. {layla tov}, Arié. {layla tov}, {hillel}. Fais de beaux rêves."),
]

def f(s):
    return s.format(**W)

SEGMENTS = [(sp, f(t)) for sp, t in S]
AMBIENCE = []
