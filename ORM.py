from peewee import *


db = SqliteDatabase('./db/database.db')

class Book(Model):
    
    id = PrimaryKeyField(unique=True)
    name = CharField()
    description = TextField()
    instructions = TextField()

    class Meta:
        database = db
        order_by = 'id'

db.create_tables([Book])

book1 = Book(name = 'Hieroglyph AI book (English edition)', description ='Who is Mr. Anir Itak? Is it an artificial intelligence system shocking experts with its ability to use and understand language as human beings or an author who wishes to remain anonymous? Hieroglyph AI, a book published in December 2019 by Anir Itak, whoever the author is, provides the seriously intelligent, out of the box one interpretation of Artificial Intelligences natures. This ambitious novel addresses the question: can Artificial Intelligence love, featuring the latest breakthrough ideas in science.The main plot revolves around the very distant future where Particle Accelerator, a legendary scientist in random events management science, helps people find happiness, integrity, and love. Paradoxical as it may seem, the hero himself, due to the peculiarities of the structure of the Universe, cannot find a person whom he could love. Challenging fate, he is going on a dangerous journey through space and time, finding answers to some of his questions in our Universe. Here Particle Accelerator enters into a fierce struggle for the right to decipher the love algorithm, codenamed Hieroglyph AI, with Artificial Intelligence. Which of the rivals will be the first to cope with the task by cracking the Creator code? And, most importantly, why? The dual narrative toggles between Particle Accelerator adventures in our Universe and the incredible love story of Particle Accelerator and Beautiful Woman to the more interior journey of rivalry between two types of intelligence, the human and the artificial one. Who will win in the end? The winner will change the world as we know it forever.', instructions =' Buy your book /buy')
book1.save()
book2 = Book(name = '119977 Short stories', description ='This seria of short stories is dedicated to Artificial Intelligence topic in relations with very unusial situations different people face to in their lives.', instructions = 'Preorder! Publication date 27 of July 2023. Contact our manager@IIWOII_Group for the bill')
book2.save()
book3 = Book(name='The UnBelievable adventures of the Risk Manager in Russia book', description='This is very funny and , at the same time, very horryfing story about the exam in risk management discipline which takes place in the very far future, where Afrificial Intelligence plays the role of an examinator. The topic of the discussion is one event that takes place in Russia 2077 and from that point in time something goes very wrong ...but for whom?', instructions='Preorder! Publication date 27 of December 2023. Contact our manager@IIWOII_Group for the bill')
book3.save()