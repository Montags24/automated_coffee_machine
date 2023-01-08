import ascii_art
import menu

MENU = menu.MENU
resources = menu.resources


# Function to get ingredients from drink
def menu_data(drink):
    water = MENU[drink]["ingredients"]["water"]
    milk = MENU[drink]["ingredients"]["milk"]
    coffee = MENU[drink]["ingredients"]["coffee"]
    return [water, milk, coffee]


# Function to check if resources are sufficient for drink
def resources_sufficient(drink):
    enough_resource = True
    ingredients = menu_data(drink)
    depleted_item = []
    for i, resource in enumerate(resources):
        if resources[resource] < ingredients[i]:
            enough_resource = False
            depleted_item.append(resource)
    if enough_resource:
        return True
    else:
        print("Sorry, there is not enough:")
        for item in depleted_item:
            print(f"{item}")
        return False


# Prompt user to insert coins if resources are sufficient
def calculate_money(drink):
    quarters = int(input("How many quarters?: "))
    dimes = int(input("How many dimes?: "))
    nickles = int(input("How many nickles?: "))
    pennies = int(input("How many pennies?: "))
    total_cash = (quarters * 0.25) + (dimes * 0.1) + (nickles * 0.05) + (pennies * 0.01)
    return total_cash


# Check if transaction was successful
def transaction_successful(drink, cash):
    if cash >= MENU[drink]["cost"]:
        return True
    else:
        print("Sorry, that's not enough money. Money refunded")
        return False


# Function that deducts ingredients from coffee machine and adds coins
def remove_ingredients_add_cash(drink):
    for i, resource in enumerate(resources):
        resources[resource] -= menu_data(drink)[i]


# Function that calculates change given
def calculate_change(user_cash, drink):
    """Function that calculates change based on drink selected and cash entered"""
    user_change = 0
    if user_cash > MENU[drink]["cost"]:
        user_change = user_cash - MENU[drink]["cost"]
    return user_change


# Prints the current status of the machine
def report_feature():
    print(f"The machine has\n-------------\n{resources['water']}ml water\n{resources['milk']}ml milk"
          f"\n{resources['coffee']}g coffee\nMoney: ${machine_cash}\n-------------\n")


def refill_machine():
    resources["water"] += int(input("Add how much water?: "))
    resources["milk"] += int(input("Add how much milk?: "))
    resources["coffee"] += int(input("Add how much coffee?: "))


# Prints the menu and prices - allows for scalability within menu
def list_menu():
    print("What would you like?\n-------------")
    for drink in MENU:
        print(f"{drink.capitalize()}: {MENU[drink]['cost']}")
    print("-------------")


# Repeat prompt to serve next user
go_again = True

machine_cash = 0
while go_again:
    list_menu()
    user_choice = input().lower()

    if user_choice == "off":
        print("Shutting down")
        go_again = False
    elif user_choice == "report":
        report_feature()
    elif user_choice == "refill":
        refill_machine()
    else:
        if user_choice not in MENU:
            print("That's not available. Please enter again.")
        else:
            if resources_sufficient(user_choice):
                machine_cash += MENU[user_choice]["cost"]
                total_cash = calculate_money(user_choice)
            if transaction_successful(user_choice, total_cash):
                print(f"Here is your {user_choice}!")
                print(f"{ascii_art.drinks[user_choice]}")
                remove_ingredients_add_cash(user_choice)
                change = calculate_change(total_cash, user_choice)
                if change > 0:
                    print(f"Here is ${change:.2f} dollars in change.\n")
                else:
                    go_again = False
            else:
                go_again = False
