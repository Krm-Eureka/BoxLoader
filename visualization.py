# visualization.py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

def plot_pallet(pallet, containers=None):
    """
    วาดภาพพาเลทและกล่องที่วางอยู่บนพาเลท
    Args:
        pallet (Pallet): พาเลทที่ต้องการวาด
        containers (list): รายการตู้คอนเทนเนอร์ (ถ้ามี)
    """
    fig = plt.figure(figsize=(12, 8))  # สร้างรูปภาพ
    ax = fig.add_subplot(111, projection='3d')  # สร้างแกน 3 มิติ
    
    pallet.draw_pallet_frame(ax)  # วาดโครงพาเลท
    
    if containers:
        for container in containers:
            container.draw(ax, pallet.frame_height)  # วาดตู้คอนเทนเนอร์ (ถ้ามี)
    
    for box in pallet.boxes:  # วนลูปเพื่อวาดกล่องแต่ละใบ
        x, y, z = box.position  # ตำแหน่งของกล่อง
        dx, dy, dz = box.width, box.length, box.height  # ขนาดของกล่อง
        
        # กำหนดจุดยอดของกล่อง
        verts = [
            [(x, y, z), (x+dx, y, z), (x+dx, y+dy, z), (x, y+dy, z)],
            [(x, y, z+dz), (x+dx, y, z+dz), (x+dx, y+dy, z+dz), (x, y+dy, z+dz)],
            [(x, y, z), (x, y, z+dz), (x, y+dy, z+dz), (x, y+dy, z)],
            [(x+dx, y, z), (x+dx, y, z+dz), (x+dx, y+dy, z+dz), (x+dx, y+dy, z)],
            [(x, y, z), (x, y, z+dz), (x+dx, y, z+dz), (x+dx, y, z)],
            [(x, y+dy, z), (x, y+dy, z+dz), (x+dx, y+dy, z+dz), (x+dx, y+dy, z)]
        ]
        
        # วาดกล่องลงบนกราฟ
        ax.add_collection3d(Poly3DCollection(verts, facecolors=box.color, alpha=0.9, edgecolors='black', linewidths=1))
        # แสดงชื่อกล่องบนกล่อง
        ax.text(x+dx/2, y+dy/2, z+dz/2, box.box_type, color='black', fontsize=8, ha='center')

    # กำหนดขอบเขตของแกน
    ax.set_xlim([0, pallet.width])
    ax.set_ylim([0, pallet.length])
    ax.set_zlim([0, pallet.height])
    
    # กำหนดชื่อแกน
    ax.set_xlabel('Width (X)')
    ax.set_ylabel('Length (Y)')
    ax.set_zlabel('Height (Z)')
    
    plt.title('Pallet Loading Visualization (Strict Priority Order)')  # กำหนดชื่อกราฟ
    plt.tight_layout()  # ปรับขนาดกราฟ
    plt.show()  # แสดงกราฟ
