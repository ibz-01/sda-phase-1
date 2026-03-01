class ConsoleWriter:

    def write(self, records):

        print("\n========== RESULT ==========\n")

        if not records:
            print("No data found.")
            return

        for record in records:
            for key, value in record.items():
                print(f"{key}: {value}")
            print("---------------------------")

        print("\n============================\n")