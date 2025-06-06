import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"

def test_list_products():
    print("\n=== Testando Listagem de Produtos ===")
    
    # Listar todos os produtos
    response = requests.get(f"{BASE_URL}/products_placeholder/")
    print(f"\nBuscando todos os produtos:")
    print(f"Status: {response.status_code}")
    
    if response.status_code not in [200, 201]:
        print(f"Erro ao listar produtos: {response.text}")
        return
    
    products = response.json()
    print(f"\nProdutos encontrados: {len(products['products'])}")
    
    # Exibir detalhes de cada produto
    for i, product in enumerate(products['products'], 1):
        print(f"\nProduto {i}:")
        print(f"ID: {product['id']}")
        print(f"Nome: {product['name']}")
        print(f"Descrição: {product['description']}")
        print(f"Metacritic: {product['metacritic_score']}")
        print(f"Avaliação: {product['rating']}/{product['rating_top']}")
        print(f"Data de Lançamento: {product['released_date']}")
        print(f"Website: {product['website']}")
        print(f"Gêneros: {', '.join(product['genres']) if product['genres'] else 'N/A'}")
        print(f"Desenvolvedores: {', '.join(product['developers']) if product['developers'] else 'N/A'}")
        print(f"Publicadores: {', '.join(product['publishers']) if product['publishers'] else 'N/A'}")
        print(f"Número de Fotos: {len(product['photos'])}")
        
        # Exibir URLs das fotos
        if product['photos']:
            print("\nFotos:")
            for j, photo in enumerate(product['photos'], 1):
                print(f"  {j}. {photo['url']}")
        else:
            print("\nNenhuma foto encontrada")
        
        print("-" * 80)

def main():
    print("Iniciando teste de listagem de produtos...")
    test_list_products()
    print("\nTeste de listagem concluído!")

if __name__ == "__main__":
    main() 