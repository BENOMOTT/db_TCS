import random
from flask import Flask, jsonify, render_template, request
import datetime
from flask_cors import CORS
from transbank.webpay.webpay_plus.transaction import Transaction

# Importar transbank solo si es necesario
# from transbank.error.transbank_error import TransbankError
# from transbank.webpay.webpay_plus.transaction import Transaction

api = Flask(__name__)
CORS(api)

def get_current_datetime():
    return datetime.datetime.utcnow().isoformat()

# Base de datos simulada de productos (lista de diccionarios)
products = [

{
        "id": 1,
        "Código del producto": "PS4",
        "Categoria": "Acción/Aventura",
        "Marca": "Sony",
        "Código": "PS-67891",
        "Nombre": "The Last of Us Part II",
        "Fecha": "2020-06-19",
        "Precio": 89090.99,
        "Imagen": "https://juegosdigitaleschile.com/files/images/productos/1594745236-the-last-of-us-part-ii-ps4.jpg"
    },
    {
        "id": 2,
        "Código del producto": "PC",
        "Categoria": "Realidad Virtual",
        "Marca": "Valve",
        "Código": "STEAM-12345",
        "Nombre": "Half-Life Alyx",
        "Fecha": "2020-03-23",
        "Precio": 49990.50,
        "Imagen": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/546560/capsule_616x353.jpg?t=1673391297"
    },
    {
        "id": 3,
        "Código del producto": "XBOX",
        "Categoria": "Shooter",
        "Marca": "Microsoft",
        "Código": "XBOX-34567",
        "Nombre": "Halo Infinite",
        "Fecha": "2021-12-08",
        "Precio": 79990.99,
        "Imagen": "https://juegosdigitaleschile.com/files/images/productos/1644611182-halo-infinite-xbox-serie-xs.jpg"
    },
    {
        "id": 4,
        "Código del producto": "PC",
        "Categoria": "RPG",
        "Marca": "CD Projekt",
        "Código": "CP-67890",
        "Nombre": "Cyberpunk 2077",
        "Fecha": "2020-12-10",
        "Precio": 74990.75,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRM2r9dAZKHVDUhjQ411KdQdmlv9B1RQtzZ6g&s"
    },
    {
        "id": 5,
        "Código del producto": "NSW",
        "Categoria": "Aventura",
        "Marca": "Nintendo",
        "Código": "NSW-12345",
        "Nombre": "The Legend of Zelda: Breath of the Wild",
        "Fecha": "2017-03-03",
        "Precio": 62990.80,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLr0O8V0NUMBMwIHVt9-6rB9FnoXzgKJOCOA&s"
    },
    {
        "id": 6,
        "Código del producto": "PS5",
        "Categoria": "Acción/Aventura",
        "Marca": "Sony",
        "Código": "PS5-45678",
        "Nombre": "Spider-Man: Miles Morales",
        "Fecha": "2020-11-12",
        "Precio": 39990.00,
        "Imagen": "https://juegosdigitaleschile.com/files/images/productos/1606596198-marvels-spider-man-miles-morales-ps5.jpg"
    },
    {
        "id": 7,
        "Código del producto": "PC",
        "Categoria": "RPG",
        "Marca": "Bethesda",
        "Código": "BS-98764",
        "Nombre": "Skyrim Special Edition",
        "Fecha": "2016-10-28",
        "Precio": 29990.99,
        "Imagen": "https://store-images.s-microsoft.com/image/apps.25872.14594732668559524.b556ac33-8bda-4b99-96c5-074063c78980.1ac836c3-296e-4006-bffc-057f731bfd02?q=90&w=177&h=177"
    },
    {
        "id": 8,
        "Código del producto": "NSW",
        "Categoria": "Plataformas",
        "Marca": "Nintendo",
        "Código": "NSW-45678",
        "Nombre": "Super Mario Odyssey",
        "Fecha": "2017-10-27",
        "Precio": 54990.00,
        "Imagen": "https://sm.ign.com/ign_es/game/s/super-mari/super-mario-odyssey_d3t1.jpg"
    },
    {
        "id": 9,
        "Código del producto": "PC",
        "Categoria": "Acción/Aventura",
        "Marca": "Rockstar",
        "Código": "RS-24680",
        "Nombre": "Grand Theft Auto V",
        "Fecha": "2013-09-17",
        "Precio": 69990.00,
        "Imagen": "https://www.gta-growth.com/secciones/gtav/descargas/avatares/gtav_logo_256.jpg"
    },
    {
        "id": 10,
        "Código del producto": "PS4",
        "Categoria": "Acción/Aventura",
        "Marca": "Sony",
        "Código": "PS4-78901",
        "Nombre": "God of War",
        "Fecha": "2018-04-20",
        "Precio": 89990.00,
        "Imagen": "https://juegosdigitaleschile.com/files/images/productos/1570562820-god-of-war-ps4.png"
    },
    {
        "id": 11,
        "Código del producto": "PC",
        "Categoria": "Simulación",
        "Marca": "Electronic Arts",
        "Código": "EA-11223",
        "Nombre": "The Sims 4",
        "Fecha": "2014-09-02",
        "Precio": 39990.99,
        "Imagen": "https://cdn1.epicgames.com/offer/2a14cf8a83b149919a2399504e5686a6/EGS_TheSims4DigitalDeluxeUpgrade_Maxis_DLC_S2_1200x1600-b69f09362d348b4e3df86431cd156c4d"
    },
    {
        "id": 12,
        "Código del producto": "XBOX",
        "Categoria": "Aventura",
        "Marca": "Microsoft",
        "Código": "XBOX-54321",
        "Nombre": "Forza Horizon 4",
        "Fecha": "2018-10-02",
        "Precio": 69990.50,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpAudpr6g8b7U24Q8Ed14goSd2ujRxdMQ0oQ&s"
    },
    {
        "id": 13,
        "Código del producto": "NSW",
        "Categoria": "Acción",
        "Marca": "Nintendo",
        "Código": "NSW-78901",
        "Nombre": "Splatoon 2",
        "Fecha": "2017-07-21",
        "Precio": 45990.00,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZnbMSnDp-2QCfBP7jKAHeg0XEi5iubD-x0Q&s"
    },
    {
        "id": 14,
        "Código del producto": "PS5",
        "Categoria": "RPG",
        "Marca": "Sony",
        "Código": "PS5-11223",
        "Nombre": "Demon's Souls",
        "Fecha": "2020-11-12",
        "Precio": 69990.00,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRF-0jf8NnjihRpQ6kZ3m3KnaoHk2Tu-QAUrA&s"
    },
    {
        "id": 15,
        "Código del producto": "PC",
        "Categoria": "Acción/Aventura",
        "Marca": "Ubisoft",
        "Código": "UBI-12345",
        "Nombre": "Assassin's Creed Valhalla",
        "Fecha": "2020-11-10",
        "Precio": 79990.00,
        "Imagen": "https://http2.mlstatic.com/D_NQ_NP_764286-MLA46477664878_062021-O.webp"
    },
    {
        "id": 16,
        "Código del producto": "NSW",
        "Categoria": "RPG",
        "Marca": "Nintendo",
        "Código": "NSW-67890",
        "Nombre": "Fire Emblem: Three Houses",
        "Fecha": "2019-07-26",
        "Precio": 59990.00,
        "Imagen": "https://m.media-amazon.com/images/I/817KFp1wiOL.jpg"
    },
    {
        "id": 17,
        "Código del producto": "PS4",
        "Categoria": "RPG",
        "Marca": "Square Enix",
        "Código": "SQEX-12345",
        "Nombre": "Final Fantasy VII Remake",
        "Fecha": "2020-04-10",
        "Precio": 64990.99,
        "Imagen": "https://juegosdigitaleschile.com/files/images/productos/1624296462-final-fantasy-vii-remake-ps4-flash-sale.jpg"
    },
    {
        "id": 18,
        "Código del producto": "PC",
        "Categoria": "Estrategia",
        "Marca": "Paradox Interactive",
        "Código": "PI-98765",
        "Nombre": "Stellaris",
        "Fecha": "2016-05-09",
        "Precio": 49990.00,
        "Imagen": "data:image/jpeg;base64,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"
    },
    {
        "id": 19,
        "Código del producto": "XBOX",
        "Categoria": "Deportes",
        "Marca": "EA Sports",
        "Código": "EA-11223",
        "Nombre": "FIFA 22",
        "Fecha": "2021-10-01",
        "Precio": 79990.00,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQAf5czrb9AJIkmgXEhLOteQMas_0KJ4YWvcg&s"
    },
    {
        "id": 21,
        "Código del producto": "PS5",
        "Categoria": "Acción/Aventura",
        "Marca": "Sony",
        "Código": "PS5-22334",
        "Nombre": "Ratchet & Clank: Rift Apart",
        "Fecha": "2021-06-11",
        "Precio": 79990.00,
        "Imagen": "https://clsonyb2c.vtexassets.com/arquivos/ids/457225/PS5-Ratchet-Clank_RA-Cover1.jpg?v=637587311896230000"
    },
    {
        "id": 22,
        "Código del producto": "XBOX",
        "Categoria": "Deportes",
        "Marca": "EA Sports",
        "Código": "XBOX-22334",
        "Nombre": "NBA 2K21",
        "Fecha": "2021-09-10",
        "Precio": 69990.00,
        "Imagen": "https://http2.mlstatic.com/D_NQ_NP_666522-MLA45731814802_042021-O.webp"
    },
    {
        "id": 21,
        "Código del producto": "PS4",
        "Categoria": "Acción/Aventura",
        "Marca": "Sony",
        "Código": "PS4-23456",
        "Nombre": "Uncharted 4: A Thief's End",
        "Fecha": "2016-05-10",
        "Precio": 79990.00,
        "Imagen": "https://jdigitales.cl/cdn/shop/products/Uncharted_4.jpg?v=1555461221"
    },
    {
        "id": 22,
        "Código del producto": "XBOX",
        "Categoria": "Acción/Aventura",
        "Marca": "Microsoft",
        "Código": "XBOX-67892",
        "Nombre": "Gears 5",
        "Fecha": "2019-09-10",
        "Precio": 49990.00,
        "Imagen": "https://http2.mlstatic.com/D_NQ_NP_664480-MLA47092942677_082021-O.webp"
    },
    {
        "id": 23,
        "Código del producto": "NSW",
        "Categoria": "Acción/Aventura",
        "Marca": "Nintendo",
        "Código": "NSW-23456",
        "Nombre": "Fire Emblem: Three Houses",
        "Fecha": "2019-07-26",
        "Precio": 59990.00,
        "Imagen": "https://m.media-amazon.com/images/I/817KFp1wiOL.jpg"
    },
    {
        "id": 24,
        "Código del producto": "PC",
        "Categoria": "Acción/Aventura",
        "Marca": "Bethesda",
        "Código": "BS-45678",
        "Nombre": "DOOM Eternal",
        "Fecha": "2020-03-20",
        "Precio": 79990.00,
        "Imagen": "https://cdn1.epicgames.com/offer/b5ac16dc12f3478e99dcfea07c13865c/EGS_DOOMEternal_idSoftware_S2_1200x1600-9a018727ccc708b2d98f2a8746c2d377"
    },
    {
        "id": 25,
        "Código del producto": "PS4",
        "Categoria": "Acción/Aventura",
        "Marca": "Sony",
        "Código": "PS4-34567",
        "Nombre": "Horizon Zero Dawn",
        "Fecha": "2017-02-28",
        "Precio": 54990.00,
        "Imagen": "data:image/jpeg;base64,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"
    },
    {
        "id": 26,
        "Código del producto": "XBOX",
        "Categoria": "Acción",
        "Marca": "Microsoft",
        "Código": "XBOX-45678",
        "Nombre": "Sea of Thieves",
        "Fecha": "2018-03-20",
        "Precio": 39990.00,
        "Imagen": "https://m.media-amazon.com/images/I/61rlurCGiJL._AC_UF894,1000_QL80_.jpg"
    },
    {
        "id": 27,
        "Código del producto": "PS5",
        "Categoria": "RPG",
        "Marca": "Sony",
        "Código": "PS5-23456",
        "Nombre": "Demon's Souls",
        "Fecha": "2020-11-12",
        "Precio": 69990.00,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRF-0jf8NnjihRpQ6kZ3m3KnaoHk2Tu-QAUrA&s"
    },
    {
        "id": 28,
        "Código del producto": "NSW",
        "Categoria": "Acción/Aventura",
        "Marca": "Nintendo",
        "Código": "NSW-34567",
        "Nombre": "Super Mario 3D World + Bowser's Fury",
        "Fecha": "2021-02-12",
        "Precio": 62990.00,
        "Imagen": "https://i5.walmartimages.com/seo/Super-Mario-3D-World-Bowser-s-Fury-Nintendo-Switch-Physical_cfe423d6-6b5b-4313-b0c5-5ebe536bf56a.44dd8185c895d0ef3a52d5238cada3cf.jpeg"
    },
    {
        "id": 29,
        "Código del producto": "PS4",
        "Categoria": "Aventura",
        "Marca": "Sony",
        "Código": "PS4-45679",
        "Nombre": "The Last of Us Part II",
        "Fecha": "2020-06-19",
        "Precio": 89090.99,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoabHZVFjD0dLY3MZzBT0PJuJz1KDFNh9h-Q&s"
    },
    {
        "id": 30,
        "Código del producto": "XBOX",
        "Categoria": "Aventura",
        "Marca": "Microsoft",
        "Código": "XBOX-67893",
        "Nombre": "Ori and the Will of the Wisps",
        "Fecha": "2020-03-11",
        "Precio": 59990.00,
        "Imagen": "https://store-images.s-microsoft.com/image/apps.25149.14047496556148589.9fda5cef-7995-4dbb-a626-66d2ab3feb4f.0c29cd80-70d5-4bab-bed6-664f385cb0ef"
    },
    {
        "id": 31,
        "Código del producto": "NSW",
        "Categoria": "Acción/Aventura",
        "Marca": "Nintendo",
        "Código": "NSW-56789",
        "Nombre": "Animal Crossing: New Horizons",
        "Fecha": "2020-03-20",
        "Precio": 49990.00,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGmvJm7G_5cZwgSVhL4nC150ojbh2pwvp75A&s"
    },
    {
        "id": 32,
        "Código del producto": "PS4",
        "Categoria": "Aventura",
        "Marca": "Sony",
        "Código": "PS4-56789",
        "Nombre": "God of War",
        "Fecha": "2018-04-20",
        "Precio": 89990.00,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8BP_iuz31x-pg9Kltt1jGosfV6TZ5qdF7cg&s"
    },
    {
        "id": 33,
        "Código del producto": "XBOX",
        "Categoria": "RPG",
        "Marca": "Microsoft",
        "Código": "XBOX-78901",
        "Nombre": "The Elder Scrolls V: Skyrim Special Edition",
        "Fecha": "2016-10-28",
        "Precio": 29990.99,
        "Imagen": "https://m.media-amazon.com/images/I/71p2QFdJujL.jpg"
    },
    {
        "id": 34,
        "Código del producto": "PC",
        "Categoria": "Shooter",
        "Marca": "Activision",
        "Código": "ACT-12345",
        "Nombre": "Call of Duty: Warzone",
        "Fecha": "2020-03-10",
        "Precio": 49990.00,
        "Imagen": "https://www.nvidia.com/content/dam/en-zz/Solutions/geforce/news/call-of-duty-warzone-out-now-pc-system-requirements/geforce-grd-magma-grd-article-thumb-1200x630.jpg"
    },
    {
        "id": 35,
        "Código del producto": "PS5",
        "Categoria": "Acción",
        "Marca": "Sony",
        "Código": "PS5-34567",
        "Nombre": "Ratchet & Clank: Rift Apart",
        "Fecha": "2021-06-11",
        "Precio": 79990.00,
        "Imagen": "https://clsonyb2c.vtexassets.com/arquivos/ids/457225-800-800?v=637587311896230000&width=800&height=800&aspect=true"
    },
    {
        "id": 36,
        "Código del producto": "PC",
        "Categoria": "Acción/Aventura",
        "Marca": "Square Enix",
        "Código": "SQEX-56789",
        "Nombre": "Tomb Raider: Definitive Edition",
        "Fecha": "2014-01-28",
        "Precio": 39990.00,
        "Imagen": "https://jdigitales.cl/cdn/shop/products/jT7kkwSWEinafnaYWMZoReRr4LlmYmym.webp?v=1651678795"
    },
    {
        "id": 37,
        "Código del producto": "XBOX",
        "Categoria": "Shooter",
        "Marca": "Microsoft",
        "Código": "XBOX-12345",
        "Nombre": "Destiny 2",
        "Fecha": "2017-09-06",
        "Precio": 39990.00,
        "Imagen": "https://m.media-amazon.com/images/I/81p-wa-ebWL.jpg"
    },
    {
        "id": 38,
        "Código del producto": "NSW",
        "Categoria": "Acción",
        "Marca": "Nintendo",
        "Código": "NSW-12345",
        "Nombre": "Splatoon 2",
        "Fecha": "2017-07-21",
        "Precio": 45990.00,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZnbMSnDp-2QCfBP7jKAHeg0XEi5iubD-x0Q&s"
    },
    {
        "id": 39,
        "Código del producto": "PS5",
        "Categoria": "Acción/Aventura",
        "Marca": "Sony",
        "Código": "PS5-45678",
        "Nombre": "Spider-Man: Miles Morales",
        "Fecha": "2020-11-12",
        "Precio": 69990.00,
        "Imagen": "https://juegosdigitaleschile.com/files/images/productos/1606596198-marvels-spider-man-miles-morales-ps5.jpg"
    },
    {
        "id": 40,
        "Código del producto": "XBOX",
        "Categoria": "RPG",
        "Marca": "Microsoft",
        "Código": "XBOX-78902",
        "Nombre": "The Witcher 3: Wild Hunt",
        "Fecha": "2015-05-19",
        "Precio": 79990.00,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrbEWZPUNZfNl3tFQ2hOgTh57rQdZYwhYokw&s"
    },
    {
        "id": 41,
        "Código del producto": "NSW",
        "Categoria": "Acción/Aventura",
        "Marca": "Nintendo",
        "Código": "NSW-67890",
        "Nombre": "The Legend of Zelda: Breath of the Wild",
        "Fecha": "2017-03-03",
        "Precio": 59990.00,
        "Imagen": "https://imagedelivery.net/4fYuQyy-r8_rpBpcY7lH_A/falabellaCL/5587019_1/w=1004,h=1500,fit=cover"
    },
    {
        "id": 42,
        "Código del producto": "PS4",
        "Categoria": "RPG",
        "Marca": "Sony",
        "Código": "PS4-67891",
        "Nombre": "Persona 5",
        "Fecha": "2016-09-15",
        "Precio": 64990.00,
        "Imagen": "https://www.todojuegos.cl/Productos/_mediaProd/15756/persona5ph.JPG"
    },
    {
        "id": 43,
        "Código del producto": "XBOX",
        "Categoria": "Acción",
        "Marca": "Microsoft",
        "Código": "XBOX-12346",
        "Nombre": "Halo: The Master Chief Collection",
        "Fecha": "2014-11-11",
        "Precio": 49990.00,
        "Imagen": "https://http2.mlstatic.com/D_NQ_NP_625180-MLU79152727077_092024-O.webp"
    },
    {
        "id": 44,
        "Código del producto": "PS4",
        "Categoria": "Aventura",
        "Marca": "Sony",
        "Código": "PS4-78901",
        "Nombre": "The Last of Us Remastered",
        "Fecha": "2014-07-29",
        "Precio": 44990.00,
        "Imagen": "https://jdigitales.cl/cdn/shop/products/The-last-of-us-PS4.jpg?v=1598978934"
    },
    {
        "id": 45,
        "Código del producto": "PC",
        "Categoria": "Acción/Aventura",
        "Marca": "Rockstar Games",
        "Código": "ROCK-23456",
        "Nombre": "Red Dead Redemption 2",
        "Fecha": "2018-10-26",
        "Precio": 79990.00,
        "Imagen": "https://image.api.playstation.com/cdn/UP1004/CUSA03041_00/Hpl5MtwQgOVF9vJqlfui6SDB5Jl4oBSq.png"
    },
    {
        "id": 46,
        "Código del producto": "XBOX",
        "Categoria": "Acción",
        "Marca": "Microsoft",
        "Código": "XBOX-23457",
        "Nombre": "Forza Horizon 4",
        "Fecha": "2018-09-28",
        "Precio": 49990.00,
        "Imagen": "https://cjmdigitales.cl/wp-content/uploads/2023/07/1194-1.webp"
    },
    {
        "id": 47,
        "Código del producto": "NSW",
        "Categoria": "Acción/Aventura",
        "Marca": "Nintendo",
        "Código": "NSW-23456",
        "Nombre": "Super Mario Odyssey",
        "Fecha": "2017-10-27",
        "Precio": 54990.00,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9PUwn8ojm-vWRS2YXhu7YbAqaGiTgNGlvRg&s"
    },
    {
        "id": 48,
        "Código del producto": "PS4",
        "Categoria": "Aventura",
        "Marca": "Sony",
        "Código": "PS4-67892",
        "Nombre": "Uncharted: The Nathan Drake Collection",
        "Fecha": "2015-10-09",
        "Precio": 49990.00,
        "Imagen": "https://imagedelivery.net/4fYuQyy-r8_rpBpcY7lH_A/falabellaCL/110418404_01/w=1500,h=1500,fit=pad"
    },
    {
        "id": 49,
        "Código del producto": "XBOX",
        "Categoria": "Acción/Aventura",
        "Marca": "Microsoft",
        "Código": "XBOX-34567",
        "Nombre": "Sunset Overdrive",
        "Fecha": "2014-10-28",
        "Precio": 39990.00,
        "Imagen": "https://http2.mlstatic.com/D_NQ_NP_736309-MLU73786509960_012024-O.webp"
    },
    {
        "id": 50,
        "Código del producto": "NSW",
        "Categoria": "RPG",
        "Marca": "Nintendo",
        "Código": "NSW-78901",
        "Nombre": "Xenoblade Chronicles 2",
        "Fecha": "2017-12-01",
        "Precio": 64990.00,
        "Imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvBL1qloZ2d4i6gVtQL0QzfqAESAQLRjw5qQ&s"
    }
]


