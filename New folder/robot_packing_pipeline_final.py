import pandas as pd
import time
import os
import matplotlib.pyplot as plt
from typing import Tuple

# ===== PARAMETERS =====
CONTAINER_SPECS = {
    "pallet": lambda h: (1100, 1100, h),
    "f15": (1100, 1100, 1060),
    "f5": (1100, 1100, 680)
}

GAP = 5  # default gap (can be updated dynamically)

# ===== CORE ALGORITHM =====
def is_colliding(candidate, placed_boxes):
    for box in placed_boxes:
        if not (
            candidate["X"] + candidate["Length"] <= box["X"] or
            candidate["X"] >= box["X"] + box["Length"] or
            candidate["Y"] + candidate["Width"] <= box["Y"] or
            candidate["Y"] >= box["Y"] + box["Width"] or
            candidate["Z"] + candidate["Height"] <= box["Z"] or
            candidate["Z"] >= box["Z"] + box["Height"]
        ):
            return True
    return False

def is_supported_multibox(x, y, z, box_L, box_W, placed_boxes):
    com_x = x + box_L / 2
    com_y = y + box_W / 2
    if z == 0:
        return True
    support_area = 0
    for b in placed_boxes:
        if abs(b["Z"] + b["Height"] - z) < 1e-6:
            if b["X"] <= com_x <= b["X"] + b["Length"] and b["Y"] <= com_y <= b["Y"] + b["Width"]:
                return True
            overlap_x = max(0, min(x + box_L, b["X"] + b["Length"]) - max(x, b["X"]))
            overlap_y = max(0, min(y + box_W, b["Y"] + b["Width"]) - max(y, b["Y"]))
            support_area += overlap_x * overlap_y
    return support_area >= (box_L * box_W * 0.5)

def generate_candidate_positions_with_floor(placed_boxes, gap, container_dims):
    candidates = set()
    for x in range(0, container_dims[0], 50):
        for y in range(0, container_dims[1], 50):
            candidates.add((x, y, 0))
    for b in placed_boxes:
        for dx in [0, b["Length"]]:
            for dy in [0, b["Width"]]:
                for dz in [0, b["Height"]]:
                    x = b["X"] + dx
                    y = b["Y"] + dy
                    z = b["Z"] + dz
                    if 0 <= x < container_dims[0] and 0 <= y < container_dims[1] and 0 <= z < container_dims[2]:
                        candidates.add((x, y, z))
    return sorted(list(candidates), key=lambda pos: (pos[2], pos[1], pos[0]))

def greedy_surface_fit(df: pd.DataFrame, container_dims: Tuple[int, int, int], gap: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    placed, roller = [], []
    for priority in sorted(df["Priority"].unique()):
        df_priority = df[df["Priority"] == priority]
        for _, row in df_priority.iterrows():
            for _ in range(int(row["QTY"])):  # ใช้ QTY เพื่อเพิ่มจำนวนกล่อง
                box_L = int(row["Length"] + gap)
                box_W = int(row["Width"] + gap)
                box_H = int(row["Height"] + gap)
                candidates = generate_candidate_positions_with_floor(placed, gap, container_dims)
                placed_flag = False
                for x, y, z in candidates:
                    if x + box_L > container_dims[0] or y + box_W > container_dims[1] or z + box_H > container_dims[2]:
                        continue
                    candidate_box = {"X": x, "Y": y, "Z": z, "Length": box_L, "Width": box_W, "Height": box_H}
                    if not is_colliding(candidate_box, placed) and is_supported_multibox(x, y, z, box_L, box_W, placed):
                        candidate_box.update({"SKU": row["BoxTypes"], "Priority": row["Priority"]})
                        placed.append(candidate_box)
                        placed_flag = True
                        break
                if not placed_flag:
                    roller.append(row.to_dict())
    df_placed = pd.DataFrame(placed)
    df_unplaced = pd.DataFrame(roller)
    df_placed["Z"] = df_placed["Z"] + df_placed["Height"]  # convert to top of box
    return df_placed, df_unplaced

# ===== VISUALIZATION =====
def plot_3d(df: pd.DataFrame, container_dims: Tuple[int, int, int], utilization: float):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([0, container_dims[0]])
    ax.set_ylim([0, container_dims[1]])
    ax.set_zlim([0, container_dims[2]])
    for box in df.itertuples():
        ax.bar3d(box.X, box.Y, box.Z - box.Height, box.Length, box.Width, box.Height, shade=True)
    plt.title(f"3D Box Placement (Utilization: {utilization:.2f}%)")
    plt.savefig("placement_visualization.png")
    plt.show()

# ===== EXPORT FILES =====
def export_output(df_placed: pd.DataFrame, df_unplaced: pd.DataFrame):
    df_placed.to_csv("placed_boxes.csv", index=False)
    df_unplaced.to_csv("free_roller_boxes.csv", index=False)

# ===== MAIN LOOP =====
def determine_container_type(container_type: str, pallet_height: int):
    return CONTAINER_SPECS[container_type](pallet_height) if container_type == "pallet" else CONTAINER_SPECS[container_type]

def main():
    # อ่านข้อมูลจากไฟล์ forinput.csv
    input_file_path = "D:\\forimport.csv"
    if not os.path.exists(input_file_path):
        print(f"Error: File {input_file_path} not found.")
        return

    # โหลดข้อมูลกล่องจากไฟล์ CSV
    df = pd.read_csv(input_file_path)
    print("Input data loaded successfully.")

    # กำหนดประเภทคอนเทนเนอร์และความสูงของพาเลท (ถ้าใช้พาเลท)
    container_type = "pallet"  # ตัวอย่าง: "pallet", "f15", "f5"
    pallet_height = 1200  # ความสูงของพาเลท (ถ้าใช้ "pallet")
    container_dims = determine_container_type(container_type, pallet_height)

    # เรียกใช้ฟังก์ชันจัดเรียงกล่อง
    df_placed, df_unplaced = greedy_surface_fit(df, container_dims, GAP)

    # คำนวณการใช้งานพื้นที่
    total_volume = container_dims[0] * container_dims[1] * container_dims[2]
    used_volume = (df_placed["Length"] * df_placed["Width"] * df_placed["Height"]).sum()
    utilization = (used_volume / total_volume) * 100 if total_volume > 0 else 0

    # แสดงผลการจัดเรียงกล่องในรูปแบบ 3D
    plot_3d(df_placed, container_dims, utilization)

    # ส่งออกผลลัพธ์เป็นไฟล์ CSV
    export_output(df_placed, df_unplaced)
    print("Output files exported successfully.")

if __name__ == "__main__":
    main()