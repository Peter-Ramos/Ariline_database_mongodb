import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
from bson import ObjectId
from datetime import datetime
import json, os, sys

sys.path.append("./data")
import prepare_data


mongodb_hostname = os.environ.get("MONGO_HOSTNAME", "localhost")
client = MongoClient("mongodb://" + mongodb_hostname + ":27017/")

db = client["DigitalAirlines"]
collUsers = db["AirlineUserCollection"]
collFlights = db["AirlineFlightsCollection"]
collReservations = db["AirlineReservationsCollections"]
    

print("Database is running!")

app = Flask(__name__)
import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.INFO)


# check if data existence
def check_data():
    try:
        if not collUsers.find_one({}):
            prepare_data.insert_all()
    except Exception as e:
        print(e)
        # raise e


@app.route("/sign_up", methods=["POST"])
def sign_up():
    if request.data:
        data = json.loads(request.data)

        # inserting new user
        try:
            if (
                data["username"] != ""
                and data["name"] != ""
                and data["surname"] != ""
                and data["email"] != ""
                and data["password"] != ""
                and data["birthdate"] != ""
                and data["country"] != ""
                and data["passport"] != ""
            ):
                # check if there exists a user with the same email or username
                if collUsers.find_one({"email": data["email"]}):
                    return Response(
                        "Email already exists", status=500, mimetype="application/json"
                    )
                if collUsers.find_one({"username": data["username"]}):
                    return Response(
                        "Username already exists",
                        status=500,
                        mimetype="application/json",
                    )
                if not date_correct(data["birthdate"]):
                    return Response(
                        "Information incorrect", status=500, mimetype="application/json"
                    )

                data["category"] = "user"
                data["entered_system"] = False
                collUsers.insert_one(data)
                return Response(
                    data["name"] + " was added to the database",
                    status=200,
                    mimetype="application/json",
                )
        except:
            return Response("bad json content", status=500, mimetype="application/json")

    return Response("bad json content", status=500, mimetype="application/json")


@app.route("/login", methods=["POST"])
def login():
    if request.data:
        data = json.loads(request.data)
        # inserting new user
        if data["email"] != "" and data["password"] != "":
            # check if there exists a user with the same email or username
            if collUsers.find_one(
                {"email": data["email"], "password": data["password"]}
            ):
                collUsers.update_one(
                    {"email": data["email"], "password": data["password"]},
                    {"$set": {"entered_system": True}},
                )
                return Response(
                    data["email"] + " entered the system",
                    status=200,
                    mimetype="application/json",
                )
    return Response("bad json content", status=500, mimetype="application/json")


@app.route("/logout", methods=["DELETE"])
def logout():
    try:
        email = request.args.get("mail")
        password = request.headers.get("Authorization")
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )
    if not logedin_test(email, password):
        return Response(
            "User not loged in system", status=500, mimetype="application/json"
        )
    collUsers.update_one(
        {"email": email, "password": password},
        {"$set": {"entered_system": False}},
    )
    return Response(
        email + "loged out of the system",
        status=200,
        mimetype="application/json",
    )


@app.route("/search_flights", methods=["GET"])
def search_flights():
    try:
        password = request.headers.get("Authorization")
        if not logedin_test(request.args.get("mail"), password):
            return Response(
                "User not loged in system", status=500, mimetype="application/json"
            )
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )

    output = {}

    data = json.loads(request.data)
    if ("start_ariport" in data) and ("destination_airport" in data):
        if "date" in data:
            for things in collFlights.find(
                {
                    "start_ariport": data["start_ariport"],
                    "destination_airport": data["destination_airport"],
                    "date": data["date"],
                },
                {
                    "economy_seats": 0,
                    "economy_cost": 0,
                    "business_seats": 0,
                    "business_cost": 0,
                },
            ):
                things["_id"] = str(things["_id"])
                output.update(things)
        else:
            for things in collFlights.find(
                {
                    "start_ariport": data["start_ariport"],
                    "destination_airport": data["destination_airport"],
                },
                {
                    "economy_seats": 0,
                    "economy_cost": 0,
                    "business_seats": 0,
                    "business_cost": 0,
                },
            ):
                things["_id"] = str(things["_id"])
                output.update(things)
    elif "date" in data:
        for things in collFlights.find(
            {"date": data["date"]},
            {
                "economy_seats": 0,
                "economy_cost": 0,
                "business_seats": 0,
                "business_cost": 0,
            },
        ):
            things["_id"] = str(things["_id"])
            output.update(things)
    else:
        for things in collFlights.find(
            {},
            {
                "economy_seats": 0,
                "economy_cost": 0,
                "business_seats": 0,
                "business_cost": 0,
            },
        ):
            things["_id"] = str(things["_id"])
            output.update(things)
    if output:
        return Response(output, status=200, mimetype="application/json")
    return Response("bad json content", status=500, mimetype="application/json")


