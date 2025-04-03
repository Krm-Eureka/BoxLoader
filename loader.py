# loader.py
import csv
import io
from box import Box

def load_boxes_from_csv(csv_data):
    boxes = []
    reader = csv.DictReader(io.StringIO(csv_data))
    
    for row in reader:
        try:
            box = Box(
                box_type=row['BoxType'],
                width=float(row['w'])/10,
                length=float(row['l'])/10,
                height=float(row['h'])/10,
                max_weight=float(row['Max weight']),
                conveyor=int(row['conveyor']),
                priority=int(row['Priority']),
                qty=int(row['QTY'])
            )
            boxes.append(box)
        except Exception as e:
            print(f"Error processing row: {row}\nError: {e}")
    
    return boxes
