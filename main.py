# Name: Jinghan Wu
# UMID: 77132944
# E-mail: kevinwuu@umich.edu
# Collaborators: I'm working by myself. I wrote everything.
# AI disclosure:

import csv
import unittest

# === Functions ===
def load_data(csv_file):
    return {}

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

if __name__ == "__main__":
    main()


# === Tests ===
class TestProject1(unittest.TestCase):

    def test_load_data_basic(self):
        pass

    def test_load_data_edge_empty(self):
        pass

    # Test tech_stats()
    def test_tech_stats_basic(self):
        pass

    def test_tech_stats_edge_zero_sales(self):
        pass