from enum import Enum

class AgricultureType(Enum):
    SOYA = 1
    SUGAR_CANE = 2
    COFFE = 3

    def describe(self):
        description = {
            self.SOYA: "Soja",
            self.SUGAR_CANE: "Cana de açucar",
            self.COFFE: "Café"
        }
        return description[self]

    def water_per_month_necessary(self):
        if self == AgricultureType.SOYA:
            return 30

        if self == AgricultureType.SUGAR_CANE:
            return 3

        if self == AgricultureType.COFFE:
            return 4

