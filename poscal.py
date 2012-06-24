"""positivist.py - Library for converting gregorian dates to
dates in the positivist calendar.

Copyright (c) 2008 - 2012 James Mitchelhill (james@jamesmitchelhill.com)

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import datetime

# define useful lists and dicts

# Positivist months have both a name and a dedication
positivist_months = (("Moses", "Humanity"),
                     ("Homer", "Marriage"),
                     ("Aristotle", "Paternity"),
                     ("Archimedes", "Filiation"),
                     ("Caesar", "Fraternity"),
                     ("Saint-Paul", "Domesticity"),
                     ("Charlemagne", "Fetishism"),
                     ("Dante", "Polytheism"),
                     ("Gutenburg", "Monotheism"),
                     ("Shakespeare", "Women"),
                     ("Descartes", "the Priest"),
                     ("Frederick", "the Proletariat"),
                     ("Bichat", "Industry"))
                     
# Positivist day names are the same as Gregorian day names
days_of_the_week = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday")

# suffixes for the day names
suffix_dict = {1: "st", 2: "nd", 3: "rd", 21: "st", 22: "nd", 23: "rd"}
                     
# Every positivist day is dedicated to a person. From Monday to Saturday there
# are two names - the first is used for non-leap s and the second is used
# only in leap years. Sundays have just the one name which is used regardless.
positivist_day_names = ((u'Prometheus', u'Kadmus'), (u'Hercules', u'Theseus'),
(u'Orpheus', u'Tiresias'), (u'Ulysses',), (u'Lycurgus',), (u'Romulus',),
(u'Numa',), (u'Belus',), (u'Sesostris',), (u'Menu',), (u'Cyrus',),
(u'Zoroaster',), (u'The Druids', u'Ossian'), (u'Buddha',), (u'Fu-Xi',),
(u'Laozi',), (u'Mencius',), (u'The Theocracies of Tibet',),
(u'The Theocracies of Japan',), (u'Manco Capac', u'Kamehameha'),
(u'Confucius',), (u'Abraham',), (u'Joseph',), (u'Samuel',),
(u'Solomon', u'David'), (u'Isaac',), (u'Saint John the Baptist',),
(u'Muhammad',), (u'Hesiod',), (u'Tyrtaeus', u'Sappho'), (u'Anacreon',),
(u'Pindar',), (u'Sophocles', u'Euripides'), (u'Theocritus', u'Longus'),
(u'Aeschylus',), (u'Scopas',), (u'Zeuxis',), (u'Ictinus',), (u'Praxiteles',),
(u'Lysippos',), (u'Apelles',), (u'Phidias',), (u'Aesop', u'Pilpay'),
(u'Aristophanes',), (u'Terence', u'Menander'), (u'Phaedrus',), (u'Juvenal',),
(u'Lucian',), (u'Plautus',), (u'Ennius',), (u'Lucretius',), (u'Horace',),
(u'Tibullus',), (u'Ovid',), (u'Lucan',), (u'Virgil',), (u'Anaximander',),
(u'Anaximenes',), (u'Heraclitus',), (u'Anaxagorus',), (u'Democritus',),
(u'Herodotus',), (u'Thales',), (u'Solon',), (u'Xenophanes',), (u'Empedocles',),
(u'Thucydides',), (u'Archytas',), (u'Apollonius of Tyana',), (u'Pythagorus',),
(u'Aristippus',), (u'Antisthenes',), (u'Zeno',),
(u'Cicero', u'Pliny the Younger'), (u'Epictetus', u'Arrian'), (u'Tacitus',),
(u'Socrates',), (u'Xenocrates',), (u'Philo of Alexandria',),
(u'Saint John the Evangelist',), (u'Saint Justin', u'Saint Irenaeus'),
(u'Saint Clement of Alexandria',), (u'Origen',), (u'Plato',),
(u'Theophrastus',), (u'Herophilus',), (u'Erasistratus',), (u'Celsus',),
(u'Galen',), (u'Avicenna', u'Averroes'), (u'Hippocrates',), (u'Euclid',),
(u'Aristeas',), (u'Theodosius of Bithynia',), (u'Hero',), (u'Pappus',),
(u'Diophantus',), (u'Apollonius',), (u'Eudoxus', u'Aratus'),
(u'Pytheas', u'Nearchus'), (u'Aristarchus', u'Berossus'),
(u'Eratosthenes', u'Sosigenes'), (u'Ptolemy',), (u'Albategnius', u'Nasreddin'),
(u'Hipparchus',), (u'Varro',), (u'Columella',), (u'Vitruvius',), (u'Strabo',),
(u'Frontinus',), (u'Plutarch',), (u'Pliny the Elder',), (u'Miltiades',),
(u'Leonidas',), (u'Aristides',), (u'Cimon',), (u'Xenophon',),
(u'Phocion', u'Epnaminondas'), (u'Themistocles',), (u'Pericles',),
(u'Philip',), (u'Demosthenes',), (u'Ptolemy I Soter',), (u'Philopoemen',),
(u'Polybius',), (u'Alexander',), (u'Junius Brutus',), (u'Camillus',),
(u'Fabricius', u'Regulus'), (u'Hannibal',), (u'Paulus Aemilius',),
(u'Marius', u'The Gracchi'), (u'Scipio',), (u'Augustus', u'Maecenas'),
(u'Vespasian',), (u'Hadrian',), (u'Antonius', u'Marcus Aurelius'),
(u'Papinian', u'Ulpian'), (u'Alexander Severus',), (u'Trajan',),
(u'Saint Luke',), (u'Saint Cyprian',), (u'Saint Athanasius',),
(u'Saint Jerome',), (u'Saint Ambrose',), (u'Saint Monica',),
(u'Saint Augustine',), (u'Constantine',), (u'Theodosius',),
(u'Saint Chrysostom', u'Saint Basil'), (u'Saint Pulcheria',),
(u'Sainte Genevi\xe8ve of Paris',), (u'Saint Gregory the Great',),
(u'Hildebrand',), (u'Saint Benedict', u'Saint Anthony'),
(u'Saint Boniface', u'Saint Austin'),
(u'Saint Isidore of Seville', u'Saint Bruno'),
(u'Lanfranc', u'Saint Anselm'), (u'Heloise',),
(u'The Architects of the Middle Ages', u'Saint B\xe9n\xe9zet'),
(u'Saint Bernard',), (u'Saint Francis Xavier', u'Ignatius of Loyola'),
(u'Saint Charles Borromeo', u'Federico Borromeo'),
(u'Saint Theresa', u'Saint Catherine of Siena'),
(u'Saint Vincent de Paul', u'Fl\xe9chier'), (u'Bourdaloue', u'Claude Fleury'),
(u'William Penn', u'George Fox'), (u'Bossuet',), (u'Theodoric the Great',),
(u'Pelagius',), (u'Otto the Great', u'Henry I the Fowler'), (u'Saint Henry',),
(u'Villiers', u'La Valette'), (u'Don John of Austria', u'John III Sobieski'),
(u'Alfred',), (u'Charles Martel',), (u'El Cid', u'Tancred'),
(u'Richard', u'Saladin'), (u'Joan of Arc',),
(u'Albuquerque', u'Walter Raleigh'), (u'Bayard',), (u'Godfrey',),
(u'Saint Leo the Great',), (u'Gerbert', u'Peter Damian'),
(u'Peter the Hermit',), (u'Suger', u'Saint Eligius'),
(u'Alexander III', u'Thomas Becket'),
(u'Saint Francis of Assisi', u'Saint Dominic'), (u'Pope Innocent III',),
(u'Saint Clotilde',), (u'Saint Balthild',), (u'Saint Stephen I of Hungary',),
(u'Saint Elisabeth of Hungary',), (u'Blanche of Castile',),
(u'Saint Ferdinand III', u'Alfonso X'), (u'Saint Louis',),
(u'The Troubadours',), (u'Boccaccio',), (u'Cervantes',), (u'Rabelais',),
(u'La Fontaine',), (u'Fo\xe9', u'Goldsmith'), (u'Ariosto',),
(u'Leonardo da Vinci', u'Titian'), (u'Michelangelo', u'Salvatore Rosa'),
(u'Holbein', u'Rembrandt'), (u'Poussin', u'Lesueur'),
(u'Murillo', u'Alonzo Cano'), (u'Teniers', u'Rubens'), (u'Raphael',),
(u'Froissart', u'Joinville'), (u'Camoens',), (u'The Spanish Romantics',),
(u'Chateaubriand',), (u'Walter Scott',), (u'Manzoni',), (u'Tasso',),
(u'Petrarch',), (u'Thomas \xe0 Kempis', u'Louis of Grenada'),
(u'Madame de La Fayette', u'Madame de Sta\xebl'),
(u'F\xe9nelon', u'Saint Francis de Sales'), (u'Klopstock', u'Gessner'),
(u'Byron',), (u'Milton',), (u'Marco Polo', u'Chardin'),
(u'Jacques Coeur', u'Gresham'), (u'Vasco da Gama', u'Magellan'),
(u'Napier', u'Briggs'), (u'Lacaille', u'Delambre'), (u'Cook', u'Tasman'),
(u'Columbus',), (u'Benvenuto Cellini',), (u'Amontons', u'Wheatstone'),
(u'Harrison', u'Pierre Leroy'), (u'Dollond', u'Graham'),
(u'Arkwright', u'Jacquart'), (u'Cont\xe9',), (u'Vaucanson',),
(u'Stevin', u'Torricelli'), (u'Mariotte', u'Boyle'), (u'Papin', u'Worcester'),
(u'Black',), (u'Jouffroy', u'Fulton'), (u'Dalton', u'Thilorier'), (u'Watt',),
(u'Bernard Palissy',), (u'Guglielmini', u'Riquet'), (u'Duhamel du Monceau',),
(u'Saussure', u'Bouguer'), (u'Coulomb', u'Borda'), (u'Carnot', u'Vauban'),
(u'Montgolfier',), (u'Lope de Vega',), (u'Moreto', u'Guill\xe9n de Castro'),
(u'Rojas',), (u'Otway',), (u'Lessing',), (u'Goethe',), (u'Calderon',),
(u'Tirso',), (u'Vondel',), (u'Racine',), (u'Voltaire',),
(u'Alfieri', u'Metastasio'), (u'Schiller',), (u'Corneille',), (u'Alarc\xf3n',),
(u'Madame de Motteville', u'Madame Roland'),
(u'Madame de S\xe9vign\xe9', u'Lady Montague'), (u'Lesage', u'Sterne'),
(u'Madame de Staal', u'Miss Edgeworth'), (u'Fielding', u'Richardson'),
(u'Moli\xe8re',), (u'Pergolesi', u'Palestrina'), (u'Sacchini', u'Gr\xe9try'),
(u'Gluck', u'Lully'), (u'Beethoven', u'Handel'), (u'Rossini', u'Weber'),
(u'Bellini', u'Donizetti'), (u'Mozart',),
(u'Albert Magnus', u'Vincent of Beauvais'), (u'Roger Bacon', u'Ramon Llull'),
(u'Saint Bonaventure', u'Joachim'), (u'Ramus', u'Cardan'),
(u'Montaigne', u'Erasmus'), (u'Campanella', u'Morus'),
(u'Saint Thomas Aquinas',), (u'Hobbes', u'Spinoza'),
(u'Pascal', u'Giordano Bruno'), (u'Locke', u'Malebranche'),
(u'Vauvenargues', u'Marquise de Lambert,'), (u'Diderot', u'Duclos'),
(u'Cabanis', u'George Leroy'), (u'Lord Bacon',), (u'Grotius', u'Cujacius'),
(u'Fontenelle',), (u'Vico', u'Herder'), (u'Fr\xe9ret', u'Winckelmann'),
(u'Montesquieu', u"d'Aguesseau"), (u'Buffon',), (u'Leibnitz',),
(u'Adam Smith', u'Robertson'), (u'Kant',), (u'Condorcet', u'Ferguson'),
(u'Fichte',), (u'Joseph de Maistre', u'Bonald'),
(u'Hegel', u'Marie-Sophie Germain'), (u'Hume',), (u'Mar\xeda de Molina',),
(u"Cosimo de' Medici",), (u'Philippe de Commines', u'Guicciardini'),
(u'Isabella I of Castile',), (u'Charles V', u'Pope Sixtus V'), (u'Henri IV',),
(u'Louis XI',), (u'Coligny', u"l'H\xf4pital"), (u'Barneveldt',),
(u'Gustavus Adolphus',), (u'De Witt',), (u'Ruyter',), (u'William III',),
(u'William I, Prince of Orange',), (u'Ximenes',), (u'Sully', u'Oxenstierna'),
(u'Colbert', u'Louis XIV'), (u'Walpole', u'Mazarin'), (u"d'Aranda", u'Pombal'),
(u'Turgot', u'Campomanes'), (u'Richelieu',), (u'Sidney', u'Lambert'),
(u'Franklin',), (u'Washington',), (u'Jefferson',), (u'Bolivar',),
(u'Francia',), (u'Cromwell',), (u'Copernicus', u'Tycho Brahe'), (u'Kepler',),
(u'Huygens', u'Varignon'), (u'Jacob Bernoulli', u'Johann Bernoulli'),
(u'Bradley', u'Halley'), (u'Volta', u'Amp\xe8re'), (u'Galileo',),
(u'Vi\xe8te', u'Harriott'), (u'Wallis', u'Fermat'),
(u'Clairaut', u'Maupertuis'), (u'Euler', u'Monge'),
(u"d'Alembert", u'Daniel Bernoulli'), (u'Lagrange', u'Joseph Fourier'),
(u'Newton',), (u'Bergmann', u'Scheele'), (u'Priestley', u'Dary'),
(u'Cavendish',), (u'Guyton Morveau',), (u'Berthollet',), (u'Berzelius',),
(u'Lavoisier',), (u'Harvey', u'Charles Bell'), (u'Boerhaave', u'Stahl'),
(u'Linnaeus', u'Bernard de Jussieu'), (u'Haller', u"Vicq-d'Azyr"),
(u'Lamarck', u'Oken'), (u'Broussais', u'Morgagni'), (u'Gall',))

# There are two festival days, on the 365th day and (for leap years)
festival_days = ["festival of the dead", "festival of women"]

month_suffix = "th"

        
class PositivistDate:
    """
    A date in the positivist calender. Takes a datetime.date as its
    argument.
    
    attributes
        is_festival - True if the day is a festival day
        month - number of the month from 0 to 12
        month_name - name of the month
        month_dedication - name of the quality the month is dedicated to
        day_of_month - number of the month from 1 to 28
        day_of_week - day of the week from 0 to 6
        day_of_week_name - name of the weekday (monday, tuesday, etc.)
        day_dedication - name of the person the day is dedicated to
    """
    def __init__(self, d):
        self.gregorian_date = d
        self.g_year = d.year
        self.year = d.year - 1788 # positivist year one was 1789
        self.day_of_year = self.get_day_of_year(d)
        self.leap_year = self.is_leap_year() # same leap years
        if self.day_of_year > 364:
            self.is_festival = True
            self.month = None
            self.month_name = None
            self.month_dedication = None
            self.day_of_month = None
            self.day_suffix = None
            self.day_of_week = None
            self.day_of_week_name = None
            if self.day_of_year == 365:
                self.day_dedication = festival_days[0] 
            elif self.day_of_year == 366:
                self.day_dedication = festival_days[1]
        else:
            self.is_festival = False
            self.month = (self.day_of_year) / 29
            self.month_name, self.month_dedication = positivist_months[self.month]
            self.day_of_month = ((self.day_of_year-1) % 28) + 1
            self.day_suffix = suffix_dict.get(self.day_of_month, month_suffix)
            self.day_of_week = self.day_of_year % 7
            self.day_of_week_name = days_of_the_week[self.day_of_week]
            self.day_dedication = self.get_day_dedication()
            
    def get_day_of_year(self, d):
        """
        Returns the day number of the year. January 1st is day 1, December
        31st is day 365 or day 366 in a leap year.
        """
        return (d - datetime.date(d.year-1, 12, 31)).days
        
    def is_leap_year(self):
        """
        Returns True if self.g_year is a leap year and False if it's not.
        """
        first_day_of_next_year = datetime.date(self.g_year+1, 1, 1)
        last_day_of_this_year = first_day_of_next_year - datetime.timedelta(days=1)
        return self.get_day_of_year(last_day_of_this_year) == 366
        
    def get_day_dedication(self):
        """
        Returns the dedication for self.day_of_year.
        """
        dedications = positivist_day_names[self.day_of_year-1]
        if self.leap_year:
            return dedications[-1]
        else:
            return dedications[0]
            
    def __str__(self):
        """
        Returns a string representing the full name of the date.
        """
        if self.is_festival:
            return "%(day_dedication)s, %(year)i" %\
                    {"day_dedication": self.day_dedication, "year": self.p_year} 
        else:
            sdict = {
                "day_of_week_name": self.day_of_week_name,
                "day_of_month": self.day_of_month,
                "day_suffix": self.day_suffix,
                "month_name": self.month_name,
                "year": self.p_year,
                "day_dedication": self.day_dedication,
                "month_dedication": self.month_dedication
            }
            return "%(day_of_week_name)s %(day_of_month)i%(day_suffix)s " \
                    "%(month_name)s, %(year)i - the day of %(day_dedication)s " \
                    "in the month of %(month_dedication)s" % sdict