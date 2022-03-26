#Virology: the Genetic Research



You are the Genome Researcher. You are meddling with Coronavirus SARS-Cov-2 RNA...
Try to change the RNA at your disposal to uncover as many medical breakthroughs as possible.
Good luck researcher.
Our souls fates' depend on you!

### HOW TO COLLECT FLAGS IN CHALLENGE 3:

---

- **nucleocreator** --> call POST /nucleotide endpoint (10 times)
- **aminoacid_appender** --> call POST /triplets endpoint (10 times)
- **mutator** --> call PATCH /triplets/{triplet_id} endpoint (10 times)
- **reductor** --> call DELETE /triplets/{triplet_id} endpoint (10 times)
- **eradicator** --> the flag is completed once the sequence is deleted (0 nucleotides, empty sample)
- **architect** --> call POST /triplets endpoint (50 times)
- **observer** --> call GET /sample_sequence endpoint (5 times)
- **proteomaster** --> all above flags collected + call GET /translation endpoint

### AVAILABLE ENDPOINTS:

---

- GET /information - information about the task
- POST /register_as_technician - register you as an employee
- GET /check_flags - list of flags to capture with the status of completion
- GET /primary_sequence - sequence of primary, not modified sample
- GET /sample_sequence - sequence of working sample with your modifications
- GET /copy - copy primary sample sequence into working sample sequence
- GET /triplets/{triplet_id} - n-th triplet from working sample sequence
- POST /triplets/ - adds triplet to the end of working sample sequence
- PATCH /triplets/{triplet_id} - substitutes n-th triplet with provided triplet
- PUT /triplets/ - substitutes whole sequence of working sample with provided triplet
- DELETE /triplets/{triplet_id} - deletes n-th triplet from working sample sequence
- GET /nucleotides/{nucleotide_id} - returns n-th triplet from working sample sequence
- POST /nucleotides/ - adds nucleotide to the end of working sample sequence
- PATCH /nucleotides/{nucleotide_id} - substitutes n-th nucleotide with provided nucleotide
- PUT /nucleotides/ - substitutes whole sequence of working sample with provided nucleotide
- DELETE /nucleotides/{nucleotide_id} - deletes n-th nucleotide from working sample sequence
- GET /translation - returns sequence of aminoacids (peptide) which was created based on working sample sequence