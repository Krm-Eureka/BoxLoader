# visualization.py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

def plot_pallet(pallet, containers=None, utilization=0, output_file="pallet_visualization.png"):
    """
    วาดภาพพาเลทและกล่องที่วางอยู่บนพาเลท
    Args:
        pallet (Pallet): พาเลทที่ต้องการวาด
        containers (list): รายการตู้คอนเทนเนอร์ (ถ้ามี)
        utilization (float): เปอร์เซ็นต์การใช้พื้นที่
        output_file (str): ชื่อไฟล์สำหรับบันทึกภาพ
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

    add_volume_utilization_text(ax, utilization)  # Display utilization
    add_pickup_points(ax, pallet.boxes)  # Add pickup points

    # กำหนดขอบเขตของแกน
    ax.set_xlim([0, pallet.width])
    ax.set_ylim([0, pallet.length])
    ax.set_zlim([0, pallet.height])
    
    # กำหนดชื่อแกน
    ax.set_xlabel('Width (X)')
    ax.set_ylabel('Length (Y)')
    ax.set_zlabel('Height (Z)')
    
    # Save images from four corners
    views = {
        "front_left": (45, 30),
        "front_right": (-45, 30),
        "back_left": (135, 30),
        "back_right": (-135, 30)
    }
    for view_name, (azim, elev) in views.items():
        ax.view_init(elev=elev, azim=azim)
        plt.title(f'Pallet Loading Visualization ({view_name.replace("_", " ").capitalize()} View)\nVolume Utilization: {utilization:.2f}%')
        plt.savefig(f"{output_file.replace('.png', '')}_{view_name}.png")  # Save each view

    plt.show()  # แสดงกราฟ

def add_volume_utilization_text(ax, utilization):
    """
    แสดงข้อความการใช้พื้นที่เป็นเปอร์เซ็นต์บนกราฟ
    Args:
        ax (Axes3D): แกน 3 มิติ
        utilization (float): เปอร์เซ็นต์การใช้พื้นที่
    """
    ax.text2D(0.05, 0.95, f"Volume Utilization: {utilization:.2f}%", transform=ax.transAxes, fontsize=12, color='blue')

def add_pickup_points(ax, boxes):
    """
    แสดงจุด pickup บนกล่อง
    Args:
        ax (Axes3D): แกน 3 มิติ
        boxes (list): รายการกล่อง
    """
    for box in boxes:
        x, y, z = box.position
        dx, dy, dz = box.width, box.length, box.height
        pickup_x, pickup_y, pickup_z = x + dx / 2, y + dy / 2, z + dz
        ax.scatter(pickup_x, pickup_y, pickup_z, color='red', s=20, label='Pickup Point')
