from helpers import getFernetObj

username = "prakhar"
password = "prakhar"

fObj = getFernetObj(username, password)
print(fObj.encrypt("userinfo:&ō&:prakhar:&ō&:prakhar:&ō&:prakhar@email.com".encode()).decode())
print(fObj.encrypt("password:&ō&:Facebook:&ō&:https://www.facebook.com/:&ō&:prakhar99:&ō&:EpicStrongPassword:&ō&:social:&ō&:22-02-22".encode()).decode())
print(fObj.encrypt("note:&ō&:Remember this:&ō&:BJP ko jitana h bhai, apki baar modi sarkaar!!:&ō&:22-02-22".encode()).decode())
print(fObj.encrypt("contact:&ō&:Aman Verma:&ō&:amankaemail@gmail.com".encode()).decode())

# print(fObj.decrypt("gAAAAABh1gApDG7jav7J1dce19XqApRNHx4xKmET5KqXPzAl6eVpCVBkwlkS30Ft6ro8g_vd5F7GUYttwfaVJmiJQEize3w9xJnSwkbOM5u7fC18exqiVIbCh4INAC8xWVDrww5i55NTZEqwgzCshNYG8jtRJEzF2g==".encode()).decode().split(":&ō&:"))

print(fObj.encrypt("password:&ō&:Gla University:&ō&:https://glauniversity.in:8085:&ō&:prakhar99:&ō&:EpicStrongPassword:&ō&:other:&ō&:22-02-22".encode()).decode())
print(fObj.encrypt("password:&ō&:Internshala:&ō&:https://www.internshala.com/:&ō&:prakhar99:&ō&:EpicStrongPassword:&ō&:career:&ō&:22-02-22".encode()).decode())
print(fObj.encrypt("password:&ō&:binance:&ō&:https://www.binance.com/:&ō&:prakhar99:&ō&:EpicStrongPassword:&ō&:business:&ō&:22-02-22".encode()).decode())
print(fObj.encrypt("password:&ō&:Mahindra:&ō&:https://www.mahindra.in/:&ō&:prakhar99:&ō&:EpicStrongPassword:&ō&:finance:&ō&:22-02-22".encode()).decode())
print(fObj.encrypt("password:&ō&:Make my trip:&ō&:https://mmt.com/:&ō&:prakhar99:&ō&:EpicStrongPassword:&ō&:travel:&ō&:22-02-22".encode()).decode())
print(fObj.encrypt("password:&ō&:flipkart:&ō&:https://www.flipkart.com/:&ō&:prakhar99:&ō&:EpicStrongPassword:&ō&:shopping:&ō&:22-02-22".encode()).decode())
print(fObj.encrypt("password:&ō&:f2movies:&ō&:https://www3.f2movies.ru/:&ō&:prakhar99:&ō&:EpicStrongPassword:&ō&:entertainment:&ō&:22-02-22".encode()).decode())
print(fObj.encrypt("password:&ō&:Facebook:&ō&:https://www.facebook.com/:&ō&:prakhar99:&ō&:EpicStrongPassword:&ō&:social:&ō&:22-02-22".encode()).decode())