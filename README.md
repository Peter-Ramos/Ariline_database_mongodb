# Εργασία πληροφοριακών συστημάτων

Το συγκεκριμένο project αφορά το εργαστήριο του μαθήματος **«(ΨΣ-152) Πληροφοριακά Συστήματα»** του τμήματος **Ψηφιακών Συστημάτων** του **Πανεπιστημίου Πειραιώς**.

## Δομές των collection

Στην βάση υπάρχουνε 3 collection: collUsers, collFlights, collReservations

### 1. collUsers

'''
{
\_id : type ObjectId
username : type string
name : type string
surname : type string
email : type string
password : type string
birthdate : type string
country : type string
passport : type string
category : type string ("user" or "administrator")
entered_system : type boolean
}

'''

### 2. collFlights

'''
{
'\_id' : type ObjectId
'start_ariport' : type string
'destination_airport' : type string
'date' : type string
'economy_seats' : type integer
'economy_cost' : type float
'business_seats' : type integer
'business_cost' : type float
}
'''

### 3. collReservations

'''
{
'\_id' : type ObjectId
'flight_id' : type string
'name' : type string
'surname' : type string
'passport' : type string
'email' : type string
'class' : type string
'birth_date' : type string
}

'''

## Λειτουργείες συστήματος

### 1. Sign up

Δημιουργία λογαριασμού στο σύστημα γίνεται στο ‘/sign_up’.
Ο χρήστης πρέπει να εισάγει τα στοιχεία του στο σύστημα (username, name, surname, email, password, birthdate, country, passport number).
Στην συνέχεια γίνεται έλεγχος για το αν υπάρχει ήδη ένας χρήστης με το ίδιο email η user name στα σύστημα και εισάγονται δυο νέα στοιχεία, η κατηγορία του χρήστη πουπαίρνει τιμή ‘user’ και μια μεταβλητή που ελέγχει αν έχει κάνει login:

```
data["category"] = "user"
data["entered_system"] = False
```

- Τέλος εισάγονται όλα τα στοιχεία στην βάση δεδομένων, στο collection που απευθύνεται στους χρήστες

```
collUsers.insert_one(data)
```

#### Παράδειγμα

- χρήστης πει στο: `[POST] http://[URL]:5000/sign_up`
- ειασάγει τα στιχεάα του

```
{
  "username": "IlikeMangos",
  "name": "peter",
  "surname": "Ramos",
  "email": "petrosramos@gmail.com",
  "password": "1234567",
  "birthdate": "08/08/2002",
  "country": "Greece",
  "passport": "123456789",
}
```

- Η απάντηση του συστήματος είναι

```
peter was added to the database
```

### 2. Login

Η είσοδος στο σύστημα γίνεται στο ‘/login’
Ο χρήστης πρέπει να εισάγει τα στοιχεία του στο σύστημα (email, password).
Στην συνέχεια το σύστημα ψάχνει τον χρήστη με αυτά τα στοιχεία:

```
collUsers.find_one({"email": data["email"], "password": data["password"]}
):
```

- Αν τον βρει τότε δηλώνει ότι ο χρήστης έχει κάνει login στο σύστημα:

```
collUsers.update_one(
{"email": data["email"], "password": data["password"]},{"$set": {"entered_system": True}})
```

- Αν δεν τον βρει τότε γυρνάει αντίστοιχο μνήμα

### 3. Logout

Η έξοδος από το σύστημα γίνεται στο ‘/logout’ και την χρήση ενός argument για το email
Στην συνέχεια λαμβάνεται το email από το argument και το password από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```
email = request.args.get("mail")
password = request.headers.get("Authorization")
```

```
logedin_test(email, password)
```

Αν βρει τον χρήστη τότε δηλώνει ότι έχει κάνει logout από το σύστημα

```
collUsers.update_one(
        {"email": email, "password": password},
        {"$set": {"entered_system": False}},
    )
```

- Αν δεν τον βρει τότε γυρνάει αντίστοιχο μνήμα
  ###4. Search flights
  Η αναζήτηση πτήσεων γίνεται στο ‘/search_flights’ μαζί με την χρήση ενός argument για το email
  λαμβάνεται το email από το argument και το password από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```
email = request.args.get("mail")
password = request.headers.get("Authorization")
```

