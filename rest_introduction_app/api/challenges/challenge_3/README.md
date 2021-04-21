HOW TO COLLECT FLAGS IN CHALLENGE 3:

nucleocreator -> call POST /nucleotide endpoint (10 times)
aminoacid_appender -> call POST /triplets endpoint (10 times)
mutator -> call PATCH /triplets/{triplet_id} endpoint (10 times)
reductor -> call DELETE /triplets/{triplet_id} endpoint (10 times)
eradicator -> the flag is completed once the sequence is deleted (0 nucleotides, empty sample)
architect -> call POST /triplets endpoint (50 times)
observer -> call GET /sample_sequence endpoint (5 times)

proteomaster -> all above flags collected + call GET /translation endpoint


GET /information - zwraca informacje o zadaniu
POST /register_as_technician - zakłada konto w laboratorium
GET /check_flags - zwraca listę flag wraz ze stanem ich wykonania
GET /primary_sequence - zwraca sekwencję próbki pierwotnej, niezmodyfikowanej
GET /sample_sequence - zwraca sekwencję próbki modyfikowanej, która podlega naszym modyfikacjom
GET /copy - kopiuje sekwencje próbki pierwotnej do próbki modyfikowanej
GET /triplets/{triplet_id} - zwraca n-ty triplet z sekwencji modyfikowanej
POST /triplets/ - dodaje triplet na końcu sekwencji modyfikowanej
PATCH /triplets/{triplet_id} - w miejsce n-tego tripletu podstawia inny triplet
PUT /triplets/ - zastępuje sekwencję próbki modyfikowanej podanym tripletem
DELETE /triplets/{triplet_id} - usuwa n-ty triplet z sekwencji próbki modyfikowanej
GET /nucleotides/{nucleotide_id} - zwraca n-ty nukleotyd z sekwencji modyfikowanej
POST /nucleotides/ - dodaje nukleotyd na końcu sekwencji modyfikowanej
PATCH /nucleotides/{nucleotide_id} - w miejsce n-tego nukleotydu podstawia inny nukleotyd
PUT /nucleotides/ - zastępuje sekwencję próbki modyfikowanej podanym nukleotydem
DELETE /nucleotides/{nucleotide_id} - usuwa n-ty nukleotyd z sekwencji próbki modyfikowanej
GET /translation - zwraca sekwencję aminokwasów (peptyd), która została utworzona na podstawie sekwencji próbki modyfikowanej.