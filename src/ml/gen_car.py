import random
from datetime import date, timedelta
import csv

class Car:
    id: int
    model: str
    year_of_manufacture: int
    mileage: int
    count_trip: int
    last_maintenance_date: date
    to: int

    id_count = 40001

    def __init__(self):
        self.id = Car.id_count
        Car.id_count += 1
        self.model = self.generate_random_model()
        self.year_of_manufacture = self.generate_random_year_of_manufacture()
        self.mileage = self.cal_mileage()
        self.count_trip = self.cal_count_trip()
        self.last_maintenance_date = self.calculate_maintenance_dates()
        self.to = self.need_to()

    @staticmethod
    def generate_random_model():
        model_list = ["Hyundai Solaris", "Volkswagen Polo", "Kia Rio", "Chevrolet Aveo", "Hyundai Accent", "Nissan Note", "Renault Logan", "Chevrolet Lacetti", "KIA Spectra", "Haval F7", "Geely Tugella", "EXEED TXL", "LADA (VAZ) Vesta", "Chery Tiggo 4", "Chery Tiggo 7 Pro" ]
        models = random.choice(model_list)
        return models

    @staticmethod
    def generate_random_year_of_manufacture():
        today = date.today().year
        years_ranges = {
            "Hyundai Solaris": (2013, today),
            "Volkswagen Polo": (2013, today),
            "Kia Rio": (2013, today),
            "Chevrolet Aveo": (2014, today),
            "Hyundai Accent": (2013, today),
            "Nissan Note": (2013, today),
            "Renault Logan": (2015, today),
            "Chevrolet Lacetti": (2013, today),
            "Kia K5": (2013, today),
            "Haval F7": (2019, today),
            "Geely Tugella": (2020, today),
            "EXEED TXL": (2020, today),
            "LADA (VAZ) Vesta": (2015,today),
            "Chery Tiggo 4": (2017, today),
            "Chery Tiggo 7 Pro": (2020, today)

        }
        model = Car.generate_random_model()
        start, end = years_ranges.get(model, (2013, today))
        years = random.randint(start, end)
        return years

    def cal_mileage(self):
        years_of_use = date.today().year - self.year_of_manufacture
        years_of_use = min(years_of_use, 5)
        annual_milt_2024 = random.randint(1000, 30000)
        if years_of_use < 1:
            return annual_milt_2024
        annual_mil = random.randint(50000, 80000)
        return years_of_use * annual_mil

    def cal_count_trip(self):
        years_of_use = date.today().year - self.year_of_manufacture
        years_of_use = min(years_of_use, 5)

        annual_milt_2024 = random.randint(30, 30000)
        if years_of_use < 1:
            return annual_milt_2024
        annual_trips = random.randint(100000, 150000)
        return years_of_use * annual_trips

    def calculate_maintenance_dates(self):
        self.today = date.today()
        if self.year_of_manufacture <= 2019:
            last_date_before = self.today - timedelta(days=random.randint(181, 365))
            return last_date_before
        else:
            last_date_after = self.today - timedelta(days=random.randint(366, 720))
            return last_date_after

    def need_to(self):
        days_since_last = (self.today - self.last_maintenance_date).days
        if self.year_of_manufacture <= 2019:
            if days_since_last > 180:
                return 1
            else:
                return 0
        else:
            if days_since_last > 365:
                return 1
            else:
                return 0


    def get_formated(self):
        return [
            self.id,
            self.model,
            self.year_of_manufacture,
            self.mileage,
            self.count_trip,
            self.last_maintenance_date,
            self.to

        ]

header = [
    'id',
    'model',
    'year_of_manufacture',
    'mileage',
    'count_trip',
    'last_maintenance_date',
    'to'
]
with open("gen_car_1.csv", "w") as f:
    writer = csv.writer(f)
    for _ in range(10000):
        writer.writerow(Car().get_formated())