```
logedin_test(email, password)
```

Εισάγονται τα στοιχεία σε μεταβλητή και ελέγχεται με βάση ποια στοιχεία θέλει να γίνει η αναζήτηση των πτήσεων

```
if ("start_ariport" in data) and ("destination_airport" in data):
    if "date" in data:
        ...
    else:
        ...
elif "date" in data:
    ...
else:
    ...
```

Οι πληροφορίες για τις πτήσεις εισάγονται σε μια μεταβλητή και γίνονται return στόν χρήστη

```
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
```

```
Response(output, status=200, mimetype="application/json")
```

### 5. Information about a flight

Η αναζήτηση πληροφορίας για μια πτήση γίνεται στο ‘/flight_information μαζί με την χρήση ενός argument για το email
λαμβάνεται το email από το argument και το password από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```
email = request.args.get("mail")
password = request.headers.get("Authorization")
```

```
logedin_test(email, password)
```

εισάγεται το id της πτήσης σε μεταβλητή

```
data = json.loads(request.data)
```

μετα εισάγονται τα κατάλληλα στοιχεία αυτής της πτήσης σε μια μεταβλητή

```
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
})
```

γίνεται έλεγχος για το αν έχει βρεθεί η πτήση και μετα γινεται το response

```
if output:
    return Response(output, status=200, mimetype="application/json")
```

### 6. Flight reservation

Η κράτηση πτήσης γίνεται στο ‘/search_flights’ μαζί με την χρήση ενός argument για το email
λαμβάνεται το email από το argument και το password από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```
email = request.args.get("mail")
password = request.headers.get("Authorization")
```

```
logedin_test(email, password)
```

παίρνει τα στοιχεία και ελέγχει αν υπάρχει στο collection που αφορά της πτήσεις η συγκεκριμένη πτήση που αναζητάει

```
data = json.loads(request.data)
```

```
if not collFlights.find_one({"_id": ObjectId(data["flight_id"])}):
    return Response(
        "Flight not found", status=500, mimetype="application/json"
    )
```

στην συνέχεια ελέγχει αν υπάρχουνε θέσεις ελεύθερες για την κατηγορία που θέλει να κάτσει ο χρήστης (economy, business). Αν βρει τότε μειώνει κατά 1 το στοιχείο που δείχνειπόσες ελεύθερες θέσεις υπάρχουνε στην πτήση

```
if data["class"] == "economy" and flight["economy_seats"] > 0:
    collFlights.update_one(
        {"_id": ObjectId(dat["flight_id"])},
        {"$set": {"economy_seats":fligh["economy_seats"] - 1}},
    )
elif data["class"] == "business" andfligh["business_seats"] > 0:
    collFlights.update_one(
        {"_id": ObjectId(dat["flight_id"])},
        {"$set": {"business_seats":fligh["business_seats"] - 1}},
    )
else:
    return Response(
        "No seats left on flight"status=200,mimetype="applicationjson"
    )
```

τέλος εισάγονται τα στοιχεία στο collection που αφορά τα reservations

```
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
```

αν δεν βρεθεί ένα value στα εισερχόμενα στοιχεία γυρνάει error message

```
return Response("bad json content", status=500, mimetype="application/json")
```

### 7. Information about reservations

Η πληροφόρηση για τις κρατήσεις ‘/reservation_review μαζί με την χρήση ενός argument για το email
λαμβάνεται το email από το argument και το password από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```
email = request.args.get("mail")
password = request.headers.get("Authorization")
```

```
logedin_test(email, password)
```

με βάση το email του χρήστη γίνεται αναζήτηση στο collReservations και εισάγονται σε μεταβλητή όλες οι κρατήσεις που έχουνε γίνει σε αυτό το email

```
for things in collReservations.find({"email": email}, {"flight_id": 0}):
        things["_id"] = str(things["_id"])
        output.update(things)
    if output:
        return Response(output, status=200, mimetype="application/json")
    return Response(
        "No reservations found", status=200, mimetype="application/json"
    )
```

### 8. Ιnformation about a reservation

