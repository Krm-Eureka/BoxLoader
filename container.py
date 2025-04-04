# container.py
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Container:
    """
    คลาส Container: แทนตู้คอนเทนเนอร์
    """
    def __init__(self, container_type, length, width, height, thickness, color, alpha):
        """
        Constructor ของคลาส Container
        Args:
            container_type (str): ชนิดของตู้คอนเทนเนอร์ (เช่น 'F15')
            length (float): ความยาวของตู้คอนเทนเนอร์ (หน่วย: เซนติเมตร)
            width (float): ความกว้างของตู้คอนเทนเนอร์ (หน่วย: เซนติเมตร)
            height (float): ความสูงของตู้คอนเทนเนอร์ (หน่วย: เซนติเมตร)
            thickness (float): ความหนาของผนังตู้คอนเทนเนอร์ (หน่วย: เซนติเมตร)
            color (str): สีของตู้คอนเทนเนอร์
            alpha (float): ความโปร่งใสของตู้คอนเทนเนอร์ (0.0 - 1.0)
        """
        self.container_type = container_type
        self.length = length
        self.width = width
        self.height = height
        self.thickness = thickness
        self.color = color
        self.alpha = alpha
        self.x = 0  # ตำแหน่ง x ของตู้คอนเทนเนอร์บนพาเลท
        self.y = 0  # ตำแหน่ง y ของตู้คอนเทนเนอร์บนพาเลท

    def draw(self, ax, frame_height):
        """
        วาดตู้คอนเทนเนอร์ลงบนกราฟ 3 มิติ
        Args:
            ax (matplotlib.axes._subplots.Axes3DSubplot): แกนของกราฟ 3 มิติ
            frame_height (float): ความสูงของโครงพาเลท (หน่วย: เซนติเมตร)
        """
        x, y, z = self.x, self.y, frame_height  # กำหนดตำแหน่งเริ่มต้นของตู้คอนเทนเนอร์
        dx, dy, dz = self.length, self.width, self.height  # กำหนดขนาดของตู้คอนเทนเนอร์
        
        # กำหนดจุดยอดของตู้คอนเทนเนอร์
        vertices = np.array([
            [x, y, z], [x+dx, y, z], [x+dx, y+dy, z], [x, y+dy, z],
            [x, y, z+dz], [x+dx, y, z+dz], [x+dx, y+dy, z+dz], [x, y+dy, z+dz]
        ])
        
        # กำหนดหน้าของตู้คอนเทนเนอร์
        faces = [
            [vertices[4], vertices[5], vertices[6], vertices[7]],  # ด้านบน
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # ฐาน
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # ด้านหน้า
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # ด้านหลัง
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # ด้านขวา
            [vertices[0], vertices[3], vertices[7], vertices[4]]    # ด้านซ้าย
        ]
        
        # วาดหน้าของตู้คอนเทนเนอร์ลงบนกราฟ
        ax.add_collection3d(Poly3DCollection(faces[1:], facecolor=self.color, alpha=self.alpha))  # 5 ด้านที่ไม่เปิด
        ax.add_collection3d(Poly3DCollection([faces[0]], facecolor=self.color, alpha=0))  # เปิดด้านบน

class F15Container(Container):
    def __init__(self):
        super().__init__("F15", 100, 100, 106, 2, "brown", 0.4)

class F9Container(Container):
    def __init__(self):
        super().__init__("F9", 90, 90, 96, 2, "blue", 0.3)
