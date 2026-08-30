from flask import Flask, render_template, request, abort
import json
import os

app = Flask(__name__)

# -----------------------------------------
# Зареждане на автомобилите
# -----------------------------------------

def load_cars():
    try:
        with open("cars.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# -----------------------------------------
# Начална страница
# -----------------------------------------

@app.route("/")
def index():

    cars = load_cars()

    search = request.args.get("search", "").strip().lower()
    car_class = request.args.get("class", "").strip()
    sort_by = request.args.get("sort", "name")

    # Търсене
    if search:
        cars = [
            car for car in cars
            if search in car.get("name", "").lower()
            or search in car.get("manufacturer", "").lower()
        ]

    # Филтър по клас
    if car_class:
        cars = [
            car for car in cars
            if car.get("class", "") == car_class
        ]

    # Сортиране
    if sort_by == "speed":
        cars.sort(
            key=lambda car: car.get("top_speed_mph", 0),
            reverse=True
        )

    elif sort_by == "acceleration":
        cars.sort(
            key=lambda car: car.get("zero_to_100_mph", 999)
        )

    elif sort_by == "price":
        cars.sort(
            key=lambda car: car.get("price", 0)
        )

    else:
        cars.sort(
            key=lambda car: car.get("name", "")
        )

    # Всички класове
    all_cars = load_cars()

    classes = sorted(
        set(
            car.get("class", "Unknown")
            for car in all_cars
        )
    )

    # Топ 10 най-бързи
    top_cars = sorted(
        all_cars,
        key=lambda car: car.get("top_speed_mph", 0),
        reverse=True
    )[:10]

    return render_template(
        "index.html",
        cars=cars,
        classes=classes,
        search=search,
        selected_class=car_class,
        selected_sort=sort_by,
        top_cars=top_cars
    )


# -----------------------------------------
# Страница на конкретна кола
# -----------------------------------------

@app.route("/car/<int:car_id>")
def car_details(car_id):

    cars = load_cars()

    car = next(
        (
            car for car in cars
            if car.get("id") == car_id
        ),
        None
    )

    if car is None:
        abort(404)

    return render_template(
        "car.html",
        car=car
    )


# -----------------------------------------
# Стартиране
# -----------------------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )