var guestCount = 0;
var actualGuestCount = 0; // lol

var meals = [
    "Meal Choice?",
    "Petite Filet Mignon",
    "Roast Tenderloin of Beef",
    "Chicken Fingers (12 & under)",
    "Vegetable Stir Fry in Teriyaki Sauce",
    "Roasted Vegetable Wellington"
];

function addGuest() {
    var div = document.getElementById("dynamic_elements");
    var id = "guest" + guestCount;
    console.log(id);

    guestCount += 1;
    actualGuestCount += 1;
    var gc = document.getElementById("guestCount");
    gc.value = guestCount;
    var gcr = document.getElementById("guestCounter");
    gcr.innerText = actualGuestCount;

    var guestDiv = document.createElement("div");
    guestDiv.className = "guestDiv";
    guestDiv.id = id;

    var row1 = document.createElement("div");
    row1.className = "row";

    var nameDiv = document.createElement("div");
    nameDiv.className = "col-sm-6";
    var nameInput = document.createElement("input");
    nameInput.type = "text";
    nameInput.id = nameInput.name = id+"-name";
    nameInput.placeholder = "Guest name";
    nameDiv.appendChild(nameInput);

    var safDiv = document.createElement("div");
    safDiv.className = "col-sm-6";
    var safInput = document.createElement("select");
    safInput.name = safInput.id = id+"-safari";
    var safPrompt = document.createElement("option");
    safPrompt.innerText = safPrompt.value = "Riding Safari?";
    var safYes = document.createElement("option");
    safYes.innerText = safYes.value = "Yes: Riding";
    var safNo = document.createElement("option");
    safNo.innerText = safNo.value = "No: Not Riding";
    safInput.appendChild(safPrompt);
    safInput.appendChild(safYes);
    safInput.appendChild(safNo);
    safDiv.appendChild(safInput);

    row1.appendChild(nameDiv);
    row1.appendChild(safDiv);
    guestDiv.appendChild(row1);

    var row2 = document.createElement("div");
    row2.className = "row";

    var mealDiv = document.createElement("div");
    mealDiv.className = "col-sm-7";
    var mealInput = document.createElement("select");
    for (var i = 0; i<meals.length; i += 1)
    {
        var opt = document.createElement("option");
        opt.innerText = opt.value = meals[i];
        mealInput.appendChild(opt);
    }
    mealDiv.appendChild(mealInput);

    var delDiv = document.createElement("div");
    delDiv.className = "col-sm-5";
    var delBut = document.createElement("button");
    delBut.type = "button";
    delBut.onclick = function() { delGuest(id); };
    delBut.className = "btn-3";
    delBut.appendChild(document.createTextNode("Remove"));
    delDiv.appendChild(delBut);

    row2.appendChild(mealDiv);
    row2.appendChild(delDiv);
    guestDiv.appendChild(row2);

    div.appendChild(guestDiv);
}

function delGuest(id) {
    console.log("remove" + id);
    var guestDiv = document.getElementById(id);
    guestDiv.remove();

    actualGuestCount -= 1;
    var gcr = document.getElementById("guestCounter");
    gcr.innerText = actualGuestCount;
}

function doRsvp() {
    console.log("rsvp sent");
    // TODO - validate then submit
}