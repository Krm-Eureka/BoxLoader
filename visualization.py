# visualization.py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

def plot_pallet(pallet, container=None):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    pallet.draw_pallet_frame(ax)
    
    if container:
        container.draw(ax, pallet.frame_height)
    
    for box in pallet.boxes:
        x, y, z = box.position
        dx, dy, dz = box.width, box.length, box.height
        
        verts = [
            [(x, y, z), (x+dx, y, z), (x+dx, y+dy, z), (x, y+dy, z)],
            [(x, y, z+dz), (x+dx, y, z+dz), (x+dx, y+dy, z+dz), (x, y+dy, z+dz)],
            [(x, y, z), (x, y, z+dz), (x, y+dy, z+dz), (x, y+dy, z)],
            [(x+dx, y, z), (x+dx, y, z+dz), (x+dx, y+dy, z+dz), (x+dx, y+dy, z)],
            [(x, y, z), (x, y, z+dz), (x+dx, y, z+dz), (x+dx, y, z)],
            [(x, y+dy, z), (x, y+dy, z+dz), (x+dx, y+dy, z+dz), (x+dx, y+dy, z)]
        ]
        
        ax.add_collection3d(Poly3DCollection(verts, facecolors=box.color, alpha=0.9, edgecolors='black', linewidths=1))
        ax.text(x+dx/2, y+dy/2, z+dz/2, box.box_type, color='black', fontsize=8, ha='center')

    ax.set_xlim([0, pallet.width])
    ax.set_ylim([0, pallet.length])
    ax.set_zlim([0, pallet.height])
    
    ax.set_xlabel('Width (X)')
    ax.set_ylabel('Length (Y)')
    ax.set_zlabel('Height (Z)')
    
    plt.title('Pallet Loading Visualization (Strict Priority Order)')
    plt.tight_layout()
    plt.show()
