# container.py
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Container:
    def __init__(self, container_type, length, width, height, thickness, color, alpha):
        self.container_type = container_type
        self.length = length
        self.width = width
        self.height = height
        self.thickness = thickness
        self.color = color
        self.alpha = alpha
        self.x = 0
        self.y = 0

    def draw(self, ax, frame_height):
        x, y, z = self.x, self.y, frame_height
        dx, dy, dz = self.length, self.width, self.height
        
        vertices = np.array([
            [x, y, z], [x+dx, y, z], [x+dx, y+dy, z], [x, y+dy, z],
            [x, y, z+dz], [x+dx, y, z+dz], [x+dx, y+dy, z+dz], [x, y+dy, z+dz]
        ])
        
        faces = [
            [vertices[4], vertices[5], vertices[6], vertices[7]],  # ด้านบน
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # ฐาน
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # ด้านหน้า
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # ด้านหลัง
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # ด้านขวา
            [vertices[0], vertices[3], vertices[7], vertices[4]]    # ด้านซ้าย
        ]
        
        ax.add_collection3d(Poly3DCollection(faces[1:], facecolor=self.color, alpha=self.alpha))  # 5 ด้านที่ไม่เปิด
        ax.add_collection3d(Poly3DCollection([faces[0]], facecolor=self.color, alpha=0))  # เปิดด้านบน