@app.route("/flight_information", methods=["GET"])
def flight_information():
    try:
        if not logedin_test(
            request.args.get("mail"), request.headers.get("Authorization")
        ):
            return Response(
                "User not loged in system", status=500, mimetype="application/json"
            )
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )

    if request.data:
        data = json.loads(request.data)
        output = {}
        try:
            output = collFlights.find_one(
                {"_id": ObjectId(data["_id"])},
                {
                    "_id": 0,
                    "start_ariport": 1,
                    "destination_airport": 1,
                    "date": 1,
                    "economy_seats": 1,
                    "economy_cost": 1,
                    "business_seats": 1,
                    "business_cost": 1,
                },
            )
        except:
            return Response("bad json content", status=500, mimetype="application/json")

        if output:
            return Response(output, status=200, mimetype="application/json")

        return Response(
            "No flights where found", status=200, mimetype="application/json"
        )

    return Response("bad json content", status=500, mimetype="application/json")


@app.route("/flight_reservation", methods=["POST"])
def flight_reservation():
    try:
        email = request.args.get("mail")
        if not logedin_test(email, request.headers.get("Authorization")):
            return Response(
                "User not loged in system", status=500, mimetype="application/json"
            )
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )

    if request.data:
        data = json.loads(request.data)

        try:
            if not collFlights.find_one({"_id": ObjectId(data["flight_id"])}):
                return Response(
                    "Flight not found", status=500, mimetype="application/json"
                )
            flight = collFlights.find_one({"_id": ObjectId(data["flight_id"])})

            if data["class"] == "economy" and flight["economy_seats"] > 0:
                collFlights.update_one(
                    {"_id": ObjectId(data["flight_id"])},
                    {"$set": {"economy_seats": flight["economy_seats"] - 1}},
                )
            elif data["class"] == "business" and flight["business_seats"] > 0:
                collFlights.update_one(
                    {"_id": ObjectId(data["flight_id"])},
                    {"$set": {"business_seats": flight["business_seats"] - 1}},
                )
            else:
                return Response(
                    "No seats left on flight", status=200, mimetype="application/json"
                )

            # _id
            # id of the flight
            # user Name
            # user Surname
            # user email
            # passport number
            # date of birth
            # economy or business class
            if not date_correct(data["birthdate"]):
                return "birth date is wrong"
            collReservations.insert_one(
                {
                    "flight_id": data["flight_id"],
                    "name": data["name"],
                    "surname": data["surname"],
                    "passport": data["passport"],
                    "email": email,
                    "birthdate": data["birthdate"],
                    "class": data["class"],
                }
            )
            return Response(
                "Reservation complete", status=200, mimetype="application/json"
            )
        except:
            return Response("bad json content", status=500, mimetype="application/json")

    return Response("bad json content", status=500, mimetype="application/json")


@app.route("/reservation_review", methods=["GET"])
def reservation_review():
    try:
        email = request.args.get("mail")
        if not logedin_test(email, request.headers.get("Authorization")):
            return Response(
                "User not loged in system", status=500, mimetype="application/json"
            )
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )

    output = {}
    try:
        for things in collReservations.find({"email": email}, {"flight_id": 0}):
            things["_id"] = str(things["_id"])
            output.update(things)

        if output:
            return Response(output, status=200, mimetype="application/json")
        return Response(
            "No reservations found", status=200, mimetype="application/json"
        )
    except:
        return Response("bad content", status=500, mimetype="application/json")


