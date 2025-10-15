# Name: Jinghan Wu
# UMID: 77132944
# E-mail: kevinwuu@umich.edu
# Collaborators: I'm working by myself. I wrote everything.
# AI disclosure:

import csv
import unittest

# === Functions ===
def load_data(csv_file):
    """
    Load CSV file into a nested dictionary:
    {
        "Shipment Detail": {header1: [..], header2: [..], ...},
        "About Shipment": {header8: [..], header9: [..], ...},
        "Item Count": n
    }
    """

    return_dict = {"Shipment Detail": {}, "About Shipment": {}, "Item Count": 0}

    infile = open(csv_file, "r")
    csv_reader = csv.reader(infile)

    headers = next(csv_reader)
    total_cols = len(headers)

    # split header groups for "Shipment Detail" and "About Shipment" sub-dictionaries
    shipment_headers = headers[:7]
    about_headers = headers[7:]

    # initialize empty sub-dictionary lists for all keys
    for h in shipment_headers:
        return_dict["Shipment Detail"][h] = []
    for h in about_headers:
        return_dict["About Shipment"][h] = []

    valid_count = 0 # keep track of how many lines has valid amount of values for each column

    # iterate over each line
    for row in csv_reader:
        if len(row) == total_cols:  # skip malformed lines
            valid_count += 1
            for i in range(total_cols): # smart sorting that adds each value in each line to corresponding dictionary location
                value = row[i].strip()
                col_name = headers[i]

                if col_name in shipment_headers:
                    return_dict["Shipment Detail"][col_name].append(value)
                elif col_name in about_headers:
                    return_dict["About Shipment"][col_name].append(value)

    return_dict["Item Count"] = valid_count

    infile.close()

    return return_dict

def tech_stats(data):
    """
    Compute the percentage of technology orders for each city.

    Input structure (from load_data):
      data["Shipment Detail"]["City"]        -> list[str]
      data["About Shipment"]["Category"]     -> list[str]
      data["Item Count"]                     -> int

    Returns:
      dict[str, float]  # { city_name: tech_order_pct }
    """
    cities = data["Shipment Detail"]["City"]
    categories = data["About Shipment"]["Category"]
    total_lines = data["Item Count"]

    counts_dict = {} # nested dict of {city_name : [total_order_count, is_tech_count]}

    for i in range(total_lines):
        curr_city = cities[i].strip()
        curr_category = categories[i].strip().lower()

        if curr_city not in counts_dict: # add new city nested dict to counts_dict
            counts_dict[curr_city] = [0, 0]

        counts_dict[curr_city][0] += 1 # total_order_count += 1

        if curr_category == "technology": # if is tech order: is_tech_count += 1
            counts_dict[curr_city][1] += 1

    percentages = {} # dict of {city_name : percentage_is_tech_orders}
    for curr_city, (total, tech) in counts_dict.items():
        if total > 0:
            percentages[curr_city] = tech / total
        else: # account for 0/0 edge case
            percentages[curr_city] = 0.0

    # New list of tuples of sort values from highest to lowest percentages
    sorted_items = sorted(percentages.items(), key=lambda item: item[1], reverse=True)

    # Step 4: rebuild dictionary in sorted order
    sorted_percentages = {}
    for city, pct in sorted_items:
        sorted_percentages[city] = pct

    return sorted_percentages


def sales_rank(data):
    pass

def output_file(calc1, calc2):
    # for key, value in calc1.items():
    #     print(f"City {key} = {value}%")
    pass

# === Main ===
def main():
    data = load_data("SampleSuperstore.csv")
    calc1 = tech_stats(data)
    calc2 = sales_rank(data)
    output_file(calc1, calc2)

# === Tests ===
class TestProject1(unittest.TestCase):
    data = load_data("SampleSuperstore.csv")

# ======== Test load_data() ========
    def test_load_data_9994(self):
        self.assertEqual(self.data["Item Count"], 9994)

    def test_load_data_first_row_vals(self):
        # Second line from SampleSuperstore.csv
        # Second Class,Consumer,United States,Henderson,Kentucky,42420,South,Furniture,Bookcases,261.96,2,0,41.9136
        shipment_details = self.data["Shipment Detail"]
        about_shipment = self.data["About Shipment"]

        self.assertEqual(shipment_details["Ship Mode"][0], "Second Class")
        self.assertEqual(shipment_details["City"][0], "Henderson")
        self.assertEqual(about_shipment["Category"][0], "Furniture")
        self.assertEqual(about_shipment["Sales"][0], "261.96")

    # Edge cases: 
    def test_load_data_header_partition(self):
        # Check if keys are separated correctly
        shipment_details_keys = set(self.data["Shipment Detail"].keys())
        about_shipment_keys = set(self.data["About Shipment"].keys())
        self.assertEqual(shipment_details_keys, {"Ship Mode","Segment","Country","City","State","Postal Code","Region"})
        self.assertEqual(about_shipment_keys, {"Category","Sub-Category","Sales","Quantity","Discount","Profit"})
        self.assertTrue(shipment_details_keys.isdisjoint(about_shipment_keys))

    def test_load_data_missing_file(self):
        # Expect FileNotFoundError for non-existent file
        with self.assertRaises(FileNotFoundError):
            load_data("non_existent.csv")


# ======== Test tech_stats() ========
    def test_load_data_edge_empty(self):
        pass


# ======== Test sales_rank() ========
    def test_tech_stats_basic(self):
        pass


# ======== Test output_file() ========
    def test_tech_stats_edge_zero_sales(self):
        pass



# ==== main() & unittest.main() ==== 
if __name__ == '__main__':
    print("=== Running main program ===")
    main()

    print("\n=== Running test cases ===")
    unittest.main(verbosity=2)

