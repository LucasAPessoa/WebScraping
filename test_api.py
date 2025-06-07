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

def test_promotion():
    promotion_data = {
        "name": "Promoção de Verão"
    }
    
    response = requests.post(f"{BASE_URL}/promotions/", json=promotion_data)
    print(f"\nCriando promoção: {json.dumps(promotion_data, indent=2)}")
    
    if response.status_code != 201:
        print(f"Erro ao criar promoção: {response.status_code}")
        print(response.text)
        return None
    
    print(f"Promoção criada: {json.dumps(response.json(), indent=2)}")
    
    promotion_id = response.json()["id"]
    
    # Teste de atualização
    update_data = {
        "name": "Promoção de Verão Atualizada"
    }
    
    response = requests.put(f"{BASE_URL}/promotions/{promotion_id}", json=update_data)
    print(f"\nAtualizando promoção: {json.dumps(update_data, indent=2)}")
    
    if response.status_code != 200:
        print(f"Erro ao atualizar promoção: {response.status_code}")
        print(response.text)
        return None
    
    print(f"Promoção atualizada: {json.dumps(response.json(), indent=2)}")
    
    return promotion_id

def test_establishment():
    establishment_data = {
        "name": "Loja de Games",
        "url": "https://lojadegames.com"
    }
    
    response = requests.post(f"{BASE_URL}/establishments/", json=establishment_data)
    print(f"\nCriando estabelecimento: {json.dumps(establishment_data, indent=2)}")
    
    if response.status_code != 201:
        print(f"Erro ao criar estabelecimento: {response.status_code}")
        print(response.text)
        return None
    
    print(f"Estabelecimento criado: {json.dumps(response.json(), indent=2)}")
    
    establishment_id = response.json()["id"]
    
    # Teste de atualização
    update_data = {
        "name": "Loja de Games Atualizada",
        "url": "https://lojadegames.com.br"
    }
    
    response = requests.put(f"{BASE_URL}/establishments/{establishment_id}", json=update_data)
    print(f"\nAtualizando estabelecimento: {json.dumps(update_data, indent=2)}")
    
    if response.status_code != 200:
        print(f"Erro ao atualizar estabelecimento: {response.status_code}")
        print(response.text)
        return None
    
    print(f"Estabelecimento atualizado: {json.dumps(response.json(), indent=2)}")
    
    return establishment_id

def test_product_placeholder():
    product_data = {
        "name": "The Witcher 3"
    }
    
    response = requests.post(f"{BASE_URL}/product-placeholders/", json=product_data)
    print(f"\nCriando produto: {json.dumps(product_data, indent=2)}")
    
    if response.status_code != 201:
        print(f"Erro ao criar produto: {response.status_code}")
        print(response.text)
        return None
    
    print(f"Produto criado: {json.dumps(response.json(), indent=2)}")
    
    product_id = response.json()["id"]
    
    # Teste de atualização
    update_data = {
        "name": "The Witcher 3: Wild Hunt"
    }
    
    response = requests.put(f"{BASE_URL}/product-placeholders/{product_id}", json=update_data)
    print(f"\nAtualizando produto: {json.dumps(update_data, indent=2)}")
    
    if response.status_code != 200:
        print(f"Erro ao atualizar produto: {response.status_code}")
        print(response.text)
        return None
    
    print(f"Produto atualizado: {json.dumps(response.json(), indent=2)}")
    
    return product_id

def test_product(product_placeholder_id, establishment_id, promotion_id):
    product_data = {
        "original_price": 199.90,
        "discounted_price": 149.90,
        "product_placeholder_id": product_placeholder_id,
        "establishment_id": establishment_id,
        "promotion_id": promotion_id
    }
    
    response = requests.post(f"{BASE_URL}/products/", json=product_data)
    print(f"\nCriando produto: {json.dumps(product_data, indent=2)}")
    
    if response.status_code != 201:
        print(f"Erro ao criar produto: {response.status_code}")
        print(response.text)
        return None
    
    print(f"Produto criado: {json.dumps(response.json(), indent=2)}")
    
    product_id = response.json()["id"]
    
    # Teste de atualização
    update_data = {
        "original_price": 189.90,
        "discounted_price": 139.90
    }
    
    response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data)
    print(f"\nAtualizando produto: {json.dumps(update_data, indent=2)}")
    
    if response.status_code != 200:
        print(f"Erro ao atualizar produto: {response.status_code}")
        print(response.text)
        return None
    
    print(f"Produto atualizado: {json.dumps(response.json(), indent=2)}")
    
    return product_id

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
    
    # Teste de promoção
    promotion_id = test_promotion()
    if not promotion_id:
        return
    
    # Teste de estabelecimento
    establishment_id = test_establishment()
    if not establishment_id:
        return
    
    # Teste de produto placeholder
    product_placeholder_id = test_product_placeholder()
    if not product_placeholder_id:
        return
    
    # Teste de produto
    product_id = test_product(product_placeholder_id, establishment_id, promotion_id)
    if not product_id:
        return
    
    print("\nTodos os testes foram concluidos com sucesso!")

if __name__ == "__main__":
    main() 