@app.route("/reservation_info", methods=["GET"])
def reservation_info():
    try:
        if not logedin_test(
            request.args.get("mail"), request.headers.get("Authorization")
        ):
            return Response(
                "User not loged in system", status=500, mimetype="application/json"
            )
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )

    if request.data:
        data = json.loads(request.data)
        try:
            reservation_info = collReservations.find_one(
                {"_id": ObjectId(data["_id"])}, {"_id": 0}
            )
            flight_info = collFlights.find_one(
                {"_id": ObjectId(reservation_info["flight_id"])},
                {
                    "_id": 0,
                    "economy_seats": 0,
                    "economy_cost": 0,
                    "business_seats": 0,
                    "business_cost": 0,
                },
            )
            reservation_info.update(flight_info)
            return Response(reservation_info, status=200, mimetype="application/json")
        except:
            return Response("bad json content", status=500, mimetype="application/json")

    return Response("bad json content", status=500, mimetype="application/json")


@app.route("/reservation_delete", methods=["DELETE"])
def reservation_delete():
    try:
        if not logedin_test(
            request.args.get("mail"), request.headers.get("Authorization")
        ):
            return Response(
                "User not loged in system", status=500, mimetype="application/json"
            )
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )

    if request.data:
        data = json.loads(request.data)
        try:
            reservation_info = collReservations.find_one({"_id": ObjectId(data["_id"])})
            flight_info = collFlights.find_one(
                {"_id": ObjectId(reservation_info["flight_id"])}
            )
            collReservations.delete_one({"_id": ObjectId(data["_id"])})

            if reservation_info["class"] == "economy":
                collFlights.update_one(
                    {"_id": ObjectId(reservation_info["flight_id"])},
                    {"$set": {"economy_seats": flight_info["economy_seats"] + 1}},
                )
            elif reservation_info["class"] == "business":
                collFlights.update_one(
                    {"_id": ObjectId(reservation_info["flight_id"])},
                    {"$set": {"business_seats": flight_info["business_seats"] + 1}},
                )

            return Response(
                "Reservation deleted", status=200, mimetype="application/json"
            )
        except:
            return Response("bad json content", status=500, mimetype="application/json")

    return Response("bad json content", status=500, mimetype="application/json")


@app.route("/account_delete", methods=["DELETE"])
def account_delete():
    try:
        email = request.args.get("mail")
        if not logedin_test(email, request.headers.get("Authorization")):
            return Response(
                "User not loged in system", status=500, mimetype="application/json"
            )
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )

    try:
        collUsers.delete_one({"email": email})
        return Response("All went fine", status=200, mimetype="application/json")
    except:
        return Response("bad json content", status=500, mimetype="application/json")


# Administrator functions


@app.route("/create_flight", methods=["POST"])
def create_flight():
    try:
        if not logedin_test_admin(
            request.args.get("mail"), request.headers.get("Authorization")
        ):
            return Response(
                "User not loged in system", status=500, mimetype="application/json"
            )
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )

    if request.data:
        data = json.loads(request.data)
        if not date_correct(data["date"]):
            return Response("bad json content", status=500, mimetype="application/json")

        try:
            collFlights.insert_one(
                {
                    "start_ariport": data["start_ariport"],
                    "destination_airport": data["destination_airport"],
                    "date": data["date"],
                    "economy_seats": data["economy_seats"],
                    "economy_cost": data["economy_cost"],
                    "business_seats": data["business_seats"],
                    "business_cost": data["business_cost"],
                }
            )
            return Response("Flight added", status=200, mimetype="application/json")
        except:
            return Response("bad json content", status=500, mimetype="application/json")
    return Response("bad json content", status=500, mimetype="application/json")


