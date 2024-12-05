import numpy as np
import random
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
from stl import mesh

def esferico_para_cartesiano_esfera(r, pontos):
    """
    Converte coordenadas esféricas para coordenadas cartesianas em uma esfera.

    Parâmetros:
    r : float
        O raio da esfera.
    pontos : array-like
        Conjunto de pontos esféricos (theta, phi), onde theta é o ângulo azimutal 
        (0 a 360 graus) e phi é o ângulo polar (0 a 180 graus).

    Retorna:
    numpy.ndarray
        Conjunto de pontos convertidos para coordenadas cartesianas (x, y, z).
    """
    xyz = []
    for theta, phi in pontos:
        theta_rad = np.radians(theta)
        phi_rad = np.radians(phi)
        x = r * np.sin(phi_rad) * np.cos(theta_rad)
        y = r * np.sin(phi_rad) * np.sin(theta_rad)
        z = r * np.cos(phi_rad)
        xyz.append([x, y, z])
    return np.array(xyz)


def gerar_pontos_iniciais(n_tipos, pontos_por_tipo):
    """
    Gera pontos iniciais de forma aleatória sobre a esfera para diferentes tipos.

    Parâmetros:
    n_tipos : int
        Número de tipos diferentes de pontos.
    pontos_por_tipo : list of int
        Lista contendo o número de pontos para cada tipo.

    Retorna:
    numpy.ndarray, list of int
        - Um conjunto de pontos iniciais em coordenadas esféricas (theta, phi).
        - Lista com os tipos dos pontos correspondentes.
    """
    pontos = []
    tipos = []
    for tipo, n_pontos in enumerate(pontos_por_tipo):
        for _ in range(n_pontos):
            theta = random.uniform(0, 360)
            phi = random.uniform(0, 180)
            pontos.append([theta, phi])
            tipos.append(tipo)
    return np.array(pontos), tipos


def distancia_ponderada_esfera(variaveis, r, pesos, tipos):
    """
    Calcula a soma das distâncias ponderadas entre os pontos sobre uma esfera.

    Parâmetros:
    variaveis : array-like
        Vetor contendo as coordenadas esféricas dos pontos.
    r : float
        O raio da esfera.
    pesos : dict
        Dicionário com os pesos de distâncias entre pares de tipos de pontos.
    tipos : list of int
        Lista com os tipos de cada ponto.

    Retorna:
    float
        Soma das distâncias ponderadas entre todos os pares de pontos.
    """
    n_pontos = len(variaveis) // 2
    pontos = np.reshape(variaveis, (n_pontos, 2))  
    cartesianos = esferico_para_cartesiano_esfera(r, pontos)

    soma_distancias_ponderadas = 0
    for i in range(n_pontos):
        for j in range(i + 1, n_pontos):
            dist = np.linalg.norm(cartesianos[i] - cartesianos[j])  
            tipo_i = tipos[i]
            tipo_j = tipos[j]
            if (tipo_i, tipo_j) in pesos:
                k_ij = pesos[(tipo_i, tipo_j)]
            else:
                k_ij = pesos[(tipo_j, tipo_i)]  
            soma_distancias_ponderadas += k_ij / dist  
    return soma_distancias_ponderadas


def otimizar_pontos_esfera(r, n_tipos, pontos_por_tipo, pesos):
    """
    Otimiza a distribuição dos pontos sobre uma esfera, minimizando a soma das distâncias ponderadas.

    Parâmetros:
    r : float
        O raio da esfera.
    n_tipos : int
        Número de tipos diferentes de pontos.
    pontos_por_tipo : list of int
        Lista contendo o número de pontos para cada tipo.
    pesos : dict
        Dicionário com os pesos de distâncias entre pares de tipos de pontos.

    Retorna:
    numpy.ndarray, float
        - Conjunto de pontos otimizados sobre a esfera.
        - Valor da função objetivo (distância ponderada) no ponto ótimo.
    """
    pontos_iniciais, tipos = gerar_pontos_iniciais(n_tipos, pontos_por_tipo)
    variaveis_iniciais = pontos_iniciais.flatten()

    resultado = minimize(
        distancia_ponderada_esfera,
        variaveis_iniciais,
        args=(r, pesos, tipos),
        method='L-BFGS-B',
        bounds=[(0, 360) if i % 2 == 0 else (0, 180) for i in range(len(variaveis_iniciais))],
        options={'maxiter': 20000}
    )
    
    pontos_otimizados = np.reshape(resultado.x, (sum(pontos_por_tipo), 2))
    soma_distancias_ponderadas_final = distancia_ponderada_esfera(resultado.x, r, pesos, tipos)
    return esferico_para_cartesiano_esfera(r, pontos_otimizados), soma_distancias_ponderadas_final


def salvar_em_stl(pontos_3d, nome_arquivo='pontos_otimizados.stl'):
    """
    Salva os pontos 3D otimizados em um arquivo STL.

    Parâmetros:
    pontos_3d : numpy.ndarray
        Conjunto de pontos 3D a serem salvos no arquivo STL.
    nome_arquivo : str, opcional
        Nome do arquivo STL (padrão: 'pontos_otimizados.stl').

    Retorna:
    None
    """
    hull = ConvexHull(pontos_3d)  
    polygon_mesh = mesh.Mesh(np.zeros(hull.simplices.shape[0], dtype=mesh.Mesh.dtype))
    for i, simplex in enumerate(hull.simplices):
        for j in range(3):
            polygon_mesh.vectors[i][j] = pontos_3d[simplex[j], :]
    polygon_mesh.save(nome_arquivo)
    print(f"Arquivo STL salvo como '{nome_arquivo}'")