# Base de datos simulada de perfiles (lista de diccionarios)
profiles = [
    {
        "ID": 1,
        "NOMBRE": "Usuario de Prueba",
        "RUT": "12345678-9",
        "CORREO": "prueba@ejemplo.com",
        "CONTRASEÑA": "1234",
        "TIPO_PERFIL": 1,
        "DIRECCIÓN": "Calle Falsa 123",
        "REGIÓN": "Región Metropolitana",
        "COMUNA": "Santiago"
    },
    {
        "ID": 2,
        "NOMBRE": "Ana Perez",
        "RUT": "23456789-0",
        "CORREO": "ana.perez@ejemplo.com",
        "CONTRASEÑA": "abcd1234",
        "TIPO_PERFIL": 2,
        "DIRECCIÓN": "Avenida Siempre Viva 456",
        "REGIÓN": "Región de Valparaíso",
        "COMUNA": "Valparaíso"
    },
    {
        "ID": 3,
        "NOMBRE": "Carlos Lopez",
        "RUT": "34567890-1",
        "CORREO": "carlos.lopez@ejemplo.com",
        "CONTRASEÑA": "efgh5678",
        "TIPO_PERFIL": 3,
        "DIRECCIÓN": "Calle Principal 789",
        "REGIÓN": "Región del Biobío",
        "COMUNA": "Concepción"
    },
    {
        "ID": 4,
        "NOMBRE": "Maria Gonzalez",
        "RUT": "45678901-2",
        "CORREO": "maria.gonzalez@ejemplo.com",
        "CONTRASEÑA": "ijkl9101",
        "TIPO_PERFIL": 4,
        "DIRECCIÓN": "Pasaje Central 1011",
        "REGIÓN": "Región de la Araucanía",
        "COMUNA": "Temuco"
    },
    {
        "ID": 5,
        "NOMBRE": "Jorge Martinez",
        "RUT": "56789012-3",
        "CORREO": "jorge.martinez@ejemplo.com",
        "CONTRASEÑA": "mnop1213",
        "TIPO_PERFIL": 5,
        "DIRECCIÓN": "Camino Real 1213",
        "REGIÓN": "Región de Los Lagos",
        "COMUNA": "Puerto Montt"
    }
]

