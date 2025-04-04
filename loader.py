# loader.py
import csv
import io
import logging
from box import Box

logger = logging.getLogger(__name__)

def load_boxes_from_csv(csv_data):
    """
    Loads box data from CSV data.
    Args:
        csv_data (str): CSV data as a string.
    Returns:
        list: List of Box objects loaded from the CSV.
    """
    boxes = []
    reader = csv.DictReader(io.StringIO(csv_data))

    for row in reader:
        # Skip rows with all empty values or whitespace-only BoxType
        if all(row[key] is None for key in row) or not row['BoxTypes'].strip():
            logger.warning(f"Skipping empty or invalid row: {row}")
            continue

        try:
            # Trim whitespace from BoxType
            box_type = row['BoxTypes'].strip()
            
            # Handle missing Max weight
            max_weight = float(row.get('Max weight', 100)) # Default to 100 if missing

            # Create Box object
            box = Box(
                box_type=box_type,
                width=float(row['Width'])/10,
                length=float(row['Length'])/10,
                height=float(row['Height'])/10,
                max_weight=max_weight,
                conveyor=int(row['Conveyor']),
                priority=int(row['Priority']),
                qty=int(row['QTY'])
            )
            boxes.append(box)
        except Exception as e:
            logger.error(f"Error processing row: {row}\nError: {e}")

    return boxes
