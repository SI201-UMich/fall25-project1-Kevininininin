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
    pass

def sales_rank(data):
    pass

def output_file(calc1, calc2):
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

