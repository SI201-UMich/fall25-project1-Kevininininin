# Name: Jinghan Wu
# UMID: 77132944
# E-mail: kevinwuu@umich.edu
# Collaborators: I'm working by myself.
# AI disclosure: As instructed, I first made function decomposition without AI assistance, with each function,
                #I also designed step-by-step breakdowns that the program should calculate.
                #I then fed my plan to ChatGPT where it outputed initial codes. From there I made lots of
                #edits, asked for clarifications, carefully read through each line to make sure I understood everything
                #and that everything looked as intended. 

import csv
import unittest

# === Functions ===
def load_data(csv_file):
    """
    Load CSV file into a nested dictionary:
    {
        "Shipment Detail": {header1: [...], ...},
        "About Shipment": {header8: [...], ...},
        "Item Count": n
    }
    """
    return_dict = {"Shipment Detail": {}, "About Shipment": {}, "Item Count": 0}

    # columns to cast
    int_cols = {"Postal Code", "Quantity"}
    float_cols = {"Sales", "Discount", "Profit"}

    infile = open(csv_file, "r")
    csv_reader = csv.reader(infile)

    headers = next(csv_reader)
    total_cols = len(headers)

    # split header groups
    shipment_headers = headers[:7]
    about_headers = headers[7:]

    # init lists
    for h in shipment_headers:
        return_dict["Shipment Detail"][h] = []
    for h in about_headers:
        return_dict["About Shipment"][h] = []

    valid_count = 0

    for row in csv_reader:
        if len(row) == total_cols:   # only accept complete rows
            valid_count += 1
            for i in range(total_cols):
                raw = row[i].strip()
                col_name = headers[i]

                # cast types
                if col_name in int_cols:
                    value = int(raw)
                elif col_name in float_cols:
                    value = float(raw)
                else:
                    value = raw

                if col_name in shipment_headers:
                    return_dict["Shipment Detail"][col_name].append(value)
                elif col_name in about_headers:
                    return_dict["About Shipment"][col_name].append(value)

    return_dict["Item Count"] = valid_count
    infile.close()
    return return_dict

def tech_stats(data):
    """
    Question to answer (used 3 columns of data highlighted in <>): 
    Which <state> has the highest percentage of <Technology orders> for <First Class> shipments.

    Input structure (from load_data):
      data["Shipment Detail"]["State"]       -> list[str]
      data["Shipment Detail"]["Ship Mode"]   -> list[str]
      data["About Shipment"]["Category"]     -> list[str]
      data["Item Count"]                     -> int

    Returns:
      dict[str, float]  # { state_name: tech_order_pct }, sorted from highest to lowest
    """
    states = data["Shipment Detail"]["State"]
    ship_modes = data["Shipment Detail"]["Ship Mode"]
    categories = data["About Shipment"]["Category"]
    total_lines = data["Item Count"]

    # Getting # counts for tech_order & total_order
    counts_dict = {}  # { state_name : [total_order_count, tech_order_count] }

    # Count total and tech orders per state (First Class only)
    for i in range(total_lines):
        if ship_modes[i].strip().lower() != "first class": # filter to only consider "first class" orders
            continue

        curr_state = states[i].strip()
        curr_category = categories[i].strip().lower()

        if curr_state not in counts_dict:
            counts_dict[curr_state] = [0, 0]

        counts_dict[curr_state][0] += 1  # total orders for that state
        if curr_category == "technology":
            counts_dict[curr_state][1] += 1  # tech orders

    # Calculate percentages per state
    percentages = {}
    for curr_state, (total, tech) in counts_dict.items():
        if total > 0:
            percentages[curr_state] = tech / total
        else:
            percentages[curr_state] = 0.0

    # Sort by percentage (highest first)
    # percentaged.items() = [("CA", 0.5), ("FL", 0.8), ...]
    sorted_items = sorted(percentages.items(), key=lambda item: item[1], reverse=True)

    # Rebuild sorted dictionary
    sorted_percentages = {}
    for state, pct in sorted_items:
        sorted_percentages[state] = pct

    return sorted_percentages