Η πληροφόρηση για μια κρατησή ‘/reservation_info μαζί με την χρήση ενός argument για το email
λαμβάνεται το email από το argument και το password από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```
email = request.args.get("mail")
password = request.headers.get("Authorization")
```

```
logedin_test(email, password)
```

παίρνει το id της κράτησης που έχει εισάγει ο χρήστης και με βάση αυτό ψάχνει την κράτηση στο collReservations και τα στοιχεία της πτήσης από το collFlights

```
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
```

αν κάποιο από τα στοιχεία δεν είναι σωστά τότε στέλνει αντίστοιχο μήνυμα

### 9. Delete reservation

Η διαγραφή μιας κράτησης γήνεται στο ‘/reservation_delete μαζί με την χρήση ενός argument για το email
λαμβάνεται το email από το argument και τοpassword από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```
email = request.args.get("mail")
password = request.headers.get("Authorization")
```

```
logedin_test(email, password)
```

λαμβάνει το id της πτήσεις που έχει εισάγει ο χρήστης και παίρνει τις πληροφορίες για την πτήση και για την κράτηση και διαγράφει την κράτηση

```
reservation_info = collReservations.find_one({"_id": ObjectId(data["_id"])})
flight_info = collFlights.find_one(
    {"_id": ObjectId(reservation_info["flight_id"])}
)
collReservations.delete_one({"_id": ObjectId(data["_id"])})
```

ακύρωση κράτησης σημαίνει ότι ο θα ελευθερωθεί μια θέση στο αεροπλάνο άρα αυξάνονται τα αντίστοιχα στοιχεία κατά ένα

```
if reservation_info["class"] == "economy":
    collFlights.update_one(
        {"_id": ObjectId(reservation_info["flight_id"])},
        {"$set": {"economy_seats": flight_in["economy_seats"] + 1}},
    )
elif reservation_info["class"] == "business":
    collFlights.update_one(
        {"_id": ObjectId(reservation_info["flight_id"])},
        {"$set": {"business_seats": flight_in["business_seats"] + 1}},
    )

```

### 10. Delete account

Η διαγραφή μιας κράτησης γήνεται στο ‘/reservation_delete μαζί με την χρήση ενός argument για το email
λαμβάνεται το email από το argument και τοpassword από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```

email = request.args.get("mail")
password = request.headers.get("Authorization")

```

```

logedin_test(email, password)

```

στην συνέχεια με βάση το email γίνεται διαγραφή του λογαριασμού

```

try:
collUsers.delete_one({"email": email})
return Response("All went fine", status=200, mimetype="application/json")
except:
return Response("bad json content", status=500, mimetype="application/json")

```

### 11. Create a new flight

Η δημιουργία νέου στοιχείου πτήσης γίνεται στο ‘/create_flight μαζί με την χρήση ενός argument για το email
αφού είναι λειτουργία που επιτρέπεται να εκτελέσει μόνο ο χρήστης, πρέπει να γίνει αντίστοιχος έλεγχος
λαμβάνεται το email από το argument και τοpassword από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```

email = request.args.get("mail")
password = request.headers.get("Authorization")

```

ο έλεγχος γίνεται από διαφορετικό function που ελέγχει αν ο χρήστης είναι administrator

```

logedin_test_admin(email, password)

```

στην συνέχεια παίρνει τα στοιχεία που έβαλε ο χρήστης και ελέγχει αν η ημερομηνία είναι σωστά γραμμένη και εισάγει τα στοιχεία

```

data = json.loads(request.data)
if not date_correct(data["date"]):
return Response("bad json content", status=500, mimetype="application/json")

```

```

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

```

### 12. Update flight information

Η αλλαγή των στοιχείων μιας πτήσης γίνεται στο ‘/update_flight' μαζί με την χρήση ενός argument για το email
αφού είναι λειτουργία που επιτρέπεται να εκτελέσει μόνο ο χρήστης, πρέπει να γίνει αντίστοιχος έλεγχος
λαμβάνεται το email από το argument και τοpassword από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```

email = request.args.get("mail")
password = request.headers.get("Authorization")

```

ο έλεγχος γίνεται από διαφορετικό function που ελέγχει αν ο χρήστης είναι administrator

```

logedin_test_admin(email, password)

```

