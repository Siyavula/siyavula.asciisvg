namesCsv = """
Jessica,female
Daniel,male
Nicole,female
Kevin,male
Emma,female
David,male
Monique,female
Andrew,male
Courtney,female
Emmanuel,male
Kayla,female
Megan,female
Ben,male
Kelly,female
Joshua,male
Angelique,female
Chris,male
Hannah,female
Richard,male
Phillip,male
Melanie,female
Justine,female
Gift,male
Deborah,female
Christopher,male
Jacob,male
Mario,male
Carina,female
Talwar,male
Matthew,male
Nicky,female
Jacques,male
Amy,female
Louis,male
Werner,male
Johan,male
Mike,male
Sarah,female
Lisa,female
Peter,male
Ali,male
Kabir,male
Abdoul,male
Amirah,female
Nthabiseng,female
Vaishna,female
Anita,female
Yaseen,male
Riaan,male
Ben,male
Langa,male
Dumile,male
Lulamile,male
Mzwandile,male
Khuthala,female
Anathi,both
Mcebisi,male
Cokisa,female
Bukelwa,female
Methuli,male
Phozisa,female
Fezekile,male
Songezo,male
Ntombebhongo,female
Bonani,male
Zenzile,male
Mkhuseli,male
Mandilakhe,male
Thobeka,female
Nontsikelelo,female
Mphikeleli,male
Zwelibanzi,male
Ntombikanina,female
Xolile,female
Khayalethu,male
Qiniso,both
Jabulile,female
Langalibalele,male
Lindiwe,female
Bongani,male
Jezile,female
Nqobani,male
Gabisile,female
Sandile,male
Ntuthuko,female
Xabanisile,female
Yengwayo,male
Sindisiwe,female
Jwayelani,male
Nkosingiphile,male
Sehlolo,male
Lefu,male
Mohato,male
Phetoho,male
Realeboha,male
Rethabile,male
Khethang,male
Tlali,male
Nthofeela,male
Likengkeng,female
Kutlwano,female
Masoabi,female
Moselantja,female
Reabilwe,female
Mathe,female
Tlotliso,female
Liboko,female
Limpho,female
Nyakallo,female
""".strip()

namesCsv = [entry.split(',') for entry in namesCsv.split('\n')]
allNames = [entry[0] for entry in namesCsv]
maleNames = [entry[0] for entry in namesCsv if entry[1] in ['male','both']]
femaleNames = [entry[0] for entry in namesCsv if entry[1] in ['female','both']]

def generate():
    random = ENVIRONMENT.random
    return allNames[random.randint(0, len(allNames)-1)]

def generate_male():
    random = ENVIRONMENT.random
    return maleNames[random.randint(0, len(maleNames)-1)]

def generate_female():
    random = ENVIRONMENT.random
    return femaleNames[random.randint(0, len(femaleNames)-1)]
