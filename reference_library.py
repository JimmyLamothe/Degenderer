import json
from collections import OrderedDict

with open('reference/nb_names.json', 'r') as filename:
    NB_NAMES = json.load(filename) #List
    
with open('reference/nb_names_by_decade.json', 'r') as filename:
    NB_NAMES_BY_DECADE = json.load(filename) #Dict

with open('reference/gendered_names.json', 'r') as filename:
    GENDERED_NAMES = json.load(filename) #List

with open('reference/gendered_names_by_decade.json', 'r') as filename:
    GENDERED_NAMES_BY_DECADE = json.load(filename) #Dict

with open('reference/boy_names.json', 'r') as filename:
    BOY_NAMES = json.load(filename) #List

with open('reference/boy_names_by_decade.json', 'r') as filename:
    BOY_NAMES_BY_DECADE = json.load(filename) #Dict

with open('reference/girl_names.json', 'r') as filename:
    GIRL_NAMES = json.load(filename) #List

with open('reference/girl_names_by_decade.json', 'r') as filename:
    GIRL_NAMES_BY_DECADE = json.load(filename) #Dict    
    
with open('reference/nb_names_modern.json', 'r') as filename:
    invalid = NB_NAMES + ['Infant', 'Baby', 'Unknown','Lorenza','Elisha','Kalani']
    NB_NAMES_MODERN = [name for name in json.load(filename) if not name in invalid]

AMBIGUOUS_NAMES = ['Jesus','King','Princess','Summer','Rose','April','May','June']
    
