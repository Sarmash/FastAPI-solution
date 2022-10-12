import time

from elasticsearch import Elasticsearch, helpers

GENRES = (
    {"genre": "Drama", "id": "1cacff68-643e-4ddd-8f57-84b62538081a"},
    {"genre": "Adventure", "id": "120a21cf-9097-479e-904a-13dd7198c1dd"},
    {"genre": "Animation", "id": "6a0a479b-cfec-41ac-b520-41b2b007b611"},
)


def filling_indexes():
    """Функция заполнения индекса жанров тестовыми данными"""

    genres = [
        {"genre": "Sci-Fi", "id": "6c162475-c7ed-4461-9184-001ef3d9f26e"},
        {"genre": "Action", "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"},
        {"genre": "Comedy", "id": "5373d043-3f41-4ea8-9947-4b746c601bbd"},
        {"genre": "Music", "id": "56b541ab-4d66-4021-8708-397762bff2d4"},
        {"genre": "Documentary", "id": "6d141ad2-d407-4252-bda4-95590aaf062a"},
        {"genre": "Biography", "id": "ca124c76-9760-4406-bfa0-409b1e38d200"},
        {"genre": "Crime", "id": "63c24835-34d3-4279-8d81-3c5f4ddb0cdc"},
        {"genre": "Mystery", "id": "ca88141b-a6b4-450d-bbc3-efa940e4953f"},
        {"genre": "Drama", "id": "1cacff68-643e-4ddd-8f57-84b62538081a"},
        {"genre": "Adventure", "id": "120a21cf-9097-479e-904a-13dd7198c1dd"},
        {"genre": "Animation", "id": "6a0a479b-cfec-41ac-b520-41b2b007b611"},
        {"genre": "Family", "id": "55c723c1-6d90-4a04-a44b-e9792040251a"},
        {"genre": "Fantasy", "id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd"},
        {"genre": "Romance", "id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5"},
        {"genre": "Western", "id": "0b105f87-e0a5-45dc-8ce7-f8632088f390"},
        {"genre": "Short", "id": "a886d0ec-c3f3-4b16-b973-dedcf5bfa395"},
        {"genre": "Thriller", "id": "526769d7-df18-4661-9aa6-49ed24e9dfd8"},
        {"genre": "Game-Show", "id": "fb58fd7f-7afd-447f-b833-e51e45e2a778"},
        {"genre": "Reality-TV", "id": "e508c1c8-24c0-4136-80b4-340c4befb190"},
        {"genre": "Musical", "id": "9c91a5b2-eb70-4889-8581-ebe427370edd"},
        {"genre": "History", "id": "eb7212a7-dd10-4552-bf7b-7a505a8c0b95"},
        {"genre": "War", "id": "c020dab2-e9bd-4758-95ca-dbe363462173"},
        {"genre": "Horror", "id": "f39d7b6d-aef2-40b1-aaf0-cf05e7048011"},
        {"genre": "Sport", "id": "2f89e116-4827-4ff4-853c-b6e058f71e31"},
        {"genre": "News", "id": "f24fd632-b1a5-4273-a835-0119bd12f829"},
        {"genre": "Talk-Show", "id": "31cabbb5-6389-45c6-9b48-f7f173f6c40f"},
    ]
    films = [
        {
            "actors": [
                {"id": "a91ff1c9-98a3-46af-a0d0-e9f2a2b4f51e", "name": "Suzy Stokey"},
                {"id": "040147e3-0965-4117-8112-55a2087e0b84", "name": "Marya Gant"},
                {"id": "b258f144-d771-4fa2-b6a2-42805c13ce4a", "name": "Sandy Brooke"},
                {"id": "f51f4731-3c26-4a72-9d68-cd0cd3d90a26", "name": "Ross Hagen"},
            ],
            "actors_names": ["Suzy Stokey", "Marya Gant", "Sandy Brooke", "Ross Hagen"],
            "description": "Two women who have been unjustly confined to a prison planet plot their escape, "
            "all the while having to put up with lesbian guards, crazed wardens and mutant rodents.",
            "director": "Fred Olen Ray",
            "genre": ["Sci-Fi", "Action", "Comedy"],
            "id": "00af52ec-9345-4d66-adbe-50eb917f463a",
            "imdb_rating": 3.5,
            "title": "Star Slammer",
            "writers": [
                {"id": "a2fd6df4-9f3c-4a26-8d59-914470d2aea0", "name": "Fred Olen Ray"},
                {
                    "id": "82416ac7-26fa-40a6-a433-1c756c0fad6e",
                    "name": "Miriam L. Preissel",
                },
                {"id": "dac61d8f-f36e-4351-a4d8-9048b87d00a6", "name": "Michael Sonye"},
            ],
            "writers_names": ["Fred Olen Ray", "Miriam L. Preissel", "Michael Sonye"],
        },
        {
            "actors": [
                {"id": "a91ff1c9-98a3-46af-a0d0-e9f2a2b4f51e", "name": "Suzy Stokey"},
                {
                    "id": "bdd44e92-7498-445b-998e-0c2bd9591052",
                    "name": "Erik Bauersfeld",
                },
                {"id": "ccf38643-1f0a-4b04-bcb5-dd27dde321f6", "name": "Clive Revill"},
            ],
            "actors_names": ["Suzy Stokey", "Erik Bauersfeld", "Clive Revill"],
            "description": "Be a Rebel pilot during the Galactic Civil War. "
            "Fly the most famous Star Wars starfighters in furious battles against Imperial pilots.",
            "director": "",
            "genre": ["Action", "Sci-Fi"],
            "id": "00e2e781-7af9-4f82-b4e9-14a488a3e184",
            "imdb_rating": 8.1,
            "title": "Star Wars: X-Wing",
            "writers": [
                {"id": "567bedb8-982c-444a-af7d-df47cac1906d", "name": "Edward Kilham"},
                {
                    "id": "4d2b6d34-a5d7-46f8-8f42-80f754226c11",
                    "name": "Lawrence Holland",
                },
                {"id": "e03e9083-891b-48c4-b075-4b39c45979ac", "name": "David Wessman"},
            ],
            "writers_names": ["Edward Kilham", "Lawrence Holland", "David Wessman"],
        },
        {
            "actors": [
                {
                    "id": "1fe46055-fceb-4714-90be-5c3a8728d020",
                    "name": "Barbara Church",
                },
                {"id": "89734888-0254-4040-b87c-30e2cb144d0d", "name": "Bernard Baur"},
                {"id": "8aee78d1-87f4-4269-bb10-3d58ab009c2c", "name": "Steven Adler"},
                {"id": "0cce8da2-8839-4a78-a878-45f5252588c9", "name": "Gilby Clarke"},
            ],
            "actors_names": [
                "Barbara Church",
                "Bernard Baur",
                "Steven Adler",
                "Gilby Clarke",
            ],
            "description": "A biography of Axl Rose.",
            "director": "Angela Turner",
            "genre": ["Music", "Documentary", "Biography"],
            "id": "01ab9e34-4ceb-4337-bb69-68a1b0de46b2",
            "imdb_rating": 6.9,
            "title": "Axl Rose: The Prettiest Star",
            "writers": [
                {"id": "37c36461-9a0d-4fd9-b257-fae0b2b6e8ad", "name": "Angela Turner"}
            ],
            "writers_names": ["Angela Turner"],
        },
        {
            "actors": [
                {"id": "b6d704c8-dc2d-41dc-9619-b3e5099a61e6", "name": "Raymond Burr"},
                {
                    "id": "f897aaf2-0e39-462e-9181-79412cfb3b4b",
                    "name": "William R. Moses",
                },
                {"id": "7f6bf45e-c94f-447a-8440-968a50fbd01d", "name": "Barbara Hale"},
                {
                    "id": "64a4a502-2794-4bf0-a370-b73274aa37ad",
                    "name": "Alexandra Paul",
                },
            ],
            "actors_names": [
                "Raymond Burr",
                "William R. Moses",
                "Barbara Hale",
                "Alexandra Paul",
            ],
            "description": "Thatcher Horton is owner of a Denver sports arena and a couple of sports teams. "
            "Bobby Spencer a friend of Ken was one of his hockey players."
            " It seems that Horton verbally promised him that he would take care of him "
            "if he gets injured, which happened. Now it seems that Horton is reneging and he "
            "has asked Ken to represent him in his suit against Horton. Bobby threatened Horton "
            "and not long after that Horton was killed and the murder weapon was found in Bobby's"
            " possession. So Perry comes to help defend Bobby. It seems that Horton was not liked by "
            "other people including his wife and son, and it also seems that the killer was"
            " a professional assassin, so did one of them hire him?",
            "director": "Christian I. Nyby II",
            "genre": ["Crime", "Mystery", "Drama"],
            "id": "01cd80e2-5db8-4914-9a80-74f15a3a1a24",
            "imdb_rating": 6.9,
            "title": "Perry Mason: The Case of the All-Star Assassin",
            "writers": [
                {
                    "id": "ec011e65-36d8-4147-95e9-4c1c1f41afb2",
                    "name": "Robert Hamilton",
                },
                {"id": "7e0a3634-e433-4264-955d-82094e588562", "name": "Joel Steiger"},
                {"id": "5e1cdf38-dbb2-41d8-89e2-a20d0563acc3", "name": "Dean Hargrove"},
                {"id": "37c36461-9a0d-4fd9-b257-fae0b2b6e8ad", "name": "Angela Turner"},
            ],
            "writers_names": [
                "Robert Hamilton",
                "Joel Steiger",
                "Dean Hargrove",
                "Angela Turner",
            ],
        },
        {
            "actors": [
                {"id": "acb691d0-694b-4444-bbe6-6a5ec4dd5763", "name": "Bo Bice"},
                {
                    "id": "cbceaa01-910c-4f0e-b992-7faf7d27131a",
                    "name": "Carrie Underwood",
                },
                {
                    "id": "8b197ae2-38c2-48c7-8cf6-6dc234d16efb",
                    "name": "Americus Abesamis",
                },
                {
                    "id": "57ce8bb4-e1c8-4a5d-bd57-694c6ee7f317",
                    "name": "Christina Applegate",
                },
            ],
            "actors_names": [
                "Bo Bice",
                "Carrie Underwood",
                "Americus Abesamis",
                "Christina Applegate",
            ],
            "description": None,
            "director": "Adam Shankman",
            "genre": ["Music"],
            "id": "01f81c66-d968-4375-bbb0-65103aa214d1",
            "imdb_rating": 8.2,
            "title": "Carrie Underwood: An All-Star Holiday Special",
            "writers": [],
            "writers_names": [],
        },
        {
            "actors": [
                {
                    "id": "8a34f121-7ce6-4021-b467-abec993fc6cd",
                    "name": "Zachary Quinto",
                },
                {"id": "f89a9bad-5bd3-446d-bbdf-e1fd0d217e5d", "name": "John Cho"},
                {"id": "9f38323f-5912-40d2-a90c-b56899746f2a", "name": "Chris Pine"},
                {"id": "2cf03687-ebc3-47dc-a99f-602f6cc55f7a", "name": "Simon Pegg"},
            ],
            "actors_names": ["Zachary Quinto", "John Cho", "Chris Pine", "Simon Pegg"],
            "description": "Kirk and Spock team up against the Gorn.",
            "director": "",
            "genre": ["Adventure", "Action", "Sci-Fi"],
            "id": "020adfa7-7251-4fb9-b6db-07b60664cb67",
            "imdb_rating": 6.9,
            "title": "Star Trek",
            "writers": [
                {
                    "id": "69e600f2-2cc2-4473-be29-3e61ebfd883c",
                    "name": "Marianne Krawczyk",
                },
                {"id": "9b58c99a-e5a3-4f24-8f67-a038665758d6", "name": "Roberto Orci"},
                {"id": "82b7dffe-6254-4598-b6ef-5be747193946", "name": "Alex Kurtzman"},
            ],
            "writers_names": ["Marianne Krawczyk", "Roberto Orci", "Alex Kurtzman"],
        },
        {
            "actors": [
                {"id": "fb6717bf-4be2-4f2f-96d0-e73d995d0ff9", "name": "Stephen Furst"},
                {"id": "57c0c78d-8c7f-45e9-bee0-f5c940b68f86", "name": "Larry Miller"},
                {"id": "60e64205-b2a3-403f-a625-78b77cceb267", "name": "Tim Allen"},
                {
                    "id": "06cf22cd-e7f8-4d1f-9c72-fddc61be084a",
                    "name": "Nicole Sullivan",
                },
            ],
            "actors_names": [
                "Stephen Furst",
                "Larry Miller",
                "Tim Allen",
                "Nicole Sullivan",
            ],
            "description": "After a successful mission in which his partner, Warp Darkmatter, "
            "fell in battle, Buzz Lightyear vows never to put another partner at "
            "risk and works solo. This vow, however is challenged by Star Command who assigns "
            "young Mira Nova to be Warp's replacement over Buzz's objections. In addition, the LGMs "
            "suggest he tries a new robot for an assistant while a lowly janitor, Booster, has his"
            " dreams of joining the Space Rangers. Together, this group of disparate heroes find they"
            " must work together to save the galaxy when Emporer Zurg hatches his "
            "grandest scheme for conquest yet.",
            "director": "George Lucas",
            "genre": ["Adventure", "Sci-Fi", "Animation", "Comedy", "Family", "Action"],
            "id": "0236282f-8ea5-418e-ab9b-13662a4688a9",
            "imdb_rating": 6.2,
            "title": "Buzz Lightyear of Star Command: The Adventure Begins",
            "writers": [
                {
                    "id": "d9aed3ed-3943-4040-bc9d-1e45f6efcec8",
                    "name": "Robert Schooley",
                },
                {"id": "948d3351-ee5c-48c2-9553-3acd196e7e6b", "name": "Bill Motz"},
                {"id": "6e50ec85-bd49-45e6-9f2c-cd22a828c973", "name": "Bob Roth"},
                {"id": "c576f59c-df96-4f8f-901b-44de16ffac6b", "name": "Mark McCorkle"},
            ],
            "writers_names": [
                "Robert Schooley",
                "Bill Motz",
                "Bob Roth",
                "Mark McCorkle",
            ],
        },
        {
            "actors": [
                {"id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1", "name": "Harrison Ford"},
                {"id": "26e83050-29ef-4163-a99d-b546cac208f8", "name": "Mark Hamill"},
                {
                    "id": "efdd1787-8871-4aa9-b1d7-f68e55b913ed",
                    "name": "Billy Dee Williams",
                },
                {"id": "b5d2b63a-ed1f-4e46-8320-cf52a32be358", "name": "Carrie Fisher"},
            ],
            "actors_names": [
                "Harrison Ford",
                "Mark Hamill",
                "Billy Dee Williams",
                "Carrie Fisher",
            ],
            "description": "Luke Skywalker battles horrible Jabba the Hut and cruel"
            " Darth Vader to save his comrades in the Rebel Alliance and triumph over "
            "the Galactic Empire. Han Solo and Princess Leia reaffirm their love and team"
            " with Chewbacca, Lando Calrissian, the Ewoks and the androids C-3PO and R2-D2 "
            "to aid in the disruption of the Dark Side and the defeat of the evil emperor.",
            "director": "George Lucas",
            "genre": ["Adventure", "Sci-Fi", "Fantasy", "Action"],
            "id": "025c58cd-1b7e-43be-9ffb-8571a613579b",
            "imdb_rating": 8.3,
            "title": "Star Wars: Episode VI - Return of the Jedi",
            "writers": [
                {"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "George Lucas"},
                {
                    "id": "3217bc91-bcfc-44eb-a609-82d228115c50",
                    "name": "Lawrence Kasdan",
                },
            ],
            "writers_names": ["George Lucas", "Lawrence Kasdan"],
        },
        {
            "actors": [
                {"id": "079a361b-2574-4fc9-98e9-4107dc5b6a71", "name": "Yancy Butler"},
                {
                    "id": "3bb17a72-15b9-495d-afc9-b36512d99c48",
                    "name": "Johnny Rey Diaz",
                },
                {"id": "ef7c2589-fdd5-4410-a14e-b354989fa674", "name": "Rance Howard"},
                {"id": "8e6051e5-8478-4090-8081-84fe3759fd23", "name": "Terence Knox"},
            ],
            "actors_names": [
                "Yancy Butler",
                "Johnny Rey Diaz",
                "Rance Howard",
                "Terence Knox",
            ],
            "description": "Three Magi Priests journey the unforgiving desert in search of the new born King.",
            "director": "Bret Miller",
            "genre": ["Adventure"],
            "id": "027ba6c5-d805-402a-addf-484b34292625",
            "imdb_rating": 3.1,
            "title": "Chasing the Star",
            "writers": [
                {"id": "606c74bd-ab92-4748-a5da-759f9cba91f8", "name": "DJ Perry"}
            ],
            "writers_names": ["DJ Perry"],
        },
        {
            "actors": [
                {"id": "c03ee7bb-6617-4a98-8cbd-3875e402015e", "name": "Richard Boone"},
                {
                    "id": "a74b53ea-2e9b-4de4-b37f-15cef4ec8ba3",
                    "name": "Mamie Van Doren",
                },
                {"id": "a8f78bbb-66b8-4508-8d86-e2e309ac8346", "name": "Coleen Gray"},
                {"id": "771f8445-19ea-4947-8153-3b038674508a", "name": "John Agar"},
            ],
            "actors_names": [
                "Richard Boone",
                "Mamie Van Doren",
                "Coleen Gray",
                "John Agar",
            ],
            "description": "The sheriff of Gunlock is planning to hang Sam Hall,"
            " who shot three farmers found on cattle land, at sundown."
            " At the casino, betting is 8 to 3 he won't make it. The cattlemen are"
            " set to rescue Sam; the farmers hope to lynch him before he can be rescued;"
            " and Hall schemes for escape with his girl Nellie. But Sheriff Jorden is most "
            "concerned with finding out who hired Hall: a leading suspect is the sheriff's "
            "future brother-in-law.",
            "director": "Charles F. Haas",
            "genre": ["Romance", "Drama", "Western"],
            "id": "02c24a84-1667-4f98-b459-f08933befa3d",
            "imdb_rating": 6.1,
            "title": "Star in the Dust",
            "writers": [
                {"id": "3ce3f12a-d6b4-450a-9d03-940b63b8e587", "name": "Lee Leighton"},
                {"id": "f4db9cfb-8af0-4c13-bc45-4f8a87f9811a", "name": "Oscar Brodney"},
            ],
            "writers_names": ["Lee Leighton", "Oscar Brodney"],
        },
    ]
    persons = [
        {"full_name": "Fred Olen Ray", "id": "a2fd6df4-9f3c-4a26-8d59-914470d2aea0"},
        {"full_name": "Suzy Stokey", "id": "a91ff1c9-98a3-46af-a0d0-e9f2a2b4f51e"},
        {
            "full_name": "Miriam L. Preissel",
            "id": "82416ac7-26fa-40a6-a433-1c756c0fad6e",
        },
        {"full_name": "Marya Gant", "id": "040147e3-0965-4117-8112-55a2087e0b84"},
        {"full_name": "Sandy Brooke", "id": "b258f144-d771-4fa2-b6a2-42805c13ce4a"},
        {"full_name": "Ross Hagen", "id": "f51f4731-3c26-4a72-9d68-cd0cd3d90a26"},
        {"full_name": "Michael Sonye", "id": "dac61d8f-f36e-4351-a4d8-9048b87d00a6"},
        {"full_name": "Nick Jameson", "id": "087de4c7-8d61-4337-beae-d5ce3c440b00"},
        {"full_name": "Erik Bauersfeld", "id": "bdd44e92-7498-445b-998e-0c2bd9591052"},
        {"full_name": "Edward Kilham", "id": "567bedb8-982c-444a-af7d-df47cac1906d"},
    ]

    client = Elasticsearch("http://elasticsearch:9200")
    genres_for_bulk = [
        {
            "_index": "genres",
            "_id": genre["id"],
            "_type": "_doc",
            "genre": genre["genre"],
            "id": genre["id"],
        }
        for genre in genres
    ]
    helpers.bulk(client, genres_for_bulk)

    movies_for_bulk = [
        {
            "_index": "movies",
            "_id": film["id"],
            "_type": "_doc",
            "actors": film["actors"],
            "actors_names": film["actors_names"],
            "description": film["description"],
            "director": film["director"],
            "genre": film["genre"],
            "id": film["id"],
            "imdb_rating": film["imdb_rating"],
            "title": film["title"],
            "writers": film["writers"],
            "writers_names": film["writers_names"],
        }
        for film in films
    ]

    helpers.bulk(client, movies_for_bulk)

    persons_for_bulk = [
        {
            "_index": "persons",
            "_id": person["id"],
            "_type": "_doc",
            "full_name": person["full_name"],
            "id": person["id"],
        }
        for person in persons
    ]

    helpers.bulk(client, persons_for_bulk)
    time.sleep(1)
    client.close()
