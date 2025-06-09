import requests
from sqlmodel import Session, select
from app.models.models import Product_Placeholder
from app.schemas.product_placeholder_schema import ProductPlaceholderCreate
from app.schemas.product_schema import ProductCreate
from app.schemas.establishment_schema import EstablishmentCreate
from app.database import session
from app.schemas.promotion_schema import PromotionCreate

def create_games_and_products(session: Session):
    # Lista fictícia de 50 jogos (apenas nomes para exemplo)
    jogos = [
    "The Legend of Zelda: Breath of the Wild",
    "God of War",
    "Red Dead Redemption 2",
    "The Witcher 3: Wild Hunt",
    "Minecraft",
    "Fortnite",
    "Call of Duty: Modern Warfare",
    "Apex Legends",
    "Overwatch",
    "Cyberpunk 2077",
    "Horizon Zero Dawn",
    "Dark Souls III",
    "Elden Ring",
    "Super Mario Odyssey",
    "Grand Theft Auto V",
    "Animal Crossing: New Horizons",
    "DOOM Eternal",
    "Sekiro: Shadows Die Twice",
    "Metal Gear Solid V",
    "Resident Evil 2",
    "Persona 5",
    "Final Fantasy VII Remake",
    "Bloodborne",
    "Splatoon 2",
    "Monster Hunter: World",
    "FIFA 21",
    "Rocket League",
    "Celeste",
    "Stardew Valley",
    "Hollow Knight",
    "Among Us",
    "Fall Guys",
    "Dead Cells",
    "Cuphead",
    "The Last of Us Part II",
    "Uncharted 4",
    "Bayonetta 2",
    "Disco Elysium",
    "The Outer Worlds",
    "Control",
    "Diablo III",
    "Destiny 2",
    "Borderlands 3",
    "The Sims 4",
    "Battlefield V",
    "Marvel's Spider-Man",
    "FIFA 22",
    "Super Smash Bros. Ultimate",
    "Ghost of Tsushima",
    "Death Stranding"
]
    establishment = EstablishmentCreate(name="Steam123", url="https://store.steampowered.com")
    response_establishment = requests.post("http://localhost:8000/establishments/", json=establishment.model_dump())
    print(f"Status code: {response_establishment.status_code}")
    print(f"Response content: {response_establishment.text}")
    
    if response_establishment.status_code != 200: 
        raise Exception("Erro ao criar estabelecimento")

    establishment_id = response_establishment.json().get("id")
    if not establishment_id:
        raise Exception("Resposta da API não contém 'id'")
    
    
    promotion = PromotionCreate(  name="supersale",
    description="string",
    min_discount_percentage=0,
    max_discount_percentage=100)
    
    response_promotion = requests.post("http://localhost:8000/promotions/", json=promotion.model_dump())
    print(f"Status code: {response_promotion.status_code}")
    print(f"Response content: {response_promotion.text}")
    
    if response_promotion.status_code != 201:
        raise Exception("Erro ao criar promoção")
    
    promotion_id = response_promotion.json().get("id")
    if not promotion_id:
        raise Exception("Resposta da API não contém 'id'")
    



    for nome_jogo in jogos:
        # Cria um placeholder para o jogo
        game_placeholder = ProductPlaceholderCreate(name=nome_jogo)
        response = requests.post("http://localhost:8000/product-placeholders/", json=game_placeholder.model_dump())

        if response.status_code not in (200, 201):
            print(f"Erro ao criar product-placeholder para '{nome_jogo}':", response.status_code, response.text)
            continue

        try:
            game_placeholder_id = response.json()["id"]
        except (KeyError, ValueError) as e:
            print(f"Resposta inesperada ao criar product-placeholder para '{nome_jogo}':", response.text)
            continue

        # Cria 2 produtos diferentes para o mesmo jogo
        product1 = ProductCreate(
            price=120.00,
            discount_price=80.00,
            url="https://store.steampowered.com/app/1202070/Sekiro_Shadows_Die_Twice/",
            product_placeholder_id=game_placeholder_id,
            establishment_id=establishment_id,
            promotion_id=promotion_id
        )
        product2 = ProductCreate(
            price=43.98,
            discount_price=20.99,
            url="https://store.steampowered.com/app/1202070/Sekiro_Shadows_Die_Twice/",
            product_placeholder_id=game_placeholder_id,
            establishment_id=establishment_id,
            promotion_id=promotion_id
        )

        for product in [product1, product2]:
            response = requests.post("http://localhost:8000/products/", json=product.model_dump())
            if response.status_code not in (200, 201):
                print(f"Erro ao criar produto para '{nome_jogo}':", response.status_code, response.text)

    print("48 jogos e 2 produtos para cada criados com sucesso!")
if __name__ == "__main__":
    create_games_and_products(session)