def sales_rank(data):
    """
    Question to answer (used 3 columns of data highlighted in <>): 
    What is the ranking for total <Sales> (USD) by <City> for <First Class shipments>.

    Input (from load_data):
      data["Shipment Detail"]["City"]      -> list[str]
      data["Shipment Detail"]["Ship Mode"] -> list[str]
      data["About Shipment"]["Sales"]      -> list[float]
      data["Item Count"]                   -> int

    Returns:
      dict[str, float]  # { city_name: total_sales_usd } in descending order
    """
    cities = data["Shipment Detail"]["City"]
    ship_modes = data["Shipment Detail"]["Ship Mode"]
    sales = data["About Shipment"]["Sales"]
    total_lines = data["Item Count"]

    totals = {}  # {city: total_sales}

    for i in range(total_lines):
        # Filter to include only "First Class" shipments
        if ship_modes[i].strip().lower() != "first class":
            continue

        curr_city = cities[i].strip()
        curr_sale = sales[i]  # already float from load_data()

        # Add city to dictionary if new, else aggregate
        if curr_city not in totals:
            totals[curr_city] = 0.0
        totals[curr_city] += curr_sale

    # Sort by total sales (descending)
    sorted_items = sorted(totals.items(), key=lambda item: item[1], reverse=True)

    # Rebuild ordered dict
    ranked = {}
    for city, total in sorted_items:
        ranked[city] = total

    return ranked

def output_file(calc1, calc2, out_path="project1_output.txt"):
    """
    Write analysis results to a plain text file with the following structure:

    Proportion of tech order by state (ranked descending):
    <state>: <percentage>%

    Total tech sales by city (ranked descending):
    <city>: $<total_sales>

    Parameters:
      calc1: dict[state -> percentage of Technology orders for First Class]
      calc2: dict[city -> total First Class Sales USD]
      out_path: str (default = "project1_output.txt")

    Returns:
      str  # path of the output file
    """

    with open(out_path, "w") as f:
        # Section 1: Tech order proportion by state
        f.write("Proportion of tech order by state (ranked descending):\n")
        for state, pct in calc1.items():
            f.write(f"{state}: {round(pct * 100, 2)}%\n")  # convert ratio → %
        
        f.write("\n")  # spacing between sections

        # Section 2: Total tech sales by city
        f.write("Total tech sales by city (ranked descending):\n")
        for city, total_sales in calc2.items():
            f.write(f"{city}: ${round(total_sales, 2)}\n")

    return out_path



# === Main ===
def main():
    data = load_data("SampleSuperstore.csv")
    calc1 = tech_stats(data)
    calc2 = sales_rank(data)
    output_file(calc1, calc2)

