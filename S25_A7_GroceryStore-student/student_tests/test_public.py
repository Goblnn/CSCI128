from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon
from autograder_platform.Executors.Executor import Executor
from autograder_platform.Executors.Environment import ExecutionEnvironmentBuilder, getResults
from autograder_platform.StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder

class GroceryStorePublicTests(TestCommon):

    def setUp(self) -> None:
        self.environmentBuilder = ExecutionEnvironmentBuilder()\
        .setTimeout(5)
        self.environment = self.environmentBuilder.build()

    def assert_process_inventory(self, parameters, expectedOutput):
        runner = PythonRunnerBuilder(self.studentSubmission)\
            .setEntrypoint(function="process_inventory")\
            .addParameter(parameters[0])\
            .addParameter(parameters[1])\
            .addParameter(parameters[2])\
            .build()

        Executor.execute(self.environment, runner)

        actualOutput = getResults(self.environment).parameter[1]

        self.assertListEqual(expectedOutput, actualOutput)

    def assert_process_sale(self, parameters, expectedOutput, expectedList):
        runner = PythonRunnerBuilder(self.studentSubmission)\
            .setEntrypoint(function="process_sale")\
            .addParameter(parameters[0])\
            .addParameter(parameters[1])\
            .addParameter(parameters[2])\
            .addParameter(parameters[3])\
            .build()

        Executor.execute(self.environment, runner)

        actualOutput = getResults(self.environment).return_val
        actualList = getResults(self.environment).parameter[1]

        self.assertEqual(expectedOutput, actualOutput)
        self.assertListEqual(expectedList, actualList)

    def assert_generate_eod_report(self, parameters, expectedOutput):
        runner = PythonRunnerBuilder(self.studentSubmission)\
            .setEntrypoint(function="generate_eod_report")\
            .addParameter(parameters[0])\
            .addParameter(parameters[1])\
            .addParameter(parameters[2])\
            .addParameter(parameters[3])\
            .build()

        Executor.execute(self.environment, runner)

        actualOutput = getResults(self.environment).return_val

        self.assertListEqual(expectedOutput, actualOutput)


    @Number(1.1)
    @Weight(0.33)
    def test_process_inventory_example(self):
        """`process_inventory` - Given Example"""

        items = ["banana", "apple", "orange"]
        current_inventory = [0, 5, 3]
        inventory_delta = [6, -3, -4]

        expectedOutput = [6, 2, 0]
        
        self.assert_process_inventory([items, current_inventory, inventory_delta], expectedOutput)

    @Number(1.2)
    @Weight(0.33)
    def test_process_sale_example(self):
        """`process_sale` - Given Example"""

        items = ["banana", "apple", "orange"]
        current_inventory = [6, 2, 0]
        item = "banana"
        itemQuantity = 7

        expectedOutput = "banana 6"
        expectedInventory = [0, 2, 0]

        self.assert_process_sale([items, current_inventory, item, itemQuantity], expectedOutput, expectedInventory)

    @Number(1.3)
    @Weight(0.34)
    def test_generate_eod_report_example(self):
        """`generate_eod_report` - Given Example"""

        items = ["banana", "apple", "orange"]
        current_inventory = [6, 2, 0]
        prices = [.59, 2.49, 3.39]
        running_sales_report = ["banana 5", "orange 15"]

        expectedOutput = [
            "banana: Inventory: 6 $3.54 Sold: 5 $2.95",
            "apple: Inventory: 2 $4.98 Sold: 0 $0.00",
            "orange: Inventory: 0 $0.00 Sold: 15 $50.85"
        ]

        self.assert_generate_eod_report([items, current_inventory, prices, running_sales_report], expectedOutput)

    @Number(2.1)
    @Weight(.5)
    def test_process_inventory_all_empty_lists(self):
        """`process_inventory` - All Empty Lists"""

        items = []
        current_inventory = []
        inventory_delta = []

        expectedOutput = []

        self.assert_process_inventory([items, current_inventory, inventory_delta], expectedOutput)

    @Number(2.2)
    @Weight(.5)
    def test_process_inventory_longer_items_list(self):
        """`process_inventory` - Longer Items List"""

        items = ["apple", "bread", "cheese", "dorito", "egg", "flour", "hot dog", "ice", "jelly", "kool-aid", "lettuce", "milk",
                 "nuts",]
        current_inventory = [15, 7, 83, 9, 0, 5, 1, 8, 140, 24, 53, 41, 3]
        inventory_delta = [-5, -23, 9, 0, 0, -2, -15, 0, 0, -5, 13, 7, -1]

        expectedOutput = [10, 0, 92, 9, 0, 3, 0, 8, 140, 19, 66, 48, 2]

        self.assert_process_inventory([items, current_inventory, inventory_delta], expectedOutput)

    @Number(2.3)
    @Weight(.5)
    def test_process_sale_refunds(self):
        """`process_sale` - Refunds"""

        items = ["pringles", "bags", "bars", "tortillas", "butter"]
        current_inventory = [3, 17, 0, 5, 1]
        item = "butter"
        itemQuantity = -4

        expectedOutput = "butter -4"
        expectedInventory = [3, 17, 0, 5, 5]

        self.assert_process_sale([items, current_inventory, item, itemQuantity], expectedOutput, expectedInventory)

    @Number(2.4)
    @Weight(.5)
    def test_process_sale_overselling(self):
        """`process_sale` - Overselling"""

        items = ["pringles", "bags", "soap", "tortillas", "butter"]
        current_inventory = [3, 17, 0, 5, 1]
        item = "bags"
        itemQuantity = 45

        expectedOutput = "bags 17"
        expectedInventory = [3, 0, 0, 5, 1]

        self.assert_process_sale([items, current_inventory, item, itemQuantity], expectedOutput, expectedInventory)


    @Number(2.5)
    @Weight(1)
    def test_generate_eod_report_no_sales(self):
        """`generate_eod_report` - No Sales"""

        items = ["asparagus", "cucumbers", "parsley", "donuts", "bread"]
        current_inventory = [5, 22, 0, 4, 12]
        prices = [1.29, .79, .09, 1.99, 3.99]
        running_sales_report = []


        expectedOutput = [
            "asparagus: Inventory: 5 $6.45 Sold: 0 $0.00",
            "cucumbers: Inventory: 22 $17.38 Sold: 0 $0.00",
            "parsley: Inventory: 0 $0.00 Sold: 0 $0.00",
            "donuts: Inventory: 4 $7.96 Sold: 0 $0.00",
            "bread: Inventory: 12 $47.88 Sold: 0 $0.00"
        ]

        self.assert_generate_eod_report([items, current_inventory, prices, running_sales_report], expectedOutput)

    @Number(2.6)
    @Weight(1)
    def test_generate_eod_report_sold_out(self):
        """`generate_eod_report` - Sold Out"""

        items = ["asparagus", "cucumbers", "parsley", "donuts", "bread"]
        current_inventory = [0, 0, 0, 0, 0]
        prices = [1.29, .79, .09, 1.99, 3.99]
        running_sales_report = ["asparagus 5", "cucumbers 22", "parsley 0", "donuts 4", "bread 12"]


        expectedOutput = [
            "asparagus: Inventory: 0 $0.00 Sold: 5 $6.45",
            "cucumbers: Inventory: 0 $0.00 Sold: 22 $17.38",
            "parsley: Inventory: 0 $0.00 Sold: 0 $0.00",
            "donuts: Inventory: 0 $0.00 Sold: 4 $7.96",
            "bread: Inventory: 0 $0.00 Sold: 12 $47.88"
        ]

        self.assert_generate_eod_report([items, current_inventory, prices, running_sales_report], expectedOutput)

    @Number(3.1)
    @Weight(1)
    def test_process_inventory_generic(self):
        """`process_inventory` - Generic Inputs"""

        items = ['cheese', 'pizza', 'pasta', 'water', 'sausage', 'tea', 'sandwiches', 'coffee', 'cupcakes', 'candy', 'granola', 'cleaners']
        current_inventory = [9, 13, 14, 10, 17, 8, 16, 13, 13, 18, 17, 7]
        inventory_delta = [-10, -10, -11, 1, -9, 4, -10, -10, -7, -13, -8, 1]

        expectedOutput = [0, 3, 3, 11, 8, 12, 6, 3, 6, 5, 9, 8]

        self.assert_process_inventory([items, current_inventory, inventory_delta], expectedOutput)

    @Number(3.2)
    @Weight(1)
    def test_process_inventory_overselling_public(self):
        """`process_inventory` - Overselling!"""

        items = ['cheese', 'pizza', 'pasta', 'water', 'sausage', 'tea', 'sandwiches', 'coffee', 'cupcakes', 'candy', 'granola', 'cleaners']
        current_inventory = [0, 3, 7, 22, 1, 8, 16, 2, 0, 0, 5, 73]
        inventory_delta = [-15, -20, -11, 4, -9, -8, -33, -16, -7, -17, -8, -42]

        expectedOutput = [0, 0, 0, 26, 0, 0, 0, 0, 0, 0, 0, 31]

        self.assert_process_inventory([items, current_inventory, inventory_delta], expectedOutput)


    @Number(3.3)
    @Weight(1)
    def test_process_sale_generic(self):
        """`process_sale` - Generic Inputs"""

        items = ['sausage', 'fish', 'paper']
        current_inventory = [18, 9, 4]
        itemSold = 'paper'
        quantitySold = -4

        expectedOutput = "paper -4"
        expectedInventory = [18, 9, 8]

        self.assert_process_sale([items, current_inventory, itemSold, quantitySold], expectedOutput, expectedInventory)


    @Number(3.4)
    @Weight(1)
    def test_generate_eod_report_generic_one(self):
        """`generate_eod_report` - Generic Inputs 1"""

        items = ['candy', 'soap', 'mayo']
        current_inventory = [12, 12, 11]
        prices = [5.33, 10.27, 0.66]
        running_sales_report = ['mayo 4', 'soap 4']

        expectedOutput = [
            'candy: Inventory: 12 $63.96 Sold: 0 $0.00',
            'soap: Inventory: 12 $123.24 Sold: 4 $41.08',
            'mayo: Inventory: 11 $7.26 Sold: 4 $2.64'
        ]

        self.assert_generate_eod_report([items, current_inventory, prices, running_sales_report], expectedOutput)

    @Number(3.5)
    @Weight(1)
    def test_generate_eod_report_generic_two(self):
        """`generate_eod_report` - Generic Inputs 2"""

        items = ['chicken', 'cleaners', 'pizza', 'cheese', 'yogurt', 'chips']
        current_inventory = [14, 7, 7, 10, 7, 18]
        prices = [3.14, 8.39, 10.0, 0.69, 6.3, 8.89]
        running_sales_report = ['cheese 16', 'cleaners 16', 'pizza 5', 'chicken 0', 'yogurt 14']

        expectedOutput = [
            'chicken: Inventory: 14 $43.96 Sold: 0 $0.00',
            'cleaners: Inventory: 7 $58.73 Sold: 16 $134.24',
            'pizza: Inventory: 7 $70.00 Sold: 5 $50.00',
            'cheese: Inventory: 10 $6.90 Sold: 16 $11.04',
            'yogurt: Inventory: 7 $44.10 Sold: 14 $88.20',
            'chips: Inventory: 18 $160.02 Sold: 0 $0.00'
        ]
        
        self.assert_generate_eod_report([items, current_inventory, prices, running_sales_report], expectedOutput)
