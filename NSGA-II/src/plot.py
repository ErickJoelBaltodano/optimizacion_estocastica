# plot.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # necesario para 3D

def plot_comparacion(fr_approx: list, fr_opt: list):
    """
    Dibuja en una única ventana dos subplots 3D:
      - Izquierda: frente aproximado
      - Derecha:  frente teórico
    Ambos coloreados con un colormap 'rainbow'.
    """
    # Convertir a arrays
    F_approx = np.array(fr_approx)
    F_opt    = np.array(fr_opt)

    # Crear figura y dos ejes 3D
    fig = plt.figure(figsize=(12, 6))
    
    # Colormaps
    cmap_approx = plt.cm.rainbow(np.linspace(0, 1, len(F_approx)))
    cmap_opt    = plt.cm.rainbow(np.linspace(0, 1, len(F_opt)))

    # Subplot 1: aproximado
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.scatter(F_approx[:,0], F_approx[:,1], F_approx[:,2],
                c=cmap_approx, s=20)
    ax1.set_title('Frente Aproximado')
    ax1.set_xlabel('f₁')
    ax1.set_ylabel('f₂')
    ax1.set_zlabel('f₃')

    # Subplot 2: teórico
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.scatter(F_opt[:,0],    F_opt[:,1],    F_opt[:,2],
                c=cmap_opt,    s=20)
    ax2.set_title('Frente Teórico')
    ax2.set_xlabel('f₁')
    ax2.set_ylabel('f₂')
    ax2.set_zlabel('f₃')

    plt.tight_layout()
    plt.show()
