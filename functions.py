import re,os
os.system('clear')

class DataValidator:
    def __init__(self):
        self.carRegex = r'^\w{2}\d{2}\w{2}\d{4}\b' #AA00BB1234
        self.slotRegex = r"\d{"+ str(len(str(self.parkingLotSize))) + "}" #0 #99
        
    
    def isValidCarNumber(self, carNumber):
        regex = re.compile(self.carRegex)
        return regex.match(carNumber) is not None

    def isValidSlotId(self, slotNumber):
        if not slotNumber:
            print(7)
            return False
        regex = re.compile(self.slotRegex)
        if not regex.match(str(slotNumber)) is None:
            # print(regex.match(str(slotNumber)))
            # print(slotNumber in self.slotRange)
            
            return int(slotNumber) in self.slotRange




class ParkingLot(DataValidator):

    def __init__(self, size):
        # self.slotDataStructure = {}
        self.slotsAvailable = True
        self.parkingLotSize = size
        # self.slotId = 0
        self.slotRange = range(1, self.parkingLotSize+1)
        self.carDataStructure = dict.fromkeys(list(self.slotRange), None)
        self.emptySlots = list(self.slotRange)
        DataValidator.__init__(self)


    def insert(self, carNumber):
        response = dict()
        if not self.carDataStructure:
            print("Parking Lot Is Empty, Good Morning") #Debug Checking
        if not self.slotsAvailable:
            response["error"] = "Parking Lot Full"
            return response,400
        if not self.emptySlots:
            self.slotsAvailable = False
            response["error"] = "Parking Lot Full"
            return response,400
        if not carNumber:
            response['error'] = "Empty Car Number"
            return response,400
        if self.isValidCarNumber(carNumber):
            if self.carDataStructure and self.carDataStructure.get(carNumber):
                return self.fetchInfo(carNumber, alrdyParked= True)
            # setattr(self, 'slotId', self.slotId+1)
            slotId = self.emptySlots[0]
            self.carDataStructure[carNumber] = slotId
            self.carDataStructure[slotId] = carNumber
            response['Car_Number'] = carNumber
            response['Parking_Slot'] = slotId
            response['Message'] = f"Park Your Car at Slot {slotId}"
            self.emptySlots.pop(0)
            if slotId>=self.parkingLotSize:
                self.slotsAvailable = False
        else:
            response['error'] = "Invalid Car Number! Please Provide Valid Car Number"
        return response, 200 if "error" not in response else 400

    def fetchInfo(self, carNumber = None, slotId = None, alrdyParked = False):
        response = dict()
        if not self.carDataStructure:
            response['error'] = "Parking Lot Is Empty! No Cars Found"
            return response,400
        if carNumber:
            if  self.isValidCarNumber(carNumber):
                if (slotId:=self.carDataStructure.get(carNumber)):
                    response['Car_Number'] = carNumber
                    response['Parking_Slot'] = slotId
                    response['message'] = f"Your Car {carNumber} is {'Already ' if alrdyParked else ''}Parked at Slot Number {slotId}"
                    return response,200
                else:
                    response['error'] = "Car Not Parked"
            else:
                response['error'] = "Invalid Car Number"
        elif slotId:
            if self.isValidSlotId(slotId):
                slotId = int(slotId)
                if (carNumber:=self.carDataStructure.get(slotId)):
                    response['Car_Number'] = carNumber
                    response['Parking_Slot'] = slotId
                    response['message'] = f"Your Car {carNumber} is Parked at Slot Number {slotId}"
                else:
                    response['error'] = "Slot Empty"
            else:
                response['error'] = "Invalid Slot Number"
        return response, 200 if "error" not in response else 400


    def delete(self, slotId: int):
        response = dict()
        if not self.carDataStructure:
            response['error'] = "Parking Lot Is Empty! No Car available to unpark"
            return response,400
        print(slotId)
        if self.isValidSlotId(slotId):
            if (carNumber:=self.carDataStructure.get(int(slotId))):
                del self.carDataStructure[carNumber]
                self.carDataStructure[int(slotId)] = None
                response['message'] = f"Car {carNumber} Is Unparked and Slot {slotId} is now empty"
                self.emptySlots.append(int(slotId))
                self.slotsAvailable = True
            else:
                response['error'] = f"Slot is Empty! No Car is Parked at Slot {slotId}"
        else:
            response['error'] = "Invalid Slot"
        return response, 200 if "error" not in response else 400


    def move(self, carNumber = None, slotId = None):
        response = dict()
        if not self.carDataStructure:
            response['error'] = "Parking Lot Is Empty! No Car available to unpark"
            return response,400
        if not self.slotsAvailable:
                response['error'] = "No Slots Empty! You cannot move your car"
                return response,404
        if carNumber or slotId:
            if carNumber:
                if self.isValidCarNumber(carNumber):
                    slotId=self.carDataStructure.get(carNumber)
                    if not slotId:
                        response['error'] = "Car is Not Parked"
                        return response,400
                else:
                    response['error'] = "Invalid Car Number"
            elif slotId:
                if self.isValidSlotId(slotId):
                    slotId = int(slotId)
                    carNumber=self.carDataStructure.get(slotId)
                    if not carNumber:
                        response['error'] = "Car Not Parked"
            print(slotId, carNumber)
            if carNumber and slotId:
                self.carDataStructure[slotId] = None
                self.emptySlots.append(slotId)
                NslotId = self.emptySlots[0]
                self.emptySlots.pop(0)
                self.carDataStructure[NslotId] = carNumber
                self.carDataStructure[carNumber] = NslotId
                response['oldSlot'] = slotId
                response['newSlot'] = NslotId
                response['Car_Number'] = carNumber
                response['message'] = f"Please Shift your Car {carNumber} from Slot {slotId} to New Slot {NslotId}"
        return response, 200 if "error" not in response else 400

# os.system('clear')
# print("#"*100)
# car = ParkingLot(5)
# print(car.delete(2))
# print(car.move('UP80CY8267'))
# print("#Park")
# print(car.insert('UP80CY8263'))
# print(car.insert('UP80CY8264'))
# print(car.insert('UP80CY8265'))
# # print(car.insert('UP80CY8265'))
# print(car.insert('UP80CY8266'))
# print(car.insert('UP80CY8267'))
# print(car.insert('UP80CY8268'))
# print(car.insert('UP80CY8269'))
# print(car.insert(1))
# print(car.emptySlots)
# print(car.slotsAvailable)
# # print("#FetchInfo")
# # print(car.fetchInfo(carNumber='UP80CY8264', slotId='00'))

# # print(car.fetchInfo(slotId='a'))
# # print(car.fetchInfo(carNumber='UP80CY826O'))

# print("#Delete")
# print(car.delete(20))
# print(car.delete(5))
# # print(car.move('UP80CY8267'))
# # print(car.emptySlots)

# print(car.insert('UP80CY8267'))
# # print(car.move('UP80CY8267'))
        