PRONOUN_DICTIONARY = OrderedDict({
    'He' : 'They',
    'he' : 'they',
    'She' : 'They',
    'she' : 'they',
    'His' : 'Their(s)',
    'his' : 'their(s)',
    'Her' : 'Their',
    'her' : 'their/them',
    'hers' : 'theirs',
    'Him' : 'Them',
    'him' : 'them',
    'Himself' : 'Themself',
    'himself' : 'themself',
    'Herself' : 'Themself',
    'herself' : 'themself',
    'Man' : 'Person',
    'Men' : 'People',
    'Woman' : 'Person',
    'Women' : 'People',
    'man' : 'person',
    'men' : 'people',
    'woman' : 'person',
    'women' : 'people',
    'Mother' : 'Parent',
    'Mothers' : 'parents',
    'mother' : 'parent',
    'mothers' : 'parents',
    'Father' : 'Parent',
    'Fathers' : 'Parents',
    'father' : 'parent',
    'fathers' : 'parents',
    'Mama' : 'Mapa',
    'Mommy' : 'Mapa',
    'Mamma' : 'Mapa',
    'mama' : 'mapa',
    'mommy' : 'mapa',
    'mamma' : 'mapa',
    'Papa' : 'Mapa',
    'Poppa': 'Mapa',
    'Poppy' : 'Mapa',
    'papa' : 'mapa',
    'poppa' : 'mapa',
    'Brother' : 'Sibling',
    'Brothers' : 'Siblings',
    'brother' : 'sibling',
    'brothers' : 'brothers',
    'Bro' : 'Sib',
    'Bros' : 'Sibs',
    'bro' : 'sib',
    'bros' : 'sibs',
    'Sister' : 'Sibling',
    'Sisters' : 'Siblings',
    'Sis' : 'sis',
    'sister' : 'sibling',
    'sisters' : 'siblings',
    'Brothers and sisters' : 'siblings',
    'sis' : 'sib',
    'Mr' : 'Mx',
    'Mrs' : 'Mx',
    'Miss' : 'Mx',
    'Mistress' : 'Mx',
    'Sir' : "Sir’ram",
    'sir' : "Sir’ram",
    'Sirs' : "Sir’rams",
    'sirs' : "sir’rams",
    'Mister' : "Sir’ram",
    'Missus' : "Sir’ram",
    'Missis' : "Sir’ram",
    'Madame' : "Sir’ram",
    'Madam' : "Sir’ram",
    "Ma'am" : "Sir’ram",
    "Ma’am" : "Sir’ram",
    "ma'am" : "sir’ram",
    "ma’am" : "sir’ram",
    'Boy' : 'Youth',
    'Boys' : 'Youths',
    'boy' : 'youth',
    'boys' : 'youths',
    'Girl' : 'Youth',
    'Girls' : 'Youths',
    'girl' : 'youth',
    'girls' : 'youths',
    'Boyhood' : 'Childhood',
    'boyhood' : 'childhood',
    'Boyhoods' : 'Childhoods',
    'boyhoods' : 'boyhoods',
    'Girlhood' : 'Childhood',
    'girlhood' : 'childhood',
    'Girlhoods' : 'Childhoods',
    'girlhoods' : 'boyhoods',
    'Maiden' : 'Young person',
    'Maidens' : 'Young people',
    'maiden' : 'young person',
    'maidens' : 'young people',
    'Lad' : 'Young person',
    'Lads' : 'Young people',
    'lad' : 'young person',
    'lads' : 'young people',
    'Laddie' : 'Young person',
    'Laddies' : 'Young people',
    'laddie' : 'young person',
    'laddies' : 'young people',
    'Gal' : 'Young person',
    'Gals' : 'Young People',
    'gal' : 'young person',
    'gals' : 'young people',
    'Lady' : 'Gentleperson',
    'Ladies' : 'Gentlepeople',
    'lady' : 'gentleperson',
    'ladies' : 'gentlepeople',
    'Gentleman' : 'Gentleperson',
    'Gentlemen': 'Gentlepeople',
    'gentleman' : 'gentleperson',
    'gentlemen' : 'gentlepeople',
    'Ladies and Gentlemen' : 'Gentlepeople',
    'Ladies and gentlemen' : 'Gentlepeople',
    'ladies and gentlemen' : 'gentlepeople',
    'Uncle' : 'Auntcle',
    'Uncles' : 'Auntcles',
    'uncle' : 'auntcle',
    'uncles' : 'auntcles',
    'Aunt' : 'Auntcle',
    'aunt' : 'auntcle',
    'Aunts' : 'Auntcles',
    'aunts' : 'auntcles',
    'Uncles and aunts' : 'Auntcles',
    'Aunts and uncles' : 'Auntcles',
    'Uncles and Aunts' : 'Auntcles',
    'Aunts and Uncles' : 'Auntcles',
    'uncles and aunts' : 'auntcles',
    'aunts and uncles' : 'auntcles',
    'Niece' : 'Sibkid',
    'niece' : 'sibkid',
    'Nieces' : 'Sibkids',
    'nieces' : 'sibkids',
    'Nephew' : 'Sibkid',
    'Nephews' : 'Sibkids',
    'nephew' : 'sibkid',
    'nephews' : 'sibkids',
    'Nieces and nephews' : 'Sibkids',
    'Nephews and nieces' : 'Sibkids',
    'nieces and nephews' : 'sibkids',
    'nephews and nieces' : 'sibkids',
    'Grandfather' : 'Grandparent',
    'Grandfathers' : 'Grandparents',
    'grandfather' : 'grandparent',
    'grandfathers' : 'grandparents',
    'Grandmother' : 'Grandparent',
    'Grandmothers' : 'Grandmothers',
    'grandmother' : 'grandmother',
    'grandmothers' : 'grandmothers',
    'Grandpa' : 'Gran',
    'Grandpas' : 'Grans',
    'grandpa' : 'gran',
    'grandpas' : 'grans',
    'Grandma' : 'Gran',
    'grandma' : 'gran',
    'grandmas' : 'grans',
    'Granny' : 'Gran',
    'Grannies' : 'Grans',
    'granny' : 'gran',
    'grannies' : 'grans',
    'Girlfriend' : 'Partner',
    'Girlfriends' : 'Partners',
    'girlfriend' : 'partner',
    'girlfriends' : 'girlfriends',
    'Boyfriend' : 'Partner',
    'Boyfriends' : 'Partners',
    'boyfriend' : 'partner',
    'boyfriends' : 'partners',
    'Husband' : 'Partner',
    'Husbands' : 'Partners',
    'husband' : 'partner',
    'husbands' : 'partners',
    'Wife' : 'Partner',
    'Wives' : 'Partners',
    'wife' : 'partner',
    'wives' : 'partners',
    'Fiancée' : 'Fiancé',
    'fiancée' : 'fiancé',
    'Godfather' : 'Godparent',
    'Godfathers' : 'Godfathers',
    'godfather' : 'godparent',
    'godfather' : 'godfathers',
    'Godmother' : 'Godparent',
    'Godmothers' : 'Godparents',
    'godmother' : 'godparent',
    'godmothers' : 'godparents',
    'Son' : 'Child',
    'Sons' : 'Children',
    'son' : 'child',
    'sons' : 'children',
    'Daughter' : 'Child',
    'Daughters' : 'Children',
    'daughter' : 'child',
    'daughters' : 'children',
    'Sons and daughters' : 'Children',
    'sons and daughters' : 'children',
    'Godson' : 'Godchild',
    'Godsons' : 'Godchildren',
    'godson' : 'godchild',
    'godsons' : 'godchildren',
    'Goddaughter' : 'Godchild',
    'Goddaughters' : 'Godchildren',
    'goddaughter' : 'godchild',
    'goddaughters' : 'godchildren',
    'Grandson' : 'Grandchild',
    'Grandsons' : 'Grandchildren',
    'grandson' : 'grandchild',
    'grandsons' : 'grandchildren',
    'Granddaughter' : 'Grandchild',
    'Granddaughters' : 'Grandchildren',
    'granddaughter' : 'grandchild',
    'granddaughters' : 'grandchildren',
    'Barman' : 'Bartender',
    'Barmen' : 'Bartenders',
    'barman' : 'bartender',
    'barmen' : 'bartenders',
    'Barmaid' : 'Bartender',
    'Barmaids' : 'Bartenders',
    'barmaid' : 'bartender',
    'barmaids' : 'bartenders',
    'Businessman' : 'Businessperson',
    'Businessmen' : 'Businesspeople',
    'businessman' : 'businessperson',
    'businessmen' : 'businesspeople',
    'Businesswoman' : 'Businessperson',
    'Businesswomen' : 'Businesspeople',
    'businesswoman' : 'businessperson',
    'businesswomen' : 'businesspeople',
    'King' : 'Ruler',
    'Kings' : 'Rulers',
    'king' : 'ruler',
    'kings' : 'rulers',
    'Queen' : 'Ruler',
    'Queens' : 'Rulers',
    'queen' : 'ruler',
    'queens' : 'rulers',
    'King and Queen' : 'Rulers',
    'Priest' : 'Clergyperson',
    'Priests' : 'Clergypeople',
    'priest' : 'clergyperson',
    'priests' : 'clergypeople',
    'Priestess' : 'Clergyperson',
    'Priestesses' : 'Clergypeople',
    'priests' : 'clergyperson',
    'priestesses' : 'clergypeople',
    'Clergyman' : 'Clergyperson',
    'Clergymen' : 'Clergypeople',
    'clergyman' : 'clergyperson',
    'clergymen' : 'clergypeople',
    'Clergywoman' : 'Clergyperson',
    'Clergywomen' : 'Clergypeople',
    'clergywoman' : 'clergyperson',
    'clergywomen' : 'clergypeople',
    'Cowboy' : 'Cowhand',
    'Cowboys' : 'Cowhands',
    'cowboy' : 'cowhand',
    'cowboys' : 'cowhands',
    'Cowgirl' : 'Cowhand',
    'Cowgirls' : 'Cowhands',
    'cowgirl' : 'cowhand',
    'cowgirls' : 'cowhands',
    'Actor' : 'Comedian',
    'Actors' : 'Comedians',
    'actor' : 'comedian',
    'actors' : 'comedians',
    'Actress' : 'Comedian',
    'Actresses' : 'Comedians',
    'actress' : 'comedian',
    'actresses' : 'comedians',
    'Steward' : 'Attendant',
    'Stewards' : 'Attendants',
    'steward' : 'attendant',
    'stewards' : 'attendants',
    'Stewardess' : 'Attendant',
    'Stewardesses' : 'Attendants',
    'stewardess' : 'attendant',
    'stewardesses' : 'attendants',
    'Hero' : 'Heroic person',
    'Heros' : 'Heroic people',
    'hero' : 'heroic person',
    'heros' : 'heroic people',
    'Heroine' : 'Heroic person',
    'Heroines' : 'Heroic people',
    'heroine' : 'heroic person',
    'heroines' : 'heroic people',
    'Horseman' : 'Horse rider',
    'Horsemen' : 'Horse riders',
    'horseman' : 'horse rider',
    'horsemen' : 'horse riders',
    'Horsewoman' : 'Horse rider',
    'Horsewomen' : 'Horse riders',
    'horsewoman' : 'horse rider',
    'horsewomen' : 'horse riders',
    'Waitress' : 'Server',
    'Waitresses' : 'Servers',
    'waitress' : 'server',
    'waitresses' : 'server',
    'Prince' : 'Nobleperson',
    'Princes' : 'Noblepeople',
    'Princess' : 'Nobleperson',
    'Princesses' : 'Noblepeople',
    'Baron' : 'Nobleperson',
    'Barons' : 'Noblepeople',
    'Baroness' : 'Nobleperson',
    'Baronesses' : 'Noblepeople',
    'Duke' : 'Nobleperson',
    'Dukes' : 'Noblepeople',
    'Duchess' : 'Nobleperson',
    'Duchesses' : 'Noblepeople',
    'prince' : 'nobleperson',
    'princes' : 'noblepeople',
    'princess' : 'nobleperson',
    'princesses' : 'noblepeople',
    'Handsome' : 'Good-looking',
    'handsome' : 'good-looking',
    'Beautiful' : 'good-looking',
    'beautiful' : 'good-looking',
    'Lord' : 'Almighty',
    'Bride' : 'Spouse',
    'Brides' : 'Spouses',
    'bride' : 'spouse',
    'brides' : 'spouses',
    'Bridesmaid' : 'Spousefriend',
    'Bridesmaids' : 'Spousefriends',
    'bridesmaid' : 'spousefriend',
    'bridesmaids' : 'spousefriends',
    'Groomsman' : 'Spousefriend',
    'Groomsmen' : 'Spousefriends',
    'groomsman' : 'spousefriend',
    'groomsmen' : 'spousefriends',
    'Schoolmistress' : 'Schoolteacher',
    'schoolmistress' : 'schoolteachers',
    'Schoolgirl': 'Schoolchild',
    'Schoolgirls' : 'Schoolchildren',
    'schoolgirl' : 'schoolchild',
    'schoolgirls' : 'schoolchildren',
    'Schoolboy': 'Schoolchild',
    'Schoolboys' : 'Schoolchildren',
    'schoolboy' : 'schoolchild',
    'schoolboys' : 'schoolchildren',
    'Mailman' : 'Mail carrier',
    'Mailmen' : 'Mail carriers',
    'mailman' : 'mail carrier',
    'mailmen' : 'mail carriers',
    'Milkman' : 'Milkperson',
    'Milkmen' : 'Milkpeople',
    'milkman' : 'milkperson',
    'milkmen' : 'milkperson',
    'Salesman' : 'Salesperson',
    'Salesmen' : 'Salespeople',
    'salesman' : 'salesperson',
    'salesmen' : 'salespeople',
    'Men and women' : 'People',
    'men and women' : 'people'
})
