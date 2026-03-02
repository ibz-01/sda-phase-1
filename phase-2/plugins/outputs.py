class ConsoleWriter:

    def write(self, records):

        print("\n================ GDP ANALYSIS DASHBOARD ================\n")

        for title, data in records.items():

            print(f"\n----- {title} -----\n")

            if isinstance(data, list):
                for row in data:
                    print(row)

            else:
                print(data)

        print("\n================ END OF REPORT =========================\n")