# Base de datos simulada de pedidos (lista de diccionarios)
orders = [
    {
        "comuna": "Santiago",
        "correo": "juan.perez@example.com",
        "direccion": "Calle Falsa 123",
        "estado_envio": 1,
        "fecha_compra": "2024-07-09T02:30:07.619382",
        "nombre": "Juan Pérez",
        "order_id": 1,
        "productos": [
            {
                "cantidad": 1,
                "id": 1,
                "nombre": "Taladro Percutor Bosch",
                "precio": 89090.99,
                "total": 89090.99
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 1
    },
    {
        "comuna": "Providencia",
        "correo": "maria.lopez@example.com",
        "direccion": "Avenida Siempre Viva 742",
        "estado_envio": 2,
        "fecha_compra": "2024-07-09T02:30:09.652643",
        "nombre": "María López",
        "order_id": 2,
        "productos": [
            {
                "cantidad": 2,
                "id": 2,
                "nombre": "Martillo",
                "precio": 5000.0,
                "total": 10000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 1
    },
    {
        "comuna": "Las Condes",
        "correo": "carlos.gomez@example.com",
        "direccion": "Pasaje Los Olivos 456",
        "estado_envio": 1,
        "fecha_compra": "2024-07-09T02:30:11.694563",
        "nombre": "Carlos Gómez",
        "order_id": 3,
        "productos": [
            {
                "cantidad": 1,
                "id": 3,
                "nombre": "Sierra Circular",
                "precio": 120000.0,
                "total": 120000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 2
    },
    {
        "comuna": "Ñuñoa",
        "correo": "ana.torres@example.com",
        "direccion": "Camino Real 789",
        "estado_envio": 3,
        "fecha_compra": "2024-07-09T02:30:13.734756",
        "nombre": "Ana Torres",
        "order_id": 4,
        "productos": [
            {
                "cantidad": 3,
                "id": 4,
                "nombre": "Destornillador",
                "precio": 3000.0,
                "total": 9000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 3
    },
    {
        "comuna": "La Florida",
        "correo": "luis.martinez@example.com",
        "direccion": "Plaza Mayor 101",
        "estado_envio": 2,
        "fecha_compra": "2024-07-09T02:30:15.789561",
        "nombre": "Luis Martínez",
        "order_id": 5,
        "productos": [
            {
                "cantidad": 1,
                "id": 5,
                "nombre": "Llave Inglesa",
                "precio": 15000.0,
                "total": 15000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 1
    },
    {
        "comuna": "Santiago",
        "correo": "juan.perez@example.com",
        "direccion": "Calle Falsa 123",
        "estado_envio": 1,
        "fecha_compra": "2024-07-09T02:40:08.219602",
        "nombre": "Juan Pérez",
        "order_id": 1,
        "productos": [
            {
                "cantidad": 1,
                "id": 1,
                "nombre": "Taladro Percutor Bosch",
                "precio": 89090.99,
                "total": 89090.99
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 1
    },
    {
        "comuna": "Providencia",
        "correo": "maria.lopez@example.com",
        "direccion": "Avenida Siempre Viva 742",
        "estado_envio": 2,
        "fecha_compra": "2024-07-09T02:40:10.225306",
        "nombre": "María López",
        "order_id": 2,
        "productos": [
            {
                "cantidad": 2,
                "id": 2,
                "nombre": "Martillo",
                "precio": 5000.0,
                "total": 10000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 1
    },
    {
        "comuna": "Las Condes",
        "correo": "carlos.gomez@example.com",
        "direccion": "Pasaje Los Olivos 456",
        "estado_envio": 1,
        "fecha_compra": "2024-07-09T02:40:12.233872",
        "nombre": "Carlos Gómez",
        "order_id": 3,
        "productos": [
            {
                "cantidad": 1,
                "id": 3,
                "nombre": "Sierra Circular",
                "precio": 120000.0,
                "total": 120000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 2
    },
    {
        "comuna": "Ñuñoa",
        "correo": "ana.torres@example.com",
        "direccion": "Camino Real 789",
        "estado_envio": 3,
        "fecha_compra": "2024-07-09T02:40:14.240037",
        "nombre": "Ana Torres",
        "order_id": 4,
        "productos": [
            {
                "cantidad": 3,
                "id": 4,
                "nombre": "Destornillador",
                "precio": 3000.0,
                "total": 9000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 3
    },
    {
        "comuna": "La Florida",
        "correo": "luis.martinez@example.com",
        "direccion": "Plaza Mayor 101",
        "estado_envio": 2,
        "fecha_compra": "2024-07-09T02:40:16.257374",
        "nombre": "Luis Martínez",
        "order_id": 5,
        "productos": [
            {
                "cantidad": 1,
                "id": 5,
                "nombre": "Llave Inglesa",
                "precio": 15000.0,
                "total": 15000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 1
    },
    {
        "comuna": "Providencia",
        "correo": "pedro.rodriguez@example.com",
        "direccion": "Avenida Libertador 567",
        "estado_envio": 1,
        "fecha_compra": "2024-07-09T02:40:18.302368",
        "nombre": "Pedro Rodríguez",
        "order_id": 6,
        "productos": [
            {
                "cantidad": 1,
                "id": 1,
                "nombre": "Taladro Percutor Bosch",
                "precio": 89090.99,
                "total": 89090.99
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 1
    },
    {
        "comuna": "Las Condes",
        "correo": "marcela.sanchez@example.com",
        "direccion": "Calle Principal 321",
        "estado_envio": 2,
        "fecha_compra": "2024-07-09T02:40:20.350972",
        "nombre": "Marcela Sánchez",
        "order_id": 7,
        "productos": [
            {
                "cantidad": 2,
                "id": 2,
                "nombre": "Martillo",
                "precio": 5000.0,
                "total": 10000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 1
    },
    {
        "comuna": "Ñuñoa",
        "correo": "javier.gonzalez@example.com",
        "direccion": "Pasaje Los Aromos 789",
        "estado_envio": 1,
        "fecha_compra": "2024-07-09T02:40:22.396759",
        "nombre": "Javier González",
        "order_id": 8,
        "productos": [
            {
                "cantidad": 1,
                "id": 3,
                "nombre": "Sierra Circular",
                "precio": 120000.0,
                "total": 120000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 2
    },
    {
        "comuna": "La Florida",
        "correo": "camila.munoz@example.com",
        "direccion": "Calle Nueva 456",
        "estado_envio": 3,
        "fecha_compra": "2024-07-09T02:40:24.454935",
        "nombre": "Camila Muñoz",
        "order_id": 9,
        "productos": [
            {
                "cantidad": 3,
                "id": 4,
                "nombre": "Destornillador",
                "precio": 3000.0,
                "total": 9000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 3
    },
    {
        "comuna": "Santiago",
        "correo": "felipe.lopez@example.com",
        "direccion": "Avenida Circular 678",
        "estado_envio": 2,
        "fecha_compra": "2024-07-09T02:40:26.502417",
        "nombre": "Felipe López",
        "order_id": 10,
        "productos": [
            {
                "cantidad": 1,
                "id": 5,
                "nombre": "Llave Inglesa",
                "precio": 15000.0,
                "total": 15000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 1
    },
    {
        "comuna": "Providencia",
        "correo": "valentina.herrera@example.com",
        "direccion": "Calle Mayor 789",
        "estado_envio": 1,
        "fecha_compra": "2024-07-09T02:40:28.547011",
        "nombre": "Valentina Herrera",
        "order_id": 11,
        "productos": [
            {
                "cantidad": 1,
                "id": 1,
                "nombre": "Taladro Percutor Bosch",
                "precio": 89090.99,
                "total": 89090.99
            },
            {
                "cantidad": 2,
                "id": 2,
                "nombre": "Martillo",
                "precio": 5000.0,
                "total": 10000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 2
    },
    {
        "comuna": "Las Condes",
        "correo": "andres.castro@example.com",
        "direccion": "Pasaje de las Flores 101",
        "estado_envio": 2,
        "fecha_compra": "2024-07-09T02:40:30.579185",
        "nombre": "Andrés Castro",
        "order_id": 12,
        "productos": [
            {
                "cantidad": 1,
                "id": 3,
                "nombre": "Sierra Circular",
                "precio": 120000.0,
                "total": 120000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 1
    },
    {
        "comuna": "Ñuñoa",
        "correo": "patricia.ramirez@example.com",
        "direccion": "Calle Larga 111",
        "estado_envio": 3,
        "fecha_compra": "2024-07-09T02:40:32.638577",
        "nombre": "Patricia Ramírez",
        "order_id": 13,
        "productos": [
            {
                "cantidad": 3,
                "id": 4,
                "nombre": "Destornillador",
                "precio": 3000.0,
                "total": 9000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 3
    },
    {
        "comuna": "La Florida",
        "correo": "rodrigo.diaz@example.com",
        "direccion": "Avenida Nueva 222",
        "estado_envio": 2,
        "fecha_compra": "2024-07-09T02:40:34.693582",
        "nombre": "Rodrigo Díaz",
        "order_id": 14,
        "productos": [
            {
                "cantidad": 1,
                "id": 5,
                "nombre": "Llave Inglesa",
                "precio": 15000.0,
                "total": 15000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 1
    },
    {
        "comuna": "Santiago",
        "correo": "constanza.silva@example.com",
        "direccion": "Pasaje Central 333",
        "estado_envio": 1,
        "fecha_compra": "2024-07-09T02:40:36.748018",
        "nombre": "Constanza Silva",
        "order_id": 15,
        "productos": [
            {
                "cantidad": 1,
                "id": 1,
                "nombre": "Taladro Percutor Bosch",
                "precio": 89090.99,
                "total": 89090.99
            },
            {
                "cantidad": 2,
                "id": 2,
                "nombre": "Martillo",
                "precio": 5000.0,
                "total": 10000.0
            },
            {
                "cantidad": 1,
                "id": 3,
                "nombre": "Sierra Circular",
                "precio": 120000.0,
                "total": 120000.0
            }
        ],
        "region": "Región Metropolitana",
        "tipo_estado": 2
    }
 ]

# Contador de ID de pedidos
order_id_counter = 1

# Obtener todos los productos (GET)
@api.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(products)

# Obtener un producto por ID (GET)
@api.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((item for item in products if item["id"] == product_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({"message": "Producto no encontrado"}), 404

# Agregar un nuevo producto (POST)
@api.route('/api/products', methods=['POST'])
def add_product():
    new_product = request.json
    products.append(new_product)
    return jsonify({"message": "Producto agregado correctamente", "product": new_product}), 201

# Actualizar un producto existente (PUT)
@api.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((item for item in products if item["id"] == product_id), None)
    if product:
        updated_product = request.json
        product.update(updated_product)
        return jsonify({"message": "Producto actualizado correctamente", "product": product})
    else:
        return jsonify({"message": "Producto no encontrado"}), 404

# Eliminar un producto (DELETE)
@api.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [item for item in products if item["id"] != product_id]
    return jsonify({"message": "Producto eliminado correctamente", "products": products})

# Obtener todos los perfiles (GET)
@api.route('/api/profiles', methods=['GET'])
def get_profiles():
    return jsonify(profiles)

# Obtener un perfil por ID (GET)
@api.route('/api/profiles/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    profile = next((item for item in profiles if item["ID"] == profile_id), None)
    if profile:
        return jsonify(profile)
    else:
        return jsonify({"message": "Perfil no encontrado"}), 404

# Agregar un nuevo perfil (POST)
@api.route('/api/profiles', methods=['POST'])
def add_profile():
    new_profile = request.json
    profiles.append(new_profile)
    return jsonify({"message": "Perfil agregado correctamente", "profile": new_profile}), 201

# Actualizar un perfil existente (PUT)
@api.route('/api/profiles/<int:profile_id>', methods=['PUT'])
def update_profile(profile_id):
    profile = next((item for item in profiles if item["ID"] == profile_id), None)
    if profile:
        updated_profile = request.json
        profile.update(updated_profile)
        return jsonify({"message": "Perfil actualizado correctamente", "profile": profile})
    else:
        return jsonify({"message": "Perfil no encontrado"}), 404

# Eliminar un perfil (DELETE)
@api.route('/api/profiles/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    global profiles
    profiles = [item for item in profiles if item["ID"] != profile_id]
    return jsonify({"message": "Perfil eliminado correctamente", "profiles": profiles})

# Obtener url transbank (GET)
@api.route('/api/transbank', methods=['GET'])
def get_transbank():
    try:
        amount = request.args.get('amount')

        # Validar que el monto sea numérico y mayor a 0
        if not amount or not amount.isdigit() or float(amount) <= 0:
            return jsonify({"error": "Monto inválido"}), 400

        amount = float(amount)  # Convertir a número

        # Configurar la sesión
        buy_order = str(random.randint(1000000, 99999999))
        session_id = str(random.randint(1000000, 99999999))
        return_url = "http://127.0.0.1:8000/index"

        # Crear la transacción con Transbank
        transaction = Transaction()
        response = transaction.create(buy_order, session_id, amount, return_url)

        # Validar que la respuesta tenga los datos esperados
        if "token" not in response or "url" not in response:
            return jsonify({"error": "Error en la respuesta de Transbank"}), 500

        return jsonify(response)  # Retornar la respuesta en formato JSON

    except Exception as e:
        print("Error en la API de Transbank:", e)
        return jsonify({"error": "Error procesando el pago"}), 500

# Obtener todos los pedidos (GET)
@api.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)
# Obtener un pedido por ID (GET)
@api.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((item for item in orders if item["order_id"] == order_id), None)
    if order:
        return jsonify(order)
    else:
        return jsonify({"message": "Pedido no encontrado"}), 404

# Agregar un nuevo pedido (POST)
@api.route('/api/orders', methods=['POST'])
def add_order():
    global order_id_counter  # Asegúrate de usar la variable global
    new_order = request.json
    new_order["order_id"] = order_id_counter
    order_id_counter += 1
    new_order["fecha_compra"] = get_current_datetime()
    orders.append(new_order)
    return jsonify({"message": "Pedido agregado correctamente", "order": new_order}), 201

# Actualizar un pedido existente (PUT)
@api.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = next((item for item in orders if item["order_id"] == order_id), None)
    if order:
        updated_order = request.json
        order.update(updated_order)
        return jsonify({"message": "Pedido actualizado correctamente", "order": order})
    else:
        return jsonify({"message": "Pedido no encontrado"}), 404

# Eliminar un pedido (DELETE)
@api.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    global orders
    orders = [item for item in orders if item["order_id"] != order_id]
    return jsonify({"message": "Pedido eliminado correctamente", "orders": orders})

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000, debug=True)