@app.route("/update_flight", methods=["POST"])
def update_flight():
    try:
        if not logedin_test_admin(
            request.args.get("mail"), request.headers.get("Authorization")
        ):
            return Response(
                "User not loged in system", status=500, mimetype="application/json"
            )
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )

    if request.data:
        data = None
        try:
            data = json.loads(request.data)

            if data == None:
                return Response(
                    "No information received", status=500, mimetype="application/json"
                )

            if "economy_cost" in data:
                ident = ObjectId(data["_id"])
                collFlights.update_one(
                    {"_id": ident},
                    {"$set": {"economy_cost": data["economy_cost"]}},
                )

            if "business_cost" in data:
                collFlights.update_one(
                    {"_id": ObjectId(data["_id"])},
                    {"$set": {"business_cost": data["business_cost"]}},
                )
            return Response("Flight updated", status=200, mimetype="application/json")
        except:
            return Response("bad json content", status=500, mimetype="application/json")

    return Response("bad json content", status=500, mimetype="application/json")


@app.route("/delete_flight", methods=["DELETE"])
def delete_flight():
    try:
        if not logedin_test_admin(
            request.args.get("mail"), request.headers.get("Authorization")
        ):
            return Response(
                "User not loged in system", status=500, mimetype="application/json"
            )
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )

    if request.data:
        data = json.loads(request.data)
        if collFlights.find_one({"_id": ObjectId(data["_id"])}):
            collFlights.delete_one({"_id": ObjectId(data["_id"])})
            return Response("Flight deleted", status=200, mimetype="application/json")
        return Response(
            "flight not found content", status=500, mimetype="application/json"
        )
    return Response("bad request content", status=500, mimetype="application/json")


@app.route("/details_flight", methods=["GET"])
def details_flight():
    try:
        if not logedin_test_admin(
            request.args.get("mail"), request.headers.get("Authorization")
        ):
            return Response(
                "User not loged in system", status=500, mimetype="application/json"
            )
    except:
        return Response(
            "Incorect email or password", status=500, mimetype="application/json"
        )

    if request.data:
        data = json.loads(request.data)
        try:
            if collFlights.find_one({"_id": ObjectId(data["_id"])}):
                flight_details = collFlights.find_one(
                    {"_id": ObjectId(data["_id"])},
                    {
                        "_id": 0,
                        "date": 0,
                    },
                )
                flight_details["free_seats"] = (
                    flight_details["business_seats"] + flight_details["economy_seats"]
                )

                business_tickets = 0
                economy_tickets = 0
                flight_reservations = {}
                for i in collReservations.find(
                    {"flight_id": data["_id"]},
                    {
                        "_id": 0,
                        "flight_id": 0,
                        "passport": 0,
                        "email": 0,
                        "birthdate": 0,
                    },  # need to find which not to print
                ):
                    if i["class"] == "business":
                        business_tickets += 1
                    else:
                        economy_tickets += 1
                    flight_reservations.update(i)

                flight_details["all_seats"] = (
                    flight_details["business_seats"]
                    + flight_details["economy_seats"]
                    + business_tickets
                    + economy_tickets
                )
                flight_details["all_business_seats"] = (
                    business_tickets + flight_details["business_seats"]
                )
                flight_details["all_economy_seats"] = (
                    economy_tickets + flight_details["economy_seats"]
                )

                flight_details.update(flight_reservations)

                return Response(flight_details, status=200, mimetype="application/json")

            else:
                return Response(
                    "No flight found", status=500, mimetype="application/json"
                )
        except:
            return Response("bad json content", status=500, mimetype="application/json")
    return Response("bad json content", status=500, mimetype="application/json")


# helping functions
def logedin_test(email, password):
    if collUsers.find_one(
        {"email": email, "password": password, "entered_system": True}
    ):
        return True
    return False


def logedin_test_admin(email, password):
    if collUsers.find_one(
        {
            "email": email,
            "password": password,
            "entered_system": True,
            "category": "administrator",
        }
    ):
        return True
    return False


def date_correct(date):
    format = "%d-%m-%Y"
    print(date)
    try:
        datetime.strptime(date, format)
    except:
        return False
    return True


if __name__ == "__main__":
    check_data()
    app.run(debug=True, host="0.0.0.0", port=5000)
