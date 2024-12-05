import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
from stl import mesh


def esferico_para_cartesiano_esfera(r, pontos):
    """
    Converte coordenadas esféricas (θ, φ) para coordenadas cartesianas (x, y, z) em uma esfera de raio r.

    Parâmetros:
        r (float): Raio da esfera.
        pontos (array-like): Lista de pares (θ, φ) em graus, onde θ é o azimute e φ é o ângulo polar.

    Retorna:
        np.ndarray: Array com coordenadas cartesianas (x, y, z) dos pontos.
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


def gerar_pontos_iniciais_esfera(n_pontos):
    """
    Gera coordenadas esféricas iniciais aleatórias para pontos na superfície de uma esfera.

    Parâmetros:
        n_pontos (int): Número de pontos a serem gerados.

    Retorna:
        np.ndarray: Array de pares (θ, φ) em graus, onde θ é o azimute e φ é o ângulo polar.
    """
    pontos = []
    for _ in range(n_pontos):
        theta = np.random.uniform(0, 360)
        phi = np.random.uniform(0, 180)
        pontos.append([theta, phi])
    return np.array(pontos)


def somatorio_inverso_distancias(variaveis, r):
    """
    Calcula o inverso do somatório das distâncias entre pontos na superfície de uma esfera.

    Parâmetros:
        variaveis (np.ndarray): Coordenadas esféricas achatadas (θ, φ) dos pontos em graus.
        r (float): Raio da esfera.

    Retorna:
        float: Inverso do somatório das distâncias entre os pontos.
    """
    n_pontos = len(variaveis) // 2
    pontos = np.reshape(variaveis, (n_pontos, 2))  
    cartesianos = esferico_para_cartesiano_esfera(r, pontos)

    somatorio = 0
    for i in range(n_pontos):
        for j in range(i + 1, n_pontos):
            dist = np.linalg.norm(cartesianos[i] - cartesianos[j])
            somatorio += dist
    return 1 / somatorio  


def otimizar_pontos_esfera(r, n_pontos):
    """
    Otimiza a distribuição de pontos em uma esfera para maximizar o somatório das distâncias entre eles.

    Parâmetros:
        r (float): Raio da esfera.
        n_pontos (int): Número de pontos a serem distribuídos.

    Retorna:
        tuple: 
            - np.ndarray: Coordenadas cartesianas otimizadas (x, y, z) dos pontos.
            - float: Valor final do inverso do somatório das distâncias.
    """
    pontos_iniciais = gerar_pontos_iniciais_esfera(n_pontos)
    variaveis_iniciais = pontos_iniciais.flatten()

    resultado = minimize(
        somatorio_inverso_distancias,
        variaveis_iniciais,
        args=(r,),
        method='L-BFGS-B',
        bounds=[(0, 360) if i % 2 == 0 else (0, 180) for i in range(len(variaveis_iniciais))],
        options={'maxiter': 20000}
    )
    
    pontos_otimizados = np.reshape(resultado.x, (n_pontos, 2))
    valor_final = somatorio_inverso_distancias(resultado.x, r)
    return esferico_para_cartesiano_esfera(r, pontos_otimizados), valor_final


def salvar_em_stl(pontos_3d, nome_arquivo='pontos_otimizados_esfera.stl'):
    """
    Salva os pontos 3D como um arquivo STL, utilizando o envelope convexo dos pontos.

    Parâmetros:
        pontos_3d (np.ndarray): Coordenadas cartesianas (x, y, z) dos pontos.
        nome_arquivo (str): Nome do arquivo STL de saída (padrão: 'pontos_otimizados_esfera.stl').

    Retorna:
        Apenas Salva arquivo e exibe que esse processo foi realizado.
    """
    hull = ConvexHull(pontos_3d)  
    polygon_mesh = mesh.Mesh(np.zeros(hull.simplices.shape[0], dtype=mesh.Mesh.dtype))
    for i, simplex in enumerate(hull.simplices):
        for j in range(3):
            polygon_mesh.vectors[i][j] = pontos_3d[simplex[j], :]
    polygon_mesh.save(nome_arquivo)
    print(f"Arquivo STL salvo como '{nome_arquivo}'")