# === Tests ===
class TestProject1(unittest.TestCase):

    # Helper function: Build mock data shaped like load_data() output
    def build_dict(self, states, ship_modes, categories):
        return {
            "Shipment Detail": {
                "State": states,
                "Ship Mode": ship_modes,
            },
            "About Shipment": {
                "Category": categories,
            },
            "Item Count": len(states),
        }

    # ==== Testing Calculation 1 ====
    def test_tech_stats_correct_percentages(self):
        """
        Test normal case where states have both tech and non-tech First Class orders.

        Test dictionary content:
        CA: 3 total rows (2 First Class, 1 Standard), 1 tech First Class → expected 0.5
        TX: 2 total rows (1 First Class, 1 Second), 1 tech First Class → expected 1.0
        FL: 1 total row (1 First Class), 0 tech → expected 0.0
        """
        data = self.build_dict(
            states     = ["CA","CA","TX","FL","CA","TX"],
            ship_modes = ["First Class","First Class","First Class","First Class","Standard Class","Second Class"],
            categories = ["Technology","Furniture","Technology","Office Supplies","Technology","Technology"],
        )
        result = tech_stats(data)

        self.assertAlmostEqual(result["TX"], 1.0)
        self.assertAlmostEqual(result["CA"], 0.5)
        self.assertAlmostEqual(result["FL"], 0.0)

    def test_tech_stats_sorted_descending(self):
        """
        Test that states are sorted by descending percentage.

        Test dictionary content:
        TX: 2 total FC rows, 2 tech -> expected 1.0
        CA: 2 total FC rows, 1 tech -> expected 0.5
        FL: 1 total FC row, 0 tech -> expected 0.0
        """
        data = self.build_dict(
            states     = ["TX","TX","CA","CA","FL"],
            ship_modes = ["First Class","First Class","First Class","First Class","First Class"],
            categories = ["Technology","Office Supplies","Technology","Furniture","Furniture"],
        )
        result = tech_stats(data)

        self.assertEqual(list(result.keys()), ["TX","CA","FL"])

    def test_tech_stats_no_first_class_returns_empty(self):
        """
        Edge case: when no First Class shipments exist, result should be empty.

        Test dictionary content:
        CA: 1 row, Standard Class → ignored
        TX: 1 row, Second Class → ignored
        FL: 1 row, Same Day → ignored
        Expected: {}
        """
        data = self.build_dict(
            states     = ["CA","TX","FL"],
            ship_modes = ["Standard Class","Second Class","Same Day"],
            categories = ["Technology","Technology","Office Supplies"],
        )
        result = tech_stats(data)

        self.assertEqual(result, {})
        self.assertEqual(len(result), 0)

    def test_tech_stats_case_and_whitespace_tolerance(self):
        """
        Edge case: function should handle mixed casing and whitespace.

        Test dictionary content:
        CA: 2 rows total (2 FC), 1 tech → expected 0.5
        TX: 1 row (1 FC), 1 tech → expected 1.0
        """
        data = self.build_dict(
            states     = ["CA","CA","TX"],
            ship_modes = [" first class ","FIRST CLASS","First Class"],
            categories = [" technology ","Furniture","TECHNOLOGY"],
        )
        result = tech_stats(data)

        self.assertAlmostEqual(result["TX"], 1.0)
        self.assertAlmostEqual(result["CA"], 0.5)
        self.assertEqual(list(result.keys()), ["TX","CA"])  # sorted: 1.0 then 0.5


    # ==== Testing Calculation 2 ====
    # Helper function: Build mock data shaped like sales_rank() output
    def build_dict_sales(self, cities, ship_modes, sales):
        return {
            "Shipment Detail": {
                "City": cities,
                "Ship Mode": ship_modes,
            },
            "About Shipment": {
                "Sales": sales,  # list[float]
            },
            "Item Count": len(cities),
        }


    def test_sales_rank_correct_totals_first_class_only(self):
        """
        Calculates correct aggregate of First Class sales by city.

        Test dictionary content:
        Los Angeles: FC rows 100.0 + 25.5; Standard 50.0 (ignored) → expected 125.5
        Dallas:     FC row  200.0 → expected 200.0
        Miami:      FC row   10.0 → expected 10.0
        """
        data = self.build_dict_sales(
            cities     = ["Los Angeles","Los Angeles","Dallas","Miami","Los Angeles"],
            ship_modes = ["First Class","Standard Class","First Class","First Class","First Class"],
            sales      = [100.0, 50.0, 200.0, 10.0, 25.5],
        )
        result = sales_rank(data)

        self.assertAlmostEqual(result["Los Angeles"], 125.5)
        self.assertAlmostEqual(result["Dallas"], 200.0)
        self.assertAlmostEqual(result["Miami"], 10.0)

    def test_sales_rank_sorted_descending(self):
        """
        Test if cities are sorted by descending total sales.

        Test dictionary content:
        Los Angeles: 100.0 + 75.0 = 175.0 → expected top
        Miami:       50.0         = 50.0  → expected middle
        Dallas:      1.0          = 1.0   → expected last
        """
        data = self.build_dict_sales(
            cities     = ["Dallas","Los Angeles","Miami","Los Angeles"],
            ship_modes = ["First Class","First Class","First Class","First Class"],
            sales      = [1.0, 100.0, 50.0, 75.0],
        )
        result = sales_rank(data)

        self.assertEqual(list(result.keys()), ["Los Angeles","Miami","Dallas"])

    # Edge case
    def test_sales_rank_ties_preserve_first_seen_order(self):
        """
        Tied totals should preserve first-seen order from the sorted stable algorithm.

        Test dictionary content:
        San Jose: 100.0 + 100.0 = 200.0 (first seen)
        New York: 200.0 + 0.0   = 200.0 (second seen)
        Expected order: ["San Jose","New York"]
        """
        data = self.build_dict_sales(
            cities     = ["San Jose","New York","San Jose","New York"],
            ship_modes = ["First Class","First Class","First Class","First Class"],
            sales      = [100.0, 200.0, 100.0, 0.0],
        )
        result = sales_rank(data)

        self.assertAlmostEqual(result["San Jose"], 200.0)
        self.assertAlmostEqual(result["New York"], 200.0)
        self.assertEqual(list(result.keys()), ["San Jose","New York"])

    def test_sales_rank_no_first_class_returns_empty(self):
        """
        When there are no First Class rows, result should be empty.

        Test dictionary content:
        All rows are non-First-Class → expected {}.
        """
        data = self.build_dict_sales(
            cities     = ["Los Angeles","Dallas","Miami"],
            ship_modes = ["Standard Class","Second Class","Same Day"],
            sales      = [100.0, 200.0, 50.0],
        )
        result = sales_rank(data)

        self.assertEqual(result, {})
        self.assertEqual(len(result), 0)

# ==== main() & unittest.main() ==== 
if __name__ == '__main__':
    print("=== Running main program ===")
    main()

    print("\n=== Running test cases ===")
    unittest.main(verbosity=2)

