import requests
import json
from uuid import UUID
import time
from typing import Optional

# Configurações
BASE_URL = "http://localhost:8000"
API_KEY = "3d33178e180644ba9c0dcbaa98278664"

def check_api_status():
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("API está online e acessível!")
            return True
        else:
            print(f"API retornou status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("ERRO: Não foi possível conectar à API!")
        print("Certifique-se de que a API está rodando com o comando:")
        print("uvicorn app.main:app --reload")
        return False

def print_section(title: str):
    print("\n" + "=" * 50)
    print(" " * ((50 - len(title)) // 2) + title)
    print("=" * 50 + "\n")

def test_category():
    print("\n=== Testando Categoria ===")
    
    # Criar categoria
    category_data = {
        "name": "RPGGames"  # Nome sem espaços, apenas letras e números
    }
    response = requests.post(f"{BASE_URL}/categories/", json=category_data)
    print(f"\nCriando categoria: {json.dumps(category_data, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao criar categoria: {response.text}")
        return None
    
    category_id = response.json()["id"]
    
    # Atualizar categoria
    update_data = {
        "name": "RPGGamesPro"  # Nome sem espaços, apenas letras e números
    }
    response = requests.put(f"{BASE_URL}/categories/{category_id}", json=update_data)
    print(f"\nAtualizando categoria: {json.dumps(update_data, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao atualizar categoria: {response.text}")
        return None
    
    return category_id

def test_plataform():
    print("\n=== Testando Plataforma ===")
    
    # Criar plataforma
    plataform_data = {
        "name": "NintendoSwitch"  # Nome sem espaços, máximo 100 caracteres
    }
    response = requests.post(f"{BASE_URL}/plataforms/", json=plataform_data)
    print(f"\nCriando plataforma: {json.dumps(plataform_data, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao criar plataforma: {response.text}")
        return None
    
    plataform_id = response.json()["id"]
    
    # Atualizar plataforma
    update_data = {
        "name": "NintendoSwitchPro"  # Nome sem espaços, máximo 100 caracteres
    }
    response = requests.put(f"{BASE_URL}/plataforms/{plataform_id}", json=update_data)
    print(f"\nAtualizando plataforma: {json.dumps(update_data, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao atualizar plataforma: {response.text}")
        return None
    
    return plataform_id

def test_product_placeholder(category_id, plataform_id):
    print("\n=== Testando Produto Placeholder ===")
    
    # Criar produto
    product_data = {
        "name": "The Legend of Zelda: Tears of the Kingdom",  # Nome do jogo que existe na RAWG API
        "description": "Aventura épica no reino de Hyrule",
        "category": category_id,
        "plataform": plataform_id
    }
    response = requests.post(f"{BASE_URL}/products_placeholder/", json=product_data)
    print(f"\nCriando produto: {json.dumps(product_data, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao criar produto: {response.text}")
        return None
    
    product_id = response.json()["id"]
    
    # Verificar se o produto foi criado com as fotos
    response = requests.get(f"{BASE_URL}/products_placeholder/{product_id}")
    print(f"\nBuscando produto criado: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao buscar produto: {response.text}")
        return None
    
    product = response.json()
    if "photos" not in product:
        print("Erro: Fotos não foram retornadas com o produto")
        return None
    
    print(f"\nFotos do produto: {json.dumps(product['photos'], indent=2)}")
    
    # Atualizar produto
    update_data = {
        "name": "The Legend of Zelda: Tears of the Kingdom Deluxe",  # Nome do jogo que existe na RAWG API
        "description": "Edição deluxe da aventura épica no reino de Hyrule",
        "category": category_id,
        "plataform": plataform_id
    }
    response = requests.put(f"{BASE_URL}/products_placeholder/{product_id}", json=update_data)
    print(f"\nAtualizando produto: {json.dumps(update_data, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao atualizar produto: {response.text}")
        return None
    
    # Verificar se o produto foi atualizado com as novas fotos
    response = requests.get(f"{BASE_URL}/products_placeholder/{product_id}")
    print(f"\nBuscando produto atualizado: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao buscar produto atualizado: {response.text}")
        return None
    
    product = response.json()
    if "photos" not in product:
        print("Erro: Fotos não foram retornadas com o produto atualizado")
        return None
    
    print(f"\nFotos do produto atualizado: {json.dumps(product['photos'], indent=2)}")
    
    return product_id

def test_establishment():
    print("\n=== Testando Estabelecimento ===")
    
    # Criar estabelecimento
    establishment_data = {
        "name": "NintendoStore",  # Nome sem espaços, máximo 100 caracteres
        "url": "https://store.nintendo.com"  # URL válida começando com https://
    }
    response = requests.post(f"{BASE_URL}/establishments/", json=establishment_data)
    print(f"\nCriando estabelecimento: {json.dumps(establishment_data, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao criar estabelecimento: {response.text}")
        return None
    
    establishment_id = response.json()["id"]
    
    # Atualizar estabelecimento
    update_data = {
        "name": "NintendoStorePro",  # Nome sem espaços, máximo 100 caracteres
        "url": "https://store.nintendo.com/pro"  # URL válida começando com https://
    }
    response = requests.put(f"{BASE_URL}/establishments/{establishment_id}", json=update_data)
    print(f"\nAtualizando estabelecimento: {json.dumps(update_data, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao atualizar estabelecimento: {response.text}")
        return None
    
    return establishment_id

def test_promotion():
    print("\n=== Testando Promoção ===")
    
    # Criar promoção
    promotion_data = {
        "name": "NintendoSale2024"  # Nome sem espaços, apenas letras e números, entre 3 e 50 caracteres
    }
    response = requests.post(f"{BASE_URL}/promotions/", json=promotion_data)
    print(f"\nCriando promoção: {json.dumps(promotion_data, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao criar promoção: {response.text}")
        return None
    
    promotion_id = response.json()["id"]
    
    # Atualizar promoção
    update_data = {
        "name": "NintendoSale2024Pro"  # Nome sem espaços, apenas letras e números, entre 3 e 50 caracteres
    }
    response = requests.put(f"{BASE_URL}/promotions/{promotion_id}", json=update_data)
    print(f"\nAtualizando promoção: {json.dumps(update_data, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao atualizar promoção: {response.text}")
        return None
    
    return promotion_id

def test_product(product_placeholder_id: str, establishment_id: str, promotion_id: str):
    print_section("TESTANDO PRODUTOS COM PRECOS")
    
    try:
        # Criar produto com preco
        print("Criando produto com preco...")
        response = requests.post(
            f"{BASE_URL}/products/",
            json={
                "original_price": 399.90,
                "discounted_price": 199.90,
                "product_placeholder_id": product_placeholder_id,
                "establishment_id": establishment_id,
                "promotion_id": promotion_id
            }
        )
        print(f"Status code: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code not in [200, 201]:
            print(f"Erro ao criar produto com preco. Status code: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None
            
        product = response.json()
        print(f"Produto com preco criado: {json.dumps(product, indent=2)}")
        
        # Listar produtos com precos
        print("\nListando produtos com precos...")
        response = requests.get(f"{BASE_URL}/products/")
        print(f"Status code: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code not in [200, 201]:
            print(f"Erro ao listar produtos com precos. Status code: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None
            
        products = response.json()
        print(f"Produtos encontrados: {json.dumps(products, indent=2)}")
        
        # Filtrar produtos
        print("\nFiltrando produtos...")
        response = requests.get(
            f"{BASE_URL}/products/",
            params={
                "max_discount": 60.0,
                "establishment_id": establishment_id,
                "promotion_id": promotion_id
            }
        )
        print(f"Status code: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code not in [200, 201]:
            print(f"Erro ao filtrar produtos. Status code: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None
            
        filtered_products = response.json()
        print(f"Produtos filtrados: {json.dumps(filtered_products, indent=2)}")
        
        return True
    except Exception as e:
        print(f"Erro ao testar produtos com precos: {str(e)}")
        return None

def main():
    print("Iniciando testes da API...")
    
    # Verificar se a API está online
    try:
        response = requests.get(f"{BASE_URL}/categories/")
        if response.status_code in [200, 201]:
            print("API está online e acessível!")
        else:
            print(f"API retornou status code inesperado: {response.status_code}")
            return
    except Exception as e:
        print(f"Erro ao acessar a API: {str(e)}")
        return
    
    # Testar categorias
    category_id = test_category()
    if not category_id:
        print("Erro ao testar categorias. Abortando testes.")
        return
    
    # Testar plataformas
    plataform_id = test_plataform()
    if not plataform_id:
        print("Erro ao testar plataformas. Abortando testes.")
        return
    
    # Testar produtos
    product_id = test_product_placeholder(category_id, plataform_id)
    if not product_id:
        print("Erro ao testar produtos. Abortando testes.")
        return
    
    # Testar estabelecimentos
    establishment_id = test_establishment()
    if not establishment_id:
        print("Erro ao testar estabelecimentos. Abortando testes.")
        return
    
    # Testar promocoes
    promotion_id = test_promotion()
    if not promotion_id:
        print("Erro ao testar promocoes. Abortando testes.")
        return
    
    # Testar produtos com precos
    if not test_product(product_id, establishment_id, promotion_id):
        print("Erro ao testar produtos com precos. Abortando testes.")
        return
    
    print("\nTodos os testes foram concluidos com sucesso!")

if __name__ == "__main__":
    main() 