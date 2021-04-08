#TODO challenge
#TODO Paweł Muzyka - genetyka
## challenge 3
## genom z tripletami
#tym razem basic auth
#- cały łańcuch jest kodowany aminokwasami RNA
# endpointy
# GET /rna filtruje wszystkie ustawione na none lub "" i buduje białko na podstawie łańcucha nukleotydów
# GET/PUT/PATCH/POST/DELETE triplets/{number}
# GET/PUT/PATCH/POST/DELETE nucleotides/{number}
# flagi - nucleocreator - po 10 postach nowych nukleotydów
# flagi - aminoacid_appender - po 10 postach nowych tripletów
# flaga - mutator - po 10 patchach w tripletach
# flaga - reduktor - po 10 deletach w tripletach
# flaga eradicator - po usunięciu całego kodu RNA
# flaga architect po dodaniu 50 postów tripletów i zdobyciu flagi architekt
# flaga observer po 5 getach na /rna