τα στοιχεία που μπορεί να τροποποιήσει είναι τα κότσοι (economy class & business class). άρα παίρνει το id και τις κατηγορίες που θέλει να τροποποιήσει από τον χρήστη καιτα εισάγει στο σύστημα
economy class:

```

if "economy_cost" in data:
ident = ObjectId(data["_id"])
collFlights.update_one(
{"\_id": ident},
{"$set": {"economy_cost": data["economy_cost"]}},
)

```

business class:

```

if "business_cost" in data:
collFlights.update_one(
{"\_id": ObjectId(data["_id"])},
{"$set": {"business_cost": data["business_cost"]}},
)

```

### 13. Delete a flight

Η διαγραφή μιας πτήσης γίνεται στο '/delete_flight' μαζί με την χρήση ενός argument για το email
αφού είναι λειτουργία που επιτρέπεται να εκτελέσει μόνο ο χρήστης, πρέπει να γίνει αντίστοιχος έλεγχος
λαμβάνεται το email από το argument και τοpassword από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```

email = request.args.get("mail")
password = request.headers.get("Authorization")

```

ο έλεγχος γίνεται από διαφορετικό function που ελέγχει αν ο χρήστης είναι administrator

```

logedin_test_admin(email, password)

```

Το σύστημα παίρνει τα στοιχεία που έχει βάλει ο χρήστης. Ελέγχει αν υπάρχει πτήση με συγκεκριμένο id και αν υπάρχει τότε την διαγράφει

```

if request.data:
data = json.loads(request.data)
if collFlights.find_one({"\_id": ObjectId(data["_id"])}):
collFlights.delete_one({"\_id": ObjectId(data["_id"])})
return Response("Flight deleted", status=200, mimetype="application/json")
return Response(
"flight not found content", status=500, mimetype="application/json"
)
return Response("bad request content", status=500, mimetype="application/json")

```

###14. find extensive details about a flight
Η αναζήτηση στοιχείων μιας πτήσης γίνεται στο '/details_flight' μαζί με την χρήση ενός argument για το email
αφού είναι λειτουργία που επιτρέπεται να εκτελέσει μόνο ο χρήστης, πρέπει να γίνει αντίστοιχος έλεγχος
λαμβάνεται το email από το argument και τοpassword από τον http header και ελέγχεται αν έχει γίνει login στο σύστημα από τον χρήστη

```

email = request.args.get("mail")
password = request.headers.get("Authorization")

```

ο έλεγχος γίνεται από διαφορετικό function που ελέγχει αν ο χρήστης είναι administrator

```

logedin_test_admin(email, password)

```

στην συνέχεια παίρνει το Id που έχει βάλει ο χρήστης και αναζητά την πτήση

```

flight_details = collFlights.find_one(
{"\_id": ObjectId(data["_id"])},
{
"\_id": 0,
"date": 0,
},
)

```

υπολογίζει τις συνολικές ελεύθερες θέσεις που υπάρχουνε

```

flight_details["free_seats"] = (
flight_details["business_seats"] +flight_details["economy_seats"]
)

```

και υπολογίζει πόσα economy και business tickets έχουνε αγοραστεί από το collection των κρατήσεων. Επίσης εισάγει κάθε φορά και τα στοιχεία του κάθε χρήστη που έχει κάνειreservation

```

for i in collReservations.find(
{"flight_id": data["_id"]},
{
"\_id": 0,
"flight_id": 0,
"passport": 0,
"email": 0,
"birthdate": 0,
}, # need to find which not to print
):
if i["class"] == "business":
business_tickets += 1
else:
economy_tickets += 1
flight_reservations.update(i)

```

Τέλος υπολογίζει τα στοιχεία τον θέσεων και τα εισάγει στο dictionary το οποίο στέλνεται ως response

```

flight_details["all_seats"] = (
flight_details["business_seats"] + flight_details["economy_seats"] + business_tickets + economy_tickets
)
flight_details["all_business_seats"] = (
business_tickets + flight_details["business_seats"]
)
flight_details["all_economy_seats"] = (
economy_tickets + flight_details["economy_seats"]
)
flight_details.update(flight_reservations)
return Response(flight_details, status=200, mimetype="application/json")

```

```

```
